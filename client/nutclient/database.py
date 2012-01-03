#!/usr/bin/env python
# encoding=utf-8

from datetime import datetime, date

import peewee

from nutrsc import constants as nutrsc

dbh = peewee.SqliteDatabase('/home/reg/src/nut/client/client.db')


def _(text):
    return text

class BaseModel(peewee.Model):

    class Meta:
        database = dbh


class User(BaseModel):

    """ User account

    Stores credentials (username + hash) for offline login
    Stores Health Center infos """

    username = peewee.CharField(max_length=30, unique=True)
    pwhash = peewee.CharField(max_length=90)
    active = peewee.BooleanField()

    hc_code = peewee.CharField(max_length=20)
    hc_name = peewee.CharField(max_length=50)
    hc_ismam = peewee.BooleanField()
    hc_issam = peewee.BooleanField()
    hc_issamp = peewee.BooleanField()

    def __unicode__(self):
        return self.username

    @property
    def hc(self):
        return self.hc_name.title()

    def hc_full(self):
        return _(u"%(name)s (%(code)s)") \
               % {'name': self.hc, 'code': self.hc_code}

    def caps(self):
        caps = []
        for cap in ['mam', 'sam', 'samp']:
            if getattr(self, 'hc_is%s' % cap):
                caps.append(cap)
        return caps

    def verb_caps(self):
        return "+".join([_(cap.upper()) for cap in self.caps()])


class Setting(BaseModel):

    slug = peewee.CharField(max_length=50, unique=True)
    value = peewee.CharField(max_length=100)

    def __unicode__(self):
        return self.slug


class Options(dict, object):
    """ dumb dict store giving inst.var access to var property """

    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __getattribute__(self, name):
        try:
            return Setting.select().get(slug=name).value
        except:
            return None

# instanciate and fill-up settings dict.
config = Options()


class Period(BaseModel):

    datestr = peewee.CharField(unique=True)

    @property
    def month(self):
        return int(self.datestr[:2])

    @property
    def year(self):
        return int(self.datestr[2:6])

    def __unicode__(self):
        d = date(self.year, self.month, 1)
        return d.strftime('%B %Y')

    @classmethod
    def from_date(cls, date_obj):
        datestr = date_obj.strftime('%d%Y')
        if cls.filter(datestr=datestr).count() == 0:
            p = cls(datestr=datestr)
            p.save()
            return p
        else:
            return cls.select().get(datestr=datestr)

class Report(BaseModel):

    STATUS_DRAFT = 0
    STATUS_COMPLETE = 1
    STATUS_SENT = 2
    STATUS_REMOTE_MODIFIED = 3
    STATUS_LOCAL_MODIFIED = 4
    
    created_by = peewee.ForeignKeyField(User)
    created_on = peewee.DateTimeField()
    modified_on = peewee.DateTimeField()
    period = peewee.ForeignKeyField(Period, unique=True)
    status = peewee.IntegerField()

    def __unicode__(self):
        return self.period

class ReportHistory(BaseModel):

    report = peewee.ForeignKeyField(Report, related_name='exchanges')

    previous_status = peewee.CharField()
    # store a Pickle serialized version of changed fields
    # with previous values
    modified_fields = peewee.CharField()

    
class NUTInput(BaseModel):

    name = peewee.CharField(max_length=50)
    slug = peewee.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return self.name


class ConsumptionReport(BaseModel):

    """ Agregates InputConsumption Reports for a CAP and a Report """

    MAM = nutrsc.MODERATE
    SAM = nutrsc.SEVERE
    SAMP = nutrsc.SEVERE_COMP

    # unique_together = ('report', 'nut_type')

    report = peewee.ForeignKeyField(Report, related_name='cons_reports')
    nut_type = peewee.CharField(max_length=20)
    version = peewee.CharField(max_length=2)

    def __unicode__(self):
        cap = self.nut_type.upper()
        return ugettext(u"%(cap)s/%(period)s") \
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


class InputConsumptionReport(BaseModel):

    """ Consumption Quantities for a NUTInput and a ConsumptionReport """

    #unique_together = ('cons_report', 'nut_input')

    cons_report = peewee.ForeignKeyField(ConsumptionReport)
    nut_input = peewee.ForeignKeyField(NUTInput,
                                       related_name='nutinput_reports')

    initial = peewee.IntegerField()
    received = peewee.IntegerField()
    used = peewee.IntegerField()
    lost = peewee.IntegerField()

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


class OrderReport(Report):

    """ Aggregates InputOrderReport for a report """

    MAM = nutrsc.MODERATE
    SAM = nutrsc.SEVERE
    SAMP = nutrsc.SEVERE_COMP

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
        for inpr in InputOrderReport.objects.filter(order_report=self):
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

class InputOrderReport(BaseModel):

    """ Order Quantities for a NUTInput and an OrderReport """

    #unique_together = ('order_report', 'nut_input')

    order_report = peewee.ForeignKeyField(OrderReport)
    nut_input = peewee.ForeignKeyField(NUTInput, related_name='inputs_reports')
    quantity = peewee.IntegerField()

    def __unicode__(self):
        return ugettext(u"%(report)s/%(input)s") \
                        % {'report': self.order_report,
                           'input': self.nut_input}

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

def setup():
    """ create tables if not exist """
    for model in [User, Setting, Period,
                 #Report, ReportHistory,
                 NUTInput, ConsumptionReport, InputConsumptionReport,
                 OrderReport, InputOrderReport]:
        if not model.table_exists():
            model.create_table()

    # default setting
    load_default_settings()

    # default Inputs
    load_default_inputs()


# launch setup at import time
setup()
