#!/usr/bin/env python
# encoding=utf-8

import binascii


def generate_user_hash(username, password):
    """ A hash based on username and password provided """

    orig_str = '%s+%s' % (username, password)
    val = orig_str
    for x in range(0, 2000):
        val = str(binascii.crc32(val))
    return val

