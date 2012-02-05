#!/usr/bin/env python
# encoding=utf-8

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from common import NutritionSubReport
from NutritionReport import NutritionReport


class PECOthersReport(models.Model, NutritionSubReport):

    """ PEC Others Data """

    class Meta:
        app_label = 'nut'
        verbose_name = _(u"PEC Others Report")
        verbose_name_plural = _(u"PEC Others Reports")

    other_hiv = models.PositiveIntegerField(u"Autres - PVVIH")
    other_tb = models.PositiveIntegerField(u"Autres - Tuberculose")
    other_lwb = models.PositiveIntegerField(u"Autres - Petits poids "
                                            u"de naissance")

    nut_report = models.ForeignKey(NutritionReport,
                                   related_name='pec_other_reports',
                                   unique=True)

    @property
    def total(self):
        return sum([self.other_lwb, self.other_tb, self.other_hiv])

    def __unicode__(self):
        if not getattr(self, 'id', None):
            return self.__class__.__name__
        return ugettext(u"%(entity)s/%(period)s") \
                        % {'entity': self.nut_report.entity, \
                           'period': self.nut_report.period}

    def data_fields(self, only_data=True):
        fields = self._meta.get_all_field_names()
        if only_data:
            fields = [x for x in fields if x.startswith('other')]
        return fields

reversion.register(PECOthersReport)