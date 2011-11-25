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


class NUTReport(object):

    """ NUT Meta Report """

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
            if hasattr('%s_%s' % (cat, field)):
                sum_ += getattr(self, '%s_%s' % (cat, field))
        return sum_

    # MALE/FEMALE TOTALS
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

    @property
    def fu1_total_beginning(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def fu1_admitted(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def fu1_total_out(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def fu1_total_end(self):
        return self.male_female_sum(inspect.stack()[0][3])

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
