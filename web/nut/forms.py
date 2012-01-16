#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from itertools import chain, cycle, islice

from django import forms
from django.forms.models import inlineformset_factory

from models import (PECSAMPReport, PECSAMReport, PECMAMReport, PECOthersReport,
                    InputConsumptionReport, ConsumptionReport)



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
                      # 'healed',
                      # 'referred_out',
                      # 'deceased',
                      # 'aborted',
                      # 'non_respondant',
                      # 'medic_transfered_out',
                      # 'nut_transfered_out',
                      # 'total_out_m',
                      # 'total_out_f')


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
        names = self.field_names_matrix(prefixes, suffixes)
        for name in names:
            try:
                yield self[name]
            except KeyError:
                yield default


    def part1_form_fields(self, prefixes=None, suffixes=None,
                          default=None, refresh=False):
        """
            Return a generator that allow you to loop over all field of
            the first part of the forms since in the template we had to
            devide the form in two tables.

            The generator is cached to avoid having to set a variable
            which is hard to do in a template. We use itertools
            functions to make the fields comme in 3 rounds, in a cycle.
        """
        cache_key = self.__class__.__name__ + '.part1_form_fields'
        if cache_key not in self._cache or refresh:
            fields = list(self.fields_matrix(self.prefixes,
                                             self.part1_suffixes,
                                             default))
            l = len(self.part1_suffixes)

            self._cache[cache_key] = (x for x in (islice(fields, l),
                                                  islice(fields, l, l * 2),
                                                  islice(fields, l * 2, l * 3)))

        try:
          return self._cache[cache_key].next()
        except StopIteration:
          return self.part1_form_fields(prefixes, suffixes, default, True)


    def part2_form_fields(self, prefixes=None, suffixes=None, default=None,
                          refresh=False):
        """
            Return a generator that allow you to loop over all field of
            the second part of the forms since in the template we had to
            devide the form in two tables.

            The generator is cached to avoid having to set a variable
            which is hard to do in a template. To avoid problem with
            generator exhaustion, we wrap the generator into itertoos.cycle
        """
        cache_key = self.__class__ .__name__+ '.part2_form_fields'
        if cache_key not in self._cache or refresh:
            fields = list(self.fields_matrix(self.prefixes,
                                             self.part2_suffixes,
                                             default))
            l = len(self.part2_suffixes)
            self._cache[cache_key] = (x for x in (islice(fields, l),
                                                  islice(fields, l, l * 2),
                                                  islice(fields, l * 2, l * 3)))
        try:
          return self._cache[cache_key].next()
        except StopIteration:
          return self.part2_form_fields(prefixes, suffixes, default, True)



class PECSAMPReportForm(forms.ModelForm, BasePECForm):

    prefixes = ('u6', 'u59', 'o59')

    class Meta:
        model = PECSAMPReport


class PECSAMReportForm(forms.ModelForm, BasePECForm):

    prefixes = ('u59', 'o59', 'fu1')

    class Meta:
        model = PECSAMReport


class PECMAMReportReportForm(forms.ModelForm, BasePECForm):

    prefixes = ('u59', 'pw', 'fu12')

    class Meta:
        model = PECMAMReport


class PECOthersReportForm(forms.ModelForm):

    class Meta:
        model = PECOthersReport
        fields = ('other_hiv', 'other_tb', 'other_lwb')


InputConsumptionReportFormSet = inlineformset_factory(ConsumptionReport,
                                                      InputConsumptionReport,
                                                      extra=0)

