#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale

import reversion
from django.db import transaction
from django.conf import settings

from bolibana.models import Provider, Entity, MonthPeriod, Report
from bolibana.tools.utils import provider_can
from ylmnut.data import current_reporting_period
from nutrsc.errors import REPORT_ERRORS
from nutrsc.validators import PECReportValidator
from nutrsc.mali import uncompress_pec_field, uncompress_cons_field
from nut.models import NUTEntity, NutritionReport

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def nut_report_update(message, args, sub_cmd, **kwargs):
    """ Client sent an update to an existing report

    Only the modified fields are sent.
    Each section is coded accoding to report codes.
    All fields are coded according to nutrsc.

    > nut report-update rgaudin -1355030878 0112  #P &SAM 1d:2 "
      1h:2 1l6:2 #C &MAM a0:100 #T v:1 w:0 u:0-EOM-"""

    def resp_error(code, msg):
        # make sure we cancel whatever addition
        message.respond(u"nut report-update error %(code)s|%(msg)s" \
                        % {'code': code, 'msg': msg})
        return True

    def provider_entity(provider):
        """ Entity a Provider is attached to """
        try:
            return NUTEntity.objects.get(id=provider.first_access().target.id)
        except:
            return None

    # check that all parts made it together
    if not args.strip().endswith('-eom-'):
        return resp_error('BAD_FORM', REPORT_ERRORS['BAD_FORM'])
    else:
        args = args.strip()[:-5].strip()

    # split up sections
    sections = {}
    try:
        parts = args.strip().lower().split('#')
        for index in range(0, len(parts)):
            if index == 0:
                infos = parts[index]
            else:
                sections[parts[index][0].upper()] = parts[index][1:]
        pec_sec = sections.get('P', '').strip()
        cons_sec = sections.get('C', '').strip()
        order_sec = sections.get('O', '').strip()
        other_sec = sections.get('T', '').strip()
    except:
        return resp_error('BAD_FORM', REPORT_ERRORS['BAD_FORM'])

    # split up infos
    try:
        username, pwhash, date_str = infos.strip().split()
    except:
        return resp_error('BAD_FORM_INFO', REPORT_ERRORS['BAD_FORM_INFO'])

    # get Provider based on username
    try:
        provider = Provider.objects.get(user__username=username)
    except Provider.DoesNotExist:
        return resp_error('NO_ACC', REPORT_ERRORS['NO_ACC'])

    # check that provider pwhash is good
    if not provider.check_hash(pwhash):
        return resp_error('BAD_PASS', REPORT_ERRORS['BAD_PASS'])

    # check that user is not disabled
    if not provider.is_active:
        return resp_error('ACC_DIS', REPORT_ERRORS['ACC_DIS'])

    # check that user has permission to submit report on entity
    entity = provider_entity(provider)

    if not entity:
        return resp_error('NOT_ENT', REPORT_ERRORS['NOT_ENT'])

    eentity = Entity.objects.get(id=entity.id)
    if not provider_can('can_submit_report', provider, eentity):
        return resp_error('NO_PERM', REPORT_ERRORS['NO_PERM'])

    # parse date and check if period is valid
    try:
        month = int(date_str[0:2])
        year = int('%s%s' % ('20', date_str[2:4]))
        period = MonthPeriod.find_create_from(year=year, month=month)
    except:
        return resp_error('BAD_FORM_PERIOD', REPORT_ERRORS['BAD_FORM_PERIOD'])

    # check period is the one we want
    if not period == current_reporting_period():
        return resp_error('BAD_PERIOD', REPORT_ERRORS['BAD_PERIOD'])

    # global infos
    infos = {'entity': entity,
             'eentity': eentity,
             'provider': provider,
             'month': month,
             'year': year,
             'period': period,
             'username': username,
             'pwhash': pwhash}

    # Retrieve report
    try:
        nut_report = NutritionReport.objects.get(period=infos['period'],
                                                 entity=infos['entity'],
                                                 type=Report.TYPE_SOURCE)
    except:
        return resp_error('MISS', REPORT_ERRORS['MISS'])

    reports = []
    # common start of error message
    error_start = u"Impossible d'enregistrer le rapport. "

    logger.info("Processing PEC")

    if pec_sec:
        subs = pec_sec.split('&')
        subs = subs[1:]
        for sub in subs:
            fields = sub.split()
            cap = fields[0].lower()
            sub_report = getattr(nut_report, 'pec_%s_report' % cap)
            for field in fields[1:]:
                cfield, value = field.split(':')
                rfield = uncompress_pec_field(cfield)
                setattr(sub_report, rfield, int(value))
            validator = PECReportValidator(sub_report)
            validator.errors.reset()
            try:
                validator.validate()
            except AttributeError as e:
                return resp_error('PEC_%s' % cap.upper(),
                                  error_start + e.__str__())
            except:
                pass
            errors = validator.errors
            # return first error to user
            if errors.count() > 0:
                return resp_error('PEC_%s' % cap.upper(),
                                  error_start + errors.all()[0])
            else:
                reports.append(sub_report)

    logger.info("Processing CONS")

    if cons_sec:
        subs = cons_sec.split('&')
        subs = subs[1:]
        for sub in subs:
            fields = sub.split()
            cap = fields[0].lower()
            logger.info(cap.upper())
            for field in fields[1:]:
                cfield, value = field.split(':')
                rinpc, rfield = uncompress_cons_field(cfield)
                sub_report = getattr(getattr(nut_report, 
                                             'cons_%s_report' % cap),
                                     'icr')(rinpc)
                setattr(sub_report, rfield, int(value))
                if sub_report.valid and not sub_report in reports:
                    reports.append(sub_report)

    logger.info("Processing ORDER")

    if order_sec:
        subs = order_sec.split('&')
        subs = subs[1:]
        for sub in subs:
            logger.info("\t%s" % sub)
            fields = sub.split()
            cap = fields[0].lower()
            for field in fields[1:]:
                cfield, value = field.split(':')
                rinpc, rfield = uncompress_cons_field(cfield)
                sub_report = getattr(getattr(nut_report,
                                             'order_%s_report' % cap),
                                     'icr')(rinpc)
                setattr(sub_report, rfield, int(value))
                if not sub_report in reports:
                    reports.append(sub_report)

    logger.info("Processing OTHER")

    if other_sec:
        fields = other_sec.split()
        for field in fields[1:]:
            cfield, value = field.split(':')
            rfield = uncompress_pec_field(cfield)
            sub_report = nut_report.pec_other_report
            setattr(sub_report, rfield, int(value))
        # check validity relative to PEC
        if not sub_report.total == sub_report.nut_report.sum_all_other:
            return resp_error('OTHER_INT', REPORT_ERRORS['OTHER_INT'])
        else:
            reports.append(sub_report)


    # check validity of changes
    # save to DB
    @reversion.create_revision()
    @transaction.commit_manually
    def save_reports(reports, nut_report, provider=None):
        reversion.set_user(provider.user)
        reversion.set_comment("SMS report update")
        for report in reports:
            print("saving %s" % report)
            try:
                sub_report.save()
            except:
                transaction.rollback()
                return False
        try:
            nut_report._status = nut_report.STATUS_MODIFIED_AUTHOR
            nut_report.modified_by = provider
            nut_report.save()
        except:
            transaction.rollback()
            return False

        transaction.commit()
        return True

    logger.info("Saving reports")
    if not save_reports(reports, nut_report, provider):
        logger.warning("Unable to save reports")
        return resp_error('SRV', REPORT_ERRORS['SRV'])
    logger.info("Reports saved")

    ## CONFIRM RESPONSE
    
    confirm = "nut report-update ok %s" % nut_report.receipt

    message.respond(confirm)
    return True