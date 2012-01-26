#!/usr/bin/env python
# encoding=utf-8

NOSMSD_HANDLER = 'nutclient.sms.nosms_handler'
NOSMSD_GETTEXT = True
NOSMSD_GETTEXT_LOCALE = 'fr_FR.UTF-8'

NOSMSD_DATABASE = {'type': 'MySQL', 'name': 'nutsms'}
NOSMSD_DATABASE_OPTIONS = {'user': 'nutsms', 'passwd': 'nutsms',
                           'host': 'localhost', 'use_unicode': True}
