#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class PECNAMReportAdmin(admin.ModelAdmin):
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
                        'u59_hw_b7080_bmi_u18',
                        'u59_muac_u120',
                        ('u59_other_hiv', 'u59_other_tb', 'u59_other_lwb'),
                        'u59_new_case',
                        'u59_relapse',
                        'u59_returned',
                        'u59_nut_referred_in',
                        ('u59_admitted_m', 'u59_admitted_f'),
                        ('u59_healed', 'u59_referred_out', 'u59_deceased', 'u59_aborted', 'u59_non_respondant', 'u59_medic_transfered_out'),
                        ('u59_total_out_m', 'u59_total_out_f'),
                        ('u59_total_end_m', 'u59_total_end_f'))
       }),
       (_(u"Pregnant/Breast-feeding Women"), {
            'fields': ('pw_total_beginning_f',
                        'pw_hw_b7080_bmi_u18',
                        'pw_muac_u120',
                        ('pw_other_hiv', 'pw_other_tb', 'pw_other_lwb'),
                        'pw_new_case',
                        'pw_relapse',
                        'pw_returned',
                        'pw_nut_referred_in',
                        'pw_admitted_f',
                        ('pw_healed', 'pw_referred_out', 'pw_deceased', 'pw_aborted', 'pw_non_respondant', 'pw_medic_transfered_out'),
                        'pw_total_out_f',
                        'pw_total_end_f')
       }),
       (_(u"Follow-up URENI/URENAS"), {
            'fields': (('fu12_total_beginning_m', 'fu12_total_beginning_f'),
                        'fu12_hw_b7080_bmi_u18',
                        'fu12_muac_u120',
                        ('fu12_other_hiv', 'fu12_other_tb', 'fu12_other_lwb'),
                        'fu12_nut_referred_in',
                        ('fu12_admitted_m', 'fu12_admitted_f'),
                        ('fu12_healed', 'fu12_referred_out', 'fu12_deceased', 'fu12_aborted', 'fu12_non_respondant', 'fu12_medic_transfered_out'),
                        ('fu12_total_out_m', 'fu12_total_out_f'),
                        ('fu12_total_end_m', 'fu12_total_end_f'))
       }),
   )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('receipt',) + self.readonly_fields
        return self.readonly_fields
