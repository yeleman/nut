#!/usr/bin/env python
# encoding=utf-8

import peewee

#dbh = peewee.MySQLDatabase('my_database', user='code')
dbh = peewee.SqliteDatabase('client.db')


class BaseModel(peewee.Model):

    class Meta:
        database = dbh


class User(BaseModel):

    """ User account

    Stores credentials (username + hash) for offline login
    Stores Health Center infos """

    username = peewee.CharField(max_length=30, unique=True)
    pwhash = peewee.CharField(max_length=90)
    active = peewee.BooleanField

    hc_code = peewee.CharField(max_length=20)
    hc_name = peewee.CharField(max_length=50)
    hc_ismam = peewee.BooleanField()
    hc_issam = peewee.BooleanField()
    hc_issamp = peewee.BooleanField()

    def __unicode__(self):
        return self.username

def setup():
    """ create tables if not exist """
    for model in [User,]:
        if not model.table_exists():
            model.create_table()


# launch setup at import time
setup()
