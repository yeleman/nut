#!/usr/bin/env python
# encoding=utf-8

MODERATE = 'mam' # fr-MAM
SEVERE = 'sam' # fr-NAS
SEVERE_COMP = 'samp' # fr-NI

DEFAULT_VERSION = 'a'

POPULATIONS = {
    'u59': u"6-59 mois",
    'pw': u"Femmes enceintes",
    'fu12': u"Suivi 1&2",
    'o59': u">59 mois",
    'fu1': "Suivi URENI 1",
    'u6': u"<6 mois"}

POPULATIONS_CAP = {
    MODERATE: ['u59', 'pw', 'fu12'],
    SEVERE: ['u59', 'o59', 'fu1'],
    SEVERE_COMP: ['u6', 'u59', 'o59']}

SEXES = {
    'm': u"Homme",
    'f': u"Femme"}


def ntype(code):
    return {
        'mam': MODERATE,
        'sam': SEVERE,
        'samp': SEVERE_COMP}[code]