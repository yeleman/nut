#!/usr/bin/env python
# encoding=utf-8

from database import *
from nutrsc.tools import generate_user_hash
from nutclient.exceptions import *

from nosmsd.utils import send_sms


def offline_login(username, password):
    """ test a username/password couple locally for access """
    username = username.strip()
    password = password.strip()

    # check if username in DB and raise if not to trigger online login
    if User.filter(username=username, pwhash__ne='').count() == 0:
        raise UsernameNotFound()

    # compare hash with stored one.
    passhash = str(generate_user_hash(username, password))
    try:
        user = User.get(username=username, pwhash=passhash)
    except User.DoesNotExist:
        user = None

    return user


def remote_login_request(username, password):
    """ sends formatted SMS to server to request login """
    send_smd(u"nut login %(user)s %(pass)s" % {'user': username,
                                               'password': password})
