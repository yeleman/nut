#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib import admin
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _, ugettext

from bolibana_reporting.models import Report

import inspect

class UrenamReport(Report):
    """ """
    class Meta:
        app_label = 'nut'
        verbose_name = _(u"URENAM Report")
        verbose_name_plural = _(u"URENAM Reports")

    total_beginning_month_6_59 = models.PositiveIntegerField( \
                                           _(u"Total at the beginning of the month"))
    m_total_beginning_month_6_59 = models.PositiveIntegerField( \
                                           _(u"M total at the beginning of the month"))
    f_total_beginning_month_6_59 = models.PositiveIntegerField( \
                                           _(u"F total at the beginning of the month"))
    p_t_o70_u80_or_imc_u18_6_59 = models.PositiveIntegerField( \
                                           _(u"P/T >= 70% < 80% or IMC < 18"))
    pb_u120mm_or_pb_u210mm_6_59 = models.PositiveIntegerField( \
                                           _(u"PB < 120 mm (ou PB < 210 mm)"))
    other_6_59 = models.PositiveIntegerField( \
                                           _(u"Other"))
    new_case_6_59 = models.PositiveIntegerField( \
                                           _(u"New case"))
    relapse_6_59 = models.PositiveIntegerField( \
                                           _(u"Relapse (postwar)"))
    readimission_6_59 = models.PositiveIntegerField( \
                                           _(u"Readimission (after Abadon) or medical"))
    nutritional_reference_admission_6_59 = models.PositiveIntegerField( \
                                           _(u"Nutritional reference"))
    total_admission_6_59  = models.PositiveIntegerField( \
                                           _(u"Total admission"))
    m_total_admission_6_59  = models.PositiveIntegerField( \
                                           _(u"M total admission"))
    f_total_admission_6_59  = models.PositiveIntegerField( \
                                       _(u"F total admission"))
    refers_to_3_or_2_6_59  = models.PositiveIntegerField( \
                                           _(u"Referes 3 ou 2"))
    death_6_59  = models.PositiveIntegerField( \
                                           _(u"Death"))
    drop_6_59  = models.PositiveIntegerField( \
                                           _(u"Drop"))
    non_respondent_6_59  = models.PositiveIntegerField( \
                                           _(u"Cured"))
    medical_transfer_6_59  = models.PositiveIntegerField( \
                                           _(u"Medical transfer output"))
    total_output_6_59  = models.PositiveIntegerField( \
                                           _(u"Total output"))
    m_total_output_6_59  = models.PositiveIntegerField( \
                                           _(u"M total output"))
    f_total_output_6_59  = models.PositiveIntegerField( \
                                           _(u"Ftotal output"))
    total_remaining_to_month_end_6_59  = models.PositiveIntegerField( \
                                           _(u"Total remaining to month end"))
    m_total_remaining_to_month_end_6_59  = models.PositiveIntegerField( \
                                           _(u"M total remaining to month end"))
    f_total_remaining_to_month_end_6_59  = models.PositiveIntegerField( \
                                           _(u"F total remaining to month end"))

    total_beginning_month_fe_fa = models.PositiveIntegerField( \
                                           _(u"Total at the beginning of the month"))
    m_total_beginning_month_fe_fa = models.PositiveIntegerField( \
                                           _(u"M total at the beginning of the month"))
    f_total_beginning_month_fe_fa = models.PositiveIntegerField( \
                                           _(u"F total at the beginning of the month"))
    p_t_o70_u80_or_imc_u18_fe_fa = models.PositiveIntegerField( \
                                           _(u"P/T >= 70% < 80% or IMC < 18"))
    pb_u120mm_or_pb_u210mm_fe_fa = models.PositiveIntegerField( \
                                           _(u"PB < 120 mm (ou PB < 210 mm)"))
    other_fe_fa = models.PositiveIntegerField( \
                                           _(u"Other"))
    new_case_fe_fa = models.PositiveIntegerField( \
                                           _(u"New case"))
    relapse_fe_fa = models.PositiveIntegerField( \
                                           _(u"Relapse (postwar)"))
    readimission_fe_fa = models.PositiveIntegerField( \
                                           _(u"Readimission (after Abadon) or medical"))
    nutritional_reference_admission_fe_fa = models.PositiveIntegerField( \
                                           _(u"Nutritional reference"))
    total_admission_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Total admission "))
    f_total_admission_fe_fa  = models.PositiveIntegerField( \
                                           _(u"F total admission "))
    refers_to_3_or_2_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Referes 3 ou 2"))
    death_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Death"))
    drop_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Drop"))
    non_ respondent_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Cured"))
    medical_transfer_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Medical transfer output"))
    total_output_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Total output"))
    f_total_output_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Ftotal output"))
    total_remaining_to_month_end_fe_fa  = models.PositiveIntegerField( \
                                           _(u"Total remaining to month end"))
    f_total_remaining_to_month_end_fe_fa  = models.PositiveIntegerField( \
                                           _(u"F total remaining to month end"))

    total_beginning_month_monitoring_1_2 = models.PositiveIntegerField( \
                                           _(u"Total at the beginning of the month"))
    m_total_beginning_month_monitoring_1_2 = models.PositiveIntegerField( \
                                           _(u"M total at the beginning of the month"))
    f_total_beginning_month_monitoring_1_2 = models.PositiveIntegerField( \
                                           _(u"F total at the beginning of the month"))
    p_t_o70_u80_or_imc_u18_monitoring_1_2 = models.PositiveIntegerField( \
                                           _(u"P/T >= 70% < 80% or IMC < 18"))
    pb_u120mm_or_pb_u210mm_monitoring_1_2 = models.PositiveIntegerField( \
                                           _(u"PB < 120 mm (ou PB < 210 mm)"))
    other_monitoring_1_2 = models.PositiveIntegerField( \
                                           _(u"Other"))
    nutritional_reference_admission_monitoring_1_2 = models.PositiveIntegerField( \
                                           _(u"Nutritional reference"))
    total_admission_monitoring_1_2  = models.PositiveIntegerField( \
                                           _(u"Total admission "))
    m_total_admission_monitoring_1_2  = models.PositiveIntegerField( \
                                           _(u"M total admission "))
    f_total_admission_monitoring_1_2  = models.PositiveIntegerField( \
                                           _(u"F total admission "))
    refers_to_3_or_2_1_2  = models.PositiveIntegerField( \
                                           _(u"Referes 3 ou 2"))
    death_1_2  = models.PositiveIntegerField( \
                                           _(u"Death"))
    drop_1_2  = models.PositiveIntegerField( \
                                           _(u"Drop"))
    non_ respondent_1_2  = models.PositiveIntegerField( \
                                           _(u"Cured"))
    medical_transfer_1_2  = models.PositiveIntegerField( \
                                           _(u"Medical transfer output"))
    total_output_1_2  = models.PositiveIntegerField( \
                                           _(u"Total output"))
    m_total_output_1_2  = models.PositiveIntegerField( \
                                           _(u"M total output"))
    f_total_output_1_2  = models.PositiveIntegerField( \
                                           _(u"Ftotal output"))
    total_remaining_to_month_end_1_2  = models.PositiveIntegerField( \
                                           _(u"Total remaining to month end"))
    m_total_remaining_to_month_end_1_2  = models.PositiveIntegerField( \
                                           _(u"M total remaining to month end"))
    f_total_remaining_to_month_end_1_2  = models.PositiveIntegerField( \
                                           _(u"F total remaining to month end"))

    def add_6_59_month_data(self, total_beginning_month_6_59, \
                                m_total_beginning_month_6_59, \
                                f_total_beginning_month_6_59, \
                                p_t_o70_u80_or_imc_u18_6_59, \
                                pb_u120mm_or_pb_u210mm_6_59, \
                                other_6_59, \
                                new_case_6_59, \
                                relapse_6_59, \
                                readimission_6_59, \
                                nutritional_reference_admission_6_59, \
                                total_admission_6_59, \
                                m_total_admission_6_59, \
                                f_total_admission_6_59, \
                                refers_to_3_or_2_6_59, \
                                death_6_59, \
                                drop_6_59, \
                                non_respondent_6_59, \
                                medical_transfer_6_59, \
                                total_output_6_59, \
                                m_total_output_6_59, \
                                f_total_output_6_59, \
                                total_remaining_to_month_end_6_59, \
                                m_total_remaining_to_month_end_6_59, \
                                f_total_remaining_to_month_end_6_59):
        self.total_beginning_month_6_59 = total_beginning_month_6_59
        self.m_total_beginning_month_6_59 = m_total_beginning_month_6_59
        self.f_total_beginning_month_6_59 = f_total_beginning_month_6_59
        self.p_t_o70_u80_or_imc_u18_6_59 = p_t_o70_u80_or_imc_u18_6_59
        self.pb_u120mm_or_pb_u210mm_6_59 = pb_u120mm_or_pb_u210mm_6_59
        self.other_6_59 = other_6_59
        self.new_case_6_59 = new_case_6_59
        self.relapse_6_59 = relapse_6_59
        self.nutritional_reference_admission_6_59 = nutritional_reference_admission_6_59
        self.total_admission_6_59 = total_admission_6_59
        self.m_total_admission_6_59 = m_total_admission_6_59
        self.f_total_admission_6_59 = f_total_admission_6_59
        self.refers_to_3_or_2_6_59 = refers_to_3_or_2_6_59
        self.death_6_59 = death_6_59
        self.drop_6_59 = drop_6_59
        self.non_respondent_6_59 = non_respondent_6_59
        self.total_output_6_59 = total_output_6_59
        self.m_total_output_6_59 = m_total_output_6_59
        self.f_total_output_6_59 = f_total_output_6_59
        self.total_remaining_to_month_end_6_59 = total_remaining_to_month_end_6_59
        self.m_total_remaining_to_month_end_6_59 = m_total_remaining_to_month_end_6_59
        self.f_total_remaining_to_month_end_6_59 = f_total_remaining_to_month_end_6_59

reversion.register(UrenamReport)
