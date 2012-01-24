#!/usr/bin/env python
# encoding=utf-8

import math
from datetime import date

from nutrsc.constants import *
import gao_data

PPN = 'plumpy'
F75 = 'f75'
F100 = 'f100'
CSB = 'csb'
OIL = 'oil'
SUGAR = 'sugar'
MIL = 'mil'
NIEBE = 'niebe'
UNIMIX = 'unimix'

"""
    Input consumption at centers by malnutrition level.
    Inputs represented by codes (see inputs fixtures)
    Table is versioned.
"""
CONSUMPTION_TABLE = {
    MODERATE: {
        DEFAULT_VERSION: {CSB, UNIMIX, OIL, SUGAR, MIL, NIEBE},
    },
    SEVERE: {
        DEFAULT_VERSION: {PPN},
    },
    SEVERE_COMP: {
        DEFAULT_VERSION: {F75, F100, PPN},
    }
}

CAPS = {
    MODERATE: u"MAM",
    SEVERE: u"MAS",
    SEVERE_COMP: u"NI"}

HC_CAPS = {
    MODERATE: u"URENAM",
    SEVERE: u"URENAS",
    SEVERE_COMP: u"URENI"}

# percentage from which expected 
# and real data differing should raise warning
WARNING_DIFF_RATE = 15
AVG_GROWTH_RATE = 2.63

F75_MEAL_LWB = 70
F75_MEAL_TB_HIV = 400
F75_MEAL_U59 = 120

F100_MEAL_LWB = 70
F100_MEAL_TB_HIV = 400
F100_MEAL_U59 = 120


def compare_expected_adm_value(report, field, value):
    exp_value = get_expected_adm_value(report, field)
    if not exp_value:
        return None

    diff = (WARNING_DIFF_RATE / 100.0) * exp_value
    return value > (exp_value + diff) or value < (exp_value - diff)


def compare_expected_conso_value(period, hc_code, cap, nut_input, value):
    exp_value = get_expected_conso_value(period, hc_code, cap, nut_input)
    if not exp_value:
        return None

    diff = (WARNING_DIFF_RATE / 100.0) * exp_value
    return value > (exp_value + diff) or value < (exp_value - diff)


def compare_expected_order_value(period, hc_code, cap, nut_input, value):
    # order are consumption reports based on period + 2months
    period = period.next().next()
    return compare_expected_conso_value(period, hc_code, cap, nut_input, value)


def get_expected_adm_value(report, field):
    # if no CAP or field, report is probably erroneous, skip
    if not getattr(report, 'CAP', None) or not field:
        return None
    
    hc_code = report.report.hc_code
    year = report.report.period.year - 1
    month = report.report.period.month

    year_diff = 1

    # try to get data from last year
    last_year_value = get_total_adm_for(hc_code,
                                        report.CAP,
                                        field.split('_', 1)[0],
                                        year=year,
                                        month=month)

    # last year data not available
    if not last_year_value:
        # we don't have data for that HC, giving up
        if not hc_code in gao_data.PEC_ADM:
            return None
        else:
            # HC exists in DB. Do we have a year with data?
            avail_years = [year for year 
                           in gao_data.PEC_ADM[hc_code].keys() 
                           if month in gao_data.PEC_ADM[hc_code][year]]
            # no data for this month
            if not avail_years:
                return None
            else:
                avail_years.sort()
                last_year_value = get_total_adm_for(hc_code,
                                    report.CAP,
                                    field.split('_', 1)[0],
                                    year=avail_years[-1],
                                    month=month)
                year_diff = report.report.period.year - avail_years[-1]

    expected_value = last_year_value
    for x in range(1, year_diff + 1):
        expected_value = expected_value * AVG_GROWTH_RATE
    return expected_value


