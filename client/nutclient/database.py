#!/usr/bin/env python
# encoding=utf-8

from datetime import datetime

import peewee

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

class ReportHistory(BaseModel):

    report = peewee.ForeignKeyField(Report, related_name='exchanges')

    previous_status = peewee.CharField()
    # store a Pickle serialized version of changed fields
    # with previous values
    modified_fields = peewee.CharField()

class Report(BaseModel):

    STATUS_DRAFT = 0
    STATUS_COMPLETE = 1
    STATUS_SENT = 2
    STATUS_REMOTE_MODIFIED = 3
    STATUS_LOCAL_MODIFIED = 4
    
    created_by = peewee.ForeignKeyField(User)
    created_on = peewee.DateTimeField()
    modified_on = peewee.DateTimeField()
    month = peewee.IntegerField(null=True)
    year = peewee.IntegerField(null=True)
    status = peewee.IntegerField()

    def __unicode__(self):
        if not self.year and not self.month:
            return u"Created on %s" % created_on.strftime('%c')
        elif not self.year:
            d = datetime.now()
            d.month = self.month
            return u"%s ??" % d.strftime('%m')
        elif not self.month:
            return u"?? %d" % self.year
        else:
            d = datetime.datetime(self.year, self.month, 1)
            return u"%s" % d.strftime('%m %Y')
        

def setup():
    """ create tables if not exist """
    for model in [User,]:
        if not model.table_exists():
            model.create_table()


# launch setup at import time
setup()
