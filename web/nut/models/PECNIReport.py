#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from NUTReport import NUTReport
from bolibana.models import EntityType, Entity, Report, MonthPeriod


class PECNIReport(NUTReport, Report):

    """ PEC Report URENI """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"PEC URENI Report")
        verbose_name_plural = _(u"PEC URENI Reports")
        unique_together = ('period', 'entity', 'type')

    CATEGORIES = (('u6', _(u"Under 6 months old")),
                  ('u59', _(u"6 to 59 months old")),
                  ('o59', _(u"Over 59 months old")))

    # under 6 months
    u6_total_beginning_m = models.PositiveIntegerField( \
                                         _(u"Total male at Begining of Month"))
    u6_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    u6_hw_u70_bmi_u16 = models.PositiveIntegerField( \
                                                     _(u"H/W <70% or BMI <16"))
    u6_muac_u11_muac_u18 = models.PositiveIntegerField( \
                                                    _(u"MUAC <11 or MUAC <18"))
    u6_oedema = models.PositiveIntegerField( \
                                                                  _(u"Oedema"))
    u6_other_hiv = models.PositiveIntegerField( \
                                                  _(u"Other: Living with HIV"))
    u6_other_tb = models.PositiveIntegerField( \
                                                               _(u"Other: TB"))
    u6_other_lwb = models.PositiveIntegerField( \
                                              _(u"Other: Low weight at birth"))
    u6_new_case = models.PositiveIntegerField( \
                                                                _(u"New Case"))
    u6_relapse = models.PositiveIntegerField( \
                                                  _(u"Relapse (after healed)"))
    u6_returned = models.PositiveIntegerField( \
                                     _(u"Returned (after leaving) or medical"))
    u6_nut_transfered_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    u6_admitted_m = models.PositiveIntegerField( \
                                                     _(u"Total male admitted"))
    u6_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    u6_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    u6_deceased = models.PositiveIntegerField( \
                                                                _(u"Deceased"))
    u6_aborted = models.PositiveIntegerField( \
                                                                 _(u"Aborted"))
    u6_non_respondant = models.PositiveIntegerField( \
                                                          _(u"Non respondant"))
    u6_medic_transfered_out = models.PositiveIntegerField( \
                                                       _(u"Medical transfert"))
    u6_nut_transfered_out = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    u6_total_out_m = models.PositiveIntegerField( \
                                                     _(u"Total male departed"))
    u6_total_out_f = models.PositiveIntegerField( \
                                                   _(u"Total female departed"))
    u6_total_end_m = models.PositiveIntegerField( \
                                              _(u"Total male at end of month"))
    u6_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))

    # Between 6 months and 59 months
    u59_total_beginning_m = models.PositiveIntegerField( \
                                         _(u"Total male at Begining of Month"))
    u59_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    u59_hw_u70_bmi_u16 = models.PositiveIntegerField( \
                                                     _(u"H/W <70% or BMI <16"))
    u59_muac_u11_muac_u18 = models.PositiveIntegerField( \
                                                    _(u"MUAC <11 or MUAC <18"))
    u59_oedema = models.PositiveIntegerField( \
                                                                  _(u"Oedema"))
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
    u59_nut_transfered_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    u59_admitted_m = models.PositiveIntegerField( \
                                                     _(u"Total male admitted"))
    u59_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    u59_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    u59_deceased = models.PositiveIntegerField( \
                                                                _(u"Deceased"))
    u59_aborted = models.PositiveIntegerField( \
                                                                 _(u"Aborted"))
    u59_non_respondant = models.PositiveIntegerField( \
                                                          _(u"Non respondant"))
    u59_medic_transfered_out = models.PositiveIntegerField( \
                                                       _(u"Medical transfert"))
    u59_nut_transfered_out = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    u59_total_out_m = models.PositiveIntegerField( \
                                                     _(u"Total male departed"))
    u59_total_out_f = models.PositiveIntegerField( \
                                                   _(u"Total female departed"))
    u59_total_end_m = models.PositiveIntegerField( \
                                              _(u"Total male at end of month"))
    u59_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))

    # over 59 months
    o59_total_beginning_m = models.PositiveIntegerField( \
                                         _(u"Total male at Begining of Month"))
    o59_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    o59_hw_u70_bmi_u16 = models.PositiveIntegerField( \
                                                     _(u"H/W <70% or BMI <16"))
    o59_muac_u11_muac_u18 = models.PositiveIntegerField( \
                                                    _(u"MUAC <11 or MUAC <18"))
    o59_oedema = models.PositiveIntegerField( \
                                                                  _(u"Oedema"))
    o59_other_hiv = models.PositiveIntegerField( \
                                                  _(u"Other: Living with HIV"))
    o59_other_tb = models.PositiveIntegerField( \
                                                               _(u"Other: TB"))
    o59_other_lwb = models.PositiveIntegerField( \
                                              _(u"Other: Low weight at birth"))
    o59_new_case = models.PositiveIntegerField( \
                                                                _(u"New Case"))
    o59_relapse = models.PositiveIntegerField( \
                                                  _(u"Relapse (after healed)"))
    o59_returned = models.PositiveIntegerField( \
                                     _(u"Returned (after leaving) or medical"))
    o59_nut_transfered_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    o59_admitted_m = models.PositiveIntegerField( \
                                                     _(u"Total male admitted"))
    o59_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    o59_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    o59_deceased = models.PositiveIntegerField( \
                                                                _(u"Deceased"))
    o59_aborted = models.PositiveIntegerField( \
                                                                 _(u"Aborted"))
    o59_non_respondant = models.PositiveIntegerField( \
                                                          _(u"Non respondant"))
    o59_medic_transfered_out = models.PositiveIntegerField( \
                                                       _(u"Medical transfert"))
    o59_nut_transfered_out = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    o59_total_out_m = models.PositiveIntegerField( \
                                                     _(u"Total male departed"))
    o59_total_out_f = models.PositiveIntegerField( \
                                                   _(u"Total female departed"))
    o59_total_end_m = models.PositiveIntegerField( \
                                              _(u"Total male at end of month"))
    o59_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))

    # Aggregation
    sources = models.ManyToManyField('PECNIReport', \
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
