#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _

from PECReport import PECReport
from NutritionReport import NutritionReport


class PECSAMPReport(models.Model, PECReport):

    """ PEC Report URENI """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"PEC URENI Report")
        verbose_name_plural = _(u"PEC URENI Reports")

    CATEGORIES = (('u6', _(u"Under 6 months old")),
                  ('u59', _(u"6 to 59 months old")),
                  ('o59', _(u"Over 59 months old")))

    nut_report = models.ForeignKey(NutritionReport,
                                   related_name='pec_samp_reports',
                                   unique=True)
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
    u6_other = models.PositiveIntegerField(_(u"Other"))

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
    u59_other = models.PositiveIntegerField(_(u"Other"))

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
    o59_other = models.PositiveIntegerField(_(u"Other"))

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

    def add_u6_data(self, u6_total_beginning_m,
                    u6_total_beginning_f, u6_hw_u70_bmi_u16,
                    u6_muac_u11_muac_u18, u6_oedema,
                    u6_other,
                    u6_new_case, u6_relapse,
                    u6_returned, u6_nut_transfered_in,
                    u6_admitted_m, u6_admitted_f,
                    u6_healed, u6_deceased,
                    u6_aborted, u6_non_respondant,
                    u6_medic_transfered_out, u6_nut_transfered_out,
                    u6_total_out_m, u6_total_out_f):
        self.u6_total_beginning_m = u6_total_beginning_m
        self.u6_total_beginning_f = u6_total_beginning_f
        self.u6_hw_u70_bmi_u16 = u6_hw_u70_bmi_u16
        self.u6_muac_u11_muac_u18 = u6_muac_u11_muac_u18
        self.u6_oedema = u6_oedema
        self.u6_other = u6_other
        self.u6_new_case = u6_new_case
        self.u6_relapse = u6_relapse
        self.u6_returned = u6_returned
        self.u6_nut_transfered_in = u6_nut_transfered_in
        self.u6_admitted_m = u6_admitted_m
        self.u6_admitted_f = u6_admitted_f
        self.u6_healed = u6_healed
        self.u6_deceased = u6_deceased
        self.u6_aborted = u6_aborted
        self.u6_non_respondant = u6_non_respondant
        self.u6_medic_transfered_out = u6_medic_transfered_out
        self.u6_nut_transfered_out = u6_nut_transfered_out
        self.u6_total_out_m = u6_total_out_m
        self.u6_total_out_f = u6_total_out_f

    def add_u59_data(self, u59_total_beginning_m,
                    u59_total_beginning_f,
                    u59_hw_u70_bmi_u16, u59_muac_u11_muac_u18,
                    u59_oedema, u59_other, u59_new_case,
                    u59_relapse, u59_returned,
                    u59_nut_transfered_in, u59_admitted_m,
                    u59_admitted_f, u59_healed,
                    u59_deceased, u59_aborted,
                    u59_non_respondant, u59_medic_transfered_out,
                    u59_nut_transfered_out, u59_total_out_m,
                    u59_total_out_f):
        self.u59_total_beginning_m = u59_total_beginning_m
        self.u59_total_beginning_f = u59_total_beginning_f
        self.u59_hw_u70_bmi_u16 = u59_hw_u70_bmi_u16
        self.u59_muac_u11_muac_u18 = u59_muac_u11_muac_u18
        self.u59_oedema = u59_oedema
        self.u59_other = u59_other
        self.u59_new_case = u59_new_case
        self.u59_relapse = u59_relapse
        self.u59_returned = u59_returned
        self.u59_nut_transfered_in = u59_nut_transfered_in
        self.u59_admitted_m = u59_admitted_m
        self.u59_admitted_f = u59_admitted_f
        self.u59_healed = u59_healed
        self.u59_deceased = u59_deceased
        self.u59_aborted = u59_aborted
        self.u59_non_respondant = u59_non_respondant
        self.u59_medic_transfered_out = u59_medic_transfered_out
        self.u59_nut_transfered_out = u59_nut_transfered_out
        self.u59_total_out_m = u59_total_out_m
        self.u59_total_out_f = u59_total_out_f

    def add_o59_data(self, o59_total_beginning_m,
                    o59_total_beginning_f,
                    o59_hw_u70_bmi_u16, o59_muac_u11_muac_u18,
                    o59_oedema, o59_other, o59_new_case,
                    o59_relapse, o59_returned,
                    o59_nut_transfered_in,
                    o59_admitted_m, o59_admitted_f,
                    o59_healed, o59_deceased,
                    o59_aborted, o59_non_respondant,
                    o59_medic_transfered_out, o59_nut_transfered_out,
                    o59_total_out_m, o59_total_out_f):
        self.o59_total_beginning_m = o59_total_beginning_m
        self.o59_total_beginning_f = o59_total_beginning_f
        self.o59_hw_u70_bmi_u16 = o59_hw_u70_bmi_u16
        self.o59_muac_u11_muac_u18 = o59_muac_u11_muac_u18
        self.o59_oedema = o59_oedema
        self.o59_other = o59_other
        self.o59_new_case = o59_new_case
        self.o59_relapse = o59_relapse
        self.o59_returned = o59_returned
        self.o59_nut_transfered_in = o59_nut_transfered_in
        self.o59_admitted_m = o59_admitted_m
        self.o59_admitted_f = o59_admitted_f
        self.o59_healed = o59_healed
        self.o59_deceased = o59_deceased
        self.o59_aborted = o59_aborted
        self.o59_non_respondant = o59_non_respondant
        self.o59_medic_transfered_out = o59_medic_transfered_out
        self.o59_nut_transfered_out = o59_nut_transfered_out
        self.o59_total_out_m = o59_total_out_m
        self.o59_total_out_f = o59_total_out_f

    # MISSING FIELDS FOR GENERAL TOTALS
    @property
    def u6_hw_b7080_bmi_u18(self):
        return 0

    @property
    def u59_hw_b7080_bmi_u18(self):
        return 0

    @property
    def o59_hw_b7080_bmi_u18(self):
        return 0

    @property
    def u6_muac_u120(self):
        return 0

    @property
    def u59_muac_u120(self):
        return 0

    @property
    def o59_muac_u120(self):
        return 0

    @property
    def u6_nut_referred_in(self):
        return 0

    @property
    def u59_nut_referred_in(self):
        return 0

    @property
    def o59_nut_referred_in(self):
        return 0

    @property
    def u6_referred_out(self):
        return 0

    @property
    def u59_referred_out(self):
        return 0

    @property
    def o59_referred_out(self):
        return 0

reversion.register(PECSAMPReport)