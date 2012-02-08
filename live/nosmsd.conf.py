#!/usr/bin/env python
# encoding=utf-8

NOSMSD_HANDLER = 'nutclient.sms.nosms_handler'
NOSMSD_GETTEXT = True
NOSMSD_GETTEXT_LOCALE = 'fr_FR.UTF-8'

NOSMSD_DATABASE = {'type': 'Sqlite', 'name': '/home/nut/gammudb/nutsms'}

NOSMSD_USE_INJECT = True
NOSMSD_INJECT_PATH = '/usr/bin/gammu-smsd-inject'