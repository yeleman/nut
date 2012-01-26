#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale

from django.utils.translation import ugettext as _
from django.conf import settings

from nutrsc.constants import *
from nutrsc.errors import REPORT_ERRORS
from nutrsc.data import CONSMAMDataHolder, CONSSAMDataHolder,
                        CONSSAMPDataHolder, CONSInputDataHolder
from nutrsc.validators import CONSReportValidator
from nut.models import ConsumptionReport, InputConsumptionReport, NUTInput
from bolibana.models import Report, MonthPeriod

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def cons_sub_report(message, cons, infos):
    """ PEC Report part of main Report SMS handling """

    def resp_error(code, msg):
        return (False, (code, msg))

    def holder_for(cap):
        return eval('CONS%sDataHolder' % cap.upper())

    # store MAM/SAM/SAM+ reports
    reports = {}

    # create Data Holder
    cons_holder = {}

    # loop on capabilities
    for capid, cap in cons.items():
        cons_cap = holder_for(capid)()

        for inpid, consstr in cap.items():

            # check that input is expected.
            if not inpid.lower() in cons_cap.inputs():
                return resp_error('BAD_FORM_CONS',
                                  REPORT_ERRORS['BAD_FORM_CONS'])

            input_cons = CONSInputDataHolder()
            input_cons.input_code = inpid

            # match field names with values
            try:
                input_data = dict(zip(input_cons.fields(), consstr.split()))
            except ValueError:
                # failure to split means we proabably lack a data or more
                # we can't process it.
                return resp_error('BAD_FORM_CONS',
                                  REPORT_ERRORS['BAD_FORM_CONS'])

            # convert form-data to int or bool respectively
            try:
                for key, value in input_data.items():
                    # all PEC data are integer
                    input_cons.set(key, int(value))
            except:
                raise
                # failure to convert means non-numeric
                # value which we can't process.
                return resp_error('BAD_FORM_CONS',
                                  REPORT_ERRORS['BAD_FORM_CONS'])

            # Associate ConsInput with CONSCAP
            cons_cap.set('input_%s' % inpid, input_cons)

        # check that all expected inputs are present
        for inp_ in cons_cap.inputs():
            if not cons_cap.get('input_%s' % inp_):
                return resp_error('BAD_FORM_CONS',
                                  REPORT_ERRORS['BAD_FORM_CONS'])

        # store Data Holder in main variable
        cons_holder[capid] = cons_cap

    # Create Validator then Report then store #recipt ID for each CAP
    for capid, data_browser in cons_holder.items():
       
        # feed data holder with guessable data
        try:
            hc = infos['entity'].slug
        except:
            hc = None
        data_browser.set('hc', hc)
        data_browser.set('month', infos['month'])
        data_browser.set('year', infos['year'])

        # create validator and fire
        validator = CONSReportValidator(data_browser)
        validator.errors.reset()

        # common start of error message
        error_start = u"Impossible d'enregistrer le rapport. "

        try:
            validator.validate()
        except AttributeError as e:
            return resp_error('CONS_%s' % capid.upper(),
                              error_start + e.__str__())
        except:
            pass
        errors = validator.errors

        # UNIQUENESS
        if ConsumptionReport.objects.filter(period=infos['period'],
                                      entity=infos['entity'],
                                      type=Report.TYPE_SOURCE,
                                      nut_type=ntype(capid)).count() > 0:
            return resp_error('UNIQ', REPORT_ERRORS['UNIQ'])

        # return first error to user
        if errors.count() > 0:
            return resp_error('CONS_%s' % capid.upper(),
                              error_start + errors.all()[0])

        reports[capid] = []
        # create the report
        try:
            period = MonthPeriod.find_create_from( \
                                                year=data_browser.get('year'), \
                                                month=data_browser.get('month'))
            report = ConsumptionReport(period=infos['period'],
                                       entity=infos['entity'],
                                       created_by=infos['provider'], \
                                       type=Report.TYPE_SOURCE,
                                       nut_type=ntype(capid))

            # need to add first so it's savec first (ref to ID)
            reports[capid].append(report)

            #report.add_all_data(data_browser)
            for input_code in data_browser.inputs():
                inp_report = InputConsumptionReport()
                inp_report.nut_input = NUTInput.objects.get(slug=input_code.lower())
                inp_report.cons_report = report
                inp_report.initial = data_browser.get('input_%s' % input_code).get('initial')
                inp_report.used = data_browser.get('input_%s' % input_code).get('consumed')
                inp_report.received = data_browser.get('input_%s' % input_code).get('received')
                inp_report.lost = data_browser.get('input_%s' % input_code).get('lost')
                reports[capid].append(inp_report)

        except Exception as e:
            #raise
            logger.error(u"Unable to save report to DB. Message: %s | Exp: %r" \
                         % (message.text, e))
            return resp_error('SRV', REPORT_ERRORS['SRV'])

    return (True, reports)
