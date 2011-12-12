#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import datetime
import logging
import locale

import reversion
from django.utils.translation import ugettext as _
from django.conf import settings

from bolibana.models import Report, Provider, Entity, MonthPeriod
from bolibana.tools.utils import provider_can
from nut.models import NUTEntity, PECMAMReport
from ylmnut.data import current_reporting_period, contact_for
from nutrsc.errors import REPORT_ERRORS
from nutrsc.tools import generate_user_hash
from nutrsc.data import PECMAMDataHolder
from nutrsc.validators import PECReportValidator

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


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

    > nut report rgaudin renaud 1111
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
    1199&SAM|plumpy 1199-EOM-

    < nut report error Error-code | Error Message
    < nut report ok #P$MAM GA1/gao-343-VO5$SAM GA1/gao-343-VO5#C$MAM
    GA1/gao-343-VO5$SAM GA1/gao-343-VO5#O$MAM GA1/gao-343-VO5$SAM
    GA1/gao-343-VO5 """

    def resp_error(code, msg):
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

    # check that all parts made it together
    if not args.strip().endswith('-eom-'):
        return resp_error('BAD_FORM', REPORT_ERRORS['BAD_FORM'])

    # split up sections
    try:
        infos, pec_sec, cons_sec, order_sec = args.strip().lower().split('#')
        pec_sec = pec_sec[1:]
        cons_sec = cons_sec[1:]
        order_sec = order_sec[1:]
    except:
        return resp_error('BAD_FORM', REPORT_ERRORS['BAD_FORM'])

    # split up infos
    try:
        username, password, date_str = infos.strip().split()
    except:
        return resp_error('BAD_FORM_INFO', REPORT_ERRORS['BAD_FORM_INFO'])

    # get Provider based on username
    try:
        provider = Provider.objects.get(user__username=username)
    except Provider.DoesNotExist:
        return resp_error('NO_ACC', REPORT_ERRORS['NO_ACC'])

    # check that provider password is good
    if not provider.check_password(password):
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

    # extract PEC section
    pec = sub_sections_from_section(pec_sec)

    # check that capabilities correspond to entity
    if not check_capabilities(pec, entity):
        return resp_error('BAD_CAP', REPORT_ERRORS['BAD_CAP'])

    # create Data Holder
    pec_holder = {}  

    # loop on capabilities
    for capid, cap in pec.items():
        pec_cap = PECMAMDataHolder()

        for ageid, age in cap.items():

            # match field names with values
            try:
                age_data = dict(zip(pec_cap.fields_for(ageid), age.split()))
            except ValueError:
                # failure to split means we proabably lack a data or more
                # we can't process it.
                return resp_error('BAD_FORM_PEC', REPORT_ERRORS['BAD_FORM_PEC'])

            # convert form-data to int or bool respectively
            try:
                for key, value in age_data.items():
                    # all PEC data are integer
                    pec_cap.set(key, int(value))
            except:
                raise
                # failure to convert means non-numeric
                # value which we can't process.
                return resp_error('BAD_FORM_PEC', REPORT_ERRORS['BAD_FORM_PEC'])

        # store Data Holder in main variable
        pec_holder[capid] = pec_cap

    # Create Validator then Report then store #recipt ID for each CAP
    report_receipts = {}
    for capid, data_browser in pec_holder.items():
    
        # feed data holder with guessable data
        try:
            hc = entity.slug
        except:
            hc = None
        data_browser.set('hc', hc)
        data_browser.set('month', month)
        data_browser.set('year', year)

        # create validator and fire
        validator = PECReportValidator(data_browser)
        validator.errors.reset()

        # common start of error message
        error_start = u"Impossible d'enregistrer le rapport. "

        try:
            validator.validate()
        except AttributeError as e:
            return resp_error('PEC_%s' % capid.upper(),
                              error_start + e.__str__())
        except:
            raise
        errors = validator.errors
        import pprint
        pprint.pprint(errors.all())
        # UNIQUENESS
        #?????????????????????????

        # return first error to user
        if errors.count() > 0:
            return resp_error('PEC_%s' % capid.upper(),
                              error_start + errors.all()[0])

        # create the report
        try:
            period = MonthPeriod.find_create_from( \
                                                year=data_browser.get('year'), \
                                                month=data_browser.get('month'))
            report = PECMAMReport.start(period, entity, provider, \
                                         type=Report.TYPE_SOURCE)

            report.add_u59_data(*data_browser.data_for_cat('u59'))
            report.add_pw_data(*data_browser.data_for_cat('pw'))
            report.add_fu12_data(*data_browser.data_for_cat('fu12'))
            
            with reversion.create_revision():
                report.save()
                reversion.set_user(provider.user)

        except Exception as e:
            raise
            logger.error(u"Unable to save report to DB. Message: %s | Exp: %r" \
                         % (message.text, e))
            return resp_error('SRV', REPORT_ERRORS['SRV'])

        report_receipts[capid] = report.receipt

    """nut report ok #P$MAM GA1/gao-343-VO5$SAM GA1/gao-343-VO5#C$MAM
    GA1/gao-343-VO5$SAM GA1/gao-343-VO5#O$MAM GA1/gao-343-VO5$SAM
    GA1/gao-343-VO5"""
    pec_receipts = ""
    for capid, rec in report_receipts.items():
        pec_receipts += "&%(capid)s %(rec)s" % {'capid': capid, 'rec': rec}
    confirm = u"nut report ok #P%(pecr)s" % {'pecr': pec_receipts}

    message.respond(confirm)
    return True
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
