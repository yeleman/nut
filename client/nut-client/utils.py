#!/usr/bin/env python
# encoding=utf-8

from database import *
from nutrsc.tools import generate_user_hash
from nutclient.exceptions import *

def must_login():
    """ whether user *must* login again

    cases include:
        - never logged in
        - is not logged in right now (main window has no user attached)
        - logged-in but user is not active """

    # Test if session holds a valid user
    

    # Test if we have a user in the DB.
    if User.select().count() == 0:
        return True

    # test if there exist 
    if User.filter(active=True).count() == 0:
        return True


def offline_login(username, password):

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
