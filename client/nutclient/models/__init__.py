#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from datetime import date, datetime

import peewee

dbh = peewee.SqliteDatabase('/home/reg/src/nut/client/client.db')


def _(text):
    return text


class BaseModel(peewee.Model):

    class Meta:
        database = dbh

    def create_safe(self, *args, **kwargs):
        pass

    @classmethod
    def all(cls):
        return list(cls.select())

    def delete_safe(self):
        self.delete_instance()

class User(BaseModel):

    """ User account

    Stores credentials (username + hash) for offline login
    Stores Health Center infos """

    username = peewee.CharField(max_length=30, unique=True)
    pwhash = peewee.CharField(max_length=90)
    active = peewee.BooleanField()

    # Health Center informations
    # Subject to change over time
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
        datestr = date_obj.strftime('%m%Y')
        if cls.filter(datestr=datestr).count() == 0:
            p = cls(datestr=datestr)
            p.save()
            return p
        else:
            return cls.select().get(datestr=datestr)
    

class NUTInput(BaseModel):

    name = peewee.CharField(max_length=50)
    slug = peewee.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return self.name

from report import Report, ReportHistory
from consumption import ConsumptionReport, InputConsumptionReport
from order import OrderReport, InputOrderReport
from pec import PECMAMReport, PECSAMReport, PECSAMPReport
from settings import Options, Setting

# instanciate and fill-up settings dict.
config = Options()