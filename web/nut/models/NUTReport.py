#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import inspect

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib import admin
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana.models import EntityType, Entity, Report, MonthPeriod
from bolibana.tools.utils import generate_receipt
from nutrsc.constants import *


class NUTReport(object):

    """ NUT Meta Report """

    def cap_from_class(self):
        for cap in ('mam', 'samp', 'sam'):
            if cap in str(self.__class__).lower():
                return cap.upper()
            

    def __unicode__(self):
        cap = self.cap_from_class()
        return ugettext(u"%(entity)s/%(cap)s/%(period)s") \
                        % {'entity': self.entity, \
                           'period': self.period,
                           'cap': cap}

    @property
    def dirty_fields(self, only_data=True):
        """ List of fields which have changed since previous revision """
        # no dirty fields if validated
        if self._status >= self.STATUS_VALIDATED:
            return []

        versions = reversion.get_for_object(self)
        
        # no dirty fields if only one rev.
        if len(versions) <= 1:
            return []
        
        last, previous = versions[0:2]

        diff = []

        fields = self._meta.get_all_field_names()
        if only_data:
            # only data fields
            # ie. the ones starting by the age prefix
            fields = [x for x in fields if x[0:3] \
                     in ([('%s_' % k)[0:3] for k in POPULATIONS.keys()])]
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
        return version[1].field_dict[field]

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        mp = self.period
        mp.__class__ = MonthPeriod
        return mp

    @classmethod
    def start(cls, period, entity, author, \
               type=Report.TYPE_SOURCE, *args, **kwargs):
        """ creates a report object with meta data only. Object not saved """
        report = cls(period=period, entity=entity, created_by=author, \
                     modified_by=author, _status=cls.STATUS_CREATED, \
                     type=type)
        for arg, value in kwargs.items():
            try:
                setattr(report, arg, value)
            except AttributeError:
                pass

        return report

    def to_dict(self):
        d = {}
        for field in self._meta.get_all_field_names():
            try:
                if not field.split('_')[0] in ('u5', 'o5', 'pw', 'stockout'):
                    continue
            except:
                continue
            d[field] = getattr(self, field)
        return d

    def get(self, slug):
        """ [data browser] returns data for a slug variable """
        return getattr(self, slug)

    def field_name(self, slug):
        """ [data browser] returns name of field for a slug variable """
        return self._meta.get_field(slug).verbose_name

    def validate(self):
        """ runs MalariaReportValidator """
        #validator = MalariaReportValidator(self)
        #validator.validate()
        #return validator.errors
        return []

    # HELPERS
    def male_female_sum(self, field):
        """ sum of male + female for a field """
        male = getattr(self, '%s_m' % field) \
            if hasattr(self, '%s_m' % field) else 0
        female = getattr(self, '%s_f' % field) \
            if hasattr(self, '%s_f' % field) else 0
        return male + female

    def other_sum(self, field):
        """ sum of all other field for an age """
        hiv = getattr(self, '%s_hiv' % field) \
            if hasattr(self, '%s_hiv' % field) else 0
        tb = getattr(self, '%s_tb' % field) \
            if hasattr(self, '%s_tb' % field) else 0
        lwb = getattr(self, '%s_lwb' % field) \
            if hasattr(self, '%s_lwb' % field) else 0
        return sum([hiv, tb, lwb])

    def all_for_field(self, field):
        """ returns sum of all ages for a field """
        sum_ = 0
        for cat, cat_name in self.CATEGORIES:
            if hasattr(self, '%s_%s' % (cat, field)):
                sum_ += getattr(self, '%s_%s' % (cat, field))
        return sum_

    def total_end_for(self, age, sex):
        """ calculates remaining people for an age and sex """
        initial = getattr(self, '%s_total_beginning_%s' % (age, sex))
        admitted = getattr(self, '%s_total_admitted_%s' % (age, sex))
        out = getattr(self, '%s_total_out_%s' % (age, sex))
        return (initial + admitted) - out

    def add_all_data(self, data_browser):
        """ Add all data to report from data browser by calling sub meth. """
        for catid, catname in self.CATEGORIES:
            getattr(self, 'add_%s_data' \
                          % catid)(*data_browser.data_for_cat(catid))

    # REMAINING
    @property
    def u6_total_end_f(self):
        return self.total_end_for('u6', 'f')

    @property
    def u6_total_end_m(self):
        return self.total_end_for('u6', 'm')

    @property
    def u59_total_end_f(self):
        return self.total_end_for('u59', 'f')

    @property
    def u59_total_end_m(self):
        return self.total_end_for('u59', 'm')

    @property
    def o59_total_end_f(self):
        return self.total_end_for('o59', 'f')

    @property
    def o59_total_end_m(self):
        return self.total_end_for('o59', 'm')

    @property
    def fu1_total_end_f(self):
        return self.total_end_for('fu1', 'f')

    @property
    def fu1_total_end_m(self):
        return self.total_end_for('fu1', 'm')

    @property
    def pw_total_end_f(self):
        return self.total_end_for('pw', 'f')

    @property
    def pw_total_end_m(self):
        return self.total_end_for('pw', 'm')

    @property
    def fu12_total_end_f(self):
        return self.total_end_for('fu12', 'f')

    @property
    def fu12_total_end_m(self):
        return self.total_end_for('fu12', 'm')

    # OTHERS
    @property
    def u6_other(self):
        return self.other_sum(inspect.stack()[0][3])

    @property
    def u59_other(self):
        return self.other_sum(inspect.stack()[0][3])

    @property
    def o59_other(self):
        return self.other_sum(inspect.stack()[0][3])

    @property
    def fu1_other(self):
        return self.other_sum(inspect.stack()[0][3])

    @property
    def pw_other(self):
        return self.other_sum(inspect.stack()[0][3])

    @property
    def fu12_other(self):
        return self.other_sum(inspect.stack()[0][3])

    # MALE/FEMALE TOTALS
    @property
    def u6_total_beginning(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def u6_admitted(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def u6_total_out(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def u6_total_end(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def u59_total_beginning(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def u59_admitted(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def u59_total_out(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def u59_total_end(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def o59_total_beginning(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def o59_admitted(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def o59_total_out(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def o59_total_end(self):
        return self.male_female_sum(inspect.stack()[0][3])

    # ALL AGE TOTALS
    @property
    def all_total_beginning(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_beginning_m(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_beginning_f(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_hw_b7080_bmi_u18(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_muac_u120(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_hw_u70_bmi_u16(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_muac_u11_muac_u18(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_oedema(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_other(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_other_hiv(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_other_tb(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_other_lwb(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_new_case(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_relapse(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_returned(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_nut_transfered_in(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_nut_referred_in(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_admitted(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_admitted_m(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_admitted_f(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_healed(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_referred_out(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_deceased(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_aborted(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_non_respondant(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_medic_transfered_out(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_nut_transfered_out(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_out(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_out_m(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_out_f(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_end(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_end_m(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_total_end_f(self):
        return self.all_for_field(inspect.stack()[0][3][4:])


def pre_save_report(sender, instance, **kwargs):
    print("pre_save_report: %s" % instance)
    """ change _status property of Report on save() at creation """
    if instance._status == instance.STATUS_UNSAVED:
        instance._status = instance.STATUS_CLOSED
    # following will allow us to detect failure in registration
    if not instance.receipt:
        instance.receipt = 'NO_RECEIPT'


def post_save_report(sender, instance, **kwargs):
    """ generates the receipt """
    if instance.receipt == 'NO_RECEIPT':
        instance.receipt = generate_receipt(instance, fix='P',
                                            add_random=True)
        instance.save()
