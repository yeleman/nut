#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from nutrsc.errors import LOGIN_ERRORS
from nutrsc.tools import generate_user_hash

from nutclient.event import send_event, Event
from nutclient.database import User

def nut_report_feedback(message, args, sub_cmd, **kwargs):
    """ User successfully logged-into server.

    After a login request, server sends a confirmation with login informations

    < nut logged-in rgaudin 4663950500290933446 mam+sam ntil|N'Tillit
                hash capabilities HC-code | HC Name """

    # if successful
    #   create revision