#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from nutrsc.proxy import proxy_field_name
from nutrsc.data import DataHolder

class PECSAMDataHolder(DataHolder):

    def fields_for(self, cat):
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
                        'u59_nut_referred_in',
                        'u59_admitted_m',
                        'u59_admitted_f',
                        'u59_healed',
                        'u59_referred_out',
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
                        'o59_nut_referred_in',
                        'o59_admitted_m',
                        'o59_admitted_f',
                        'o59_healed',
                        'o59_referred_out',
                        'o59_deceased',
                        'o59_aborted',
                        'o59_non_respondant',
                        'o59_medic_transfered_out',
                        'o59_nut_transfered_out',
                        'o59_total_out_m',
                        'o59_total_out_f']
        fu1_fields = ['fu1_total_beginning_m',
                        'fu1_total_beginning_f',
                        'fu1_hw_u70_bmi_u16',
                        'fu1_muac_u11_muac_u18',
                        'fu1_oedema',
                        'fu1_other',
                        'fu1_new_case',
                        'fu1_relapse',
                        'fu1_returned',
                        'fu1_nut_transfered_in',
                        'fu1_nut_referred_in',
                        'fu1_admitted_m',
                        'fu1_admitted_f',
                        'fu1_healed',
                        'fu1_referred_out',
                        'fu1_deceased',
                        'fu1_aborted',
                        'fu1_non_respondant',
                        'fu1_medic_transfered_out',
                        'fu1_nut_transfered_out',
                        'fu1_total_out_m',
                        'fu1_total_out_f']
        try:
            return eval('%s_fields' % cat)
        except:
            return []
