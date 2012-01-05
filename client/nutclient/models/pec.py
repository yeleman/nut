#!/usr/bin/env python
# encoding=utf-8

import peewee

from . import BaseModel, Report


class PECReport(object):

    @property
    def status(self):
        return self.report.status

    STATUS_CREATED = Report.STATUS_CREATED
    STATUS_DRAFT = Report.STATUS_DRAFT
    STATUS_COMPLETE = Report.STATUS_COMPLETE
    STATUS_SENT = Report.STATUS_SENT
    STATUS_REMOTE_MODIFIED = Report.STATUS_REMOTE_MODIFIED
    STATUS_LOCAL_MODIFIED = Report.STATUS_LOCAL_MODIFIED


class PECMAMReport(BaseModel, PECReport):

    report = peewee.ForeignKeyField(Report, unique=True,
                                    related_name='pec_mam_reports')

    # over 59 months
    u59_total_beginning_m = peewee.IntegerField(default=0)
    u59_total_beginning_f = peewee.IntegerField(default=0)
    u59_hw_b7080_bmi_u18 = peewee.IntegerField(default=0)
    u59_muac_u120 = peewee.IntegerField(default=0)
    u59_other = peewee.IntegerField(default=0)
    u59_new_case = peewee.IntegerField(default=0)
    u59_relapse = peewee.IntegerField(default=0)
    u59_returned = peewee.IntegerField(default=0)
    u59_nut_referred_in = peewee.IntegerField(default=0)
    u59_admitted_m = peewee.IntegerField(default=0)
    u59_admitted_f = peewee.IntegerField(default=0)

    # OUT
    u59_healed = peewee.IntegerField(default=0)
    u59_referred_out = peewee.IntegerField(default=0)
    u59_deceased = peewee.IntegerField(default=0)
    u59_aborted = peewee.IntegerField(default=0)
    u59_non_respondant = peewee.IntegerField(default=0)
    u59_medic_transfered_out = peewee.IntegerField(default=0)
    u59_total_out_m = peewee.IntegerField(default=0)
    u59_total_out_f = peewee.IntegerField(default=0)

    # pregnant women or feed_breasting women
    pw_total_beginning_f = peewee.IntegerField(default=0)
    pw_hw_b7080_bmi_u18 = peewee.IntegerField(default=0)
    pw_muac_u120 = peewee.IntegerField(default=0)
    pw_other = peewee.IntegerField(default=0)
    pw_new_case = peewee.IntegerField(default=0)
    pw_relapse = peewee.IntegerField(default=0)
    pw_returned = peewee.IntegerField(default=0)
    pw_nut_referred_in = peewee.IntegerField(default=0)
    pw_admitted_f = peewee.IntegerField(default=0)

    # OUT
    pw_healed = peewee.IntegerField(default=0)
    pw_referred_out = peewee.IntegerField(default=0)
    pw_deceased = peewee.IntegerField(default=0)
    pw_aborted = peewee.IntegerField(default=0)
    pw_non_respondant = peewee.IntegerField(default=0)
    pw_medic_transfered_out = peewee.IntegerField(default=0)
    pw_total_out_f = peewee.IntegerField(default=0)

    # Follow_up (1) and (2)
    # pregnant women or feed_breasting women
    fu12_total_beginning_m = peewee.IntegerField(default=0)
    fu12_total_beginning_f = peewee.IntegerField(default=0)
    fu12_hw_b7080_bmi_u18 = peewee.IntegerField(default=0)
    fu12_muac_u120 = peewee.IntegerField(default=0)
    fu12_other = peewee.IntegerField(default=0)
    fu12_nut_referred_in = peewee.IntegerField(default=0)
    fu12_admitted_m = peewee.IntegerField(default=0)
    fu12_admitted_f = peewee.IntegerField(default=0)

    # OUT
    fu12_healed = peewee.IntegerField(default=0)
    fu12_referred_out = peewee.IntegerField(default=0)
    fu12_deceased = peewee.IntegerField(default=0)
    fu12_aborted = peewee.IntegerField(default=0)
    fu12_non_respondant = peewee.IntegerField(default=0)
    fu12_medic_transfered_out = peewee.IntegerField(default=0)
    fu12_total_out_m = peewee.IntegerField(default=0)
    fu12_total_out_f = peewee.IntegerField(default=0)


