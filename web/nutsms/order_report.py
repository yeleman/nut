#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale

from django.utils.translation import ugettext as _
from django.conf import settings

from nutrsc.constants import *
from nutrsc.errors import REPORT_ERRORS
from nutrsc.data import CONSMAMDataHolder, CONSSAMDataHolder, CONSSAMPDataHolder, ORDERInputDataHolder
from nutrsc.validators import ORDERReportValidator
from nut.models import OrderReport, InputOrderReport, NUTInput
from bolibana.models import Report, MonthPeriod

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def order_sub_report(message, order, infos, *args):
    """ PEC Report part of main Report SMS handling """

    def resp_error(code, msg):
        return (False, (code, msg))

    def holder_for(cap):
        return eval('CONS%sDataHolder' % cap.upper())

    # store MAM/SAM/SAM+ reports
    reports = {}

    # create Data Holder
    order_holder = {}

    # loop on capabilities
    for capid, cap in order.items():
        order_cap = holder_for(capid)()

        for inpid, orderstr in cap.items():

            # check that input is expected.
            if not inpid.lower() in order_cap.inputs():
                return resp_error('BAD_FORM_ORDER',
                                  REPORT_ERRORS['BAD_FORM_ORDER'])

            input_order = ORDERInputDataHolder()
            input_order.input_code = inpid

            # match field names with values
            try:
                order_data = dict(zip(input_order.fields(), orderstr.split()))
            except ValueError:
                # failure to split means we proabably lack a data or more
                # we can't process it.
                return resp_error('BAD_FORM_ORDER',
                                  REPORT_ERRORS['BAD_FORM_ORDER'])

            # convert form-data to int or bool respectively
            try:
                for key, value in order_data.items():
                    # all PEC data are integer
                    input_order.set(key, int(value))
            except:
                raise
                # failure to convert means non-numeric
                # value which we can't process.
                return resp_error('BAD_FORM_ORDER',
                                  REPORT_ERRORS['BAD_FORM_ORDER'])

            # Associate OrderInput with ORDERCAP
            order_cap.set('input_%s' % inpid, input_order)

        # check that all expected inputs are present
        for inp_ in order_cap.inputs():
            if not order_cap.get('input_%s' % inp_):
                return resp_error('BAD_FORM_ORDER',
                                  REPORT_ERRORS['BAD_FORM_ORDER'])

        # store Data Holder in main variable
        order_holder[capid] = order_cap

    # Create Validator then Report then store #recipt ID for each CAP
    for capid, data_browser in order_holder.items():
       
        # feed data holder with guessable data
        try:
            hc = infos['entity'].slug
        except:
            hc = None
        data_browser.set('hc', hc)
        data_browser.set('month', infos['month'])
        data_browser.set('year', infos['year'])

        # create validator and fire
        validator = ORDERReportValidator(data_browser)
        validator.errors.reset()

        # common start of error message
        error_start = u"Impossible d'enregistrer le rapport. "

        try:
            validator.validate()
        except AttributeError as e:
            return resp_error('ORDER_%s' % capid.upper(),
                              error_start + e.__str__())
        except:
            pass
        errors = validator.errors

        # UNIQUENESS
        if OrderReport.objects.filter(period=infos['period'],
                                      entity=infos['entity'],
                                      type=Report.TYPE_SOURCE,
                                      nut_type=ntype(capid)).count() > 0:
            return resp_error('UNIQ', REPORT_ERRORS['UNIQ'])

        # return first error to user
        if errors.count() > 0:
            return resp_error('ORDER_%s' % capid.upper(),
                              error_start + errors.all()[0])

        reports[capid] = []
        # create the report
        try:
            period = MonthPeriod.find_create_from( \
                                                year=data_browser.get('year'), \
                                                month=data_browser.get('month'))
            report = OrderReport(period=infos['period'],
                               entity=infos['entity'],
                               created_by=infos['provider'], \
                               type=Report.TYPE_SOURCE,
                               nut_type=ntype(capid))

            # need to add first so it's savec first (ref to ID)
            reports[capid].append(report)

            #report.add_all_data(data_browser)
            for input_code in data_browser.inputs():
                inp_report = InputOrderReport()
                inp_report.nut_input = NUTInput.objects.get(slug=input_code.lower())
                inp_report.order_report = report
                inp_report.quantity = data_browser.get('input_%s' % input_code).get('quantity')
                reports[capid].append(inp_report)

        except Exception as e:
            #raise
            logger.error(u"Unable to save report to DB. Message: %s | Exp: %r" \
                         % (message.content, e))
            return resp_error('SRV', REPORT_ERRORS['SRV'])

    return (True, reports)
