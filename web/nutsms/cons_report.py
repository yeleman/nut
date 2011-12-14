#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

import logging
import locale

from django.utils.translation import ugettext as _
from django.conf import settings

from nutrsc.errors import REPORT_ERRORS

logger = logging.getLogger(__name__)
locale.setlocale(locale.LC_ALL, settings.DEFAULT_LOCALE)


def cons_sub_report(message, pec, infos):
    """ PEC Report part of main Report SMS handling """

    def resp_error(code, msg):
        return (False, (code, msg))

    return (True, {'mam': 'reg', 'sam': 'rig'})
