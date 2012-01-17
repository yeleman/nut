#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from nutrsc.mali import *
from table import *
from report import *
from elements import *


class PECReportTable(ReportFlexibleTable):

    def __init__(self, parent, report, page):
        super(PECReportTable, self).__init__(parent, report, page)

        self.report_fields = []
        self.vheaders = self.build_vheaders()

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
                for fname in self.report_fields:
                    # skip None fields (delimiters)
                    if not fname:
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
        self.report_fields = [None,
                              'total_beginning_m',
                              'total_beginning_f',
                              'hw_b7080_bmi_u18',
                              'muac_u120',
                              'hw_u70_bmi_u16',
                              'muac_u11_muac_u18',
                              'oedema',
                              'other',
                              None]

    def load_data(self, readonly=False):

        self.data = []
        cols = len(self.hheaders)
        def blank_line():
            return [BlankCell(self) for x in range(0, cols)]
        # Add SAMP section
        if self.report.is_samp:
            # add blank line for SAM section header
            self.data.append(blank_line())
            # retrieve sam report
            sampr = self.report.pec_samp_report
            for age in POPULATIONS_CAP[sampr.CAP]:
                cells = []
                cells.append(ReportAutoBeginingTotal(self, samr, age))
                cells.append(ReportValueEditItem(self, 
                                             samr, '%s_total_beginning_m' % age))
                cells.append(ReportValueEditItem(self,
                                             samr, '%s_total_beginning_f' % age))
                cells.append(BlankCell(self))
                cells.append(BlankCell(self))
                for fname in ('hw_u70_bmi_u16', 'muac_u11_muac_u18',
                              'oedema', 'other'):
                    cells.append(ReportValueEditItem(self, 
                                                 samr, '%s_%s' % (age, fname)))
                cells.append(ReportAutoAdmissionTotal(self, samr, age))
                
                self.data.append(cells)

        # Add SAM section
        if self.report.is_sam:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            samr = self.report.pec_sam_report

            for age in POPULATIONS_CAP[samr.CAP]:

                cells = []
                cells.append(ReportAutoBeginingTotal(self, samr, age))
                cells.append(ReportValueEditItem(self, 
                                             samr, '%s_total_beginning_m' % age))
                cells.append(ReportValueEditItem(self,
                                             samr, '%s_total_beginning_f' % age))
                cells.append(BlankCell(self))
                cells.append(BlankCell(self))
                for fname in ('hw_u70_bmi_u16', 'muac_u11_muac_u18',
                              'oedema', 'other'):
                    cells.append(ReportValueEditItem(self, 
                                                 samr, '%s_%s' % (age, fname)))
                cells.append(ReportAutoAdmissionTotal(self, samr, age))
                
                self.data.append(cells)

        # Add MAM section
        if self.report.is_mam:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            mamr = self.report.pec_mam_report

            for age in POPULATIONS_CAP[mamr.CAP]:

                cells = []
                cells.append(ReportAutoBeginingTotal(self, mamr, age))
                if age == 'pw':
                    cells.append(BlankCell(self))
                else:
                    cells.append(ReportValueEditItem(self, 
                                             mamr, '%s_total_beginning_m' % age))
                cells.append(ReportValueEditItem(self,
                                             mamr, '%s_total_beginning_f' % age))

                cells.append(ReportValueEditItem(self, 
                                                 mamr, '%s_%s' % (age, 'hw_b7080_bmi_u18')))

                cells.append(ReportValueEditItem(self, 
                                                 mamr, '%s_%s' % (age, 'muac_u120')))

                cells.append(BlankCell(self))
                cells.append(BlankCell(self))
                cells.append(BlankCell(self))

                cells.append(ReportValueEditItem(self, 
                                                 mamr, '%s_%s' % (age, 'other')))

                cells.append(ReportAutoAdmissionTotal(self, mamr, age))
                
                self.data.append(cells)

        # add total line
        self.data.append([ColumnSumItem(self, None, None) for x in range(0, cols)])

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

        self.report_fields = [None, None, None,
                              'new_case',
                              'relapse',
                              'returned',
                              'nut_transfered_in',
                              'nut_referred_in',
                               None,
                              'admitted_m',
                              'admitted_f']

    def load_data(self, readonly=False):

        self.data = []
        cols = len(self.hheaders)
        def blank_line():
            return [BlankCell(self) for x in range(0, cols)]

        # Add SAMP section
        if self.report.is_samp:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            sampr = self.report.pec_samp_report

            for age in POPULATIONS_CAP[sampr.CAP]:

                cells = []
                cells.append(ReportAutoBeginingTotal(self, sampr, age))
                cells.append(ReportAutoCustomField(self, 
                                     sampr, '%s_total_beginning_m' % age, age))
                cells.append(ReportAutoCustomField(self,
                                     sampr, '%s_total_beginning_f' % age, age))

                for fname in ('new_case', 'relapse',
                              'returned', 'nut_transfered_in'):
                              
                    cells.append(ReportValueEditItem(self, 
                                                 sampr, '%s_%s' % (age, fname)))

                cells.append(BlankCell(self))

                cells.append(ReportMultipleAutoAdmissionTotal(self, sampr, age))

                cells.append(ReportValueEditItem(self, 
                                           sampr, '%s_%s' % (age, 'admitted_m')))

                cells.append(ReportValueEditItem(self, 
                                           sampr, '%s_%s' % (age, 'admitted_f')))
                
                self.data.append(cells)
                #self.data.append(blank_line())

        # Add SAM section
        if self.report.is_sam:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            samr = self.report.pec_sam_report

            for age in POPULATIONS_CAP[samr.CAP]:

                cells = []
                cells.append(ReportAutoBeginingTotal(self, samr, age))
                cells.append(ReportAutoCustomField(self, 
                                      samr, '%s_total_beginning_m' % age, age))
                cells.append(ReportAutoCustomField(self,
                                      samr, '%s_total_beginning_f' % age, age))

                for fname in ('new_case', 'relapse',
                              'returned', 'nut_transfered_in',
                              'nut_referred_in'):
                    cells.append(ReportValueEditItem(self, 
                                                 samr, '%s_%s' % (age, fname)))

                cells.append(ReportMultipleAutoAdmissionTotal(self, samr, age))

                cells.append(ReportValueEditItem(self, 
                                           samr, '%s_%s' % (age, 'admitted_m')))

                cells.append(ReportValueEditItem(self, 
                                           samr, '%s_%s' % (age, 'admitted_f')))
                
                self.data.append(cells)

        # Add MAM section
        if self.report.is_mam:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            mamr = self.report.pec_mam_report

            for age in POPULATIONS_CAP[mamr.CAP]:

                cells = []
                cells.append(ReportAutoBeginingTotal(self, mamr, age))

                if age == 'pw':
                    cells.append(BlankCell(self))
                else:
                    cells.append(ReportAutoCustomField(self, 
                                       mamr, '%s_total_beginning_m' % age, age))
                cells.append(ReportAutoCustomField(self,
                                       mamr, '%s_total_beginning_f' % age, age))

                for fname in ('new_case', 'relapse',
                              'returned'):
                    if age == 'fu12':
                        cells.append(BlankCell(self))
                    else:
                        cells.append(ReportValueEditItem(self, 
                                                 mamr, '%s_%s' % (age, fname)))
                cells.append(BlankCell(self))

                cells.append(ReportValueEditItem(self, 
                                     mamr, '%s_%s' % (age, 'nut_referred_in')))

                
                cells.append(ReportMultipleAutoAdmissionTotal(self, mamr, age))
                if age == 'pw':
                    cells.append(BlankCell(self))
                else:
                    cells.append(ReportValueEditItem(self, 
                                           mamr, '%s_%s' % (age, 'admitted_m')))

                cells.append(ReportValueEditItem(self, 
                                           mamr, '%s_%s' % (age, 'admitted_f')))
                
                self.data.append(cells)
                #self.data.append(blank_line())

        # add total line
        self.data.append([ColumnSumItem(self, None, None) for x in range(0, cols)])

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

        self.report_fields = ['healed',
                              'referred_out',
                              'deceased',
                              'aborted',
                              'non_respondant',
                              'medic_transfered_out',
                              'nut_transfered_out',
                               None,
                              'total_out_m',
                              'total_out_m']

    def load_data(self, readonly=False):

        self.data = []
        cols = len(self.hheaders)
        def blank_line():
            return [BlankCell(self) for x in range(0, cols)]

        # Add SAMP section
        if self.report.is_samp:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            sampr = self.report.pec_samp_report

            for age in POPULATIONS_CAP[sampr.CAP]:

                cells = []

                for fname in ('healed', 'referred_out',
                              'deceased',
                              'aborted',
                              'non_respondant',
                              'medic_transfered_out',
                              'nut_transfered_out'):
                              
                    cells.append(ReportValueEditItem(self, 
                                                 sampr, '%s_%s' % (age, fname)))

                cells.append(ReportAutoOutTotal(self, sampr, age))

                cells.append(ReportValueEditItem(self, 
                                           sampr, '%s_%s' % (age, 'total_out_m')))

                cells.append(ReportValueEditItem(self, 
                                           sampr, '%s_%s' % (age, 'total_out_f')))
                
                self.data.append(cells)

        # Add SAM section
        if self.report.is_sam:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            samr = self.report.pec_sam_report

            for age in POPULATIONS_CAP[samr.CAP]:

                cells = []
                for fname in ('healed', 'referred_out',
                              'deceased',
                              'aborted',
                              'non_respondant',
                              'medic_transfered_out',
                              'nut_transfered_out'):
                              
                    cells.append(ReportValueEditItem(self, 
                                                 samr, '%s_%s' % (age, fname)))

                cells.append(ReportAutoOutTotal(self, samr, age))

                cells.append(ReportValueEditItem(self, 
                                           samr, '%s_%s' % (age, 'total_out_m')))

                cells.append(ReportValueEditItem(self, 
                                           samr, '%s_%s' % (age, 'total_out_f')))
                
                self.data.append(cells)

        # Add MAM section
        if self.report.is_mam:
            # add blank line for SAM section header
            self.data.append(blank_line())

            # retrieve sam report
            mamr = self.report.pec_mam_report

            for age in POPULATIONS_CAP[mamr.CAP]:

                cells = []
                for fname in ('healed', 'referred_out',
                              'deceased',
                              'aborted',
                              'non_respondant',
                              'medic_transfered_out'):
                              
                    cells.append(ReportValueEditItem(self, 
                                                 mamr, '%s_%s' % (age, fname)))

                cells.append(BlankCell(self))

                cells.append(ReportAutoOutTotal(self, mamr, age))

                if age == 'pw':
                    cells.append(BlankCell(self))
                else:
                    cells.append(ReportValueEditItem(self, 
                                           mamr, '%s_%s' % (age, 'total_out_m')))

                cells.append(ReportValueEditItem(self, 
                                           mamr, '%s_%s' % (age, 'total_out_f')))
                
                self.data.append(cells)

        # add total line
        self.data.append([ColumnSumItem(self, None, None) for x in range(0, cols)])

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

        self.startTimer(1000)

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
        max_rows = 4
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
            #self.killTimer(event.timerId())
        


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
                        errstr = (u"<b>%s Admissions %s</b>: <b>%d</b>"
                                  u" supérieur au "
                                  u"Total début + Total Admis: <b>%d</b>.") \
                             % (HC_CAPS[cap], 
                                POPULATIONS[total_out.age], total_out.value,
                                total_out.max_value)

                    if total_out.is_gender_mismatch():
                        errstr = (u"<b>%s Admissions %s</b>: <b>%d</b> "
                                  u"différent de la répartition par " 
                                  u" sexe: <b>%d</b>.") \
                             % (HC_CAPS[cap], 
                                POPULATIONS[total_out.age], total_out.value,
                                total_out.gender_value)

                    box.addWidget(ErrorLabel(errstr))
                    box.addStretch(50)
                    wbox = QtGui.QWidget()
                    wbox.setLayout(box)
                    self.elems.append(wbox)

        self.refresh()