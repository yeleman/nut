#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin


from nutrsc.constants import *
from nutrsc.mali import *
from nutrsc.proxy import proxy_field_name


class DataHolder(object):

    def get(self, slug):
        return getattr(self, slug)

    def field_name(self, slug):
        return proxy_field_name(slug)

    def set(self, slug, data):
        try:
            setattr(self, slug, data)
        except AttributeError:
            exec 'self.%s = None' % slug
            setattr(self, slug, data)

    def fields_for(self, cat):
        return []

    def data_for_cat(self, cat, as_dict=False):
        data = []
        for field in self.fields_for(cat):
            data.append(self.get(field))
        return data


class CONSInputDataHolder(DataHolder):

    input_code = ''
    initial = 0
    received = 0
    consumed = 0
    lost = 0

    def fields(self):
        return ['initial', 'received', 'consumed', 'lost']

    @property
    def got(self):
        return (initial + received)

    @property
    def used(self):
        return (consomed + lost)

    @property
    def left(self):
        return self.got() - self.used()

    @property
    def valid(self):
        return self.used <= self.left


class CONSDataHolder(DataHolder):

    version = DEFAULT_VERSION
    cap = ''

    def inputs(self):
        h = {'mam': MODERATE,
             'sam': SEVERE,
             'samp': SEVERE_COMP}
        return CONSUMPTION_TABLE[h[self.cap]][self.version]


class CONSMAMDataHolder(CONSDataHolder):
    cap = 'mam'


class CONSSAMDataHolder(CONSDataHolder):
    cap = 'sam'


class CONSSAMPDataHolder(CONSDataHolder):
    cap = 'samp'


class ORDERInputDataHolder(DataHolder):

    input_code = ''
    quantity = 0

    def fields(self):
        return ['quantity']

from PECMAM import PECMAMDataHolder
from PECSAM import PECSAMDataHolder
from PECSAMP import PECSAMPDataHolder

