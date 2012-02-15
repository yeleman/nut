#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import reversion
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _

from nutrsc.constants import MODERATE, SEVERE, SEVERE_COMP
from bolibana.models.Report import Report, pre_save_report, post_save_report
from bolibana.tools.utils import generate_receipt
from bolibana.models import MonthPeriod


class NutritionReport(Report):

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Nutrition Report")
        verbose_name_plural = _(u"Nutrition Reports")
        unique_together = ('period', 'entity', 'type')

    is_mam = models.BooleanField(verbose_name=_(u"is MAM?"))
    is_sam = models.BooleanField(verbose_name=_(u"is SAM?"))
    is_samp = models.BooleanField(verbose_name=_(u"is SAM+?"))

    sources = models.ManyToManyField('NutritionReport',
                                     verbose_name=_(u"Sources"),
                                     blank=True, null=True)


    @classmethod
    def start(cls, period, entity, author, *args, **kwargs):
        """ create a blank report filling all non-required fields """
        report = cls(period=period, entity=entity, created_by=author, \
                     modified_by=author, _status=cls.STATUS_UNSAVED,
                     is_mam=entity.is_mam, is_sam=entity.is_sam,
                     is_samp=entity.is_samp)
        for arg, value in kwargs.items():
            try:
                setattr(report, arg, value)
            except AttributeError:
                pass
        return report

    def delete_safe(self):
        for report in self.tied_reports():
            report.delete_safe()
        self.delete()

    def tied_reports(self):
        return self.pec_reports() \
               + self.cons_reports() \
               + self.order_reports() \
               + [self.pec_other_report]

    @property
    def mperiod(self):
        """ casted period to MonthPeriod """
        mp = self.period
        mp.__class__ = MonthPeriod
        return mp

    @classmethod
    def generate_receipt(cls, instance):
        return generate_receipt(instance, fix='N', add_random=True)

    def caps(self):
        caps = []
        for cap in [SEVERE_COMP, SEVERE, MODERATE]:
            if getattr(self, 'is_%s' % cap):
                caps.append(cap)
        return caps

    def get_reports(self, type_):
        reports = []
        for cap in self.caps():
            report = getattr(self, 'get_%s_report' % type_)(cap)
            if report:
                reports.append(report)
        return reports

    def pec_reports(self):
        return self.get_reports('pec')

    def cons_reports(self):
        return self.get_reports('cons')

    def order_reports(self):
        return self.get_reports('order')

    def get_pec_report(self, cap):
        try:
            return getattr(self, 'pec_%s_reports' % cap.lower()).get()
        except:
            return None

    def get_cons_report(self, cap):
        try:
            return self.all_cons_reports.get(nut_type=cap)
        except:
            return None

    def get_order_report(self, cap):
        try:
            return self.all_order_reports.get(nut_type=cap)
        except:
            return None

    @property
    def pec_mam_report(self):
        return self.get_pec_report(MODERATE)

    @property
    def pec_sam_report(self):
        return self.get_pec_report(SEVERE)

    def pec_samp_report(self):
        return self.get_pec_report(SEVERE_COMP)

    @property
    def cons_mam_report(self):
        return self.get_cons_report(MODERATE)

    @property
    def cons_sam_report(self):
        return self.get_cons_report(SEVERE)

    @property
    def cons_samp_report(self):
        return self.get_cons_report(SEVERE_COMP)

    @property
    def order_mam_report(self):
        return self.get_order_report(MODERATE)

    @property
    def order_sam_report(self):
        return self.get_order_report(SEVERE)

    @property
    def order_samp_report(self):
        return self.get_order_report(SEVERE_COMP)

    @property
    def pec_other_report(self):
        return self.pec_other_reports.get(nut_report=self)

    def is_dirty(self):
        return False

    def is_complete(self):
        return True

    @property
    def sum_all_other(self):
        return sum([r.all_other for r in self.pec_reports()])


pre_save.connect(pre_save_report, sender=NutritionReport)
post_save.connect(post_save_report, sender=NutritionReport)

reversion.register(NutritionReport)