class PECSAMReport(BaseModel, PECReport):

    report = peewee.ForeignKeyField(Report, unique=True,
                                    related_name='pec_sam_reports')

    # 6 months old to 59 months old
    u59_total_beginning_m = peewee.IntegerField(default=0)
    u59_total_beginning_f = peewee.IntegerField(default=0)
    u59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    u59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    u59_oedema = peewee.IntegerField(default=0)
    u59_other = peewee.IntegerField(default=0)

    u59_new_case = peewee.IntegerField(default=0)
    u59_relapse = peewee.IntegerField(default=0)
    u59_returned = peewee.IntegerField(default=0)
    u59_nut_transfered_in = peewee.IntegerField(default=0)
    u59_nut_referred_in = peewee.IntegerField(default=0)
    u59_admitted_m = peewee.IntegerField(default=0)
    u59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    u59_healed = peewee.IntegerField(default=0)
    u59_referred_out = peewee.IntegerField(default=0)
    u59_deceased = peewee.IntegerField(default=0)
    u59_aborted = peewee.IntegerField(default=0)
    u59_non_respondant = peewee.IntegerField(default=0)
    u59_medic_transfered_out = peewee.IntegerField(default=0)
    u59_nut_transfered_out = peewee.IntegerField(default=0)
    u59_total_out_m = peewee.IntegerField(default=0)
    u59_total_out_f = peewee.IntegerField(default=0)

    # over 59 months
    o59_total_beginning_m = peewee.IntegerField(default=0)
    o59_total_beginning_f = peewee.IntegerField(default=0)
    o59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    o59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    o59_oedema = peewee.IntegerField(default=0)
    o59_other = peewee.IntegerField(default=0)

    o59_new_case = peewee.IntegerField(default=0)
    o59_relapse = peewee.IntegerField(default=0)
    o59_returned = peewee.IntegerField(default=0)
    o59_nut_transfered_in = peewee.IntegerField(default=0)
    o59_nut_referred_in = peewee.IntegerField(default=0)
    o59_admitted_m = peewee.IntegerField(default=0)
    o59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    o59_healed = peewee.IntegerField(default=0)
    o59_referred_out = peewee.IntegerField(default=0)
    o59_deceased = peewee.IntegerField(default=0)
    o59_aborted = peewee.IntegerField(default=0)
    o59_non_respondant = peewee.IntegerField(default=0)
    o59_medic_transfered_out = peewee.IntegerField(default=0)
    o59_nut_transfered_out = peewee.IntegerField(default=0)
    o59_total_out_m = peewee.IntegerField(default=0)
    o59_total_out_f = peewee.IntegerField(default=0)

    # Follow_up URENI (1)
    fu1_total_beginning_m = peewee.IntegerField(default=0)
    fu1_total_beginning_f = peewee.IntegerField(default=0)
    fu1_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    fu1_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    fu1_oedema = peewee.IntegerField(default=0)
    fu1_other = peewee.IntegerField(default=0)

    fu1_new_case = peewee.IntegerField(default=0)
    fu1_relapse = peewee.IntegerField(default=0)
    fu1_returned = peewee.IntegerField(default=0)
    fu1_nut_transfered_in = peewee.IntegerField(default=0)
    fu1_nut_referred_in = peewee.IntegerField(default=0)
    fu1_admitted_m = peewee.IntegerField(default=0)
    fu1_admitted_f = peewee.IntegerField(default=0)
    # OUT
    fu1_healed = peewee.IntegerField(default=0)
    fu1_referred_out = peewee.IntegerField(default=0)
    fu1_deceased = peewee.IntegerField(default=0)
    fu1_aborted = peewee.IntegerField(default=0)
    fu1_non_respondant = peewee.IntegerField(default=0)
    fu1_medic_transfered_out = peewee.IntegerField(default=0)
    fu1_nut_transfered_out = peewee.IntegerField(default=0)
    fu1_total_out_m = peewee.IntegerField(default=0)
    fu1_total_out_f = peewee.IntegerField(default=0)


