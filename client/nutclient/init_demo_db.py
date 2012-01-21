#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

import sys

from database import *

def main(args):

    drop_tables = True

    if 'keep' in [arg.lower() for arg in args]:
        drop_tables = False

    # drop and create tables
    setup(drop_tables=drop_tables)

    # add demo users:
    reg = User.create(username='rgaudin',
               pwhash='4663950500290933446',
               active=True,
               hc_code=u"ntil",
               hc_name=u"N'Tillit",
               hc_ismam=True,
               hc_issam=True,
               hc_isamp=False)

    anne = User.create(username='anne',
               pwhash='4788589492570640862',
               active=True,
               hc_code=u"lobo",
               hc_name=u"Lobou",
               hc_ismam=True,
               hc_issam=True,
               hc_isamp=False)

if __name__ == '__main__':
    main(sys.argv)