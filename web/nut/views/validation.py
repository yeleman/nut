#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import calendar
import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.datastructures import SortedDict


from bolibana.web.decorators import provider_permission
from bolibana.models import MonthPeriod

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

    period = MonthPeriod.find_create_from(year=year, month=month)

    ctx = {'year': year, 'month': month, 'entity': entity}

    qs1 = ConsumptionReport.objects.filter(period=period, entity=entity)
    qs2 = entity.nut_orderreport_reports.filter(period=period, entity=entity)

    reports = SortedDict((

    ('pec_samp_report', extract(entity.nut_pecsampreport_reports.filter(period=period),
                               0, default=None)),
    ('pec_sam_report', extract(entity.nut_pecsamreport_reports.filter(period=period),
                               0, default=None)),
    ('pec_mam_report', extract(entity.nut_pecmamreport_reports.filter(period=period),
                               0, default=None)),
    ('pec_other_report', extract(entity.nut_pecothersreport_reports.filter(period=period),
                                 0, default=None)),

    ('cons_samp_report', extract(qs1.filter(nut_type=constants.SEVERE_COMP),
                                 0, default=None)),
    ('cons_sam_report', extract(qs1.filter(nut_type=constants.SEVERE),
                                0, default=None)),
    ('cons_mam_report', extract(qs1.filter(nut_type=constants.MODERATE),
                                0, default=None)),

    ('order_samp_report', extract(qs2.filter(nut_type=constants.SEVERE_COMP),
                                  0, default=None)),
    ('order_sam_report', extract(qs2.filter(nut_type=constants.SEVERE),
                                 0, default=None)),
    ('order_mam_report', extract(qs2.filter(nut_type=constants.MODERATE),
                                 0, default=None)),

    ))

    if not any(reports.itervalues()):
      raise Http404


    forms = SortedDict((
        ('pec_samp_form', PECSAMPReportForm(data, instance=reports['pec_samp_report'],
                                            prefix='pec_samp_report')),
        ('pec_sam_form', PECSAMReportForm(data, instance=reports['pec_sam_report'],
                                          prefix='pec_sam_report')),
        ('pec_mam_form', PECMAMReportReportForm(data, instance=reports['pec_mam_report'],
                                                prefix='pec_mam_report')),
        ('pec_other_form', PECOthersReportForm(data, instance=reports['pec_other_report'],
                                               prefix="pec_other_report")),

        ('cons_samp_form', InputConsumptionReportFormSet(data,
                                                       prefix='cons_samp_report',
                                                       instance=reports['cons_samp_report'])),
        ('cons_sam_form', InputConsumptionReportFormSet(data,
                                                       prefix='cons_sam_report',
                                                       instance=reports['cons_sam_report'])),
        ('cons_mam_form', InputConsumptionReportFormSet(data,
                                                       prefix='cons_mam_report',
                                                       instance=reports['cons_mam_report'])),

        ('order_samp_form', InputOrderReportFormSet(data,
                                                  prefix='order_samp_report',
                                                  instance=reports['order_samp_report'])),
        ('order_sam_form', InputOrderReportFormSet(data,
                                                  prefix='order_sam_report',
                                                  instance=reports['order_sam_report'])),
        ('order_mam_form', InputOrderReportFormSet(data,
                                                  prefix='order_mam_report',
                                                  instance=reports['order_mam_report']))
    ))

    forms_with_instances = []
    for i, form in enumerate(forms.itervalues()):
        if reports.value_for_index(i):
            forms_with_instances.append(form)

    is_valid = all(form.is_valid() for form in forms_with_instances)
    if is_valid:
        for form in forms_with_instances:
            form.save()
        messages.success(request, u'Le rapport de %s pour la '
                                  u'période du %s/%s a été validé '
                                  u'avec succès' % (entity, month, year))

    ctx = locals()
    ctx.update(forms)
    ctx.update(reports)

    return render(request, 'validation.html', ctx)