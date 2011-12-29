#!/usr/bin/env python
# encoding=utf-8

import sys
import zmq


def _(text):
    return text


class Event(object):

    LOGIN_SUCCESS = 0
    LOGIN_FAILED = 1
    SMS_SERVICE = 2
    REPORT_SUCCESS = 3
    REPORT_FAILED = 4
    REPORT_UPDATED = 5
    LOW_BATTERY = 6
    SMS_ERROR = 7

    EV_TYPES = ((LOGIN_SUCCESS, _(u"Remote login successful")),
                (LOGIN_FAILED, _(u"Remote login failed")),
                (SMS_SERVICE, _(u"Service message received")),
                (REPORT_SUCCESS, _(u"Report accepted")),
                (REPORT_FAILED, _(u"Report rejected")),
                (REPORT_UPDATED, _(u"Report has been updated")),
                (LOW_BATTERY, _(u"Low battery")),
                (SMS_ERROR, _(u"SMS device error")))

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


def send_raw_event(event):
    # Socket to talk to server
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.send_pyobj(event)
        socket.close()
        return True
    except Exception as e:
        return False


def send_event(type_, detail=None):
    e = Event(type_, detail)
    return send_raw_event(e)
