#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

import inspect

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from NUTReport import NUTReport, pre_save_report, post_save_report
from bolibana.models import EntityType, Entity, Report, MonthPeriod


class PECSAMReport(NUTReport, Report):

    """ PEC Report URENAS """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"PEC URENAS Report")
        verbose_name_plural = _(u"PEC URENAS Reports")
        unique_together = ('period', 'entity', 'type')

    CATEGORIES = (('u59', _(u"6 to 59 months old")),
                  ('o59', _(u"Over 59 months old")),
                  ('fu1', _(u"Follow-up URENI 1")))

    # 6 months old to 59 months old
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
    o59_nut_referred_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional reference"))
    o59_admitted_m = models.PositiveIntegerField( \
                                                     _(u"Total male admitted"))
    o59_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    o59_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    o59_referred_out = models.PositiveIntegerField( \
                                                      _(u"Referred to URENAM"))
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

    # Follow_up URENI (1)
    fu1_total_beginning_m = models.PositiveIntegerField( \
                                         _(u"Total male at Begining of Month"))
    fu1_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    fu1_hw_u70_bmi_u16 = models.PositiveIntegerField( \
                                                     _(u"H/W <70% or BMI <16"))
    fu1_muac_u11_muac_u18 = models.PositiveIntegerField( \
                                                    _(u"MUAC <11 or MUAC <18"))
    fu1_oedema = models.PositiveIntegerField( \
                                                                  _(u"Oedema"))
    fu1_other = models.PositiveIntegerField(_(u"Other"))

    fu1_new_case = models.PositiveIntegerField( \
                                                                _(u"New Case"))
    fu1_relapse = models.PositiveIntegerField( \
                                                  _(u"Relapse (after healed)"))
    fu1_returned = models.PositiveIntegerField( \
                                     _(u"Returned (after leaving) or medical"))
    fu1_nut_transfered_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    fu1_nut_referred_in = models.PositiveIntegerField( \
                                                   _(u"Nutritional reference"))
    fu1_admitted_m = models.PositiveIntegerField( \
                                                     _(u"Total male admitted"))
    fu1_admitted_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    # OUT
    fu1_healed = models.PositiveIntegerField( \
                                                                  _(u"Healed"))
    fu1_referred_out = models.PositiveIntegerField( \
                                                      _(u"Referred to URENAM"))
    fu1_deceased = models.PositiveIntegerField( \
                                                                _(u"Deceased"))
    fu1_aborted = models.PositiveIntegerField( \
                                                                 _(u"Aborted"))
    fu1_non_respondant = models.PositiveIntegerField( \
                                                          _(u"Non respondant"))
    fu1_medic_transfered_out = models.PositiveIntegerField( \
                                                       _(u"Medical transfert"))
    fu1_nut_transfered_out = models.PositiveIntegerField( \
                                                   _(u"Nutritional transfert"))
    fu1_total_out_m = models.PositiveIntegerField( \
                                                     _(u"Total male departed"))
    fu1_total_out_f = models.PositiveIntegerField( \
                                                   _(u"Total female departed"))

    # Aggregation
    sources = models.ManyToManyField('PECSAMReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

    def add_u59_data(self, u59_total_beginning_m, u59_total_beginning_f,
                    u59_hw_u70_bmi_u16, u59_muac_u11_muac_u18,
                    u59_oedema, u59_other,
                    u59_new_case, u59_relapse,
                    u59_returned, u59_nut_transfered_in,
                    u59_nut_referred_in,
                    u59_admitted_m, u59_admitted_f,
                    u59_healed, u59_referred_out,
                    u59_deceased, u59_aborted,
                    u59_non_respondant,
                    u59_medic_transfered_out, u59_nut_transfered_out,
                    u59_total_out_m, u59_total_out_f):
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
        self.u59_nut_referred_in = u59_nut_referred_in
        self.u59_admitted_m = u59_admitted_m
        self.u59_admitted_f = u59_admitted_f
        self.u59_healed = u59_healed
        self.u59_referred_out = u59_referred_out
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
                    o59_nut_transfered_in, o59_nut_referred_in,
                    o59_admitted_m, o59_admitted_f,
                    o59_healed, o59_referred_out,
                    o59_deceased, o59_aborted,
                    o59_non_respondant, o59_medic_transfered_out,
                    o59_nut_transfered_out,
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
        self.o59_nut_referred_in = o59_nut_referred_in
        self.o59_admitted_m = o59_admitted_m
        self.o59_admitted_f = o59_admitted_f
        self.o59_healed = o59_healed
        self.o59_referred_out = o59_referred_out
        self.o59_deceased = o59_deceased
        self.o59_aborted = o59_aborted
        self.o59_non_respondant = o59_non_respondant
        self.o59_medic_transfered_out = o59_medic_transfered_out
        self.o59_nut_transfered_out = o59_nut_transfered_out
        self.o59_total_out_m = o59_total_out_m
        self.o59_total_out_f = o59_total_out_f

    def add_fu1_data(self, fu1_total_beginning_m, fu1_total_beginning_f,
                    fu1_hw_u70_bmi_u16, fu1_muac_u11_muac_u18,
                    fu1_oedema,
                    fu1_other,
                    fu1_new_case, fu1_relapse,
                    fu1_returned, fu1_nut_transfered_in,
                    fu1_nut_referred_in,
                    fu1_admitted_m, fu1_admitted_f,
                    fu1_healed, fu1_referred_out,
                    fu1_deceased, fu1_aborted,
                    fu1_non_respondant,
                    fu1_medic_transfered_out, fu1_nut_transfered_out,
                    fu1_total_out_m, fu1_total_out_f):
        self.fu1_total_beginning_m = fu1_total_beginning_m
        self.fu1_total_beginning_f = fu1_total_beginning_f
        self.fu1_hw_u70_bmi_u16 = fu1_hw_u70_bmi_u16
        self.fu1_muac_u11_muac_u18 = fu1_muac_u11_muac_u18
        self.fu1_oedema = fu1_oedema
        self.fu1_other = fu1_other
        self.fu1_new_case = fu1_new_case
        self.fu1_relapse = fu1_relapse
        self.fu1_returned = fu1_returned
        self.fu1_nut_transfered_in = fu1_nut_transfered_in
        self.fu1_nut_referred_in = fu1_nut_referred_in
        self.fu1_admitted_m = fu1_admitted_m
        self.fu1_admitted_f = fu1_admitted_f
        self.fu1_healed = fu1_healed
        self.fu1_referred_out = fu1_referred_out
        self.fu1_deceased = fu1_deceased
        self.fu1_aborted = fu1_aborted
        self.fu1_non_respondant = fu1_non_respondant
        self.fu1_medic_transfered_out = fu1_medic_transfered_out
        self.fu1_nut_transfered_out = fu1_nut_transfered_out
        self.fu1_total_out_m = fu1_total_out_m
        self.fu1_total_out_f = fu1_total_out_f

    # MISSING FIELDS FOR GENERAL TOTALS
    @property
    def u59_hw_b7080_bmi_u18(self):
        return 0

    @property
    def o59_hw_b7080_bmi_u18(self):
        return 0

    @property
    def fu1_hw_b7080_bmi_u18(self):
        return 0

    @property
    def u59_muac_u120(self):
        return 0

    @property
    def o59_muac_u120(self):
        return 0

    @property
    def fu1_muac_u120(self):
        return 0

pre_save.connect(pre_save_report, sender=PECSAMReport)
post_save.connect(post_save_report, sender=PECSAMReport)
