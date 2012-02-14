#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import reversion
#from django.db import models
from django.utils.translation import ugettext

from nutrsc.constants import POPULATIONS
from common import NutritionSubReport


class PECReport(NutritionSubReport):

    """ PEC Meta Report """

    def cap_from_class(self):
        for cap in ('mam', 'samp', 'sam'):
            if cap in str(self.__class__).lower():
                return cap.upper()


    def __unicode__(self):
        cap = self.cap_from_class()
        if not getattr(self, 'id', None):
            return cap
        return ugettext(u"%(entity)s/%(cap)s/%(period)s") \
                        % {'entity': self.nut_report.entity, \
                           'period': self.nut_report.period,
                           'cap': cap}

    def data_fields(self, only_data=True):
        fields = self._meta.get_all_field_names()
        if only_data:
            # ie. the ones starting by the age prefix
            fields = [x for x in fields if x[0:3] \
                     in ([('%s_' % k)[0:3] for k in POPULATIONS.keys()])]
        return fields

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

    def all_for_field(self, field):
        """ returns sum of all ages for a field """
        sum_ = 0
        for cat, cat_name in self.CATEGORIES:
            val = getattr(self, '%s_%s' % (cat, field), None)
            sum_ += val if val is not None else 0
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

    # MALE/FEMALE TOTALS
    @property
    def u6_total_beginning(self):
        return self.male_female_sum('u6_total_beginning')

    @property
    def u6_admitted(self):
        return self.male_female_sum('u6_admitted')

    @property
    def u6_total_out(self):
        return self.male_female_sum('u6_total_out')

    @property
    def u6_total_end(self):
        return self.male_female_sum('u6_total_end')

    @property
    def u59_total_beginning(self):
        return self.male_female_sum('u59_total_beginning')

    @property
    def u59_admitted(self):
        return self.male_female_sum('u59_admitted')

    @property
    def u59_total_out(self):
        return self.male_female_sum('u59_total_out')

    @property
    def u59_total_end(self):
        return self.male_female_sum('u59_total_end')

    @property
    def o59_total_beginning(self):
        return self.male_female_sum('o59_total_beginning')

    @property
    def o59_admitted(self):
        return self.male_female_sum('o59_admitted')

    @property
    def o59_total_out(self):
        return self.male_female_sum('o59_total_out')

    @property
    def o59_total_end(self):
        return self.male_female_sum('o59_total_end')

    # ALL AGE TOTALS
    @property
    def all_total_beginning(self):
        return self.all_for_field('total_beginning')

    @property
    def all_total_beginning_m(self):
        return self.all_for_field('total_beginning_m')

    @property
    def all_total_beginning_f(self):
        return self.all_for_field('total_beginning_f')

    @property
    def all_hw_b7080_bmi_u18(self):
        return self.all_for_field('total_beginning_f')

    @property
    def all_muac_u120(self):
        return self.all_for_field('muac_u120')

    @property
    def all_hw_u70_bmi_u16(self):
        return self.all_for_field('hw_u70_bmi_u16')

    @property
    def all_muac_u11_muac_u18(self):
        return self.all_for_field('muac_u11_muac_u18')

    @property
    def all_oedema(self):
        return self.all_for_field('oedema')

    @property
    def all_other(self):
        return self.all_for_field('other')

    @property
    def all_new_case(self):
        return self.all_for_field('new_case')

    @property
    def all_relapse(self):
        return self.all_for_field('relapse')

    @property
    def all_returned(self):
        return self.all_for_field('returned')

    @property
    def all_nut_transfered_in(self):
        return self.all_for_field('nut_transfered_in')

    @property
    def all_nut_referred_in(self):
        return self.all_for_field('nut_referred_in')

    @property
    def all_total_admitted(self):
        return self.all_for_field('total_admitted')

    @property
    def all_total_admitted_m(self):
        return self.all_for_field('total_admitted_m')

    @property
    def all_total_admitted_f(self):
        return self.all_for_field('total_admitted_f')

    @property
    def all_healed(self):
        return self.all_for_field('healed')

    @property
    def all_referred_out(self):
        return self.all_for_field('referred_out')

    @property
    def all_deceased(self):
        return self.all_for_field('deceased')

    @property
    def all_aborted(self):
        return self.all_for_field('aborted')

    @property
    def all_non_respondant(self):
        return self.all_for_field('non_respondant')

    @property
    def all_medic_transfered_out(self):
        return self.all_for_field('medic_transfered_out')

    @property
    def all_nut_transfered_out(self):
        return self.all_for_field('nut_transfered_out')

    @property
    def all_total_out(self):
        return self.all_for_field('total_out')

    @property
    def all_total_out_m(self):
        return self.all_for_field('total_out_m')

    @property
    def all_total_out_f(self):
        return self.all_for_field('total_out_f')

    @property
    def all_total_end(self):
        return self.all_for_field('total_end')

    @property
    def all_total_end_m(self):
        return self.all_for_field('total_end_m')

    @property
    def all_total_end_f(self):
        return self.all_for_field('total_end_f')
