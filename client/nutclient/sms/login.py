#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

from nutrsc.errors import LOGIN_ERRORS
from nutrsc.tools import generate_user_hash

from nutclient.event import send_event, Event
from nutclient.database import User

def nut_logged_in(message, args, sub_cmd, **kwargs):
    """ User successfully logged-into server.

    After a login request, server sends a confirmation with login informations

    < nut logged-in rgaudin 4663950500290933446 mam+sam ntil|N'Tillit
                hash capabilities HC-code | HC Name """
    # retrieve data from formatted text
    all_args, hc_name = args.split('|')
    username, pwhash, capstr, hc_code = all_args.strip().split()
    username = username.strip()
    hc_name = hc_name.strip()
    pwhash = pwhash.strip()
    capstr = capstr.strip()
    hc_code = hc_code.strip()

    caps = capstr.split('+')

    # create or retrieve User
    if User.filter(username=username).count() > 0:
        user = User.get(username=username)
    else:
        user = User.create(username=username)
        user.save()

    # update infos
    user.pwhash = pwhash
    user.hc_code = hc_code
    user.hc_name = hc_name
    user.active = True

    for cap in caps:
        prop = 'hc_is%s' % cap.lower()
        if hasattr(user, prop):
            setattr(user, prop, True)
        else:
            raise Exception(u"unexpected cap: %s" % cap)

    user.save()

    # send event to GUI
    send_event(Event.LOGIN_SUCCESS,
               u"%s from %s logged in successfully." 
               % (username, hc_name.title()))

    return True
