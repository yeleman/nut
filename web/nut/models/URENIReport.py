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
    u6_m_total_beginning_month = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    u6_w_total_beginning_month = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    u6_p_t_u70_or_imc_u16 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    u6_pb_u11cm_or_pb_u18cm = models.PositiveIntegerField( \
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
    u6_m_total_admission  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    u6_w_total_admission  = models.PositiveIntegerField( \
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
    u6_m_total_output  = models.PositiveIntegerField( \
                       _(u"M total output"))
    u6_w_total_output  = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    u6_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    u6_m_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    u6_w_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
    # 6-59 mois
    total_beginning_month_6_59 = models.PositiveIntegerField( \
                    _(u"Total at the beginning of the month"))
    m_total_beginning_month_6_59 = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    w_total_beginning_month_6_59 = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    p_t_u70_or_imc_u16_6_59 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    pb_u11cm_or_pb_u18cm_6_59 = models.PositiveIntegerField( \
                       _(u"PB < 11cm (ou PB < 18cm"))
    edemas_6_59 = models.PositiveIntegerField( \
                       _(u"Edemas"))
    other_6_59 = models.PositiveIntegerField( \
                       _(u"Other"))
    new_case_6_59 = models.PositiveIntegerField( \
                       _(u"New case"))
    relapse_6_59 = models.PositiveIntegerField( \
                       _(u"Relapse (postwar)"))
    readimission_6_59 = models.PositiveIntegerField( \
                       _(u"Readimission (after Abadon) or medical"))
    transfer_nutritional_admission_6_59 = models.PositiveIntegerField( \
                       _(u"Transfer nutritional"))
    total_admission_6_59  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    m_total_admission_6_59  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    w_total_admission_6_59  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    cured_6_59  = models.PositiveIntegerField( \
                       _(u"cured"))
    death_6_59  = models.PositiveIntegerField( \
                       _(u"Death"))
    drop_6_59  = models.PositiveIntegerField( \
                       _(u"Drop"))
    not_responding_6_59  = models.PositiveIntegerField( \
                       _(u"Cured"))
    medical_transfer_6_59  = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    nutritional_transfer_output_6_59  = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    total_output_6_59  = models.PositiveIntegerField( \
                       _(u"Total output"))
    m_total_output_6_59  = models.PositiveIntegerField( \
                       _(u"M total output"))
    w_total_output_6_59  = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    total_remaining_to_month_end_6_59  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    m_total_remaining_to_month_end_6_59  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    w_total_remaining_to_month_end_6_59  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
    # > 59 mois
    o59_total_beginning_month = models.PositiveIntegerField( \
                       _(u"Total at the beginning of the month"))
    o59_m_total_beginning_month = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    o59_w_total_beginning_month = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    o59_p_t_u70_or_imc_u16 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    o59_pb_u11cm_or_pb_u18cm = models.PositiveIntegerField( \
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
    o59_m_total_admission  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    o59_w_total_admission  = models.PositiveIntegerField( \
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
    o59_m_total_output  = models.PositiveIntegerField( \
                       _(u"M total output"))
    o59_w_total_output  = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    o59_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    o59_m_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    o59_w_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
