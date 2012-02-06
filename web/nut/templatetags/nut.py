#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import template
from django.template.defaultfilters import stringfilter

from nutrsc.constants import POPULATIONS
from ..models import NUTInput

register = template.Library()


@register.filter(name='err_cat')
@stringfilter
def error_category(error_str):
    try:
        dat = error_str.split('] ')
        cat = dat[0].strip().replace('[', '').replace(']', '').strip()
    except:
        return u""
    if cat in POPULATIONS:
        return POPULATIONS[cat]
    try:
        return NUTInput.objects.get(slug=cat.lower()).name.upper()
    except:
        raise
        return cat.upper()


@register.filter(name='err_text')
@stringfilter
def error_text(error_str):
    try:
        dat = error_str.split('] ')
        return dat[1].strip()
    except:
        return error_str
