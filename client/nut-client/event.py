#!/usr/bin/env python
# encoding=utf-8

import sys
import zmq

class Event(object):

    LOGIN_SUCCESS = 0
    LOGIN_FAILED = 1
    SMS_SERVICE = 2
    REPORT_SUCCESS = 3
    REPORT_FAILED = 4
    REPORT_UPDATED = 5
    LOW_BATTERY = 6
    SMS_ERROR = 7

    def __init__(self, type, detail):
        self.type = type
        self.detail = detail


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
