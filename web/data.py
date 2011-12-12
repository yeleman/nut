#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import datetime, date, timedelta

from django import forms
from django.utils.translation import ugettext as _

from bolibana.models import Access, Provider
from bolibana.models import MonthPeriod


def current_period():
    """ Period of current date """
    return MonthPeriod.find_create_by_date(date.today())


def current_reporting_period():
    """ Period of reporting period applicable (last month) """
    return current_period().previous()


def contact_for(entity, recursive=True):
    """ contact person for an entity. first found at level or sup levels """
    ct, oi = Access.target_data(entity)
    providers = Provider.objects\
                        .filter(access__in=Access.objects\
                                                 .filter(content_type=ct, \
                                                         object_id=oi))
    if providers.count() == 1:
            return providers.all()[0]
    if providers.count() > 0:
        return providers.all()[0]
    if entity.parent and recursive:
        return contact_for(entity.parent)
    return None
