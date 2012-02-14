#!/usr/bin/env python
# encoding=utf_8
# maintainer: rgaudin

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import pre_save, post_save

from nutrsc.constants import MODERATE, SEVERE, SEVERE_COMP
from nutrsc.mali import CONSUMPTION_TABLE, DEFAULT_VERSION
from NutritionReport import NutritionReport
from InputConsumption import InputConsumptionReport
from common import (NUT_TYPES, OverLoadedReport,
                    ensure_completeness, InputsDependantReport,
                    NutritionSubReport)


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


class ConsumptionReport(models.Model, InputsDependantReport, NutritionSubReport):

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Consumption Report")
        verbose_name_plural = _(u"Consumption Reports")
        unique_together = ('nut_type', 'nut_report')

    nut_type = models.CharField(max_length=20, choices=NUT_TYPES,
                                           verbose_name=_(u"Nutrition Type"))
    version = models.CharField(max_length=2,
                               verbose_name=_(u"Version"),
                               default=DEFAULT_VERSION)

    nut_report = models.ForeignKey(NutritionReport,
                                   related_name='cons_reports')

    objects = models.Manager()
    mam = MAMManager()
    sam = SAMManager()
    samp = SAMPManager()

    def __unicode__(self):
        return ugettext(u"%(entity)s/%(cap)s/%(period)s") \
                        % {'entity': self.nut_report.entity, \
                           'period': self.nut_report.period,
                           'cap': self.nut_type.upper()}

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

    def icr(self, code):
        return self.input_cons_reports.get(nut_input__slug=code)


def pre_save_report(sender, instance, **kwargs):
    # check that version exist
    if not instance.version in CONSUMPTION_TABLE[instance.nut_type]:
        raise ValueError(u"Version %s does not exist for %s"
                         % (instance.version, instance.nut_type))
    # prevent updating to a wrong dest
    if instance.is_overloaded():
        raise OverLoadedReport(u"Input reports not for %s"
                               % instance.nut_type)


def post_save_report(sender, instance, **kwargs):
    ensure_completeness(instance)

reversion.register(ConsumptionReport)
pre_save.connect(pre_save_report, sender=ConsumptionReport)
post_save.connect(post_save_report, sender=ConsumptionReport)
