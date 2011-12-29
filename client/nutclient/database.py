#!/usr/bin/env python
# encoding=utf-8

import peewee

#dbh = peewee.MySQLDatabase('my_database', user='code')
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
        

def setup():
    """ create tables if not exist """
    for model in [User,]:
        if not model.table_exists():
            model.create_table()


# launch setup at import time
setup()
