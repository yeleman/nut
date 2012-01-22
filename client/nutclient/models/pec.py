#!/usr/bin/env python
# encoding=utf-8

import inspect

import peewee

from nutrsc import constants
from . import BaseModel, Report


class PECReport(object):

    @property
    def status(self):
        return self.report.status

    STATUS_CREATED = Report.STATUS_CREATED
    STATUS_DRAFT = Report.STATUS_DRAFT
    STATUS_COMPLETE = Report.STATUS_COMPLETE
    STATUS_SENT = Report.STATUS_SENT
    STATUS_REMOTE_MODIFIED = Report.STATUS_REMOTE_MODIFIED
    STATUS_LOCAL_MODIFIED = Report.STATUS_LOCAL_MODIFIED

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
            if hasattr(self, '%s_%s' % (cat, field)):
                sum_ += getattr(self, '%s_%s' % (cat, field))
        return sum_

    def total_end_for(self, age, sex):
        """ calculates remaining people for an age and sex """
        initial = getattr(self, '%s_total_beginning_%s' % (age, sex))
        admitted = getattr(self, '%s_admitted_%s' % (age, sex))
        out = getattr(self, '%s_total_out_%s' % (age, sex))
        return (initial + admitted) - out

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

    @property
    def fu12_total_beginning(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def fu12_admitted(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def fu12_total_out(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def fu12_total_end(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def pw_total_beginning(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def pw_admitted(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def pw_total_out(self):
        return self.male_female_sum(inspect.stack()[0][3])

    @property
    def pw_total_end(self):
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
    def all_admitted(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_admitted_m(self):
        return self.all_for_field(inspect.stack()[0][3][4:])

    @property
    def all_admitted_f(self):
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
    
    @property
    def sum_begining(self):
        return self.get_sum_beginning('all')
    
    def get_sum_begining(self, age):
        return getattr(self, '%s_total_beginning' % age)

    @property
    def sum_admitted_crit(self):
        return self.get_sum_admitted_details('all')

    def get_sum_admitted_crit(self, age):
        return sum([getattr(self, '%s_hw_b7080_bmi_u18' % age, 0),
                    getattr(self, '%s_muac_u120' % age, 0),
                    getattr(self, '%s_other' % age, 0),
                    getattr(self, '%s_hw_u70_bmi_u16' % age, 0),
                    getattr(self, '%s_muac_u11_muac_u18' % age, 0),
                    getattr(self, '%s_oedema' % age, 0)])

    @property
    def sum_admitted_typ(self):
        return self.get_sum_admitted_details('all')
    
    def get_sum_admitted_typ(self, age):
        return sum([getattr(self, '%s_new_case' % age, 0),
                    getattr(self, '%s_relapse' % age, 0),
                    getattr(self, '%s_returned' % age, 0),
                    getattr(self, '%s_nut_transfered_in' % age, 0),
                    getattr(self, '%s_nut_referred_in' % age, 0)])

    @property
    def sum_admitted_gender(self):
        return self.get_sum_admitted_gender('all')

    def get_sum_admitted_gender(self, age):
        return getattr(self, '%s_admitted' % age, 0)

    @property
    def sum_out_details(self):
        return self.get_sum_out_details('all')

    def get_sum_out_details(self, age):
        return sum([getattr(self, '%s_healed' % age, 0),
                    getattr(self, '%s_referred_out' % age, 0),
                    getattr(self, '%s_deceased' % age, 0),
                    getattr(self, '%s_aborted' % age, 0),
                    getattr(self, '%s_non_respondant' % age, 0),
                    getattr(self, '%s_medic_transfered_out' % age, 0),
                    getattr(self, '%s_nut_transfered_out' % age, 0)])

    @property
    def sum_out_gender(self):
        return self.get_sum_out_gender('all')


    def get_sum_out_gender(self, age):
        return getattr(self, '%s_total_out' % age)

    
    def is_valid(self):
        for age, age_name in self.CATEGORIES:
            # PEC ADM
            print('\tchecking PEC ADM %s' % age)
            if (self.get_sum_admitted_crit(age) 
                != self.get_sum_admitted_typ(age) 
                or self.get_sum_admitted_crit(age)
                != self.get_sum_admitted_gender(age)):
                
                return False

            print('\tchecking PEC OUT %s' % age)
            # PEC OUT
            if (self.get_sum_out_details(age)
                != self.get_sum_out_gender(age)):

                return False

            print('\tchecking PEC BEG+ADM<OUT %s' % age)
            # Begining + ADM <= out
            if (self.get_sum_begining(age) + self.get_sum_admitted_gender(age)
                < self.get_sum_out_gender(age)):
                return False
         
        return False

class PECMAMReport(BaseModel, PECReport):

    CATEGORIES = (('u59', u"6 to 59 months old"),
                  ('pw', u"Pregnant/Breast-feeding Women"),
                  ('fu12', u"Follow-up URENI/UNRENAS"))

    CAP = constants.MODERATE

    report = peewee.ForeignKeyField(Report, unique=True,
                                    related_name='pec_mam_reports')

    # over 59 months
    u59_total_beginning_m = peewee.IntegerField(default=0)
    u59_total_beginning_f = peewee.IntegerField(default=0)
    u59_hw_b7080_bmi_u18 = peewee.IntegerField(default=0)
    u59_muac_u120 = peewee.IntegerField(default=0)
    u59_other = peewee.IntegerField(default=0)
    u59_new_case = peewee.IntegerField(default=0)
    u59_relapse = peewee.IntegerField(default=0)
    u59_returned = peewee.IntegerField(default=0)
    u59_nut_referred_in = peewee.IntegerField(default=0)
    u59_admitted_m = peewee.IntegerField(default=0)
    u59_admitted_f = peewee.IntegerField(default=0)

    # OUT
    u59_healed = peewee.IntegerField(default=0)
    u59_referred_out = peewee.IntegerField(default=0)
    u59_deceased = peewee.IntegerField(default=0)
    u59_aborted = peewee.IntegerField(default=0)
    u59_non_respondant = peewee.IntegerField(default=0)
    u59_medic_transfered_out = peewee.IntegerField(default=0)
    u59_total_out_m = peewee.IntegerField(default=0)
    u59_total_out_f = peewee.IntegerField(default=0)

    # pregnant women or feed_breasting women
    pw_total_beginning_f = peewee.IntegerField(default=0)
    pw_hw_b7080_bmi_u18 = peewee.IntegerField(default=0)
    pw_muac_u120 = peewee.IntegerField(default=0)
    pw_other = peewee.IntegerField(default=0)
    pw_new_case = peewee.IntegerField(default=0)
    pw_relapse = peewee.IntegerField(default=0)
    pw_returned = peewee.IntegerField(default=0)
    pw_nut_referred_in = peewee.IntegerField(default=0)
    pw_admitted_f = peewee.IntegerField(default=0)

    # OUT
    pw_healed = peewee.IntegerField(default=0)
    pw_referred_out = peewee.IntegerField(default=0)
    pw_deceased = peewee.IntegerField(default=0)
    pw_aborted = peewee.IntegerField(default=0)
    pw_non_respondant = peewee.IntegerField(default=0)
    pw_medic_transfered_out = peewee.IntegerField(default=0)
    pw_total_out_f = peewee.IntegerField(default=0)

    # Follow_up (1) and (2)
    # pregnant women or feed_breasting women
    fu12_total_beginning_m = peewee.IntegerField(default=0)
    fu12_total_beginning_f = peewee.IntegerField(default=0)
    fu12_hw_b7080_bmi_u18 = peewee.IntegerField(default=0)
    fu12_muac_u120 = peewee.IntegerField(default=0)
    fu12_other = peewee.IntegerField(default=0)
    fu12_nut_referred_in = peewee.IntegerField(default=0)
    fu12_admitted_m = peewee.IntegerField(default=0)
    fu12_admitted_f = peewee.IntegerField(default=0)

    # OUT
    fu12_healed = peewee.IntegerField(default=0)
    fu12_referred_out = peewee.IntegerField(default=0)
    fu12_deceased = peewee.IntegerField(default=0)
    fu12_aborted = peewee.IntegerField(default=0)
    fu12_non_respondant = peewee.IntegerField(default=0)
    fu12_medic_transfered_out = peewee.IntegerField(default=0)
    fu12_total_out_m = peewee.IntegerField(default=0)
    fu12_total_out_f = peewee.IntegerField(default=0)

class PECSAMReport(BaseModel, PECReport):

    CATEGORIES = (('u59', u"6 to 59 months old"),
                  ('o59', u"Over 59 months old"),
                  ('fu1', u"Follow-up URENI 1"))

    CAP = constants.SEVERE

    report = peewee.ForeignKeyField(Report, unique=True,
                                    related_name='pec_sam_reports')

    # 6 months old to 59 months old
    u59_total_beginning_m = peewee.IntegerField(default=0)
    u59_total_beginning_f = peewee.IntegerField(default=0)
    u59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    u59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    u59_oedema = peewee.IntegerField(default=0)
    u59_other = peewee.IntegerField(default=0)

    u59_new_case = peewee.IntegerField(default=0)
    u59_relapse = peewee.IntegerField(default=0)
    u59_returned = peewee.IntegerField(default=0)
    u59_nut_transfered_in = peewee.IntegerField(default=0)
    u59_nut_referred_in = peewee.IntegerField(default=0)
    u59_admitted_m = peewee.IntegerField(default=0)
    u59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    u59_healed = peewee.IntegerField(default=0)
    u59_referred_out = peewee.IntegerField(default=0)
    u59_deceased = peewee.IntegerField(default=0)
    u59_aborted = peewee.IntegerField(default=0)
    u59_non_respondant = peewee.IntegerField(default=0)
    u59_medic_transfered_out = peewee.IntegerField(default=0)
    u59_nut_transfered_out = peewee.IntegerField(default=0)
    u59_total_out_m = peewee.IntegerField(default=0)
    u59_total_out_f = peewee.IntegerField(default=0)

    # over 59 months
    o59_total_beginning_m = peewee.IntegerField(default=0)
    o59_total_beginning_f = peewee.IntegerField(default=0)
    o59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    o59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    o59_oedema = peewee.IntegerField(default=0)
    o59_other = peewee.IntegerField(default=0)

    o59_new_case = peewee.IntegerField(default=0)
    o59_relapse = peewee.IntegerField(default=0)
    o59_returned = peewee.IntegerField(default=0)
    o59_nut_transfered_in = peewee.IntegerField(default=0)
    o59_nut_referred_in = peewee.IntegerField(default=0)
    o59_admitted_m = peewee.IntegerField(default=0)
    o59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    o59_healed = peewee.IntegerField(default=0)
    o59_referred_out = peewee.IntegerField(default=0)
    o59_deceased = peewee.IntegerField(default=0)
    o59_aborted = peewee.IntegerField(default=0)
    o59_non_respondant = peewee.IntegerField(default=0)
    o59_medic_transfered_out = peewee.IntegerField(default=0)
    o59_nut_transfered_out = peewee.IntegerField(default=0)
    o59_total_out_m = peewee.IntegerField(default=0)
    o59_total_out_f = peewee.IntegerField(default=0)

    # Follow_up URENI (1)
    fu1_total_beginning_m = peewee.IntegerField(default=0)
    fu1_total_beginning_f = peewee.IntegerField(default=0)
    fu1_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    fu1_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    fu1_oedema = peewee.IntegerField(default=0)
    fu1_other = peewee.IntegerField(default=0)

    fu1_new_case = peewee.IntegerField(default=0)
    fu1_relapse = peewee.IntegerField(default=0)
    fu1_returned = peewee.IntegerField(default=0)
    fu1_nut_transfered_in = peewee.IntegerField(default=0)
    fu1_nut_referred_in = peewee.IntegerField(default=0)
    fu1_admitted_m = peewee.IntegerField(default=0)
    fu1_admitted_f = peewee.IntegerField(default=0)
    # OUT
    fu1_healed = peewee.IntegerField(default=0)
    fu1_referred_out = peewee.IntegerField(default=0)
    fu1_deceased = peewee.IntegerField(default=0)
    fu1_aborted = peewee.IntegerField(default=0)
    fu1_non_respondant = peewee.IntegerField(default=0)
    fu1_medic_transfered_out = peewee.IntegerField(default=0)
    fu1_nut_transfered_out = peewee.IntegerField(default=0)
    fu1_total_out_m = peewee.IntegerField(default=0)
    fu1_total_out_f = peewee.IntegerField(default=0)


class PECSAMPReport(BaseModel, PECReport):

    CATEGORIES = (('u6', u"Under 6 months old"),
                  ('u59', u"6 to 59 months old"),
                  ('o59', u"Over 59 months old"))

    CAP = constants.SEVERE_COMP

    report = peewee.ForeignKeyField(Report, unique=True,
                                    related_name='pec_samp_reports')

    # under 6 months
    u6_total_beginning_m = peewee.IntegerField(default=0)
    u6_total_beginning_f = peewee.IntegerField(default=0)
    u6_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    u6_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    u6_oedema = peewee.IntegerField(default=0)
    u6_other = peewee.IntegerField(default=0)

    u6_new_case = peewee.IntegerField(default=0)
    u6_relapse = peewee.IntegerField(default=0)
    u6_returned = peewee.IntegerField(default=0)
    u6_nut_transfered_in = peewee.IntegerField(default=0)
    u6_admitted_m = peewee.IntegerField(default=0)
    u6_admitted_f = peewee.IntegerField(default=0)
    # OUT
    u6_healed = peewee.IntegerField(default=0)
    u6_deceased = peewee.IntegerField(default=0)
    u6_aborted = peewee.IntegerField(default=0)
    u6_non_respondant = peewee.IntegerField(default=0)
    u6_medic_transfered_out = peewee.IntegerField(default=0)
    u6_nut_transfered_out = peewee.IntegerField(default=0)
    u6_total_out_m = peewee.IntegerField(default=0)
    u6_total_out_f = peewee.IntegerField(default=0)

    # Between 6 months and 59 months
    u59_total_beginning_m = peewee.IntegerField(default=0)
    u59_total_beginning_f = peewee.IntegerField(default=0)
    u59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    u59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    u59_oedema = peewee.IntegerField(default=0)
    u59_other = peewee.IntegerField(default=0)

    u59_new_case = peewee.IntegerField(default=0)
    u59_relapse = peewee.IntegerField(default=0)
    u59_returned = peewee.IntegerField(default=0)
    u59_nut_transfered_in = peewee.IntegerField(default=0)
    u59_admitted_m = peewee.IntegerField(default=0)
    u59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    u59_healed = peewee.IntegerField(default=0)
    u59_deceased = peewee.IntegerField(default=0)
    u59_aborted = peewee.IntegerField(default=0)
    u59_non_respondant = peewee.IntegerField(default=0)
    u59_medic_transfered_out = peewee.IntegerField(default=0)
    u59_nut_transfered_out = peewee.IntegerField(default=0)
    u59_total_out_m = peewee.IntegerField(default=0)
    u59_total_out_f = peewee.IntegerField(default=0)

    # over 59 months
    o59_total_beginning_m = peewee.IntegerField(default=0)
    o59_total_beginning_f = peewee.IntegerField(default=0)
    o59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    o59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    o59_oedema = peewee.IntegerField(default=0)
    o59_other = peewee.IntegerField(default=0)

    o59_new_case = peewee.IntegerField(default=0)
    o59_relapse = peewee.IntegerField(default=0)
    o59_returned = peewee.IntegerField(default=0)
    o59_nut_transfered_in = peewee.IntegerField(default=0)
    o59_admitted_m = peewee.IntegerField(default=0)
    o59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    o59_healed = peewee.IntegerField(default=0)
    o59_deceased = peewee.IntegerField(default=0)
    o59_aborted = peewee.IntegerField(default=0)
    o59_non_respondant = peewee.IntegerField(default=0)
    o59_medic_transfered_out = peewee.IntegerField(default=0)
    o59_nut_transfered_out = peewee.IntegerField(default=0)
    o59_total_out_m = peewee.IntegerField(default=0)
    o59_total_out_f = peewee.IntegerField(default=0)