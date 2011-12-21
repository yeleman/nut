#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date

#from django.utils.translation import ugettext as _
from bolibana.reporting.validator import DataValidator
from bolibana.reporting.errors import MissingData, IncorrectReportData
#from bolibana.models import Entity, EntityType, MonthPeriod
#from pnlp_core.models import MalariaReport
#from pnlp_core.data import provider_can, time_cscom_over

from nutrsc.constants import *

def _(text):
    return text


class PECReportValidator(DataValidator):

    """ Monthly Nutrition Routine Report from CSCOM data validation """

    def validate(self):

        def fage(field, age):
            """ value of field for age or zero """
            try:
                return self.get('%s_%s' % (age, field))
            except AttributeError:
                return 0
        for age, aname in POPULATIONS.items():
        
            # ADMISSIONS (IN)
            total_admission1 = sum([fage('hw_b7080_bmi_u18', age),
                                   fage('muac_u120', age),
                                   fage('hw_u70_bmi_u16', age),
                                   fage('muac_u11_muac_u18', age),
                                   fage('oedema', age),
                                   fage('other_hiv', age),
                                   fage('other_tb', age),
                                   fage('other_lwb', age)])
            total_admission2 = sum([fage('new_case', age), fage('relapse', age),
                                   fage('returned', age),
                                   fage('nut_transfered_in', age),
                                   fage('nut_referred_in', age)])
            total_gender = sum([fage('admitted_m', age),
                                fage('admitted_f', age)])

            # TEST IF ADM BY CRITERIA = ADM BY TYPE
            if total_admission1 != total_admission2:
                self.errors.add(u"Total %(age)s admissions by criteria " \
                                u"(%(adm)s) does not match admissions by type " \
                                u"(%(typ)s)" \
                                % {'age': aname,
                                   'adm': total_admission1,
                                   'typ': total_admission2})

            # TEST IF ADM = GENDER B/D
            if total_admission2 != total_gender:
                self.errors.add(u"Total %(age)s admissions (%(adm)s) " \
                                u"does not match Gender break down " \
                                u"total (%(gen)s)" \
                                % {'age': aname,
                                   'adm': total_admission2,
                                   'gen': total_gender})

            # RELEASES (OUT)
            total_out = sum([fage('healed', age),
                             fage('referred_out', age),
                             fage('deceased', age),
                             fage('aborted', age),
                             fage('non_respondant', age),
                             fage('medic_transfered_out', age),
                             fage('nut_transfered_out', age)])

            total_gender = sum([fage('total_out_m', age),
                                fage('total_out_f', age)])

            # TEST IF OUT = GENDER B/D
            if total_out != total_gender:
                self.errors.add(u"Total %(age)s outs (%(out)s) " \
                                u"does not match Gender break down " \
                                u"total (%(gen)s)" \
                                % {'age': aname,
                                   'out': total_out,
                                   'gen': total_gender})

            # TEST OUT <= INITIAL + IN
            for sex, sname in SEXES.items():
                initial = fage('total_beginning_' + sex, age)
                admited = fage('admitted_' + sex, age)
                out = fage('total_out' + sex, age)
                if out > (initial + admited):
                    self.errors.add(u"Total %(age)s %(sex) releases " \
                                u"(%(out)s) is superior to %(sex)s at " \
                                u"beginning + admited." \
                                % {'age': aname,
                                   'out': out,
                                   'sex': sname})
                

class CONSReportValidator(DataValidator):

    def validate(self):

        for inpid in self.get('inputs')():
            try:
                rep = self.get('input_%s' % inpid)
            except:
                self.errors.add(u"Consumption data missing for %s" \
                                % inpid.upper())
                continue

            if not rep.valid():
                self.errors.add(u"Consumption values for %s is incoherent." \
                                % inpid.upper())
            

class ORDERReportValidator(DataValidator):

    def validate(self):

        for inpid in self.get('inputs')():
            try:
                rep = self.get('input_%s' % inpid)
            except:
                self.errors.add(u"Consumption data missing for %s" \
                                % inpid.upper())
                continue
