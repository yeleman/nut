#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import calendar
import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from bolibana.web.decorators import provider_permission
from bolibana.models import Period

from nutrsc import constants

from nut.models import NUTEntity, ConsumptionReport
from nut.forms import *

from utils import extract


# from ylmnut.data import (current_period, current_reporting_period,
#                          provider_entity, time_cscom_over, time_district_over,
#                          time_region_over, time_can_validate,
#                          get_not_received_reports, get_reports_to_validate,
#                          get_validated_reports)
# from bolibana.tools.utils import provider_can_or_403


@provider_permission('can_validate_report')
def validation_list(request):
    context = {'category': 'validation'}
    return render(request, 'validation_list.html', context)



@provider_permission('can_validate_report')
def report_validation(request, entity, slug, year, month):

    try:
        entity = get_object_or_404(NUTEntity, pk=int(entity))
        month, year = int(month), int(year)
    except ValueError:
        raise Http404

    data = request.POST or None

    period = Period.find_create_from(year, month)

    ctx = {'year': year, 'month': month, 'entity': entity}

    pec_samp_report = extract(entity.nut_pecsampreport_reports.filter(period=period),
                          0, default=None)

    pec_sam_report = extract(entity.nut_pecsamreport_reports.filter(period=period),
                         0, default=None)

    pec_mam_report = extract(entity.nut_pecmamreport_reports.filter(period=period),
                         0, default=None)

    pec_other_report = extract(entity.nut_pecothersreport_reports.filter(period=period),
                           0, default=None)

    cons_samp_report = extract(ConsumptionReport.objects.filter(period=period,
                                                                entity=entity,
                                                                nut_type=constants.SEVERE_COMP),
                              0, default=None)


    cons_sam_report = extract(ConsumptionReport.objects.filter(period=period,
                                                               entity=entity,
                                                               nut_type=constants.SEVERE),
                              0, default=None)

    cons_mam_report = extract(ConsumptionReport.objects.filter(period=period,
                                                               entity=entity,
                                                               nut_type=constants.MODERATE),
                              0, default=None)


    forms = dict(
        pec_samp_form = PECSAMPReportForm(data, instance=pec_samp_report),
        pec_sam_form = PECSAMReportForm(data, instance=pec_sam_report),
        pec_mam_form = PECMAMReportReportForm(data, instance=pec_mam_report),
        pec_other_form = PECOthersReportForm(data, instance=pec_other_report),
        cons_samp_form = InputConsumptionReportFormSet(data,
                                                       prefix='cons_samp_report',
                                                       instance=cons_samp_report),

        cons_sam_form = InputConsumptionReportFormSet(data,
                                                       prefix='cons_sam_report',
                                                       instance=cons_sam_report),

        cons_mam_form = InputConsumptionReportFormSet(data,
                                                       prefix='cons_mam_report',
                                                       instance=cons_mam_report)
    )

    if all(form.is_valid() for form in forms.itervalues()):
        for form in forms.itervalues():
            form.save()


    ctx = locals()
    ctx.update(forms)

    return render(request, 'validation.html', ctx)