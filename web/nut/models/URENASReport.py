#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga


from django.db import models
from django.utils.translation import ugettext_lazy as _

from bolibana_reporting.models import Report

class URENASReport(Report):
    """ """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"URENAS Report")
        verbose_name_plural = _(u"URENAS Reports")

    # 6-59 month
    u59_total_beginning_month = models.PositiveIntegerField( \
                    _(u"Total at the beginning of the month"))
    u59_total_beginning_month_m = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    u59_total_beginning_month_f = models.PositiveIntegerField( \
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
    u59_nutritional_reference_admission = models.PositiveIntegerField( \
                       _(u"Nutritional reference"))
    u59_total_admission = models.PositiveIntegerField( \
                       _(u"Total admission"))
    u59_total_admission_m = models.PositiveIntegerField( \
                       _(u"M total admission"))
    u59_total_admission_f = models.PositiveIntegerField( \
                       _(u"F total admission"))
    u59_cured = models.PositiveIntegerField( \
                       _(u"cured"))
    u59_refers_to_3_or_2 = models.PositiveIntegerField( \
                       _(u"Referes 3 ou 2"))
    u59_death = models.PositiveIntegerField( \
                       _(u"Death"))
    u59_drop = models.PositiveIntegerField( \
                       _(u"Drop"))
    u59_not_responding = models.PositiveIntegerField( \
                       _(u"Cured"))
    u59_medical_transfer = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    u59_nutritional_transfer_output = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    u59_total_output = models.PositiveIntegerField( \
                       _(u"Total output"))
    u59_total_output_m = models.PositiveIntegerField( \
                       _(u"M total output"))
    u59_total_output_f = models.PositiveIntegerField( \
                       _(u"F total output"))
    u59_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    u59_total_remaining_to_month_end_m  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    u59_total_remaining_to_month_end_f  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
    # > 59 month
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
    o59_nutritional_reference_admission = models.PositiveIntegerField( \
                       _(u"Nutritional reference"))
    o59_total_admission  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    o59_total_admission_m = models.PositiveIntegerField( \
                       _(u"M total admission"))
    o59_total_admission_f = models.PositiveIntegerField( \
                       _(u"F total admission"))
    o59_cured = models.PositiveIntegerField( \
                       _(u"cured"))
    o59_refers_to_3_or_2 = models.PositiveIntegerField( \
                       _(u"Referes 3 ou 2"))
    o59_death = models.PositiveIntegerField( \
                       _(u"Death"))
    o59_drop = models.PositiveIntegerField( \
                       _(u"Drop"))
    o59_not_responding = models.PositiveIntegerField( \
                       _(u"Cured"))
    o59_medical_transfer = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    o59_nutritional_transfer_output = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    o59_total_output = models.PositiveIntegerField( \
                       _(u"Total output"))
    o59_total_output_m = models.PositiveIntegerField( \
                       _(u"M total output"))
    o59_total_output_f = models.PositiveIntegerField( \
                       _(u"F total output"))
    o59_total_remaining_to_month_end = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    o59_total_remaining_to_month_end_m = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    o59_total_remaining_to_month_end_f = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
    # Suivi de URENI 1
    f1_total_beginning_month = models.PositiveIntegerField( \
                       _(u"Total at the beginning of the month"))
    f1_total_beginning_month_m = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    f1_total_beginning_month_f = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    f1_w_h_o70_u80_or_BMI_u16 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    f1_MUAC_u11cm_or_MUAC_u18cm = models.PositiveIntegerField( \
                       _(u"PB < 11cm (ou PB < 18cm"))
    f1_edemas = models.PositiveIntegerField( \
                       _(u"Edemas"))
    f1_other = models.PositiveIntegerField( \
                       _(u"Other"))
    f1_new_case = models.PositiveIntegerField( \
                       _(u"New case"))
    f1_relapse = models.PositiveIntegerField( \
                       _(u"Relapse (postwar)"))
    f1_readimission = models.PositiveIntegerField( \
                       _(u"Readimission (after Abadon) or medical"))
    f1_transfer_nutritional_admission = models.PositiveIntegerField( \
                       _(u"Transfer nutritional"))
    f1_nutritional_reference_admission = models.PositiveIntegerField( \
                       _(u"Nutritional reference"))
    f1_total_admission  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    f1_total_admission_m  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    f1_total_admission_f  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    f1_cured  = models.PositiveIntegerField( \
                       _(u"cured"))
    f1_refers_to_3_or_2  = models.PositiveIntegerField( \
                       _(u"Referes 3 ou 2"))
    f1_death  = models.PositiveIntegerField( \
                       _(u"Death"))
    f1_drop  = models.PositiveIntegerField( \
                       _(u"Drop"))
    f1_not_responding  = models.PositiveIntegerField( \
                       _(u"Cured"))
    f1_medical_transfer  = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    f1_nutritional_transfer_output  = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    f1_total_output  = models.PositiveIntegerField( \
                       _(u"Total output"))
    f1_total_output_m = models.PositiveIntegerField( \
                       _(u"M total output"))
    f1_total_output_f = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    f1_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    f1_total_remaining_to_month_end_m = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    f1_total_remaining_to_month_end_f = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))

reversion.register(URENASReport)
