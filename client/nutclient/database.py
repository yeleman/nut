#!/usr/bin/env python
# encoding=utf-8

from models import (Revision, Report, ReportHistory, ConsumptionReport,
                    InputConsumptionReport, OrderReport, InputOrderReport,
                    PECMAMReport, PECSAMReport, PECSAMPReport,
                    User, Period, NUTInput, Message, Setting, Options)

def load_default_settings():
    for key, value in {'SRV_NUM': '73120896',
                       'GSM_NET': 'orange',}.items():
        if Setting.filter(slug=key).count() == 0:
            s = Setting(slug=key, value=value)
            s.save()

def load_default_inputs():
    for key, value in {'unimix': u"UNIMIX",
                       'sugar': u"Sucre",
                       'plumpy': u"Plumpy Nut",
                       'oil': u"Huile",
                       'niebe': u"Niébé",
                       'mil': u"Mil",
                       'f75': u"F75",
                       'f100': u"F100",
                       'csb': u"CSB"}.items():
        if NUTInput.filter(slug=key).count() == 0:
            i = NUTInput(slug=key, name=value)
            i.save()

options = Options()

def setup(drop_tables=False):
    """ create tables if not exist """

    did_create = False

    for model in [Revision, User, Setting, Period,
                 Report, ReportHistory,
                 NUTInput, ConsumptionReport, InputConsumptionReport,
                 OrderReport, InputOrderReport,
                 PECMAMReport, PECSAMReport, PECSAMPReport, Message]:
        if drop_tables:
            model.drop_table()
        if not model.table_exists():
            model.create_table()
            did_create = True

    if did_create:
        # default setting
        load_default_settings()

        # default Inputs
        load_default_inputs()

# launch setup at import time
setup()
