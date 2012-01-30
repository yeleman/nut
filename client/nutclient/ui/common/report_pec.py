#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from nutrsc.mali import *
from table import *
from report import *
from elements import *


class PECReportTable(ReportFlexibleTable):

    report_type = 'pec'

    def __init__(self, parent, report, page):
        super(PECReportTable, self).__init__(parent, report, page)

        #self.report_fields = []
        self.report_field_dict = []
        self.vheaders = self.build_vheaders()

    @property
    def report_fields(self):
        return [fd.get('n') for fd in self.report_field_dict]

    def load_data(self, readonly=False):
        self.data = []
        cols = len(self.hheaders)
        def blank_line():
            return [BlankCell(self) for x in range(0, cols)]

        for cap in self.report.caps():
            
            # add a blank line for the section header
            self.data.append(blank_line())

            cap_report = getattr(self.report, 'get_%s_report' % self.report_type.lower())(cap)

            for age in POPULATIONS_CAP[cap_report.CAP]:
                cells = []
                for fdata in self.report_field_dict:
                    fname = fdata.get('n')
                    field = fdata.get('f')
                    readonly = fdata.get('ro')

                    # auto-column, always displayed
                    if not fname:
                        cells.append(field(self, cap_report, None, age))
                    else:
                        afname = '%s_%s' % (age, fname)
                        # report doesn't have this field
                        if not hasattr(cap_report, afname):
                            cells.append(BlankCell(self))
                        else:
                            if not field:
                                field = ReportValueEditItem
                            cells.append(field(self, cap_report, afname, age))
                self.data.append(cells)
        # add total line
        self.data.append([ColumnSumItem(self, None, None) for x in range(0, cols)])

    def focus_on_data(self):
        for rowid in xrange(0, self.rowCount()):
            for colid in xrange(0, self.columnCount()):
                item = self.item(rowid, colid)
                if item.flags().__and__(Qt.ItemIsSelectable):
                    self.setCurrentCell(rowid, colid)
                    return

    def validate(self):
        return True

    def build_vheaders(self):
        vheaders = []
        for cap in self.report.caps():
            vheaders.append(HC_CAPS[cap])
            vheaders += list(POPULATIONS[age] for age in POPULATIONS_CAP[cap])
        return vheaders

    def apply_resize_rules(self):
        index = 0
        for cap in self.report.caps():
            self.setVerticalHeaderItem(index, TableSectionHead(HC_CAPS[cap]))
            index += 4
        self.setVerticalHeaderItem(index, TableSectionHead(u"TOTAL"))
        super(PECReportTable, self).apply_resize_rules()
        self.focus_on_data()

    def save(self):
        if not self.validate():
            return False
    
        for cap in CAPS.keys():
            report = self.report.get_pec_report(cap)
            if not report:
                # no report for that cap.
                continue
            for age, agestr in report.CATEGORIES:
                for fdata in self.report_field_dict:
                    fname = fdata.get('n')
                    readonly = fdata.get('ro')
                    # skip None fields (delimiters) or read-only ones
                    if not fname or readonly:
                        continue
                    # skip fields not on that age cat
                    if not hasattr(report, '%s_%s' % (age, fname)):
                        continue
                    setattr(report, '%s_%s' % (age, fname), self.get_field_value('%s_%s' % (age, fname), report.CAP))
            report.save()
        return True


class PECADMCRITReportTable(PECReportTable):

    def __init__(self, parent, report, page):
        super(PECADMCRITReportTable, self).__init__(parent, report, page)
        self.hheaders = [u"Total au\ndébut du\nmois",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF",
                         u"P/T≥70\n<80%\nIMC<18",
                         u"PB<120\nou\nPB<210",
                         u"P/T<70%\nou\nIMC<16",
                         u"PB<11cm\nou\nPB<18cm",
                         u"Œdeme", u"Autre", "TOTAL\nADMIS"]

        self.report_field_dict = [{'f': ReportAutoBeginingTotal}]

        if self.report.has_previous_validated():
            self.report_field_dict += [{'n': 'total_beginning_m',
                                        'f': ReportAutoPrevious},
                                       {'n': 'total_beginning_f',
                                        'f': ReportAutoPrevious}]
        else:
            self.report_field_dict += [{'n': 'total_beginning_m',},
                                       {'n': 'total_beginning_f'}]

        self.report_field_dict += [{'n': 'hw_b7080_bmi_u18'},
                                   {'n': 'muac_u120'},
                                   {'n': 'hw_u70_bmi_u16'},
                                   {'n': 'muac_u11_muac_u18'},
                                   {'n': 'oedema'},
                                   {'n': 'other'},
                                   {'f': ReportAutoAdmissionTotal}]

    def validate(self):

        # nothing to validate. All by-criteria admitted must be equal to
        # the total on next stage though.
        return True