def get_total_adm_for(hc_code, cap, age, period=None, year=None, month=None):

    from database import Period, Report

    if not period:
        period = Period.from_date(date(year, month, 1))
    
    # return real data from report if it exist in DB.
    if Report.filter(period=period, hc_code=hc_code,
                     status=Report.STATUS_VALIDATED).count():
        report = Report.filter(period=period, hc_code=hc_code).get()
        return getattr(report.get_pec_report(cap), '%s_admitted' % age)
    else:
        # if not a report not in DB
        if not hc_code in gao_data.PEC_ADM:
            return None
        
        # retrieve value from flat data
        try:
            if period.year in (2009, 2010, 2011):
                return gao_data.PEC_ADM[hc_code][period.year][period.month][cap][age]
            else:
                return get_avg_adm_for(hc_code, period.month, cap, age)
        except KeyError:
            return None  # TODO

def get_avg_adm_for(hc_code, month, cap, age):
    years = gao_data.PEC_ADM[hc_code].keys()
    total = sum([gao_data.PEC_ADM[hc_code][year][month][cap][age] 
                  for year in years])
    return float(total) / len(years)


def sum_dicts(*dicts):
    ''' sums values of x dicts for each key '''
    d = {}
    keys = []
    for dic in dicts: keys += dic.keys()
    keys = list(set(keys))
    for key in keys:
        d[key] = sum([dic.get(key, 0) for dic in dicts])
    return d

def pick_mam_ration_type(csb, niebe):
    import random
    return csb
    return [csb, niebe][random.randint(0, 1)]

class DataAccessor(object):

    def __init__(self):
        self.CAP = None
        self.others_tb = 0
        self.others_lwb = 0
        self.others_hiv = 0

    @classmethod
    def from_sub_report(cls, report):
        da = cls()
        da.CAP = report.CAP
        for t in ('tb', 'lwb', 'hiv'):
            setattr(da, 'others_%s' % t, getattr(report.report, 'others_%s' % t, 0))
        for age in  POPULATIONS_CAP[report.CAP]:
            setattr(da, '%s_admitted' % age, getattr(report.report.get_pec_report(report.CAP), '%s_admitted' % age, 0))
            setattr(da, '%s_other' % age, getattr(report.report.get_pec_report(report.CAP), '%s_other' % age, 0))
        return da

    @classmethod
    def build_for_period(cls, period, hc_code, cap):
        da = cls()
        if not hc_code in gao_data.PEC_ADM:
            return da
        
        # no data for split-up
        da.CAP = cap
        da.others_tb = 0
        da.others_lwb = 0 
        da.others_hiv = 0

        for age in POPULATIONS_CAP[cap]:
            admitted = get_total_adm_for(hc_code, cap, age, period=period)
            print('calculated admitted for %s %s %s: %s' % (period, hc_code, cap, admitted))
            if not admitted:
                admitted = 0
            setattr(da, '%s_admitted' % age, admitted)
            setattr(da, '%s_other' % age, 0)
        
        return da
    
    @classmethod
    def from_period(cls, period, hc_code, cap):
        # TODO: report???
        from nutclient.database import Report
        if Report.filter(period=period, hc_code=hc_code).count():
            report = Report.filter(period=period, hc_code=hc_code).get()
            return cls.from_sub_report(report.get_cons_report(cap))
        else:
            return cls.build_for_period(period, hc_code, cap)


