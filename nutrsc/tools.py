#!/usr/bin/env python
# encoding=utf-8


def generate_user_hash(username, password):
    """ A hash based on username and password provided """

    return hash('%s+%s' % (username, password))

