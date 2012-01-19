#!/usr/bin/env python
# encoding=utf-8

from nutrsc.constants import *

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


def compare_expected_value(report, field, value):
    exp_value = get_expected_value(report, field)
    diff = (WARNING_DIFF_RATE / 100.0) * exp_value
    return value > (exp_value + diff) or value < (exp_value - diff)
    

def get_expected_value(report, field):
    return 22