def get_expected_conso_value(period, hc_code, cap, nut_input):
    data = DataAccessor.from_period(period, hc_code, cap)
    if not data.CAP:
        return None

    others_lwb = data.others_lwb
    others_tb = data.others_tb
    others_hiv = data.others_hiv
    all_others = sum([others_lwb, others_tb, others_hiv])

    try:
        lwb_percent = float(others_tb) / all_others
    except ZeroDivisionError:
        lwb_percent = 0
    try:
        tb_percent = float(others_tb) / all_others
    except ZeroDivisionError:
        tb_percent = 0
    try:
        hiv_percent = float(others_hiv) / all_others
    except ZeroDivisionError:
        hiv_percent = 0

    cons_regular = 0
    cons_lwb = 0
    cons_tb = 0
    cons_hiv = 0

    for age in POPULATIONS_CAP[data.CAP]:
        ration_regular = RATIONS_CAP.get(data.CAP)(age, None)
        ration_lwb = RATIONS_CAP.get(data.CAP)(age, 'lwb')
        ration_tb = RATIONS_CAP.get(data.CAP)(age, 'tb')
        ration_hiv = RATIONS_CAP.get(data.CAP)(age, 'hiv')

        nb_admitted = getattr(data, '%s_admitted' % age, 0)
        nb_other = getattr(data, '%s_other' % age, 0)
        nb_non_others = nb_admitted - nb_other
        # regular ones.
        cons_regular += nb_non_others * ration_regular.get(nut_input.slug, 0)

        if nb_other:
            cons_lwb += int(math.ceil(nb_other * lwb_percent)) * ration_lwb.get(nut_input.slug, 0)
            cons_tb += int(math.ceil(nb_other * tb_percent)) * ration_tb.get(nut_input.slug, 0)
            cons_hiv += int(math.ceil(nb_other * hiv_percent)) * ration_hiv.get(nut_input.slug, 0)
    return sum([cons_regular, cons_lwb, cons_tb, cons_hiv])


def ration_mam(age, other_type=None):

    # no inputs for follow-up?
    if not age in ('u59', 'pw'):
        return {}

    nb_days = 4
    
    nb_csb_per_day = 2  # kg
    nb_niebe_per_day = 1  # kg
    nb_mil_per_day = 1  # kg

    nb_oil_per_day = 200  # g
    nb_sugar_per_day = 160  # g
    
    csb_ration = {CSB: nb_csb_per_day * nb_days}
    niebe_ration = {NIEBE: nb_niebe_per_day * nb_days,
                    MIL: nb_mil_per_day * nb_days}
    
    common_ration = {OIL: nb_oil_per_day * nb_days,
                     SUGAR: nb_sugar_per_day * nb_days}

    rand_ration = pick_mam_ration_type(csb_ration, niebe_ration)

    return sum_dicts(common_ration, rand_ration)


def ration_sam(age, other_type=None):

    # no inputs for o59 nor follow-up?
    if not age in ('u59'):
        return {}

    nb_days = 4
    nb_ppn_per_day = 15

    # 1 carton PPN = 150 sachets
    ration = {PPN: nb_ppn_per_day * nb_days}
    return ration


def ration_samp(age, other_type=None):


    def phase_one(age, other_type=None):
        ''' 6 repas de F75 / jour pendant 5j '''

        nb_days = 5
        nb_meal_per_day = 6

        if other_type == 'lwb':
            f75_meal = F75_MEAL_LWB
        elif other_type in ('tb', 'hiv'):
            f75_meal = F75_MEAL_TB_HIV
        elif age == 'u59':
            f75_meal = F75_MEAL_U59
        else:
            return {}

        ration = {F75: (f75_meal * nb_meal_per_day) * nb_days}

        return ration


    def phase_two(age, other_type=None):

        nb_days = 4
        nb_meal_per_day = 6
        nb_ppn_per_day = 2
        nb_extra_ppn_child = 2
        nb_extra_ppn_adult = 8

        if other_type == 'lwb':
            f100_meal = F100_MEAL_LWB
        elif other_type in ('tb', 'hiv'):
            f100_meal = F100_MEAL_TB_HIV
        elif age == 'u59':
            f100_meal = F100_MEAL_U59
        else:
            f100_meal = 0
        
        if f100_meal:
            ration = {F100: (f100_meal * nb_meal_per_day) * nb_days,
                      PPN: (nb_ppn_per_day * nb_meal_per_day) * nb_days}
        else:
            ration = {}

        if under_59:
            extra = {PPN: nb_extra_ppn_child * nb_days}
        else:
            extra = {PPN: nb_extra_ppn_adult * nb_days}
        
        return sum_dicts(ration, extra)

    return sum_dicts(phase_one(age, other_type),
                 phase_two(age, other_type))

RATIONS_CAP = {
    MODERATE: ration_mam,
    SEVERE: ration_sam,
    SEVERE_COMP: ration_samp
}
