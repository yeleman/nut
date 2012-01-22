#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

import peewee

from nutrsc import constants as NUT
from nutrsc import mali
from . import BaseModel, Report, NUTInput


class OrderReport(BaseModel):

    """ Aggregates InputOrderReport for a report """

    MAM = NUT.MODERATE
    SAM = NUT.SEVERE
    SAMP = NUT.SEVERE_COMP

    # unique_together = ('period', 'entity', 'type', 'nut_type')

    report = peewee.ForeignKeyField(Report, related_name='order_reports')
    nut_type = peewee.CharField(max_length=20)
    version = peewee.CharField(max_length=2)

    def is_complete(self):
        for code in CONSUMPTION_TABLE[self.nut_type][self.version]:
            if not self.has(code):
                return False
        return True

    def is_overloaded(self):
        for inpr in InputOrderReport.filter(order_report=self):
            if not inpr.nut_input.slug \
               in CONSUMPTION_TABLE[self.nut_type][self.version]:
                return True
        return False

    def has(self, code):
        """ whether there is a matching input report for code """
        return InputOrderReport.filter(order_report=self,
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
        for ir in InputOrderReport.filter(order_report=self):
            ir.delete_safe()
        self.delete_instance()

    @classmethod
    def create_safe(cls, report, nut_type, version=NUT.DEFAULT_VERSION):
        
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
            in mali.CONSUMPTION_TABLE[r.nut_type][NUT.DEFAULT_VERSION]:
                ninput = NUTInput.filter(slug=input_code).get()
                ir = InputOrderReport.create_safe(order_report=r, 
                                                  nut_input=ninput)
        except:
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
        # simply check that all of them exist.
        for report in self.nutinput_reports:
            if not report.is_valid():
                return False
        return self.is_complete()

class InputOrderReport(BaseModel):

    """ Order Quantities for a NUTInput and an OrderReport """

    #unique_together = ('order_report', 'nut_input')

    order_report = peewee.ForeignKeyField(OrderReport,
                                          related_name='nutinput_reports')
    nut_input = peewee.ForeignKeyField(NUTInput, related_name='order_reports')
    quantity = peewee.IntegerField(default=0)

    def __unicode__(self):
        return ugettext(u"%(report)s/%(input)s") \
                        % {'report': self.order_report,
                           'input': self.nut_input}

    @classmethod
    def create_safe(cls, order_report, nut_input):
        
        # return existing row if applicable
        if cls.filter(order_report=order_report,
                      nut_input=nut_input).count():
            return cls.filter(order_report=order_report,
                              nut_input=nut_input).get()

        # create report
        r = cls(order_report=order_report, nut_input=nut_input)
        r.save()
        return r

    @property
    def status(self):
        return self.order_report.report.status

    @property
    def CAP(self):
        return self.order_report.nut_type
    
    def is_valid(self):
        # always valid.
        return True