#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import datetime
import logging
import locale
import re

from nosmsd.utils import send_sms
from nutclient.event import send_event, Event
from nutclient.models import Message

from .login import nut_logged_in
#from .report import nut_report


logger = logging.getLogger(__name__)


def nosms_handler(message):
    """ NUT SMS router """
    def main_nut_handler(message):
        keyword = 'nut'
        commands = {
            'logged-in': nut_logged_in,
            #'logged-out': nut_logged_out,
            #'report': nut_report,
            'test': nut_test,
            'echo': nut_echo}

        if message.content.lower().startswith('nut '):
            for cmd_id, cmd_target in commands.items():
                command = '%s %s' % (keyword, cmd_id)
                if message.content.lower().startswith(command):
                    n, args = re.split(r'^%s\s?' \
                                       % command,
                                         message.content.lower().strip())
                    return cmd_target(message,
                                      args=args,
                                      sub_cmd=cmd_id,
                                      cmd=command)
        else:
            # use default handler (store in Message)
            return nut_default(message)

    if main_nut_handler(message):
        message.status = message.STATUS_PROCESSED
        message.save()
        logger.info(u"[HANDLED] msg: %s" % message)
        return True
    logger.info(u"[NOT HANDLED] msg : %s" % message)
    return False


def nut_test(message, args, sub_cmd, cmd):
    try:
        code, msg = message.text.split('nut test')
    except:
        msg = ''

    message.respond(u"Received on %(date)s: %(msg)s" \
                    % {'date': datetime.datetime.now(), 'msg': msg})
    return True


def nut_echo(message, args, sub_cmd, cmd):
    message.respond(args)
    return True


def nut_default(message):
    """ takes arbitrary message to the Message list """
    return nut_message(message, message.content)


def nut_service(message, args, sub_cmd, cmd):
    """ Free text message or info from Server

    nut service flag|message """

    flag, text = args.split('|')
    return nut_message(message, text, flag)


def nut_message(message, text, flag=Message.INFO):
    """ [NON-SMS handler] Stores message to Message list """

    flag = flag.upper()
    if not flag in Message.FLAGS:
        flag = Message.INFO
    
    try:
        Message.create(identity=message.identity,
                           date=message.date,
                           text=text,
                           flag=flag)
        send_event(Event.SMS_SERVICE, u"SMS reçu: %s" % text[:50])
        return True
    except Exception as e:
        print(e)
        return False