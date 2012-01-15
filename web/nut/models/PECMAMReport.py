#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from NUTReport import NUTReport, pre_save_report, post_save_report, NUTReportManager
from bolibana.models import EntityType, Entity, Report, MonthPeriod


class PECMAMReport(NUTReport, Report):

    """ PEC Report URENAM """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"PEC URENAM Report")
        verbose_name_plural = _(u"PEC URENAM Reports")
        unique_together = ('period', 'entity', 'type')

    CATEGORIES = (('u59', _(u"6 to 59 months old")),
                  ('pw', _(u"Pregnant/Breast-feeding Women")),
                  ('fu12', _(u"Follow-up URENI/UNRENAS")))

    byperiod = NUTReportManager()

    # over 59 months
    u59_total_beginning_m = models.PositiveIntegerField( \
                                         _(u"Total male at Begining of Month"))
    u59_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    u59_hw_b7080_bmi_u18 = models.PositiveIntegerField( \
                                                 _(u"H/W ≥70%<80% or BMI <18"))
    u59_muac_u120 = models.PositiveIntegerField( \
                                                  _(u"MUAC <120 or MUAC <210"))
    u59_other = models.PositiveIntegerField(_(u"Other"))

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

    # pregnant women or feed_breasting women
    pw_total_beginning_f = models.PositiveIntegerField( \
                                       _(u"Total female at Begining of Month"))
    pw_hw_b7080_bmi_u18 = models.PositiveIntegerField( \
                                                 _(u"H/W ≥70%<80% or BMI <18"))
    pw_muac_u120 = models.PositiveIntegerField( \
                                                  _(u"MUAC <120 or MUAC <210"))
    pw_other = models.PositiveIntegerField(_(u"Other"))

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
    fu12_other = models.PositiveIntegerField(_(u"Other"))

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

    # Aggregation
    sources = models.ManyToManyField('PECMAMReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

    def add_u59_data(self, u59_total_beginning_m, u59_total_beginning_f,
                        u59_hw_b7080_bmi_u18, u59_muac_u120,
                        u59_other, u59_new_case,
                        u59_relapse, u59_returned,
                        u59_nut_referred_in, u59_admitted_m,
                        u59_admitted_f, u59_healed,
                        u59_referred_out, u59_deceased,
                        u59_aborted, u59_non_respondant,
                        u59_medic_transfered_out, u59_total_out_m,
                        u59_total_out_f):
        self.u59_total_beginning_m = u59_total_beginning_m
        self.u59_total_beginning_f = u59_total_beginning_f
        self.u59_hw_b7080_bmi_u18 = u59_hw_b7080_bmi_u18
        self.u59_muac_u120 = u59_muac_u120
        self.u59_other = u59_other
        self.u59_new_case = u59_new_case
        self.u59_relapse = u59_relapse
        self.u59_returned = u59_returned
        self.u59_nut_referred_in = u59_nut_referred_in
        self.u59_admitted_m = u59_admitted_m
        self.u59_admitted_f = u59_admitted_f
        self.u59_healed = u59_healed
        self.u59_referred_out = u59_referred_out
        self.u59_deceased = u59_deceased
        self.u59_aborted = u59_aborted
        self.u59_non_respondant = u59_non_respondant
        self.u59_medic_transfered_out = u59_medic_transfered_out
        self.u59_total_out_m = u59_total_out_m
        self.u59_total_out_f = u59_total_out_f

    def add_pw_data(self, pw_total_beginning_f, pw_hw_b7080_bmi_u18,
                        pw_muac_u120, pw_other,
                        pw_new_case, pw_relapse,
                        pw_returned, pw_nut_referred_in,
                        pw_admitted_f, pw_healed,
                        pw_referred_out, pw_deceased,
                        pw_aborted, pw_non_respondant,
                        pw_medic_transfered_out, pw_total_out_f):
        self.pw_total_beginning_f = pw_total_beginning_f
        self.pw_hw_b7080_bmi_u18 = pw_hw_b7080_bmi_u18
        self.pw_muac_u120 = pw_muac_u120
        self.pw_other = pw_other
        self.pw_new_case = pw_new_case
        self.pw_relapse = pw_relapse
        self.pw_returned = pw_returned
        self.pw_nut_referred_in = pw_nut_referred_in
        self.pw_admitted_f = pw_admitted_f
        self.pw_healed = pw_healed
        self.pw_referred_out = pw_referred_out
        self.pw_deceased = pw_deceased
        self.pw_aborted = pw_aborted
        self.pw_non_respondant = pw_non_respondant
        self.pw_medic_transfered_out = pw_medic_transfered_out
        self.pw_total_out_f = pw_total_out_f

    def add_fu12_data(self, fu12_total_beginning_m, fu12_total_beginning_f,
                        fu12_hw_b7080_bmi_u18, fu12_muac_u120,
                        fu12_other, fu12_nut_referred_in,
                        fu12_admitted_m, fu12_admitted_f,
                        fu12_healed, fu12_referred_out,
                        fu12_deceased, fu12_aborted,
                        fu12_non_respondant, fu12_medic_transfered_out,
                        fu12_total_out_m, fu12_total_out_f):
        self.fu12_total_beginning_m = fu12_total_beginning_m
        self.fu12_total_beginning_f = fu12_total_beginning_f
        self.fu12_hw_b7080_bmi_u18 = fu12_hw_b7080_bmi_u18
        self.fu12_muac_u120 = fu12_muac_u120
        self.fu12_other = fu12_other
        self.fu12_nut_referred_in = fu12_nut_referred_in
        self.fu12_admitted_m = fu12_admitted_m
        self.fu12_admitted_f = fu12_admitted_f
        self.fu12_healed = fu12_healed
        self.fu12_referred_out = fu12_referred_out
        self.fu12_deceased = fu12_deceased
        self.fu12_aborted = fu12_aborted
        self.fu12_non_respondant = fu12_non_respondant
        self.fu12_medic_transfered_out = fu12_medic_transfered_out
        self.fu12_total_out_m = fu12_total_out_m
        self.fu12_total_out_f = fu12_total_out_f

    # MISSING FIELDS FOR GENERAL TOTALS
    @property
    def pw_total_beginning_m(self):
        return 0

    @property
    def u59_hw_u70_bmi_u16(self):
        return 0

    @property
    def pw_hw_u70_bmi_u16(self):
        return 0

    @property
    def fu12_hw_u70_bmi_u16(self):
        return 0

    @property
    def u59_muac_u11_muac_u18(self):
        return 0

    @property
    def pw_muac_u11_muac_u18(self):
        return 0

    @property
    def fu12_muac_u11_muac_u18(self):
        return 0

    @property
    def u59_oedema(self):
        return 0

    @property
    def pw_oedema(self):
        return 0

    @property
    def fu12_oedema(self):
        return 0

    @property
    def fu12_new_case(self):
        return 0

    @property
    def fu12_relapse(self):
        return 0

    @property
    def fu12_returned(self):
        return 0

    @property
    def u59_nut_transfered_in(self):
        return 0

    @property
    def pw_nut_transfered_in(self):
        return 0

    @property
    def fu12_nut_transfered_in(self):
        return 0

    @property
    def pw_total_admitted_m(self):
        return 0

    @property
    def u59_nut_transfered_out(self):
        return 0

    @property
    def pw_nut_transfered_out(self):
        return 0

    @property
    def fu12_nut_transfered_out(self):
        return 0

    @property
    def pw_total_out_m(self):
        return 0

    @property
    def pw_total_end_m(self):
        return 0

reversion.register(PECMAMReport)

pre_save.connect(pre_save_report, sender=PECMAMReport)
post_save.connect(post_save_report, sender=PECMAMReport)
