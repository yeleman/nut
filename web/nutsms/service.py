#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from nosms.utils import send_sms


def nut_service(recipients, flag, text):
    """ Server to client alert, notice messages

    Whenever central wants to send a text message to the users.
    Messages have a flag for INFO, WARN, SUCC, CRITICAL.

    recipients: Provider

    < nut service flag | message """

    msg = u"nut service %(flag)s|%(text)s" % {'flag': flag, 'text': text}

    for recipient in recipients:
        if isinstance(recipient, basestring):
            ph = recipient
        else:
            if hasattr(recipient, 'phone_number'):
                ph = recipient.phone_number
            else:
                logger.error(u"Unable to send SMS to recipient: %s" \
                             % (recipient))
                continue
        send_sms(ph, msg)

    return 
