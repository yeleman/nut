#!/usr/bin/env python
# encoding=utf-8

from datetime import date

from nutrsc.constants import *
import gao_data


"""
    Input consumption at centers by malnutrition level.
    Inputs represented by codes (see inputs fixtures)
    Table is versioned.
"""
CONSUMPTION_TABLE = {
    MODERATE: {
        DEFAULT_VERSION: {'csb', 'unimix', 'oil', 'sugar', 'mil', 'niebe'},
    },
    SEVERE: {
        DEFAULT_VERSION: {'plumpy'},
    },
    SEVERE_COMP: {
        DEFAULT_VERSION: {'f75', 'f100', 'plumpy'},
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

# percentage from which expected and real data differing should raise warning
WARNING_DIFF_RATE = 15
AVG_GROWTH_RATE = 2.63


def compare_expected_value(report, field, value):
    exp_value = get_expected_value(report, field)
    if not exp_value:
        return None

    diff = (WARNING_DIFF_RATE / 100.0) * exp_value
    return value > (exp_value + diff) or value < (exp_value - diff)
    

def get_expected_value(report, field):
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
                return get_avg_adm_for(hc_code, period.month, cap, age)
            else:
                return gao_data.PEC_ADM[hc_code][period.year][period.month][cap][age]
        except IndexError:
            return None

def get_avg_adm_for(hc_code, month, cap, age):
    years = gao_data.PEC_ADM[hc_code].keys()
    total = sum([gao_data.PEC_ADM[hc_code][year][month][cap][age] 
                  for year in years])
    return float(total) / len(years)
