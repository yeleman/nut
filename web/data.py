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


def provider_entity(provider):
    """ Entity a Provider is attached to """
    return provider.first_access().target


def get_reports_to_validate(entity, period=current_reporting_period()):
    """ List of Entity which have sent report but are not validated """
    return [(report.entity, report) \
            for report \
            in MalariaReport.unvalidated\
                            .filter(entity__in=entity.get_children(), \
                                    period=period)]


def get_validated_reports(entity, period=current_reporting_period()):
    """ List of all Entity which report have been validated """
    return [(report.entity, report) \
            for report \
            in MalariaReport.validated\
                            .filter(entity__in=entity.get_children(), \
                                    period=period)]


def get_not_received_reports(entity, period=current_reporting_period()):
    """ List of all Entity which have not send in a report """
    units = list(entity.get_children().all())
    reports = MalariaReport.objects.filter(entity__in=entity.get_children(), \
                                           period=period)
    for report in reports:
        units.remove(report.entity)
    return units


def time_over_by_delta(delta, period=current_period()):
    """ whether current date + delta is past """
    today = date.today()
    return date.fromtimestamp(float(period.end_on.strftime('%s'))) \
                              + delta <= today


def time_cscom_over(period=current_period()):
    """ time_over_by_delta() with cscom delta """
    return time_over_by_delta(timedelta(days=10), period)


def time_district_over(period=current_period()):
    """ time_over_by_delta() with district delta """
    return time_over_by_delta(timedelta(days=20), period)


def time_region_over(period=current_period()):
    """ time_over_by_delta() with region delta """
    return time_over_by_delta(timedelta(days=30), period)


def time_can_validate(entity):
    """ is it possible to do validation now for that entity? """
    level = entity.type.slug
    if level == 'district':
        return not time_district_over()
    if level == 'region':
        return not time_region_over()
    return False


def current_stage():
    period = current_reporting_period()
    if not time_cscom_over(period):
        return 'cscom'
    if not time_district_over(period):
        return 'district'
    if not time_region_over(period):
        return 'region'
    return 'over'


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


def most_accurate_report(provider, period=current_reporting_period()):
    # don't use that anymore I think
    try:
        return MalariaReport.validated.filter(period=period)[0]
    except:
        return None


def raw_data_periods_for(entity):
    """ periods with validated report for an entity """
    return [r.mperiod for r in MalariaReport.validated.filter(entity=entity)]
