#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bolibana_reporting.models import Report

class URENAMReport(Report):
    """ """
    class Meta:
        app_label = 'nut'
        verbose_name = _(u"URENAM Report")
        verbose_name_plural = _(u"URENAM Reports")

    u59_total_beginning_month = models.PositiveIntegerField( \
                                   _(u"Total at the beginning of the month"))
    u59_total_beginning_month_m = models.PositiveIntegerField( \
                                   _(u"M total at the beginning of the month"))
    u59_total_beginning_month_f = models.PositiveIntegerField( \
                                   _(u"F total at the beginning of the month"))
    u59_w_h_o70_u80_or_BMI_u18 = models.PositiveIntegerField( \
                                           _(u"W/H >= 70% < 80% or BMI < 18"))
    u59_MUAC_u120_mor_MUAC_u210mm = models.PositiveIntegerField( \
                                           _(u"MUAC < 120 mm (ou MUAC < 210 mm)"))
    u59_other = models.PositiveIntegerField( \
                                           _(u"Other"))
    u59_new_case = models.PositiveIntegerField( \
                                           _(u"New case"))
    u59_relapse = models.PositiveIntegerField( \
                                           _(u"Relapse (postwar)"))
    u59_readimission = models.PositiveIntegerField( \
                                   _(u"Readimission (after Abadon) or medical"))
    u59_nutritional_reference_admission = models.PositiveIntegerField( \
                                           _(u"Nutritional reference"))
    u59_total_admission  = models.PositiveIntegerField( \
                                           _(u"Total admission"))
    u59_total_admission  = models.PositiveIntegerField( \
                                           _(u"M total admission"))
    u59_total_admission  = models.PositiveIntegerField( \
                                       _(u"F total admission"))
    u59_refers_to_3_or_2  = models.PositiveIntegerField( \
                                           _(u"Referes 3 ou 2"))
    u59_death  = models.PositiveIntegerField( \
                                           _(u"Death"))
    u59_drop  = models.PositiveIntegerField( \
                                           _(u"Drop"))
    u59_non_respondent  = models.PositiveIntegerField( \
                                           _(u"Cured"))
    u59_medical_transfer  = models.PositiveIntegerField( \
                                           _(u"Medical transfer output"))
    u59_total_output = models.PositiveIntegerField( \
                                           _(u"Total output"))
    u59_total_output_m  = models.PositiveIntegerField( \
                                           _(u"M total output"))
    u59_total_output_f  = models.PositiveIntegerField( \
                                           _(u"Ftotal output"))
    u59_total_remaining_to_month_end = models.PositiveIntegerField( \
                                           _(u"Total remaining to month end"))
    u59_total_remaining_to_month_end_m  = models.PositiveIntegerField( \
                                           _(u"M total remaining to month end"))
    u59_total_remaining_to_month_end_f  = models.PositiveIntegerField( \
                                           _(u"F total remaining to month end"))

    pw_total_beginning_month = models.PositiveIntegerField( \
                                   _(u"Total at the beginning of the month"))
    pw_total_beginning_month = models.PositiveIntegerField( \
                                   _(u"F total at the beginning of the month"))
    pw_w_h_o70_u80_or_BMI_u18 = models.PositiveIntegerField( \
                                           _(u"P/T >= 70% < 80% or IMC < 18"))
    pw_MUAC_u120_mor_MUAC_u210mmm = models.PositiveIntegerField( \
                                           _(u"PB < 120 mm (ou PB < 210 mm)"))
    pw_other = models.PositiveIntegerField( \
                                           _(u"Other"))
    pw_new_case = models.PositiveIntegerField( \
                                           _(u"New case"))
    pw_relapse = models.PositiveIntegerField( \
                                           _(u"Relapse (postwar)"))
    pw_readimission = models.PositiveIntegerField( \
                                   _(u"Readimission (after Abadon) or medical"))
    pw_nutritional_reference_admission = models.PositiveIntegerField( \
                                           _(u"Nutritional reference"))
    pw_total_admission  = models.PositiveIntegerField( \
                                           _(u"Total admission "))
    pw_total_admission  = models.PositiveIntegerField( \
                                           _(u"F total admission "))
    pw_cured  = models.PositiveIntegerField( \
                                           _(u"Cured"))
    pw_refers_to_3_or_2  = models.PositiveIntegerField( \
                                           _(u"Referes 3 ou 2"))
    pw_death  = models.PositiveIntegerField( \
                                           _(u"Death"))
    pw_drop  = models.PositiveIntegerField( \
                                           _(u"Drop"))
    pw_non_respondent  = models.PositiveIntegerField( \
                                           _(u"Cured"))
    pw_medical_transfer  = models.PositiveIntegerField( \
                                           _(u"Medical transfer output"))
    pw_total_output  = models.PositiveIntegerField( \
                                           _(u"Total output"))
    pw_total_output  = models.PositiveIntegerField( \
                                           _(u"Ftotal output"))
    pw_total_remaining_to_month_end  = models.PositiveIntegerField( \
                                           _(u"Total remaining to month end"))
    pw_total_remaining_to_month_end  = models.PositiveIntegerField( \
                                           _(u"F total remaining to month end"))

    f2_total_beginning_month = models.PositiveIntegerField( \
                                   _(u"Total at the beginning of the month"))
    f2_total_beginning_month_m = models.PositiveIntegerField( \
                                   _(u"M total at the beginning of the month"))
    f2_total_beginning_month_f = models.PositiveIntegerField( \
                                   _(u"F total at the beginning of the month"))
    f2_w_h_o70_u80_or_BMI_u18 = models.PositiveIntegerField( \
                                           _(u"P/T >= 70% < 80% or IMC < 18"))
    f2_MUAC_u120m_or_MUAC_u210mm = models.PositiveIntegerField( \
                                           _(u"PB < 120 mm (ou PB < 210 mm)"))
    f2_other = models.PositiveIntegerField( \
                                           _(u"Other"))
    f2_nutritional_reference_admission = models.PositiveIntegerField( \
                                           _(u"Nutritional reference"))
    f2_total_admission = models.PositiveIntegerField( \
                                           _(u"Total admission "))
    f2_total_admission_m = models.PositiveIntegerField( \
                                           _(u"M total admission "))
    f2_total_admission_f = models.PositiveIntegerField( \
                                           _(u"F total admission "))
    f2_cured = models.PositiveIntegerField( \
                                           _(u"Cured"))
    f2_refers_to_3_or_2 = models.PositiveIntegerField( \
                                           _(u"Referes 3 ou 2"))
    f2_death = models.PositiveIntegerField( \
                                           _(u"Death"))
    f2_drop = models.PositiveIntegerField( \
                                           _(u"Drop"))
    f2_non_respondent = models.PositiveIntegerField( \
                                           _(u"Cured"))
    f2_medical_transfer = models.PositiveIntegerField( \
                                           _(u"Medical transfer output"))
    f2_total_output = models.PositiveIntegerField( \
                                           _(u"Total output"))
    f2_total_output_m = models.PositiveIntegerField( \
                                           _(u"M total output"))
    f2_total_output_f = models.PositiveIntegerField( \
                                           _(u"Ftotal output"))
    f2_total_remaining_to_month_end = models.PositiveIntegerField( \
                                           _(u"Total remaining to month end"))
    f2_total_remaining_to_month_end_m = models.PositiveIntegerField( \
                                           _(u"M total remaining to month end"))
    f2_total_remaining_to_month_end_f = models.PositiveIntegerField( \
                                           _(u"F total remaining to month end"))

reversion.register(URENAMReport)
