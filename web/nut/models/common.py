#!/usr/bin/env python
# encoding=utf-8

import reversion
from django.utils.translation import ugettext_lazy as _

from nutrsc.constants import MODERATE, SEVERE, SEVERE_COMP

NUT_TYPES = (
    (MODERATE, _(u"MAM")),  # fr-MAM
    (SEVERE, _(u"SAM")),  # fr-NAS
    (SEVERE_COMP, _(u"SAM+")))  # fr-NI


class InputsDependantReport(object):

    """ Consumption & Order checks on completeness """
    def set_complete(self):
        if self.nut_report._status < self.nut_report.STATUS_COMPLETE:
            self.nut_report._status = self.nut_report.STATUS_COMPLETE
            self.nut_report.save()

    def set_incomplete(self):
        if self.nut_report._status >= self.nut_report.STATUS_COMPLETE:
            self.nut_report._status = self.nut_report.STATUS_INCOMPLETE
            self.nut_report.save()

    @property
    def tied_reports(self):
        for t in ('cons', 'order'):
            if hasattr(self, 'input_%s_reports' % t):
                return list(getattr(self, 'input_%s_reports' % t).all())
        return []


def ensure_completeness(instance):
    """ given a Report instance, test is_complete and adjust _status """
    # if not complete, declass it.
    if not instance.is_complete():
        instance.set_incomplete()
    else:
        instance.set_complete()


def previous_value_for(instance, field):
    """ return previous (from reversion) value of a field """
    return getattr(instance, field)


class OverLoadedReport(ValueError):
    pass


class NutritionSubReport(object):

    def delete_safe(self):
        tied_reports = [] \
                       + list(getattr(self, 'tied_reports', [])) \
                       + list(getattr(self, 'tied_reports', []))
        for report in tied_reports:
            report.delete_safe()
        return self.delete()

    def data_fields(self, only_data=True):
        fields = self._meta.get_all_field_names()
        if only_data:
            fields.remove('nut_report')
        return fields

    @property
    def dirty_fields(self, only_data=True):
        """ List of fields which have changed since previous revision """
        # no dirty fields if validated
        if self.nut_report._status >= self.nut_report.STATUS_VALIDATED:
            return []

        versions = reversion.get_for_object(self)

        # no dirty fields if only one rev.
        if len(versions) <= 1:
            return []

        last, previous = versions[0:2]

        diff = []

        fields = self.data_fields(only_data)
        for field in fields:
            if last.field_dict[field] != previous.field_dict[field]:
                diff.append(field)
        return diff

    def previous_value(self, field):
        """ Value of a field in previous revision """
        versions = reversion.get_for_object(self)

        # return current value if no previous one
        if len(versions) <= 1:
            return getattr(field)

        # return value form previous [1] version
        return versions[1].field_dict[field]

    def to_dict(self):
        d = {}
        for field in self.data_fields(True):
            d[field] = getattr(self, field)
        return d

    def get(self, slug):
        """ [data browser] returns data for a slug variable """
        return getattr(self, slug)

    def field_name(self, slug):
        """ [data browser] returns name of field for a slug variable """
        return self._meta.get_field(slug).verbose_name
