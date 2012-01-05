#!/usr/bin/env python
# encoding=utf-8

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from NUTReport import NUTReport, pre_save_report, post_save_report


class PECOthersReport(NUTReport):

    """ PEC Others Data """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"PEC Others Report")
        verbose_name_plural = _(u"PEC Others Reports")
        unique_together = ('period', 'entity', 'type')

    other_hiv = models.PositiveIntegerField(_(u"Others living with HIV"))
    other_tb = models.PositiveIntegerField(_(u"Others having TB"))
    other_lwb = models.PositiveIntegerField(_(u"Others with Low Weight " \
                                              u"at Birth"))

    # Aggregation
    sources = models.ManyToManyField('PECOthersReport', \
                                     verbose_name=_(u"Sources"), \
                                     blank=True, null=True)

    @property
    def total(self):
        return sum([self.other_lwb, self.other_tb, self.other_hiv])

reversion.register(PECOthersReport)

pre_save.connect(pre_save_report, sender=PECOthersReport)
post_save.connect(post_save_report, sender=PECOthersReport)