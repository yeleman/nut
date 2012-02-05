#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime
import reversion

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.datastructures import SortedDict


from bolibana.web.decorators import provider_permission
from bolibana.models import MonthPeriod

from nutrsc import constants

from nut.models import NUTEntity, ConsumptionReport, NutritionReport
from nut.forms import (PECSAMPReportForm, PECSAMReportForm,
                       PECMAMReportReportForm, PECOthersReportForm,
                       InputConsumptionReportFormSet,
                       InputOrderReportFormSet)

from utils import extract


from nut.data import (current_period, current_reporting_period,
                         provider_entity, time_cscom_over, time_district_over,
                         time_region_over, time_can_validate,
                         get_not_received_reports, get_reports_to_validate,
                         get_validated_reports, contact_for)
from bolibana.tools.utils import provider_can_or_403


@provider_permission('can_validate_report')
def validation_list(request):
    context = {'category': 'validation'}

    web_provider = request.user.get_profile()

    entity = provider_entity(web_provider)
    period = current_reporting_period()

    not_sent = [(ent, contact_for(ent)) \
                for ent in get_not_received_reports(entity, period)]

    context.update({'not_validated': get_reports_to_validate(entity, period),
                    'validated': get_validated_reports(entity, period),
                    'not_sent': not_sent})

    context.update({'is_complete': context['validated'].__len__() == \
                                   entity.get_children().__len__(),
                    'is_idle': context['not_validated'].__len__() == 0 \
                               and context['not_sent'].__len__() > 0})

    context.update({'time_cscom_over': time_cscom_over(), \
                    'time_district_over': time_district_over(), \
                    'time_region_over': time_region_over()})

    context.update({'validation_over': not time_can_validate(entity)})

    context.update({'current_period': current_period(), \
                    'current_reporting_period': period})

    # check permission or raise 403
    # should never raise as already checked by decorator
    provider_can_or_403('can_validate_report', web_provider, entity)

    return render(request, 'validation_list.html', context)



@provider_permission('can_validate_report')
def report_validation(request, report_receipt):  # entity, slug, year, month):

    try:
        # entity = get_object_or_404(NUTEntity, pk=int(entity))
        # month, year = int(month), int(year)
        report = NutritionReport.objects.get(receipt=report_receipt)
    except ValueError:
        raise Http404

    data = request.POST or None

    # period = MonthPeriod.find_create_from(year=year, month=month)

    # ctx = {'year': year, 'month': month, 'entity': entity}

    # qs1 = ConsumptionReport.objects.filter(period=period, entity=entity)
    # qs2 = entity.nut_orderreport_reports.filter(period=period, entity=entity)

    reports = SortedDict((
    ('pec_samp_report', report.pec_samp_report),
    ('pec_sam_report', report.pec_sam_report),
    ('pec_mam_report', report.pec_mam_report),
    ('pec_other_report', report.pec_other_report),
    ('cons_samp_report', report.cons_samp_report),
    ('cons_sam_report', report.cons_sam_report),
    ('cons_mam_report', report.cons_mam_report),
    ('order_samp_report', report.order_samp_report),
    ('order_sam_report', report.order_sam_report),
    ('order_mam_report', report.order_mam_report)))

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
        messages.success(request, u'Le rapport %s pour la '
                                  u'période du %s a été validé '
                                  u'avec succès' % (report.receipt, report.period))

    ctx = locals()
    ctx.update({'category': 'validation'})
    ctx.update(forms)
    ctx.update(reports)

    return render(request, 'validation.html', ctx)

@provider_permission('can_validate_report')
def report_do_validation(request, report_receipt):
    context = {'category': 'validation'}
    web_provider = request.user.get_profile()

    report = get_object_or_404(NutritionReport, receipt=report_receipt)

    # check permission or raise 403
    provider_can_or_403('can_validate_report', web_provider, report.entity)

    report._status = NutritionReport.STATUS_VALIDATED
    report.modified_by = web_provider
    report.modified_on = datetime.now()
    with reversion.create_revision():
        report.save()
        reversion.set_user(web_provider.user)
    context.update({'report': report})

    messages.info(request, u"Le rapport %(receipt)s de %(entity)s " \
                           u"a été validé." % {'receipt': report.receipt, \
                                              'entity': report.entity})
    return redirect('validation')
