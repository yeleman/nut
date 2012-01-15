#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime

import reversion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from bolibana.web.decorators import provider_required, provider_permission
"""from ylmnut.data import (current_period, current_reporting_period,
                         provider_entity, time_cscom_over, time_district_over,
                         time_region_over, time_can_validate,
                         get_not_received_reports, get_reports_to_validate,
                         get_validated_reports)
from bolibana.tools.utils import provider_can_or_403
"""

@provider_permission('can_validate_report')
def validation_list(request):
    context = {'category': 'validation'}
    return render(request, 'validation_list.html', context)



@provider_permission('can_validate_report')
def report_validation(request, entity, slug, year, month):





    return render(request, 'validation.html', locals())