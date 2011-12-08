#!/usr/bin/env python
# encoding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save, post_delete

from bolibana.models import Entity


class NUTEntity(Entity):

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Entity")
        verbose_name_plural = _(u"Entities")

    is_mam = models.BooleanField(verbose_name=_(u"is MAM?"))
    is_sam = models.BooleanField(verbose_name=_(u"is SAM?"))
    is_samp = models.BooleanField(verbose_name=_(u"is SAM+?"))

