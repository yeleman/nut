#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from NUTReport import NUTReport, pre_save_report, post_save_report
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
                                            _(u"Total female at end of month"))

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
                                            _(u"Total female at end of month"))

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
                                            _(u"Total female at end of month"))

    # Aggregation
    sources = models.ManyToManyField('PECMAMReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

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

pre_save.connect(pre_save_report, sender=PECMAMReport)
post_save.connect(post_save_report, sender=PECMAMReport)
