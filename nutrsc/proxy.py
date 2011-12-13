#!/usr/bin/env python
# encoding=utf-8

""" Proxy functions accessing either DJ models or alternative for PyQT """


def is_django():
    """ True is running within django """
    try:
        from django.conf import settings
        sid = settings.SITE_ID
        return True
    except:
        return False

# for use elsewhere
IS_DJANGO = is_django()


def proxy_field_name(slug):
    """ Verbose name of a report field slug """
    if IS_DJANGO:
        from nut.models import PECMAMReport
        try:
            return PECMAMReport._meta.get_field(slug).verbose_name
        except AttributeError:
            return slug
    else:
        return slug
