#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale

from django.utils.translation import ugettext as _
from django.conf import settings

from bolibana.models import Report, Provider, Entity, MonthPeriod
from bolibana.tools.utils import provider_can
from nut.models import NUTEntity, PECMAMReport, PECSAMReport, PECSAMPReport
from nutrsc.errors import REPORT_ERRORS
from nutrsc.data import PECMAMDataHolder, PECSAMDataHolder, PECSAMPDataHolder
from nutrsc.validators import PECReportValidator

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def pec_sub_report(message, pec, infos, *args):
    """ PEC Report part of main Report SMS handling """

    def resp_error(code, msg):
        return (False, (code, msg))

    def class_for(cap):
        return eval('PEC%sReport' % cap.upper())

    def holder_for(cap):
        return eval('PEC%sDataHolder' % cap.upper())

    # store MAM/SAM/SAM+ reports
    reports = {}

    ########## CHECK AGES

    # create Data Holder
    pec_holder = {}

    # loop on capabilities
    for capid, cap in pec.items():
        pec_cap = holder_for(capid)()

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
    for capid, data_browser in pec_holder.items():

        # class of the report to create
        ClassReport = class_for(capid)
        
        # feed data holder with guessable data
        try:
            hc = infos['entity'].slug
        except:
            hc = None
        data_browser.set('hc', hc)
        data_browser.set('month', infos['month'])
        data_browser.set('year', infos['year'])

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
            pass
        errors = validator.errors

        # UNIQUENESS
        if ClassReport.objects.filter(period=infos['period'],
                                      entity=infos['entity'],
                                      type=Report.TYPE_SOURCE).count() > 0:
            return resp_error('UNIQ', REPORT_ERRORS['UNIQ'])

        # return first error to user
        if errors.count() > 0:
            return resp_error('PEC_%s' % capid.upper(),
                              error_start + errors.all()[0])

        # create the report
        try:
            period = MonthPeriod.find_create_from( \
                                                year=data_browser.get('year'), \
                                                month=data_browser.get('month'))
            report = ClassReport.start(infos['period'],
                                       infos['entity'],
                                       infos['provider'], \
                                         type=Report.TYPE_SOURCE)

            report.add_all_data(data_browser)

        except Exception as e:
            #raise
            logger.error(u"Unable to save report to DB. Message: %s | Exp: %r" \
                         % (message.content, e))
            return resp_error('SRV', REPORT_ERRORS['SRV'])

        reports[capid] = [report, ]

    return (True, reports)
