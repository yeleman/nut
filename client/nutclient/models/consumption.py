#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

import peewee

from nutrsc.mali import *
from . import BaseModel, Report, NUTInput


class ConsumptionReport(BaseModel):

    """ Agregates InputConsumption Reports for a CAP and a Report """

    MAM = MODERATE
    SAM = SEVERE
    SAMP = SEVERE_COMP

    # unique_together = ('report', 'nut_type')

    report = peewee.ForeignKeyField(Report, related_name='cons_reports')
    nut_type = peewee.CharField(max_length=20)
    version = peewee.CharField(max_length=2, default=DEFAULT_VERSION)

    def __unicode__(self):
        cap = self.nut_type.upper()
        return u"%(cap)s/%(period)s" \
                        % {'period': self.report.period,
                           'cap': cap}

    def is_complete(self):
        for code in CONSUMPTION_TABLE[self.nut_type][self.version]:
            if not self.has(code):
                return False
        return True

    def is_overloaded(self):
        for inpr in InputConsumptionReport.filter(cons_report=self):
            if not inpr.nut_input.slug \
               in CONSUMPTION_TABLE[self.nut_type][self.version]:
                return True
        return False

    def has(self, code):
        # whether there is a matching input report for code 
        return InputConsumptionReport.filter(cons_report=self,
                                             nut_input__slug=code).count() == 1

    @property
    def mam(self):
        return self.filter(nut_type=self.MAM)

    @property
    def sam(self):
        return self.filter(nut_type=self.SAM)

    @property
    def samp(self):
        return self.filter(nut_type=self.SAMP)

    def delete_safe(self):
        for ir in InputConsumptionReport.filter(cons_report=self):
            ir.delete_safe()
        self.delete_instance()

    @classmethod
    def create_safe(cls, report, nut_type, version=DEFAULT_VERSION):

        # return existing row if applicable
        if cls.filter(report=report,
                      nut_type=nut_type, version=version).count():
            return cls.filter(report=report,
                      nut_type=nut_type, version=version).get()

        # create report
        r = cls(report=report, nut_type=nut_type, version=version)
        r.save()

        # create input-related reports
        try:
            for input_code \
            in CONSUMPTION_TABLE[r.nut_type][DEFAULT_VERSION]:
                ninput = NUTInput.filter(slug=input_code).get()
                ir = InputConsumptionReport.create_safe(cons_report=r,
                                                        nut_input=ninput)
        except:
            # something went wrong. let's chain delete everybody
            r.delete_safe()
            return None

        return r

    @property
    def status(self):
        return self.report.status

    @property
    def CAP(self):
        return self.nut_type
    
    def is_valid(self):
        # check that all Nut reports are valid
        for report in self.nutinput_reports:
            if not report.is_valid():
                return False
        # make sure all of them exist
        return self.is_complete()

class InputConsumptionReport(BaseModel):

    """ Consumption Quantities for a NUTInput and a ConsumptionReport """

    #unique_together = ('cons_report', 'nut_input')

    cons_report = peewee.ForeignKeyField(ConsumptionReport, related_name='nutinput_reports')
    nut_input = peewee.ForeignKeyField(NUTInput,
                                       related_name='cons_reports')

    initial = peewee.IntegerField(default=0)
    received = peewee.IntegerField(default=0)
    used = peewee.IntegerField(default=0)
    lost = peewee.IntegerField(default=0)

    def __unicode__(self):
        return u"%(report)s/%(input)s" \
                        % {'report': self.cons_report,
                           'input': self.nut_input}

    @property
    def consumed(self):
        return self.used + self.lost

    @property
    def possessed(self):
        return self.initial + self.received

    @property
    def left(self):
        return self.possessed - self.consumed

    @classmethod
    def create_safe(cls, cons_report, nut_input):

        # return existing row if applicable
        if cls.filter(cons_report=cons_report, nut_input=nut_input).count():
            return cls.filter(cons_report=cons_report, nut_input=nut_input).get()

        # create report
        r = cls(cons_report=cons_report, nut_input=nut_input)
        r.save()
        return r

    @property
    def status(self):
        return self.cons_report.report.status

    @property
    def CAP(self):
        return self.cons_report.nut_type
    
    def is_valid(self):
        return self.consumed <= self.possessed