#!/usr/bin/env python
# encoding=utf-8

import time
import threading
import pickle

import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message


class Event(object):

    LOGIN_SUCCESS = 0
    LOGIN_FAILED = 1
    SMS_SERVICE = 2
    REPORT_SUCCESS = 3
    REPORT_FAILED = 4
    REPORT_UPDATED = 5
    LOW_BATTERY = 6
    SMS_ERROR = 7

    EV_TYPES = ((LOGIN_SUCCESS, u"Identification distante réussie"),
                (LOGIN_FAILED, u"Identification distante infructueuse"),
                (SMS_SERVICE, u"SMS d'information reçu"),
                (REPORT_SUCCESS, u"Rapport accepté"),
                (REPORT_FAILED, u"Report rejeté"),
                (REPORT_UPDATED, u"Rapport modifié par le niveau supérieur"),
                (LOW_BATTERY, u"Batterie faible"),
                (SMS_ERROR, u"Erreur technique SMS"))

    def __init__(self, type, detail):
        self.type = type
        self.detail = detail
        self.discarded = False

    @property
    def alive(self):
        return not self.discarded

    @property
    def is_alive(self):
        return self.alive()

    def discard(self):
        self.discarded = True

    def __unicode__(self):
        return self.verbose()

    def verbose(self):
        for k, t in self.EV_TYPES:
            if k == self.type:
                return t
        return unicode(self.type)
    
    def to_dict(self):
        return {'type': self.type,
                'detail': self.detail,
                'discarded': self.discarded}
    
    @classmethod
    def from_dict(cls, dic):
        return cls(dic.get('type', ''), dic.get('detail', u''))


def send_event(type_, detail=None):
    print('send event')
    e = Event(type_, detail)
    return send_raw_event(e)


def send_raw_event(event):
    my_link = snakemq.link.Link()
    my_packeter = snakemq.packeter.Packeter(my_link)
    my_messaging = snakemq.messaging.Messaging('client', "",
                                               my_packeter)
    my_link.add_connector(("localhost", 4000))
    message = snakemq.message.Message(pickle.dumps(event.to_dict()),
                                      ttl=5)
                                        
    thread = threading.Thread(target=my_link.loop)
    thread.start()

    my_messaging.send_message('server', message)
    time.sleep(2)
    my_link.stop()