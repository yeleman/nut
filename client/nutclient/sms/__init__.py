#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import datetime
import logging
import locale
import re

from nosmsd.utils import send_sms

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
            return False

    if main_nut_handler(message):
        message.status = message.STATUS_PROCESSED
        message.save()
        logger.info(u"[HANDLED] msg: %s" % message)
        return True
    logger.info(u"[NOT HANDLED] msg : %s" % message)
    return False


def nut_test(message, **kwargs):
    try:
        code, msg = message.text.split('nut test')
    except:
        msg = ''

    message.respond(u"Received on %(date)s: %(msg)s" \
                    % {'date': datetime.datetime.now(), 'msg': msg})
    return True


def nut_echo(message, **kwargs):
    message.respond(kwargs['args'])
    return True
