#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from bolibana.models import Report
from bolibana.tools.utils import generate_receipt
from nutrsc.constants import *
from nutrsc.mali import *
from InputConsumption import InputConsumptionReport
from common import NUT_TYPES, OverLoadedReport, ensure_completeness


class MAMManager(models.Manager):

    def get_query_set(self):
        return super(MAMManager, self).get_query_set() \
                                      .filter(nut_type=MODERATE)


class SAMManager(models.Manager):

    def get_query_set(self):
        return super(SAMManager, self).get_query_set() \
                                      .filter(nut_type=SEVERE)


class SAMPManager(models.Manager):

    def get_query_set(self):
        return super(SAMPManager, self).get_query_set() \
                                      .filter(nut_type=SEVERE_COMP)


class ConsumptionReport(Report):

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Consumption Report")
        verbose_name_plural = _(u"Consumption Reports")
        unique_together = ('period', 'entity', 'type', 'nut_type')

    nut_type = models.CharField(max_length=20, choices=NUT_TYPES,
                                           verbose_name=_(u"Nutrition Type"))
    version = models.CharField(max_length=2,
                               verbose_name=_(u"Version"),
                               default=DEFAULT_VERSION)

    objects = models.Manager()
    mam = MAMManager()
    sam = SAMManager()
    samp = SAMPManager()

    def is_complete(self):
        print('is_complete %s' % self)
        for code in CONSUMPTION_TABLE[self.nut_type][self.version]:
            if not self.has(code):
                return False
        return True

    def is_overloaded(self):
        print('is_overloaded %s' % self)
        for inpr in InputConsumptionReport.objects.filter(cons_report=self):
            if not inpr.nut_input.slug \
               in CONSUMPTION_TABLE[self.nut_type][self.version]:
                return True
        return False

    def has(self, code):
        """ whether there is a matching input report for code """
        return InputConsumptionReport.objects.filter(cons_report=self,
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
        instance.receipt = generate_receipt(instance, fix='C',
                                            add_random=True)
        instance.save()
    ensure_completeness(instance)

pre_save.connect(pre_save_report, sender=ConsumptionReport)
post_save.connect(post_save_report, sender=ConsumptionReport)
