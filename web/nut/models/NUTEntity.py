#!/usr/bin/env python
# encoding=utf-8

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _

from nutrsc.constants import MODERATE, SEVERE, SEVERE_COMP
from bolibana.models import Entity


class NUTEntity(Entity):

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Entity")
        verbose_name_plural = _(u"Entities")

    is_mam = models.BooleanField(verbose_name=_(u"is MAM?"))
    is_sam = models.BooleanField(verbose_name=_(u"is SAM?"))
    is_samp = models.BooleanField(verbose_name=_(u"is SAM+?"))

    def caps(self):
        caps = []
        for cap in [SEVERE_COMP, SEVERE, MODERATE]:
            if getattr(self, 'is_%s' % cap):
                caps.append(cap)
        return caps

reversion.register(NUTEntity)