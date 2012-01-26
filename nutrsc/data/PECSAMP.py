#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from nutrsc.proxy import proxy_field_name
from nutrsc.data import DataHolder

class PECSAMPDataHolder(DataHolder):

    def fields_for(self, cat):
        u6_fields = ['u6_total_beginning_m',
                        'u6_total_beginning_f',
                        'u6_hw_u70_bmi_u16',
                        'u6_muac_u11_muac_u18',
                        'u6_oedema',
                        'u6_other',
                        'u6_new_case',
                        'u6_relapse',
                        'u6_returned',
                        'u6_nut_transfered_in',
                        'u6_admitted_m',
                        'u6_admitted_f',
                        'u6_healed',
                        'u6_deceased',
                        'u6_aborted',
                        'u6_non_respondant',
                        'u6_medic_transfered_out',
                        'u6_nut_transfered_out',
                        'u6_total_out_m',
                        'u6_total_out_f']
        u59_fields = ['u59_total_beginning_m',
                        'u59_total_beginning_f',
                        'u59_hw_u70_bmi_u16',
                        'u59_muac_u11_muac_u18',
                        'u59_oedema',
                        'u59_other',
                        'u59_new_case',
                        'u59_relapse',
                        'u59_returned',
                        'u59_nut_transfered_in',
                        'u59_admitted_m',
                        'u59_admitted_f',
                        'u59_healed',
                        'u59_deceased',
                        'u59_aborted',
                        'u59_non_respondant',
                        'u59_medic_transfered_out',
                        'u59_nut_transfered_out',
                        'u59_total_out_m',
                        'u59_total_out_f']
        o59_fields = ['o59_total_beginning_m',
                        'o59_total_beginning_f',
                        'o59_hw_u70_bmi_u16',
                        'o59_muac_u11_muac_u18',
                        'o59_oedema',
                        'o59_other',
                        'o59_new_case',
                        'o59_relapse',
                        'o59_returned',
                        'o59_nut_transfered_in',
                        'o59_admitted_m',
                        'o59_admitted_f',
                        'o59_healed',
                        'o59_deceased',
                        'o59_aborted',
                        'o59_non_respondant',
                        'o59_medic_transfered_out',
                        'o59_nut_transfered_out',
                        'o59_total_out_m',
                        'o59_total_out_f']
        try:
            return eval('%s_fields' % cat)
        except:
            return []
