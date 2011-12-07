#!/usr/bin/env python
# encoding=utf-8

from django.utils.translation import ugettext_lazy as _, ugettext

from nutrsc.constants import *

NUT_TYPES = (
    (MODERATE, _(u"MAM")),  # fr-MAM
    (SEVERE, _(u"SAM")),  # fr-NAS
    (SEVERE_COMP, _(u"SAM+")))  # fr-NI


def ensure_completeness(instance):
    """ given a Report instance, test is_complete and adjust _status """
    # if not complete, declass it.
    if not instance.is_complete():
        if instance._status >= instance.STATUS_COMPLETE:
            instance._status = instance.STATUS_INCOMPLETE
            instance.save()
    else:
        if instance._status < instance.STATUS_COMPLETE:
            instance._status = instance.STATUS_COMPLETE
            instance.save()


def previous_value_for(instance, field):
    """ return previous (from reversion) value of a field """
    return getattr(instance, field)


class OverLoadedReport(ValueError):
    pass
