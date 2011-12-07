#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext


class NUTInput(models.Model):

    """ Input """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Input")
        verbose_name_plural = _(u"Inputs")

    name = models.CharField(_(u"Name"), max_length=50)
    slug = models.SlugField(_(u"Slug"), max_length=15, primary_key=True)

    def __unicode__(self):
        return self.name
