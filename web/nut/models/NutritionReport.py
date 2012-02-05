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

    @property
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

    def sum_pec_fields(self, field):
        return sum([getattr(r, field, 0) for r in self.pec_reports()])

    @property
    def sum_all_other(self):
        return self.sum_pec_fields('all_other')

    @property
    def sum_all_total_out(self):
        return self.sum_pec_fields('all_total_out')

    @property
    def sum_all_healed(self):
        return self.sum_pec_fields('all_healed')

    @property
    def sum_all_aborted(self):
        return self.sum_pec_fields('all_aborted')

    @property
    def sum_all_deceased(self):
        return self.sum_pec_fields('all_deceased')

    @property
    def sum_all_non_respondant(self):
        return self.sum_pec_fields('all_non_respondant')

    @property
    def statistics(self):
        def rate(numerator, denominator):
            return float(numerator) / float(denominator)
        data = {'nb_out': self.sum_all_total_out,
                'nb_healed': self.sum_all_healed,
                'nb_aborted': self.sum_all_aborted,
                'nb_deceased': self.sum_all_deceased,
                'nb_non_respondant': self.sum_all_non_respondant}
        if self.type == self.TYPE_SOURCE:
            data['nb_missing_reports'] = 0
            data['nb_expected_reports'] = 1
        else:
            data['nb_expected_reports'] = len(self.entity.get_siblings())
            data['nb_missing_reports'] = data['nb_expected_reports'] - self.sources.count()
            
        data['rate_healed'] = rate(data['nb_healed'], data['nb_out'])
        data['rate_aborted'] = rate(data['nb_aborted'], data['nb_out'])
        data['rate_deceased'] = rate(data['nb_deceased'], data['nb_out'])
        data['rate_non_respondant'] = rate(data['nb_non_respondant'], data['nb_out'])
        data['rate_reports'] = rate(data['nb_missing_reports'],
                                    data['nb_expected_reports'])
        return data

    @property
    def sum_all_total_beginning(self):
        return self.sum_pec_fields('all_total_beginning')

    @property
    def sum_all_total_beginning_m(self):
        return self.sum_pec_fields('all_total_beginning_m')

    @property
    def sum_all_total_beginning_f(self):
        return self.sum_pec_fields('all_total_beginning_f')

    @property
    def sum_all_total_admitted(self):
        return self.sum_pec_fields('all_total_admitted')

    @property
    def sum_all_hw_b7080_bmi_u18(self):
        return self.sum_pec_fields('all_hw_b7080_bmi_u18')

    @property
    def sum_all_muac_u120(self):
        return self.sum_pec_fields('all_muac_u120')

    @property
    def sum_all_hw_u70_bmi_u16(self):
        return self.sum_pec_fields('all_hw_u70_bmi_u16')

    @property
    def sum_all_muac_u11_muac_u18(self):
        return self.sum_pec_fields('all_muac_u11_muac_u18')

    @property
    def sum_all_oedema(self):
        return self.sum_pec_fields('all_oedema')

    @property
    def sum_all_new_case(self):
        return self.sum_pec_fields('all_new_case')

    @property
    def sum_all_relapse(self):
        return self.sum_pec_fields('all_relapse')

    @property
    def sum_all_returned(self):
        return self.sum_pec_fields('all_returned')

    @property
    def sum_all_nut_transfered_in(self):
        return self.sum_pec_fields('all_nut_transfered_in')

    @property
    def sum_all_nut_referred_in(self):
        return self.sum_pec_fields('all_nut_referred_in')

    @property
    def sum_all_total_admitted_m(self):
        return self.sum_pec_fields('all_total_admitted_m')

    @property
    def sum_all_total_admitted_f(self):
        return self.sum_pec_fields('all_total_admitted_f')

    @property
    def sum_all_refered_out(self):
        return self.sum_pec_fields('all_refered_out')

    @property
    def sum_all_medic_transfered_out(self):
        return self.sum_pec_fields('all_total_medic_transfered_out')

    @property
    def sum_all_nut_transfered_out(self):
        return self.sum_pec_fields('all_total_nut_transfered_out')

    @property
    def sum_all_total_out_m(self):
        return self.sum_pec_fields('all_total_out_m')

    @property
    def sum_all_total_out_f(self):
        return self.sum_pec_fields('all_total_out_f')

    @property
    def sum_all_total_end(self):
        return self.sum_pec_fields('all_total_end')

    @property
    def sum_all_total_end_m(self):
        return self.sum_pec_fields('all_total_end_m')

    @property
    def sum_all_total_end_f(self):
        return self.sum_pec_fields('all_total_end_f')

pre_save.connect(pre_save_report, sender=NutritionReport)
post_save.connect(post_save_report, sender=NutritionReport)

reversion.register(NutritionReport)
