#!/usr/bin/env python
# encoding=utf-8

def _(text):
    return text

MODERATE = 'MODERATE' # fr-MAM
SEVERE = 'SEVERE' # fr-NAS
SEVERE_COMP = 'SEVERE_COMP' # fr-NI

DEFAULT_VERSION = 'a'

POPULATIONS = {
    'u59': _(u"6-59 months"),
    'pw': _("Pregnant/B-F Women"),
    'fu12': _(u"Follow-up 1&2"),
    'o59': _(u">59 months"),
    'fu1': _("Follow-up 1"),
    'u6': _(u"<6 months")}

SEXES = {
    'm': _(u"Male"),
    'f': _(u"Female")}


def ntype(code):
    return {
        'mam': MODERATE,
        'sam': SEVERE,
        'samp': SEVERE_COMP}[code]
