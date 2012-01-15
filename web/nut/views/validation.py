#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import calendar
import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from bolibana.web.decorators import provider_permission

from nut.models import NUTEntity
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

    samp_report = extract(entity.nut_pecsampreport_reports.formonth(month, year),
                          0, default=None)

    sam_report = extract(entity.nut_pecsamreport_reports.formonth(month, year),
                         0, default=None)

    mam_report = extract(entity.nut_pecmamreport_reports.formonth(month, year),
                         0, default=None)

    other_report = extract(entity.nut_pecothersreport_reports.formonth(month, year),
                           0, default=None)

    return render(request, 'validation.html', locals())