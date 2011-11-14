#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga


from django.db import models
from django.utils.translation import ugettext_lazy as _

from bolibana_reporting.models import Report

class URENIReport(Report):
    """ """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"URENI Report")
        verbose_name_plural = _(u"URENI Reports")

    # < 6 mois
    u6_total_beginning_month = models.PositiveIntegerField( \
                       _(u"Total at the beginning of the month"))
    u6_total_beginning_month_m = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    u6_total_beginning_month_f = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    u6_w_h_o70_u80_or_BMI_u16 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    u6_MUAC_u11cm_or_MUAC_u18cm = models.PositiveIntegerField( \
                       _(u"PB < 11cm (ou PB < 18cm"))
    u6_edemas = models.PositiveIntegerField( \
                       _(u"Edemas"))
    u6_other = models.PositiveIntegerField( \
                       _(u"Other"))
    u6_new_case = models.PositiveIntegerField( \
                       _(u"New case"))
    u6_relapse = models.PositiveIntegerField( \
                       _(u"Relapse (postwar)"))
    u6_readimission = models.PositiveIntegerField( \
                        _(u"Readimission (after Abadon) or medical"))
    u6_transfer_nutritional_admission = models.PositiveIntegerField( \
                       _(u"Transfer nutritional"))
    u6_total_admission  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    u6_total_admission_m  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    u6_total_admission_f  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    u6_cured  = models.PositiveIntegerField( \
                       _(u"cured"))
    u6_death  = models.PositiveIntegerField( \
                       _(u"Death"))
    u6_drop  = models.PositiveIntegerField( \
                       _(u"Drop"))
    u6_not_responding  = models.PositiveIntegerField( \
                       _(u"Cured"))
    u6_medical_transfer  = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    u6_nutritional_transfer_output  = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    u6_total_output  = models.PositiveIntegerField( \
                       _(u"Total output"))
    u6_total_output_m  = models.PositiveIntegerField( \
                       _(u"M total output"))
    u6_total_output_f  = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    u6_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    u6_total_remaining_to_month_end_m  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    u6_total_remaining_to_month_end_f  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
    # 6-59 mois
    u59_total_beginning_month = models.PositiveIntegerField( \
                    _(u"Total at the beginning of the month"))
    u59_m_total_beginning_month = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    u59_total_beginning_month = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    u59_w_h_o70_u80_or_BMI_u16 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    u59_MUAC_u11cm_or_MUAC_u18cm = models.PositiveIntegerField( \
                       _(u"PB < 11cm (ou PB < 18cm"))
    u59_edemas = models.PositiveIntegerField( \
                       _(u"Edemas"))
    u59_other = models.PositiveIntegerField( \
                       _(u"Other"))
    u59_new_case = models.PositiveIntegerField( \
                       _(u"New case"))
    u59_relapse = models.PositiveIntegerField( \
                       _(u"Relapse (postwar)"))
    u59_readimission = models.PositiveIntegerField( \
                       _(u"Readimission (after Abadon) or medical"))
    u59_transfer_nutritional_admission = models.PositiveIntegerField( \
                       _(u"Transfer nutritional"))
    u59_total_admission  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    u59_total_admission_m  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    u59_total_admission_f  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    u59_cured = models.PositiveIntegerField( \
                       _(u"cured"))
    u59_death = models.PositiveIntegerField( \
                       _(u"Death"))
    u59_drop = models.PositiveIntegerField( \
                       _(u"Drop"))
    u59_not_responding = models.PositiveIntegerField( \
                       _(u"Cured"))
    u59_medical_transfer = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    u59_nutritional_transfer_output  = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    u59_total_output = models.PositiveIntegerField( \
                       _(u"Total output"))
    u59_total_output_m = models.PositiveIntegerField( \
                       _(u"M total output"))
    u59_total_output_f = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    u59_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    u59_total_remaining_to_month_end_m  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    u59_total_remaining_to_month_end_f  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
    # > 59 mois
    o59_total_beginning_month = models.PositiveIntegerField( \
                       _(u"Total at the beginning of the month"))
    o59_total_beginning_month_m = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    o59_total_beginning_month_f = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    o59_w_h_o70_u80_or_BMI_u16 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    o59_MUAC_u11cm_or_MUAC_u18cm = models.PositiveIntegerField( \
                       _(u"PB < 11cm (ou PB < 18cm"))
    o59_edemas = models.PositiveIntegerField( \
                       _(u"Edemas"))
    o59_other = models.PositiveIntegerField( \
                       _(u"Other"))
    o59_new_case = models.PositiveIntegerField( \
                       _(u"New case"))
    o59_relapse = models.PositiveIntegerField( \
                       _(u"Relapse (postwar)"))
    o59_readimission = models.PositiveIntegerField( \
                        _(u"Readimission (after Abadon) or medical"))
    o59_transfer_nutritional_admission = models.PositiveIntegerField( \
                       _(u"Transfer nutritional"))
    o59_total_admission  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    o59_total_admission_m  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    o59_total_admission_f  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    o59_cured  = models.PositiveIntegerField( \
                       _(u"cured"))
    o59_death  = models.PositiveIntegerField( \
                       _(u"Death"))
    o59_drop  = models.PositiveIntegerField( \
                       _(u"Drop"))
    o59_not_responding  = models.PositiveIntegerField( \
                       _(u"Cured"))
    o59_medical_transfer  = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    o59_nutritional_transfer_output  = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    o59_total_output  = models.PositiveIntegerField( \
                       _(u"Total output"))
    o59_total_output_m  = models.PositiveIntegerField( \
                       _(u"M total output"))
    o59_total_output_f  = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    o59_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    o59_total_remaining_to_month_end_m  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    o59_total_remaining_to_month_end_f  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))

reversion.register(URENIReport)
