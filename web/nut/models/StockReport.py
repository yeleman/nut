#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: alou

import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bolibana_reporting.models import Report

class StockReport(Report):
    """ """
    class Meta:
        app_label = 'nut'
        verbose_name = _(u"Stock Report")
        verbose_name_plural = _(u"Stock Reports")

    stock_beginning_of_the_month_plumpy_nut = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_plumpy_nut = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_plumpy_nut = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_plumpy_nut = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_plumpy_nut = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_plumpy_nut = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_milk_f75 = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_milk_f75 = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_milk_f75 = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_milk_f75 = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_milk_f75 = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_milk_f75 = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_milk_f100 = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_milk_f100 = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_milk_f100 = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_milk_f100 = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_milk_f100 = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_milk_f100 = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_resomal = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_resomal = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_resomal = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_resomal = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_resomal = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_resomal = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_csb = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_csb = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_csb = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_csb = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_csb = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_csb = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_UNIMIX = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_UNIMIX = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_UNIMIX = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_UNIMIX = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_UNIMIX = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_UNIMIX = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_oil = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_oil = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_oil = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_oil = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_oil = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_oil = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_sugar = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_sugar = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_sugar = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_sugar = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_sugar = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_sugar = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_misola = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_misola = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_misola = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_misola = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_misola = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_misola = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_mil = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_mil = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_mil = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_mil = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_mil = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_mil = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_small_pea = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_small_pea = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_small_pea = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_small_pea = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_small_pea = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_small_pea = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

    stock_beginning_of_the_month_niebe = models.PositiveIntegerField( \
                                   _(u"Stock beginning of the month"))
    stock_received_niebe = models.PositiveIntegerField( \
                                   _(u"Stock received"))
    stock_used_niebe = models.PositiveIntegerField( \
                                   _(u"Stock used"))
    stock_lost_damaged_niebe = models.PositiveIntegerField( \
                                   _(u"Stock lost/damaged"))
    balance_end_of_the_month_niebe = models.PositiveIntegerField( \
                                   _(u"Balance end of the month"))
    expiry_date_niebe = models.PositiveIntegerField( \
                                   _(u"Expiry date"))

reversion.register(StockReport)
