#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import pickle
from datetime import date, datetime

import peewee

from nutclient import local_config

dbh = peewee.SqliteDatabase(local_config.SQLITE_PATH)


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

    def dump(self):
        return pickle.dumps(self.get_field_dict())

    def create_revision(self):
        return Revision.create(model_ref=self.model_ref,
                               datetime=datetime.now(),
                               content=self.dump())

    @property
    def revisions(self, limit=0):
        return [r.load()
                for r 
                in Revision.filter(model_ref=self.model_ref) \
                           .order_by(('datetime', 'desc')).limit(limit)]

    @property
    def last_revision(self):
        try:
            return self.revisions[-1]
        except IndexError:
            return self.get_field_dict()

    def diff(self, revision):
        return Revision.diff(revision, self.get_field_dict())

    @property
    def dirty_fields(self):
        return self.diff(self.last_revision)

    @property
    def model_ref(self):
        return '%(table)s#%(id)d' % {'table': self._meta.model_name,
                                     'id': self.id}

class Revision(peewee.Model):

    class Meta:
        database = dbh

    model_ref = peewee.CharField()
    datetime = peewee.DateTimeField()
    content = peewee.TextField()

    def load(self):
        d = pickle.loads(bytearray(self.content, 'utf-8'))
        d.update({'_revision_date': self.datetime,
                  '_revision_model': self.model})
        return d

    @property
    def model(self):
        mname, mid = self.model_ref.rsplit('#', 1)
        cls = eval(mname)
        return cls.get(id=mid)

    @classmethod
    def diff(cls, previous, last):
        d = {}
        keys = previous.keys() + last.keys()
        keys = list(set(keys))
        for key in keys:
            if key.startswith('_revision'):
                continue

            npv = False
            nlv = False

            try:
                pv = previous.get(key)
            except KeyError:
                npv = True

            try:
                lv = last.get(key)
            except KeyError:
                nlv = True

            # key missing on previous dict
            if npv:
                d[key] = lv
                continue
            # key missing on last dict
            if nlv:
                d[key] = pv
                continue

            # only add if value is different.
            # set value as the one of last dict
            if pv != lv:
                d[key] = lv
        return d


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
        return u"%(name)s (%(code)s)" \
               % {'name': self.hc, 'code': self.hc_code}

    def caps(self):
        caps = []
        for cap in ['mam', 'sam', 'samp']:
            if getattr(self, 'hc_is%s' % cap):
                caps.append(cap)
        return caps

    def verb_caps(self):
        return "+".join([cap.upper() for cap in self.caps()])


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
        return unicode(d.strftime('%B %Y').decode('utf-8'))

    @classmethod
    def from_date(cls, date_obj):
        datestr = date_obj.strftime('%m%Y')
        if cls.filter(datestr=datestr).count() == 0:
            p = cls(datestr=datestr)
            p.save()
            return p
        else:
            return cls.select().get(datestr=datestr)

    def next(self):
        if self.month < 12:
            nmonth = self.month + 1
            nyear = self.year
        else:
            nmonth = 1
            nyear = self.year + 1
        return Period.from_date(date(nyear, nmonth, 1))

    def previous(self):
        if self.month > 1:
            nmonth = self.month - 1
            nyear = self.year
        else:
            nmonth = 12
            nyear = self.year - 1
        return Period.from_date(date(nyear, nmonth, 1))


class NUTInput(BaseModel):

    name = peewee.CharField(max_length=50)
    slug = peewee.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.slug


class Message(BaseModel):

    INFO = 'INFO'
    WARN = 'WARN'
    SUCC = 'SUCC'
    CRIT = 'CRIT'

    FLAGS = (INFO, WARN, SUCC, CRIT)

    identity = peewee.CharField(max_length=50)
    date = peewee.DateTimeField()
    text = peewee.TextField()
    flag = peewee.TextField(default=INFO)

    def __unicode__(self):
        return self.date.strftime('%c')
    
    @property
    def display_date(self):
        return unicode(self.date.strftime('%d %B, %Hh%M').decode('utf-8'))


from report import Report, ReportHistory
from consumption import ConsumptionReport, InputConsumptionReport
from order import OrderReport, InputOrderReport
from pec import PECMAMReport, PECSAMReport, PECSAMPReport
from settings import Options, Setting

# instanciate and fill-up settings dict.
config = Options()