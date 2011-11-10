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
    nutritional_reference_admission_6_59 = models.PositiveIntegerField( \
                       _(u"Nutritional reference"))
    total_admission_6_59  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    m_total_admission_6_59  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    w_total_admission_6_59  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    cured_6_59  = models.PositiveIntegerField( \
                       _(u"cured"))
    refers_to_3_or_2_6_59  = models.PositiveIntegerField( \
                       _(u"Referes 3 ou 2"))
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
    o59_nutritional_reference_admission = models.PositiveIntegerField( \
                       _(u"Nutritional reference"))
    o59_total_admission  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    o59_m_total_admission  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    o59_w_total_admission  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    o59_cured  = models.PositiveIntegerField( \
                       _(u"cured"))
    o59_refers_to_3_or_2  = models.PositiveIntegerField( \
                       _(u"Referes 3 ou 2"))
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
    # Suivi de URENI 1
    ureni_total_beginning_month = models.PositiveIntegerField( \
                       _(u"Total at the beginning of the month"))
    ureni_m_total_beginning_month = models.PositiveIntegerField( \
                       _(u"M total at the beginning of the month"))
    ureni_w_total_beginning_month = models.PositiveIntegerField( \
                       _(u"F total at the beginning of the month"))
    ureni_p_t_u70_or_imc_u16 = models.PositiveIntegerField( \
                       _(u"P/T < 70% ou IMC < 16"))
    ureni_pb_u11cm_or_pb_u18cm = models.PositiveIntegerField( \
                       _(u"PB < 11cm (ou PB < 18cm"))
    ureni_edemas = models.PositiveIntegerField( \
                       _(u"Edemas"))
    ureni_other = models.PositiveIntegerField( \
                       _(u"Other"))
    ureni_new_case = models.PositiveIntegerField( \
                       _(u"New case"))
    ureni_relapse = models.PositiveIntegerField( \
                       _(u"Relapse (postwar)"))
    ureni_readimission = models.PositiveIntegerField( \
                       _(u"Readimission (after Abadon) or medical"))
    ureni_transfer_nutritional_admission = models.PositiveIntegerField( \
                       _(u"Transfer nutritional"))
    ureni_nutritional_reference_admission = models.PositiveIntegerField( \
                       _(u"Nutritional reference"))
    ureni_total_admission  = models.PositiveIntegerField( \
                       _(u"Total admission"))
    ureni_m_total_admission  = models.PositiveIntegerField( \
                       _(u"M total admission"))
    ureni_w_total_admission  = models.PositiveIntegerField( \
                       _(u"F total admission"))
    ureni_cured  = models.PositiveIntegerField( \
                       _(u"cured"))
    ureni_refers_to_3_or_2  = models.PositiveIntegerField( \
                       _(u"Referes 3 ou 2"))
    ureni_death  = models.PositiveIntegerField( \
                       _(u"Death"))
    ureni_drop  = models.PositiveIntegerField( \
                       _(u"Drop"))
    ureni_not_responding  = models.PositiveIntegerField( \
                       _(u"Cured"))
    ureni_medical_transfer  = models.PositiveIntegerField( \
                       _(u"Medical transfer output"))
    ureni_nutritional_transfer_output  = models.PositiveIntegerField( \
                       _(u"Nutritional transfer output"))
    ureni_total_output  = models.PositiveIntegerField( \
                       _(u"Total output"))
    ureni_m_total_output  = models.PositiveIntegerField( \
                       _(u"M total output"))
    ureni_w_total_output  = models.PositiveIntegerField( \
                       _(u"Ftotal output"))
    ureni_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"Total remaining to month end"))
    ureni_m_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"M total remaining to month end"))
    ureni_w_total_remaining_to_month_end  = models.PositiveIntegerField( \
                       _(u"F total remaining to month end"))
