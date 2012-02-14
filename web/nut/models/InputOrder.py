#!/usr/bin/env python
# encoding=utf-8

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import post_save, post_delete

from common import ensure_completeness, previous_value_for, NutritionSubReport


class InputOrderReport(models.Model, NutritionSubReport):

    """ Input Order Report """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Input Order Report")
        verbose_name_plural = _(u"Input Order Reports")
        unique_together = ('order_report', 'nut_input')

    order_report = models.ForeignKey('OrderReport',
                                    verbose_name=_(u"Report"),
                                    related_name='input_order_reports')
    nut_input = models.ForeignKey('NUTInput',
                              related_name='inputs_reports',
                              verbose_name=_(u"Inputs"))
    quantity = models.PositiveIntegerField(verbose_name=_(u"Quantity"))

    def __unicode__(self):
        return ugettext(u"%(report)s/%(input)s") \
                        % {'report': self.order_report,
                           'input': self.nut_input}

    def data_fields(self, only_data=True):
        fields = self._meta.get_all_field_names()
        if only_data:
            fields = ['quantity']
        return fields


def post_save_update_parent(sender, instance, **kwargs):
    print('post_save_update_parent %s' % sender)
    parent = previous_value_for(instance, 'order_report')
    if parent != instance.order_report:
        # ensure previous parent is good
        ensure_completeness(parent)
    # ensure parent is good
    ensure_completeness(instance.order_report)


def post_delete_update_parent(sender, instance, **kwargs):
    print('post_delete_update_parent %s' % sender)
    # if cons_report was complete or more, we invalidate.
    ensure_completeness(instance.cons_report)

reversion.register(InputOrderReport)

post_save.connect(post_save_update_parent, sender=InputOrderReport)
post_delete.connect(post_save_update_parent, sender=InputOrderReport)
