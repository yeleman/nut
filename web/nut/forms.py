#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from itertools import chain, cycle, islice

from django import forms
from django.forms.models import inlineformset_factory

from models import (PECSAMPReport, PECSAMReport, PECMAMReport, PECOthersReport,
                    InputConsumptionReport, ConsumptionReport, OrderReport,
                    InputOrderReport)


class BasePECForm(object):

    _cache = {}

    suffixes = ()
    part1_suffixes = ('total_beginning_m',
                      'total_beginning_f',
                      'hw_b7080_bmi_u18',
                      'muac_u120',
                      'hw_u70_bmi_u16',
                      'muac_u11_muac_u18',
                      'oedema',
                      'other')

    part2_suffixes = ('new_case',
                      'relapse',
                      'returned',
                      'nut_transfered_in',
                      'nut_referred_in',
                      'admitted_m',
                      'admitted_f',)

    part3_suffixes = ('healed',
                      'referred_out',
                      'deceased',
                      'aborted',
                      'non_respondant',
                      'medic_transfered_out',
                      'nut_transfered_out',
                      'total_out_m',
                      'total_out_f')

    exclude = ('_status', 'type', 'created_by', 'entity', 'period')


    def field_names_matrix(self, prefixes=None, suffixes=None):
        """
            Return a generator that allows you to loop over all field names in the
            form.
        """
        prefixes = prefixes if prefixes is not None else self.prefixes
        suffixes = suffixes if suffixes is not None else self.suffixes

        for prefix in prefixes:
            for suffix in suffixes:
                yield '%s_%s' % (prefix, suffix)


    def fields_matrix(self, prefixes=None, suffixes=None, default=None):
        """
            Return a generator that allows you to loop over all field in the
            form. If the field doesn't exist, return the default value.
        """
        if prefixes == ('all',):
          import ipdb; ipdb.set_trace()
        names = self.field_names_matrix(prefixes, suffixes)
        for name in names:
            try:
                yield self[name]
            except KeyError:
                yield default


    def cycle_fields(self, func, fields, cycle_size, refresh=False):
        """
            Allow to cycle through fields in 3 iterations instead of ones
            This method does just the slicing and the cache, you
            need to pass another method to it so its results get sliced.
        """

        cache_key = self.__class__.__name__ + '.' + func.__name__

        if cache_key not in self._cache or refresh:
            self._cache[cache_key] = (x for x in (
                        islice(fields, cycle_size),
                        islice(fields, cycle_size, cycle_size * 2),
                        islice(fields, cycle_size * 2, cycle_size * 3))
            )

        try:
          return self._cache[cache_key].next()
        except StopIteration:
          return self.cycle_fields(func, fields, cycle_size, True)


    def part1_form_fields(self, prefixes=None, suffixes=None,
                          default=None, refresh=False):
        """
            Return a generator that allow you to loop over all fields of
            the first part of the forms since in the template we had to
            devide the form in 3 tables.


        """
        fields = list(self.fields_matrix(self.prefixes,
                                         self.part1_suffixes,
                                         default))
        return self.cycle_fields(self.part1_form_fields,
                                 fields, len(self.part1_suffixes),
                                 refresh=refresh)



    def part2_form_fields(self, prefixes=None, suffixes=None, default=None,
                          refresh=False):
        """
            Return a generator that allow you to loop over all fields of
            the second part of the forms since in the template we had to
            devide the form in 3 tables.
        """
        fields = list(self.fields_matrix(self.prefixes,
                                         self.part2_suffixes,
                                         default))
        return self.cycle_fields(self.part2_form_fields,
                                 fields, len(self.part2_suffixes),
                                 refresh=refresh)


    def part3_form_fields(self, prefixes=None, suffixes=None, default=None,
                          refresh=False):
        """
            Return a generator that allow you to loop over all fields of
            the third part of the forms since in the template we had to
            devide the form in 3 tables.
        """
        fields = list(self.fields_matrix(self.prefixes,
                                         self.part3_suffixes,
                                         default))
        return self.cycle_fields(self.part3_form_fields,
                                 fields, len(self.part3_suffixes),
                                 refresh=refresh)


    def part_total_fields(self, suffixes, default=None):
        """
            Return a generator that allow you to loop over total fields
        """
        for name in self.field_names_matrix(('all',), suffixes):
            yield getattr(self.instance, name, default)


    def part1_total_fields(self, default=None):
        return self.part_total_fields(self.part1_suffixes, default)


    def part2_total_fields(self, default=None):
        return self.part_total_fields(self.part2_suffixes, default)


    def part3_total_fields(self, default=None):
        return self.part_total_fields(self.part3_suffixes, default)



class PECSAMPReportForm(forms.ModelForm, BasePECForm):

    prefixes = ('u6', 'u59', 'o59')

    class Meta:
        model = PECSAMPReport
        exclude = BasePECForm.exclude


class PECSAMReportForm(forms.ModelForm, BasePECForm):

    prefixes = ('u59', 'o59', 'fu1')

    class Meta:
        model = PECSAMReport
        exclude = BasePECForm.exclude


class PECMAMReportReportForm(forms.ModelForm, BasePECForm):

    prefixes = ('u59', 'pw', 'fu12')

    class Meta:
        model = PECMAMReport
        exclude = BasePECForm.exclude


class PECOthersReportForm(forms.ModelForm):

    class Meta:
        model = PECOthersReport
        fields = ('other_hiv', 'other_tb', 'other_lwb', 'id')



InputConsumptionReportFormSet = inlineformset_factory(ConsumptionReport,
                                                      InputConsumptionReport,
                                                      exclude=('nut_input', 'id'),
                                                      extra=0)


InputOrderReportFormSet = inlineformset_factory(OrderReport,
                                                InputOrderReport,
                                                exclude=('nut_input', 'id'),
                                                extra=0)