class PECADMTYPReportTable(PECReportTable):

    def __init__(self, parent, report, page):
        super(PECADMTYPReportTable, self).__init__(parent, report, page)

        self.hheaders = [u"Total au\ndébut du\nmois",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF",
                         u"Nouv.\nCas",
                         u"Rechute",
                         u"Réadm.",
                         u"Transf.\nnutri.",
                         u"Réf.\nnutri.",
                         u"TOTAL\nADMIS",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF"]

        self.report_field_dict = [{'f': ReportAutoBeginingTotal},
                                  {'n': 'total_beginning_m', 'f': ReportAutoCustomField, 'ro': True},
                                  {'n': 'total_beginning_f', 'f': ReportAutoCustomField, 'ro': True},
                                  {'n': 'new_case'},
                                  {'n': 'relapse'},
                                  {'n': 'returned'},
                                  {'n': 'nut_transfered_in'},
                                  {'n': 'nut_referred_in'},
                                  {'f': ReportMultipleAutoAdmissionTotal},
                                  {'n': 'admitted_m'},
                                  {'n': 'admitted_f'}]

    def validate(self):

        # sum of all criterias must equal the (read only) total admissions
        # AND the sum of admitted Male/Female

        def type_value(cap, age):
            return sum([self.get_field_value('%s_%s' % (age, fname), cap)
                    for fname in ('new_case',
                                  'relapse',
                                  'returned',
                                  'nut_transfered_in',
                                  'nut_referred_in')])


        def criteria_value(cap, age):
            return sum([getattr(self.report.get_pec_report(cap), '%s_%s' % (age, fname), 0)
                        for fname in ('hw_b7080_bmi_u18',
                                      'muac_u120',
                                      'hw_u70_bmi_u16',
                                      'muac_u11_muac_u18',
                                      'oedema',
                                      'other')])

        def gender_value(cap, age):
            return sum([self.get_field_value('%s_%s' % (age, fname), cap)
                        for fname in ('admitted_m',
                                      'admitted_f')])

        for cap in self.report.caps():
            for age in POPULATIONS_CAP[cap]:
        
                tv = type_value(cap, age)
                cv = criteria_value(cap, age)
                gv = gender_value(cap, age)
                
                if not tv == cv or not tv == gv:
                    return False
        return True


class PECOUTReportTable(PECReportTable):

    def __init__(self, parent, report, page):
        super(PECOUTReportTable, self).__init__(parent, report, page)

        self.hheaders = [u"Guéris",
                         u"Référés",
                         u"Décès",
                         u"Abandon",
                         u"Non\nrepond.",
                         u"Transf.\nmédical",
                         u"Transf.\nnutri.",
                         u"TOTAL\nSORTIS",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF"]

        self.report_field_dict = [{'n': 'healed'},
                                  {'n': 'referred_out'},
                                  {'n': 'deceased'},
                                  {'n': 'aborted'},
                                  {'n': 'non_respondant'},
                                  {'n': 'medic_transfered_out'},
                                  {'n': 'nut_transfered_out'},
                                  {'f': ReportAutoOutTotal},
                                  {'n': 'total_out_m'},
                                  {'n': 'total_out_f'}]

    def validate(self):

        # sum of all out must equal gender BK.
        # sum of outs must not exceed BEG + ADM
        total_out_colid = 7
        for cap in self.report.caps():
            for rowid in self.rows_for_cap(cap):
                total_out = self.item(rowid, total_out_colid)
                if isinstance(total_out, BlankCell):
                    continue
                if total_out.is_global_invalid() \
                   or total_out.is_gender_mismatch():
                    return False

        return True


class PECRECAPReportTable(PECReportTable):

    def __init__(self, parent, report, page):
        super(PECRECAPReportTable, self).__init__(parent, report, page)

        self.hheaders = [u"Total au\ndébut du\nmois",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF",
                         u"TOTAL\nADMIS",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF",
                         u"TOTAL\nSORTIS",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF",
                         u"TOTAL\nRESTANTS",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF"]

        self.report_field_dict = [{'n': 'total_beginning', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_beginning_m', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_beginning_f', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'admitted', 'f': ReportAutoAdmisssionValueRO, 'ro': True},
                                  {'n': 'admitted_m', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'admitted_f', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_out', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_out_m', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_out_f', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_end', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_end_m', 'f': ReportAutoValueRO, 'ro': True},
                                  {'n': 'total_end_f', 'f': ReportAutoValueRO, 'ro': True}]

    def validate(self):
        # retrieve LWB, TB, HIV from outer widget and check those against
        # all Others PEC values
        hiv_field = self.parentWidget().others_hiv_field
        tb_field = self.parentWidget().others_tb_field
        lwb_field = self.parentWidget().others_lwb_field

        return (sum([hiv_field.value, tb_field.value, lwb_field.value])
               == self.report.sum_all_others)

    def save(self):
        if not self.validate():
            return False
    
        # nothing to save on that table (it's a recap)
        # we'll save the Others fields (not on table though)
        for other_field in ('hiv', 'tb', 'lwb'):
            field = getattr(self.parentWidget(), 'others_%s_field' % other_field)
            setattr(self.report, 'others_%s' % other_field, field.value)
        self.report.save()
        return True


class PECInstructions(QtGui.QGroupBox):

    def __init__(self, parent, table, report, page):
        super(PECInstructions, self).__init__(u"Instructions", parent)

        self._parent = parent
        self.table = table
        self.report = table
        self.page = page

        self.elems = []


        self.default_text = (u"Les cases oranges correspondent à "
            u"des valeurs différentes de 15% des prévisions.\n"
            u"Les valeurs rouges sont des erreurs à corriger.")

        self.vbox = QtGui.QVBoxLayout(self)
        self.setLayout(self.vbox)
        self.timer = None

    def start(self):
        self.timer = self.startTimer(1000)

    def stop(self):
        if self.timer:
            self.killTimer(self.timer)

    def elems():
        def fget(self):
            return self._elems
        def fset(self, value):
            self._elems = value
        def fdel(self):
            del self._elems
        return locals()
    elems = property(**elems())

    def reset(self):
        self.elems = []
        self.clear()

    def clear(self):
        for i in range(self.vbox.count()):
            w = self.vbox.itemAt(i).widget()
            if hasattr(w, 'close'):
                w.close()

    def refresh(self):
        self.clear()
        nb_errors = len(self.elems)
        max_rows = 3
        for index in range(0, max_rows):
            try:
                self.vbox.addWidget(self.elems[index])
            except:
                break
        if nb_errors > max_rows:
            self.vbox.addWidget(ErrorLabel(u"(%d) erreurs non affichés" % nb_errors - max_rows))

        if not len(self.elems):
            self.vbox.addWidget(QtGui.QLabel(self.default_text))
        self.update()

    def live_refresh(self):
        self.refresh()

    def timerEvent(self, event):
        try:
            self.live_refresh()
        except Exception as e:
            pass


class PECADMCRITInstructions(PECInstructions):

    def timerEvent(self, event):
        self.live_refresh()
        self.killTimer(event.timerId())
        

class PECADMTYPInstructions(PECInstructions):
    
    def live_refresh(self):
        self.reset()

        total_adm_colid = 8
        curid = self.table.currentRow()
        for cap in self.table.report.caps():
            #cap_label = BoldLabel(HC_CAPS[cap])
            #self.elems.append(cap_label)
            for rowid in self.table.rows_for_cap(cap):
                total_adm = self.table.item(rowid, total_adm_colid)
                if isinstance(total_adm, BlankCell):
                    continue
                if total_adm.get_flag() == total_adm.ERROR:
                    box = QtGui.QHBoxLayout()
                    box.addWidget(IconLabel(QtGui.QPixmap('images/error.png')))
                    errstr =(u"<b>%s Admissions %s</b>: <b>%d</b> (par types). "
                             u"Par critères: <b>%d</b>. Par sexe: <b>%d</b>.") \
                             % (HC_CAPS[cap], 
                                POPULATIONS[total_adm.age], total_adm.value,
                                total_adm.criteria_value,
                                total_adm.gender_value)
                    box.addWidget(ErrorLabel(errstr))
                    box.addStretch(50)
                    wbox = QtGui.QWidget()
                    wbox.setLayout(box)
                    self.elems.append(wbox)

        self.refresh()


class PECOUTInstructions(PECInstructions):
    
    def live_refresh(self):
        self.reset()

        total_out_colid = 7
        curid = self.table.currentRow()
        for cap in self.table.report.caps():
            for rowid in self.table.rows_for_cap(cap):
                total_out = self.table.item(rowid, total_out_colid)
                if isinstance(total_out, BlankCell):
                    continue
                if total_out.get_flag() == total_out.ERROR:
                    box = QtGui.QHBoxLayout()
                    box.addWidget(IconLabel(QtGui.QPixmap('images/error.png')))

                    if total_out.is_global_invalid():
                        if total_out.is_global_invalid_gender('f'):
                            errstr = (u"<b>%s Admissions %s</b>: <b>%d femmes</b>"
                                  u" supérieur au "
                                  u"Total début femme + Total Admis femme: <b>%d</b>.") \
                               % (HC_CAPS[cap], 
                                  POPULATIONS[total_out.age], total_out.gender_value('f'),
                                  total_out.max_value('f'))
                        elif total_out.is_global_invalid_gender('m'):
                            errstr = (u"<b>%s Admissions %s</b>: <b>%d hommes</b>"
                                  u" supérieur au "
                                  u"Total début homme + Total Admis homme: <b>%d</b>.") \
                               % (HC_CAPS[cap], 
                                  POPULATIONS[total_out.age], total_out.gender_value('m'),
                                  total_out.max_value('m'))
                        else:
                            errstr = (u"<b>%s Admissions %s</b>: <b>%d</b>"
                                  u" supérieur au "
                                  u"Total début + Total Admis: <b>%d</b>.") \
                               % (HC_CAPS[cap], 
                                  POPULATIONS[total_out.age], total_out.value,
                                  total_out.max_value())
                    if total_out.is_gender_mismatch():
                        errstr = (u"<b>%s Admissions %s</b>: <b>%d</b> "
                                  u"différent de la répartition par " 
                                  u" sexe: <b>%d</b>.") \
                             % (HC_CAPS[cap], 
                                POPULATIONS[total_out.age], total_out.value,
                                total_out.gender_value())

                    box.addWidget(ErrorLabel(errstr))
                    box.addStretch(50)
                    wbox = QtGui.QWidget()
                    wbox.setLayout(box)
                    self.elems.append(wbox)

        self.refresh()


class PECRECAPInstructions(PECInstructions):

    def live_refresh(self):
        self.reset()

        # retrieve LWB, TB, HIV from outer widget and check those against
        # all Others PEC values
        hiv_field = self.table.parentWidget().others_hiv_field
        tb_field = self.table.parentWidget().others_tb_field
        lwb_field = self.table.parentWidget().others_lwb_field
        sum_filled = sum([hiv_field.value, tb_field.value, lwb_field.value])

        if (sum_filled != self.table.report.sum_all_others):
            box = QtGui.QHBoxLayout()
            box.addWidget(IconLabel(QtGui.QPixmap('images/error.png')))
            errstr = (u"La répartition des <i>Autres</i>: <b>%d</b> "
                      u"ne correspond pas à la somme des admissions "
                      u"<i>autres</i>: <b>%d</b>.") \
                 % (sum_filled, self.table.report.sum_all_others)

            box.addWidget(ErrorLabel(errstr))
            box.addStretch(50)
            wbox = QtGui.QWidget()
            wbox.setLayout(box)
            self.elems.append(wbox)
        self.refresh()
