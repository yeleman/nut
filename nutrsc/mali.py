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
