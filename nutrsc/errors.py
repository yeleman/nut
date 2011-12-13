#!/usr/bin/env python
# encoding=utf-8

def _(text):
    return text

LOGIN_ERRORS = {
    'NO_ACC': _(u"Username does not exist."),
    'BAD_PASS': _(u"Password does not match Username."),
    'ACC_DIS': _(u"Account disabled."),
    'OTHER': _(u"Unknown Error.")
}

REPORT_ERRORS = {
    'NO_ACC': _(u"Username does not exist."),
    'NO_PERM': _(u"User is not allowed to report for that HC."),
    'BAD_PASS': _(u"Password does not match Username."),
    'ACC_DIS': _(u"Account disabled."),
    'BAD_FORM': _(u"Malformed SMS (sections)."),
    'BAD_FORM_PEC': _(u"Malformed SMS (PEC)."),
    'BAD_FORM_INFO': _(u"Malformed SMS (infos)."),
    'BAD_FORM_PERIOD': _(u"Malformed SMS (period)."),
    'BAD_PERIOD': _(u"Unable to accept data for that period now."),
    'NOT_ENT': _(u"Account is not tied to any Health Center."),
    'BAD_CAP': _(u"Reports don't match HC capabilities. Try to log-in again."),
    'PEC': _(u"PEC Report Data Invalid"),
    'PEC_MAM': _(u"PEC MAM Report Data Invalid"),
    'PEC_SAM': _(u"PEC SAM Report Data Invalid"),
    'PEC_SAMP': _(u"PEC SAM+ Report Data Invalid"),
    'SRV': _(u"A technical error occured. Please contact Tech Support."),
    'UNIQ': _(u"There is already a report for that period at your HC."),
}
