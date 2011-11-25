#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class PECNASReportAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'period', 'entity', 'receipt', '_status')
    list_filter = ('period', 'type', '_status')

    fieldsets = (
      (None, {
           'fields': ('receipt', \
                      ('_status', 'type'), \
                      ('period', 'entity'), \
                      ('created_by', 'modified_by'), \
                      'sources')
       }),
       (_(u"6-59 months"), {
            'fields': (('u59_total_beginning_m', 'u59_total_beginning_f'),
                        'u59_hw_u70_bmi_u16',
                        'u59_muac_u11_muac_u18',
                        'u59_oedema',
                        ('u59_other_hiv', 'u59_other_tb', 'u59_other_lwb'),
                        'u59_new_case',
                        'u59_relapse',
                        'u59_returned',
                        'u59_nut_transfered_in',
                        'u59_nut_referred_in',
                        ('u59_admitted_m', 'u59_admitted_f'),
                        ('u59_healed', 'u59_referred_out', 'u59_deceased', 'u59_aborted', 'u59_non_respondant', 'u59_medic_transfered_out', 'u59_nut_transfered_out'),
                        ('u59_total_out_m', 'u59_total_out_f'),
                        ('u59_total_end_m', 'u59_total_end_f'))
       }),
       (_(u">59 months"), {
            'fields': (('o59_total_beginning_m', 'o59_total_beginning_f'),
                        'o59_hw_u70_bmi_u16',
                        'o59_muac_u11_muac_u18',
                        'o59_oedema',
                        ('o59_other_hiv', 'o59_other_tb', 'o59_other_lwb'),
                        'o59_new_case',
                        'o59_relapse',
                        'o59_returned',
                        'o59_nut_transfered_in',
                        'o59_nut_referred_in',
                        ('o59_admitted_m', 'o59_admitted_f'),
                        ('o59_healed', 'o59_referred_out', 'o59_deceased', 'o59_aborted', 'o59_non_respondant', 'o59_medic_transfered_out', 'o59_nut_transfered_out'),
                        ('o59_total_out_m', 'o59_total_out_f'),
                        ('o59_total_end_m', 'o59_total_end_f'))
       }),
       (_(u"Follow-up URENI 1"), {
            'fields': (('fu1_total_beginning_m', 'fu1_total_beginning_f'),
                        'fu1_hw_u70_bmi_u16',
                        'fu1_muac_u11_muac_u18',
                        'fu1_oedema',
                        ('fu1_other_hiv', 'fu1_other_tb', 'fu1_other_lwb'),
                        'fu1_new_case',
                        'fu1_relapse',
                        'fu1_returned',
                        'fu1_nut_transfered_in',
                        'fu1_nut_referred_in',
                        ('fu1_admitted_m', 'fu1_admitted_f'),
                        ('fu1_healed', 'fu1_referred_out', 'fu1_deceased', 'fu1_aborted', 'fu1_non_respondant', 'fu1_medic_transfered_out', 'fu1_nut_transfered_out'),
                        ('fu1_total_out_m', 'fu1_total_out_f'),
                        ('fu1_total_end_m', 'fu1_total_end_f'))
       }),
   )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('receipt',) + self.readonly_fields
        return self.readonly_fields
