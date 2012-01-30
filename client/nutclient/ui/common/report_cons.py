#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from database import Report, InputOrderReport, NUTInput
from nutrsc.mali import *
from table import *
from report import *
from elements import *


class CONSORDERReportTable(ReportFlexibleTable):

    def __init__(self, parent, report, page):
        super(CONSORDERReportTable, self).__init__(parent, report, page)
        self.hheaders = [u"Début mois", u"Reçus",
                         u"Utilisés", u"Perdus",
                         u"Restants", u"Commandés"]

        self.report_fields = ['initial', 'received', 'used', 'lost', None, 'quantity']
        self.vheaders = self.build_vheaders()

    def build_vheaders(self):
        vheaders = []
        def get_input_name(code):
            return NUTInput.filter(slug=code).get().name.title()

        for cap in self.report.caps():
            vheaders.append(HC_CAPS[cap])
            vheaders += list(get_input_name(code) for code in CONSUMPTION_TABLE[cap][DEFAULT_VERSION])
        return vheaders

    def get_report_for(self, row, column):
        return self.item(row, column)._report

    def get_field_for(self, row, column):
        return self.item(row, column)._field

    def get_field(self, field, cap, code=None):
        for rowid in self.rows_for_cap(cap):
            for colid in xrange(0, self.columnCount()):
                cell = self.item(rowid, colid)
                if hasattr(cell, '_field'):
                    if getattr(cell, '_field') == field:
                        if not code:
                            return cell
                        else:
                            if cell._report.nut_input.slug == code:
                                return cell
        return None

    def rows_for_cap(self, cap):
        start = 0
        end = 0
        line = 0
        for acap in self.report.caps():
            if cap == acap:
                start = line
            line += 1
            line += len(CONSUMPTION_TABLE[acap][DEFAULT_VERSION])
            if cap == acap:
                end = line
        return xrange(start, end)

    def load_data(self, readonly=False):
        self.data = []
        cols = len(self.hheaders)
        def blank_line():
            return [BlankCell(self) for x in range(0, cols)]

        for cap in self.report.caps():
            
            # add a blank line for the section header
            self.data.append(blank_line())

            cap_cons_report = getattr(self.report, 'cons_%s_report' % cap)
            cap_order_report = getattr(self.report, 'order_%s_report' % cap)

            for icr in cap_cons_report.nutinput_reports:

                ior = InputOrderReport.filter(order_report=cap_order_report,
                                              nut_input=icr.nut_input).get()

                self.vheaders.append(icr.nut_input.name.upper())
                cells = []
                cells.append(ReportValueEditItem(self, icr, 'initial', None))
                cells.append(ReportValueEditItem(self, icr, 'received', None))
                cells.append(ReportConsUsedValueEditItem(self, icr, 'used', None))
                cells.append(ReportValueEditItem(self, icr, 'lost', None))
                cells.append(ReportAutoQuantitiesLeft(self, icr, 'left', None))
                cells.append(ReportOrderValueEditItem(self, ior, 'quantity', None))

                self.data.append(cells)
        # add total line
        self.data.append([ColumnSumItem(self, None, None) for x in range(0, cols)])

        self.rows_for_cap('mam')
        self.rows_for_cap('sam')

    def focus_on_data(self):
        for rowid in xrange(0, self.rowCount()):
            for colid in xrange(0, self.columnCount()):
                item = self.item(rowid, colid)
                if item.flags().__and__(Qt.ItemIsSelectable):
                    self.setCurrentCell(rowid, colid)
                    return

    def validate(self):

        left_colid = 4
        for rowid in xrange(0, self.rowCount()):
            left = self.item(rowid, left_colid)
            if not isinstance(left, ReportAutoQuantitiesLeft):
                continue

            if left.is_invalid:
                return False

        return True

    def apply_resize_rules(self):
        index = 0
        for cap in self.report.caps():
            self.setVerticalHeaderItem(index, TableSectionHead(HC_CAPS[cap]))
            index += len(CONSUMPTION_TABLE[cap][DEFAULT_VERSION]) + 1
        self.setVerticalHeaderItem(index, TableSectionHead(u"TOTAL"))
        super(CONSORDERReportTable, self).apply_resize_rules()
        self.focus_on_data()

    def save(self):
        if not self.validate():
            return False

        for rowid in xrange(0, self.rowCount()):
            for colid in xrange(0, self.columnCount()):
                item = self.item(rowid, colid)
                if not hasattr(item, '_report') or not hasattr(item, '_field'):
                    continue
                setattr(item._report, item._field, item.value)
                item._report.save()

        return True


from report_pec import PECInstructions

class CONSORDERInstructions(PECInstructions):

    def live_refresh(self):
        self.reset()

        left_colid = 4

        for rowid in xrange(0, self.table.rowCount()):
            left = self.table.item(rowid, left_colid)

            if not isinstance(left, ReportAutoQuantitiesLeft):
                continue

            if left.is_invalid:
                box = QtGui.QHBoxLayout()
                box.addWidget(IconLabel(QtGui.QPixmap('images/error.png')))

                errstr = (u"<b>%s %s</b>: <b>%d</b> "
                              u"est inférieur à <b>zéro</b>.") \
                         % (HC_CAPS[left.report.CAP], 
                            self.table.vheaders[rowid], left.value)

                box.addWidget(ErrorLabel(errstr))
                box.addStretch(50)
                wbox = QtGui.QWidget()
                wbox.setLayout(box)
                self.elems.append(wbox)
        self.refresh()
