#!/usr/bin/env python
# encoding=utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save, post_delete

from nutrsc.exceptions import IncoherentValue
from common import ensure_completeness, previous_value_for


class InputConsumptionReport(models.Model):

    """ CONSUMPTION Report """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Input Consumption Report")
        verbose_name_plural = _(u"Input Consumption Reports")
        unique_together = ('cons_report', 'nut_input')

    cons_report = models.ForeignKey('ConsumptionReport',
                                    verbose_name=_(u"Report"))
    nut_input = models.ForeignKey('NUTInput',
                              related_name='nutinput_reports',
                              verbose_name=_(u"Inputs"))
    initial = models.PositiveIntegerField(verbose_name=_(u"Initial Stock"))
    received = models.PositiveIntegerField(verbose_name=_(u"Quantity" \
                                                          u"Received"))
    used = models.PositiveIntegerField(verbose_name=_(u"Quantity used"))
    lost = models.PositiveIntegerField(verbose_name=_(u"Quantity lost"))

    def __unicode__(self):
        return ugettext(u"%(report)s/%(input)s") \
                        % {'report': self.cons_report,
                           'input': self.nut_input}

    @property
    def consumed(self):
        return self.used + self.lost

    @property
    def possessed(self):
        return self.initial + self.received

    @property
    def left(self):
        return self.possessed - self.consumed


def check_stock_integrity(sender, instance, **kwargs):
    print('check_stock_integrity %s' % sender)
    """ check that usage of stock is coherent """
    if instance.consumed > instance.possessed:
        raise IncoherentValue(ugettext(u"Used + Lost quantities can't "\
                                       u"exceed Initial + Received"))


def post_save_update_parent(sender, instance, **kwargs):
    print('post_save_update_parent %s' % sender)
    parent = previous_value_for(instance, 'cons_report')
    if parent != instance.cons_report:
        # ensure previous parent is good
        ensure_completeness(parent)
    # ensure parent is good
    ensure_completeness(instance.cons_report)


def post_delete_update_parent(sender, instance, **kwargs):
    print('post_delete_update_parent %s' % sender)
    # if cons_report was complete or more, we invalidate.
    ensure_completeness(instance.cons_report)

pre_save.connect(check_stock_integrity, sender=InputConsumptionReport)
post_save.connect(post_save_update_parent, sender=InputConsumptionReport)
post_delete.connect(post_save_update_parent, sender=InputConsumptionReport)
