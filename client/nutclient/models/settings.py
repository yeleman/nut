#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

import peewee

from . import BaseModel


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
        def update(slug, value):
            if Setting.filter(slug=slug).count():
                sett = Setting.filter(slug=slug).get()
            else:
                sett = Setting(slug=slug)
            sett.value = value
            sett.save()
            return sett.value
        if name == 'update':
            return update
        try:
            return Setting.select().get(slug=name).value
        except:
            return None
