#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale

import reversion
from django.conf import settings
from django.db import transaction

from nosmsd.utils import send_sms
from bolibana.models import Provider, Entity, MonthPeriod
from bolibana.tools.utils import provider_can
from ylmnut.data import current_reporting_period, contact_for
from nutrsc.errors import REPORT_ERRORS
from pec_report import pec_sub_report
from cons_report import cons_sub_report
from order_report import order_sub_report
from other_report import other_sub_report
from nut.models import NUTEntity

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


SUB_REPORTS = {'pec': pec_sub_report,
               'cons': cons_sub_report,
               'order': order_sub_report,
               'other': other_sub_report}


def nut_report(message, args, sub_cmd, **kwargs):

    """ Client sent report for PEC CONS & ORDER

    Once the PEC MAM/SAM/SAM+ & CONS & ORDER is filled, all the data
    is sent via one single multipart SMS.
    SMS is divided in sections and sub sections
    #P #C #O respectively PEC, CONS and ORDER
    We don't combine sections in case we'll have to split message
    in different SMS.
    SMS can be 1000chars+
    Sub sections for capabilities: &MAM, &SAM &SAMP
    Sub sub sections for age break downs |u6 |u59 |o59 |pw |fu1 |fu12

    > nut report rgaudin 89080392890 1111
    #P&MAM|u59 6817 7162 2164 1033 6527 5715 6749 2174 4201
    3675 8412 2331 4868 4765 1896 2107 3457 6308 6238 6589 2432 5983 3871|pw
    6817 7162 2164 1033 6527 5715 6749 2174 4201 3675 8412 2331 4868 4765
    1896 2107 3457 6308 6238 6589 2432 5983 3871|fu12 6817 7162 2164 1033
    6527 5715 6749 2174 4201 3675 8412 2331 4868 4765 1896 2107 3457 6308
    6238 6589 2432 5983 3871&SAM|u59 6817 7162 2164 1033 6527 5715 6749 2174
    4201 3675 8412 2331 4868 4765 1896 2107 3457 6308 6238 6589 2432 5983
    3871|o59 6817 7162 2164 1033 6527 5715 6749 2174 4201 3675 8412 2331 4868
    4765 1896 2107 3457 6308 6238 6589 2432 5983 3871|fu1 6817 7162 2164 1033
    6527 5715 6749 2174 4201 3675 8412 2331 4868 4765 1896 2107 3457 6308
    6238 6589 2432 5983 3871#C&MAM|csb 1199 1199 1199 1199|unimix 1199 1199
    1199 1199|oil 1199 1199 1199 1199|sugar 1199 1199 1199 1199|mil 1199 1199
    1199 1199|niebe 1199 1199 1199 1199&SAM|plumpy 1199 1199 1199
    1199#O&MAM|csb 1199|unimix 1199|oil 1199|sugar 1199|mil 1199|niebe
    1199&SAM|plumpy 1199#T 1 2 3-EOM-
    
    T lwb tb hiv
    < nut report error Error-code | Error Message
    < nut report ok #P$MAM GA1/gao-343-VO5$SAM GA1/gao-343-VO5#C$MAM
    GA1/gao-343-VO5$SAM GA1/gao-343-VO5#O$MAM GA1/gao-343-VO5$SAM
    GA1/gao-343-VO5 """

    def resp_error(code, msg):
        # make sure we cancel whatever addition
        message.respond(u"nut report error %(code)s|%(msg)s" \
                        % {'code': code, 'msg': msg})
        return True

    def provider_entity(provider):
        """ Entity a Provider is attached to """
        try:
            return NUTEntity.objects.get(id=provider.first_access().target.id)
        except:
            return None


    def sub_sections_from_section(section):
        """ Returns an organised hash from raw string

        {'mam': {'u6': 'xx xx xx', 'o59': 'xx xx xx'}, 'sam': {}} """

        subs = section.split('&')
        subs = subs[1:]
        subsh = {}
        for sub in subs:
            sub_data = sub.split('|')
            subh = {}
            for age_line in sub_data[1:]:
                age_ls = age_line.split()
                subh[age_ls[0]] = ' '.join(age_ls[1:])
            subsh[sub_data[0]] = subh
        return subsh

    def check_capabilities(section, entity):
        """ return True if section's subs matches entity cap """
        for cap in ('mam', 'sam', 'samp'):
            if getattr(entity, 'is_%s' % cap):
                if not cap in section.keys():
                    return False
            else:
                if cap in section.keys():
                    return False
        return True

    @reversion.create_revision()
    @transaction.commit_manually
    def save_reports(reports, receipts, user=None):
        reversion.set_user(user)
        reversion.set_comment("SMS transmitted report")
        for secid, section in reports.items():
        
            # create key for report type (P,C,O,T)
            if not receipts.has_key(secid):
                receipts[secid] = {}
                
            for catid, reports in section.items():
            
                # create key for category (MAM,SAM,SAMP)
                if not receipts[secid].has_key(catid):
                    receipts[secid][catid] = []
                    
                for report in reports:
                    logger.info("%s > %s > %s" \
                                % (secid, catid, report.__class__))
                    try:
                        # HACK: write foreign key id if needed
                        if hasattr(report, 'cons_report_id'):
                            report.cons_report_id = report.cons_report.id

                        if hasattr(report, 'order_report_id'):
                            report.order_report_id = report.order_report.id

                        report.save()
                        # store receipt if exist.
                        if hasattr(report, 'receipt'):
                            receipts[secid][catid].append(report.receipt)
                    except Exception as e:
                        logger.error(u"Unable to save report to DB. " \
                                     u"Message: %s | Exp: %r" \
                                     % (message.text, e))
                        transaction.rollback()
                        return False
        transaction.commit()
        return True

    # check that all parts made it together
    if not args.strip().endswith('-eom-'):
        return resp_error('BAD_FORM', REPORT_ERRORS['BAD_FORM'])
    else:
        args = args.strip()[:-5].strip()

    # split up sections
    try:
        infos, pec_sec, cons_sec, order_sec, other_sec = \
                                                 args.strip().lower().split('#')
        pec_sec = pec_sec[1:]
        cons_sec = cons_sec[1:]
        order_sec = order_sec[1:]
        other_sec = other_sec[1:]
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

    # report receipts holder for confirm message
    report_receipts = {}
    # reports holder for delayed database commit
    reports = {}

    # global infos
    infos = {'entity': entity,
             'eentity': eentity,
             'provider': provider,
             'month': month,
             'year': year,
             'period': period,
             'username': username,
             'pwhash': pwhash}

    # SECTIONS
    for sid, section in {'P': 'pec', 'C': 'cons',
                         'O': 'order', 'T': 'other'}.items():

        logger.info("Processing %s" % section)

        # extract/split sub sections info from string
        sec = sub_sections_from_section(eval('%s_sec' % section))

        # check that capabilities correspond to entity
        if not check_capabilities(sec, entity):
            return resp_error('BAD_CAP', REPORT_ERRORS['BAD_CAP'])

        # call sub-report section handler
        sec_succ, sec_data = SUB_REPORTS.get(section)(message,
                                                             sec, infos)
        # cancel if sub report failed.
        if not sec_succ:
            logger.warning(u"   FAILED.")
            return resp_error(sec_data[0], sec_data[1])

        # add sub-report to list of reports
        reports[sid] = sec_data
        logger.info("---- Ended %s" % section)
    
    ## DB COMMIT
    
    # create the reports in DB
    # save receipts number
    logger.info("Saving reports")
    if not save_reports(reports, report_receipts, user=provider.user):
        logger.warning("Unable to save reports")
        return resp_error('SRV', REPORT_ERRORS['SRV'])
    logger.info("Reports saved")

    ## CONFIRM RESPONSE
    
    # list of section/sub section formatted receipts
    recstr = ""
    for secid, section in report_receipts.items():
        recstr += "#%s" % secid.upper()
        for catid, receipts in section.items():
            recstr += "&%s " % catid.upper()
            recstr += " ".join(receipts)

    confirm = "nut report ok %s" % recstr

    message.respond(confirm)
    return True

    ## TRIGGER ALERT
    
    """
    try:
        to = contact_for(report.entity.parent).phone_number
    except:
        raise
        to = None
    if not to:
        return True
    send_sms(to, u"[ALERTE] Le CSCom %(cscom)s vient d'envoyer le " \
                 u"rapport #%(receipt)s pour %(period)s." \
                 % {'cscom': report.entity.display_full_name(), \
                    'period': report.period, \
                    'receipt': report.receipt})
    return True
    """
