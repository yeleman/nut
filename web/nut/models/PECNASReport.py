#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

import inspect

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from NUTReport import NUTReport
from bolibana.models import EntityType, Entity, Report, MonthPeriod


class PECNASReport(NUTReport, Report):

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
    o59_total_end_m = models.PositiveIntegerField( \
                                              _(u"Total male at end of month"))
    o59_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))

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
    fu1_other_hiv = models.PositiveIntegerField( \
                                                  _(u"Other: Living with HIV"))
    fu1_other_tb = models.PositiveIntegerField( \
                                                               _(u"Other: TB"))
    fu1_other_lwb = models.PositiveIntegerField( \
                                              _(u"Other: Low weight at birth"))
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
    fu1_total_end_m = models.PositiveIntegerField( \
                                              _(u"Total male at end of month"))
    fu1_total_end_f = models.PositiveIntegerField( \
                                            _(u"Total frmale at end of month"))

    # Aggregation
    sources = models.ManyToManyField('PECNASReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

