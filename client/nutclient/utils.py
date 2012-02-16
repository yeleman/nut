#!/usr/bin/env python
# encoding=utf-8

import locale

from database import *
from nutrsc.tools import generate_user_hash
from nutclient.exceptions import *

from nosmsd.utils import send_sms

from sms.outgoing import report_sms, report_update_sms


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
    send_sms(config.SRV_NUM, \
             u"nut login %(user)s %(password)s" % {'user': username,
                                               'password': password})


def formatted_number(number):
    try:
        return locale.format("%d", number, grouping=True) \
                     .decode(locale.getlocale()[1])
    except:
        return "%s" % number


def send_report(report, user):
    # can only send complete reports (or re-send)
    if not report.can_send():
        return False

    # create revision if it's not a resend
    create_revision =  report.status not in (report.STATUS_SENT, 
                                             report.STATUS_MODIFIED_SENT)

    # change status
    if report.status in (report.STATUS_LOCAL_MODIFIED,
                         report.STATUS_MODIFIED_SENT):
        report.status = report.STATUS_MODIFIED_SENT
        sms_report = report_update_sms(report)
        kw = 'update-report'
    else:
        report.status = report.STATUS_SENT
        sms_report = report_sms(report)
        kw = 'report'
    
    sms = (u"nut %(kw)s %(user)s %(pwhash)s %(report)s-EOM-"
           % {'kw': kw,
              'user': user.username,
              'pwhash': user.pwhash,
              'report': sms_report})

    print(sms)
    send_sms(config.SRV_NUM, sms)

    # save status change
    report.save()

    # commit revision
    if create_revision:
        report.create_revision_safe()

    return True