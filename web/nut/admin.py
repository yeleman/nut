#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from bolibana.models import Entity, EntityType, Period
from bolibana.admin import EntityAdmin, EntityTypeAdmin, PeriodAdmin
from bolibana.models import Role, Permission, Access, Provider
from bolibana.admin import (RoleAdmin, PermissionAdmin, \
                                 AccessAdmin, ProviderAdmin)
from nut.models import PECNASReport, PECNAMReport, PECNIReport


class ProviderUserStacked(admin.StackedInline):
    model = Provider
    fk_name = 'user'
    max_num = 1


class CustomUserAdmin(UserAdmin):
    inlines = [ProviderUserStacked, ]

# Adds a provider section to the django User Admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Period, PeriodAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityType, EntityTypeAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(Permission, PermissionAdmin)


class PECNIReportAdmin(admin.ModelAdmin):
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
                        'fields': (('u6_total_beginning_m', 'u6_total_beginning_f'),
                        'u6_hw_u70_bmi_u16',
                        'u6_muac_u11_muac_u18',
                        'u6_oedema',
                        ('u6_other_hiv', 'u6_other_tb', 'u6_other_lwb'),
                        'u6_new_case',
                        'u6_relapse',
                        'u6_returned',
                        'u6_nut_transfered_in',
                        ('u6_admitted_m', 'u6_admitted_f'),
                        ('u6_healed', 'u6_deceased', 'u6_aborted', 'u6_non_respondant', 'u6_medic_transfered_out', 'u6_nut_transfered_out'),
                        ('u6_total_out_m', 'u6_total_out_f'),
                        ('u6_total_end_m', 'u6_total_end_f'))
       }),
       (_(u">59 months"), {
            'fields': (('u59_total_beginning_m', 'u59_total_beginning_f'),
                        'u59_hw_u70_bmi_u16',
                        'u59_muac_u11_muac_u18',
                        'u59_oedema',
                        ('u59_other_hiv', 'u59_other_tb', 'u59_other_lwb'),
                        'u59_new_case',
                        'u59_relapse',
                        'u59_returned',
                        'u59_nut_transfered_in',
                        ('u59_admitted_m', 'u59_admitted_f'),
                        ('u59_healed', 'u59_deceased', 'u59_aborted', 'u59_non_respondant', 'u59_medic_transfered_out', 'u59_nut_transfered_out'),
                        ('u59_total_out_m', 'u59_total_out_f'),
                        ('u59_total_end_m', 'u59_total_end_f'))
       }),
       (_(u"Follow-up URENI 1"), {
            'fields': (('o59_total_beginning_m', 'o59_total_beginning_f'),
                        'o59_hw_u70_bmi_u16',
                        'o59_muac_u11_muac_u18',
                        'o59_oedema',
                        ('o59_other_hiv', 'o59_other_tb', 'o59_other_lwb'),
                        'o59_new_case',
                        'o59_relapse',
                        'o59_returned',
                        'o59_nut_transfered_in',
                        ('o59_admitted_m', 'o59_admitted_f'),
                        ('o59_healed', 'o59_deceased', 'o59_aborted', 'o59_non_respondant', 'o59_medic_transfered_out', 'o59_nut_transfered_out'),
                        ('o59_total_out_m', 'o59_total_out_f'),
                        ('o59_total_end_m', 'o59_total_end_f'))
       }),
   )

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('receipt',) + self.readonly_fields
        return self.readonly_fields

admin.site.register(PECNIReport, PECNIReportAdmin)

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

admin.site.register(PECNAMReport, PECNAMReportAdmin)

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

admin.site.register(PECNASReport, PECNASReportAdmin)
