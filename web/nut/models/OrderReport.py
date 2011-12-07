#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from bolibana.models import EntityType, Entity, Report, MonthPeriod
from bolibana.tools.utils import generate_receipt

from InputOrder import InputOrderReport
from common import ensure_completeness
from nutrsc.constants import *
from nutrsc.mali import *


class OrderReport(Report):

    NUT_TYPES = (
        (MODERATE, _(u"MAM")),  # fr-MAM
        (SEVERE, _(u"SAM")),  # fr-NAS
        (SEVERE_COMP, _(u"SAM+")))  # fr-NI

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Order Report")
        verbose_name_plural = _(u"Order Reports")
        unique_together = ('period', 'entity', 'type', 'nut_type')

    nut_type = models.CharField(max_length=20, choices=NUT_TYPES,
                                           verbose_name=_(u"Nutrition Type"))
    version = models.CharField(max_length=2,
                               verbose_name=_(u"Version"),
                               default=DEFAULT_VERSION)

    def is_complete(self):
        print('is_complete %s' % self)
        for code in CONSUMPTION_TABLE[self.nut_type][self.version]:
            if not self.has(code):
                return False
        return True

    def is_overloaded(self):
        print('is_overloaded %s' % self)
        for inpr in InputOrderReport.objects.filter(order_report=self):
            if not inpr.nut_input.slug \
               in CONSUMPTION_TABLE[self.nut_type][self.version]:
                return True
        return False

    def has(self, code):
        """ whether there is a matching input report for code """
        return InputOrderReport.objects.filter(order_report=self,
                                               nut_input__slug=code) \
                                       .count() == 1


def pre_save_report(sender, instance, **kwargs):
    print('pre_save_report %s' % sender)
    """ change _status property of Report on save() at creation """
    if instance._status == instance.STATUS_UNSAVED:
        instance._status = instance.STATUS_CLOSED
    # following will allow us to detect failure in registration
    if not instance.receipt:
        instance.receipt = 'NO_RECEIPT'
    # check that version exist
    if not instance.version in CONSUMPTION_TABLE[instance.nut_type]:
        raise ValueError(u"Version %s does not exist for %s" \
                         % (instance.version, instance.nut_type))
    # prevent updating to a wrong dest
    if instance.is_overloaded():
        raise OverLoadedReport(u"Input reports not for %s" \
                               % instance.nut_type)


def post_save_report(sender, instance, **kwargs):
    print('post_save_report %s' % sender)
    """ generates the receipt """
    if instance.receipt == 'NO_RECEIPT':
        instance.receipt = generate_receipt(instance, fix='O',
                                            add_random=True)
        instance.save()
    ensure_completeness(instance)

pre_save.connect(pre_save_report, sender=OrderReport)
post_save.connect(post_save_report, sender=OrderReport)