class PECSAMPReport(BaseModel, PECReport):

    report = peewee.ForeignKeyField(Report, unique=True,
                                    related_name='pec_samp_reports')

    # under 6 months
    u6_total_beginning_m = peewee.IntegerField(default=0)
    u6_total_beginning_f = peewee.IntegerField(default=0)
    u6_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    u6_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    u6_oedema = peewee.IntegerField(default=0)
    u6_other = peewee.IntegerField(default=0)

    u6_new_case = peewee.IntegerField(default=0)
    u6_relapse = peewee.IntegerField(default=0)
    u6_returned = peewee.IntegerField(default=0)
    u6_nut_transfered_in = peewee.IntegerField(default=0)
    u6_admitted_m = peewee.IntegerField(default=0)
    u6_admitted_f = peewee.IntegerField(default=0)
    # OUT
    u6_healed = peewee.IntegerField(default=0)
    u6_deceased = peewee.IntegerField(default=0)
    u6_aborted = peewee.IntegerField(default=0)
    u6_non_respondant = peewee.IntegerField(default=0)
    u6_medic_transfered_out = peewee.IntegerField(default=0)
    u6_nut_transfered_out = peewee.IntegerField(default=0)
    u6_total_out_m = peewee.IntegerField(default=0)
    u6_total_out_f = peewee.IntegerField(default=0)

    # Between 6 months and 59 months
    u59_total_beginning_m = peewee.IntegerField(default=0)
    u59_total_beginning_f = peewee.IntegerField(default=0)
    u59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    u59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    u59_oedema = peewee.IntegerField(default=0)
    u59_other = peewee.IntegerField(default=0)

    u59_new_case = peewee.IntegerField(default=0)
    u59_relapse = peewee.IntegerField(default=0)
    u59_returned = peewee.IntegerField(default=0)
    u59_nut_transfered_in = peewee.IntegerField(default=0)
    u59_admitted_m = peewee.IntegerField(default=0)
    u59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    u59_healed = peewee.IntegerField(default=0)
    u59_deceased = peewee.IntegerField(default=0)
    u59_aborted = peewee.IntegerField(default=0)
    u59_non_respondant = peewee.IntegerField(default=0)
    u59_medic_transfered_out = peewee.IntegerField(default=0)
    u59_nut_transfered_out = peewee.IntegerField(default=0)
    u59_total_out_m = peewee.IntegerField(default=0)
    u59_total_out_f = peewee.IntegerField(default=0)

    # over 59 months
    o59_total_beginning_m = peewee.IntegerField(default=0)
    o59_total_beginning_f = peewee.IntegerField(default=0)
    o59_hw_u70_bmi_u16 = peewee.IntegerField(default=0)
    o59_muac_u11_muac_u18 = peewee.IntegerField(default=0)
    o59_oedema = peewee.IntegerField(default=0)
    o59_other = peewee.IntegerField(default=0)

    o59_new_case = peewee.IntegerField(default=0)
    o59_relapse = peewee.IntegerField(default=0)
    o59_returned = peewee.IntegerField(default=0)
    o59_nut_transfered_in = peewee.IntegerField(default=0)
    o59_admitted_m = peewee.IntegerField(default=0)
    o59_admitted_f = peewee.IntegerField(default=0)
    # OUT
    o59_healed = peewee.IntegerField(default=0)
    o59_deceased = peewee.IntegerField(default=0)
    o59_aborted = peewee.IntegerField(default=0)
    o59_non_respondant = peewee.IntegerField(default=0)
    o59_medic_transfered_out = peewee.IntegerField(default=0)
    o59_nut_transfered_out = peewee.IntegerField(default=0)
    o59_total_out_m = peewee.IntegerField(default=0)
    o59_total_out_f = peewee.IntegerField(default=0)