#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from NUTReport import NUTReport, pre_save_report, post_save_report
from bolibana.models import EntityType, Entity, Report, MonthPeriod


class PECNAMReport(NUTReport, Report):

    """ PEC Report URENAM """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"PEC URENAM Report")
        verbose_name_plural = _(u"PEC URENAM Reports")
        unique_together = ('period', 'entity', 'type')

    CATEGORIES = (('u59', _(u"6 to 59 months old")),
                  ('pw', _(u"Pregnant/Breast-feeding Women")),
                  ('fu12', _(u"Follow-up URENI/UNRENAS")))

    # over 59 months
    u59_total_beginning_m = models.PositiveIntegerField( \
                                         _(u"Total male at Begining of Month"))
    u59_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    u59_hw_b7080_bmi_u18 = models.PositiveIntegerField( \
                                                 _(u"H/W ≥70%<80% or BMI <18"))
    u59_muac_u120 = models.PositiveIntegerField( \
                                                  _(u"MUAC <120 or MUAC <210"))
    u59_other_hiv = models.PositiveIntegerField( \
                                                  _(u"Other: Living with HIV"))
    u59_other_tb = models.PositiveIntegerField( \
                                                               _(u"Other: TB"))
    u59_other_lwb = models.PositiveIntegerField( \
                                              _(u"Other: Low weight at birth"))
    u59_new_case = models.PositiveIntegerField( \
                                                                _(u"New Case"))
    u59_relapse = models.PositiveIntegerField( \
                                                  _(u"Relapse (after healed)"))
    u59_returned = models.PositiveIntegerField( \
                                     _(u"Returned (after leaving) or medical"))
    u59_nut_referred_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional reference"))
    u59_admitted_m = models.PositiveIntegerField( \
                                                     _(u"Total male admitted"))
    u59_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    u59_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    u59_referred_out = models.PositiveIntegerField( \
                                                      _(u"Referred to URENAM"))
    u59_deceased = models.PositiveIntegerField( \
                                                                _(u"Deceased"))
    u59_aborted = models.PositiveIntegerField( \
                                                                 _(u"Aborted"))
    u59_non_respondant = models.PositiveIntegerField( \
                                                          _(u"Non respondant"))
    u59_medic_transfered_out = models.PositiveIntegerField( \
                                                       _(u"Medical transfert"))
    u59_total_out_m = models.PositiveIntegerField( \
                                                     _(u"Total male departed"))
    u59_total_out_f = models.PositiveIntegerField( \
                                                   _(u"Total female departed"))
    u59_total_end_m = models.PositiveIntegerField( \
                                              _(u"Total male at end of month"))
    u59_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))

    # pregnant women or feed_breasting women
    pw_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    pw_hw_b7080_bmi_u18 = models.PositiveIntegerField( \
                                                 _(u"H/W ≥70%<80% or BMI <18"))
    pw_muac_u120 = models.PositiveIntegerField( \
                                                  _(u"MUAC <120 or MUAC <210"))
    pw_other_hiv = models.PositiveIntegerField( \
                                                  _(u"Other: Living with HIV"))
    pw_other_tb = models.PositiveIntegerField( \
                                                               _(u"Other: TB"))
    pw_other_lwb = models.PositiveIntegerField( \
                                              _(u"Other: Low weight at birth"))
    pw_new_case = models.PositiveIntegerField( \
                                                                _(u"New Case"))
    pw_relapse = models.PositiveIntegerField( \
                                                  _(u"Relapse (after healed)"))
    pw_returned = models.PositiveIntegerField( \
                                     _(u"Returned (after leaving) or medical"))
    pw_nut_referred_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional reference"))
    pw_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    pw_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    pw_referred_out = models.PositiveIntegerField( \
                                                      _(u"Referred to URENAM"))
    pw_deceased = models.PositiveIntegerField( \
                                                                _(u"Deceased"))
    pw_aborted = models.PositiveIntegerField( \
                                                                 _(u"Aborted"))
    pw_non_respondant = models.PositiveIntegerField( \
                                                          _(u"Non respondant"))
    pw_medic_transfered_out = models.PositiveIntegerField( \
                                                       _(u"Medical transfert"))
    pw_total_out_f = models.PositiveIntegerField( \
                                                   _(u"Total female departed"))
    pw_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))
    
    # Follow_up (1) and (2)
    # pregnant women or feed_breasting women
    fu12_total_beginning_m = models.PositiveIntegerField( \
                                         _(u"Total male at Begining of Month"))
    fu12_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    fu12_hw_b7080_bmi_u18 = models.PositiveIntegerField( \
                                                 _(u"H/W ≥70%<80% or BMI <18"))
    fu12_muac_u120 = models.PositiveIntegerField( \
                                                  _(u"MUAC <120 or MUAC <210"))
    fu12_other_hiv = models.PositiveIntegerField( \
                                                  _(u"Other: Living with HIV"))
    fu12_other_tb = models.PositiveIntegerField( \
                                                               _(u"Other: TB"))
    fu12_other_lwb = models.PositiveIntegerField( \
                                              _(u"Other: Low weight at birth"))
    fu12_nut_referred_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional reference"))
    fu12_admitted_m = models.PositiveIntegerField( \
                                                     _(u"Total male admitted"))
    fu12_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    fu12_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    fu12_referred_out = models.PositiveIntegerField( \
                                                      _(u"Referred to URENAM"))
    fu12_deceased = models.PositiveIntegerField( \
                                                                _(u"Deceased"))
    fu12_aborted = models.PositiveIntegerField( \
                                                                 _(u"Aborted"))
    fu12_non_respondant = models.PositiveIntegerField( \
                                                          _(u"Non respondant"))
    fu12_medic_transfered_out = models.PositiveIntegerField( \
                                                       _(u"Medical transfert"))
    fu12_total_out_m = models.PositiveIntegerField( \
                                                     _(u"Total male departed"))
    fu12_total_out_f = models.PositiveIntegerField( \
                                                   _(u"Total female departed"))
    fu12_total_end_m = models.PositiveIntegerField( \
                                              _(u"Total male at end of month"))
    fu12_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))

    # Aggregation
    sources = models.ManyToManyField('PECNAMReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)
    # HELPERS
    def male_female_sum(self, field):
        """ sum of male + female for a field """
        return getattr(self, '%s_m' % field) + getattr(self, '%s_f' % field)

    def all_for_field(self, field):
        """ returns sum of all ages for a field """
        sum_ = 0
        for cat, cat_name in CATEGORIES:
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

pre_save.connect(pre_save_report, sender=PECNAMReport)
post_save.connect(post_save_report, sender=PECNAMReport)
