#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale

from django.conf import settings

from nutrsc.constants import *
from nutrsc.errors import REPORT_ERRORS
#from nutrsc.data import CONSMAMDataHolder, CONSSAMDataHolder, CONSSAMPDataHolder, CONSInputDataHolder
from nutrsc.validators import CONSReportValidator
from nut.models import PECOthersReport
from bolibana.models import Report, MonthPeriod

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def other_sub_report(message, other, infos, previous_reports, *args, **kwargs):
    """ Others Report part of main Report SMS handling """

    def resp_error(code, msg):
        return (False, (code, msg))

    nut_report = kwargs.get('nut_report', None)

    # store report (std format)
    reports = {'ALL': []}

    # extract values
    try:
        lwb, tb, hiv = other.split()
        lwb = int(lwb.strip())
        tb = int(tb.strip())
        hiv = int(hiv.strip())
    except:
        return resp_error('BAD_FORM_OTHER',
                          REPORT_ERRORS['BAD_FORM_OTHER'])

    total_others = sum([lwb, tb, hiv])

    # retrieve previously generated PEC report
    total_pec = []
    for capid, cap_reports in previous_reports['P'].items():
        total_pec.append(cap_reports[0].all_other)
    total_pec_others = sum(total_pec)
          
    # UNIQUENESS
    if PECOthersReport.objects.filter(nut_report=nut_report).count() > 0:
        return resp_error('UNIQ', REPORT_ERRORS['UNIQ'])

    # check validity
    if total_others != total_pec_others:
        return resp_error('OTHER_INT', REPORT_ERRORS['UNIQ'])

    # create the report
    try:
        report = PECOthersReport(nut_report=nut_report,
                           other_lwb = lwb,
                           other_tb = tb,
                           other_hiv = hiv)

        # need to add first so it's savec first (ref to ID)
        reports['ALL'].append(report)

    except Exception as e:
        #raise
        logger.error(u"Unable to save report to DB. Message: %s | Exp: %r" \
                     % (message.content, e))
        return resp_error('SRV', REPORT_ERRORS['SRV'])

    logger.info('end others')

    return (True, reports)
