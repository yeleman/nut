#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from table import *


class ReportFlexibleTable(FlexibleTable):

    def __init__(self, parent, report, page):
        super(ReportFlexibleTable, self).__init__(parent)

        self._report = report
        self._type = page

        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)

        # set delegate factory for all data rows
        deleg = ReportItemEditorFactory()
        self.setItemDelegate(deleg)

    def get_field(self, field):
        for rowid in xrange(0, self.rowCount()):
            for colid in xrange(0, self.columnCount()):
                cell = self.item(rowid, colid)
                if hasattr(cell, '_field'):
                    if getattr(cell, '_field') == field:
                        return cell
        return None

    def get_caps_from(self, report):
        caps = []
        if report.is_samp:
            caps.append('samp')
        if report.is_sam:
            caps.append('sam')
        if report.is_mam:
            caps.append('mam')
        return caps

    def get_report_for(self, row, column):
        if self._type in ('pec_adm_crit', 'pec_adm_typ', 'pec_out', 'pec_recap'):
            ind = row / 4
            cap = self.get_caps_from(self._report)[ind]
            return getattr(self._report, 'pec_%s_report' % cap)
        return None

    def get_age_for(self, row, column):
        table = [None, 'u6', 'u59', 'o59', 
                 None, 'u59', 'o59', 'fu1',
                 None, 'u59', 'pw', 'fu12']
       
        if not self._report.is_samp:
            table = table[4:]

        if not self._report.is_sam:
            table = table[4:]

        if not self._report.is_mam:
            table = table[4:]
        return table[row]        

    def get_field_for(self, row, column):
        table = {
            'pec_adm_crit': [(None, u""),
                             ('total_beginning_m', u"Total debut"),
                             ('total_beginning_f', u""),
                             ('hw_b7080_bmi_u18', u""),
                             ('muac_u120', u""),
                             ('hw_u70_bmi_u16', u""),
                             ('muac_u11_muac_u18', u""),
                             ('oedema', u""),
                             ('other', u""),
                             (None, u"")]
        }

        if self._type in ('pec_adm_crit', 'pec_adm_typ', 'pec_out', 'pec_recap'):
            age = self.get_age_for(row, column)
            return '%s_%s' % (age, table[self._type][column][0])

    def get_field_value(self, field):
        field = self.get_field(field)
        if not field:
            return 0
        try:
            return field.value
        except:
            return -9

    def click_item(self, row, column, *args):
        pass

    def cell_updated(self, item):
        print('cell_updated: %s' % item)
        self.live_refresh()

    def live_refresh(self):
        print('live_refresh reporttable')
        for rowid in range(0, self.rowCount()):
            for colid in range(0, self.columnCount()):
                cell = self.item(rowid, colid)
                if hasattr(cell, 'live_refresh'):
                    getattr(cell, 'live_refresh')()


class PECADMCRITReportTable(ReportFlexibleTable):

    def __init__(self, parent, report, page):
        super(PECADMCRITReportTable, self).__init__(parent, report, page)

        self.hheaders = [u"Total au\ndébut du\nmois",
                         u"Dont\nSexe\nM", u"Dont\nSexe\nF",
                         u"P/T≥70\n<80%\nIMC<18",
                         u"PB<120\nou\nPB<210",
                         u"P/T<70%\nou\nIMC<16",
                         u"PB<11cm\nou\nPB<18cm",
                         u"Œdeme", u"Autre", "TOTAL\nADMIS"]
        self.vheaders = [u"URENAS 2",
                         u"6-59 mois", u"> 59 mois",
                         u"Suivi URENI 1",
                         u"URENAM 3",
                         u"6-59 mois", u"FE/FA", u"Suivi 1&2"]

        #self.table.data = build_data_from(self.table, self.report, self.readonly)

    def apply_resize_rules(self):
        self.setVerticalHeaderItem(0, TableSectionHead(u"URENAS 2"))
        self.setVerticalHeaderItem(4, TableSectionHead(u"URENAM 3"))
        self.setVerticalHeaderItem(8, TableSectionHead(u"TOTAL"))
        super(PECADMCRITReportTable, self).apply_resize_rules()


class ReportField(FlexibleWidget):

    INFO = 0
    WARNING = 1
    ERROR = 2
    COLORS = {INFO: 'green',
              WARNING: 'yellow',
              ERROR: 'darkRed'}

    def __init__(self, *args, **kwargs):
        super(ReportField, self).__init__(*args, **kwargs)
        self.default_brush = self.background()

    def flagContent(self, flag):
        if not flag in self.COLORS:
            self.setBackground(self.default_brush)
            return
        
        if isinstance(self.COLORS[flag], basestring):
            brush = QtGui.QBrush(eval('QtCore.Qt.%s' % self.COLORS[flag]))
        elif self:
            brush = QtGui.QBrush(QtGui.QColor(**self.COLORS[flag]))
        self.setBackground(brush)

    def live_refresh(self):
        self.setData(QtCore.Qt.EditRole, unicode(self.value))
        self.setData(QtCore.Qt.DisplayRole, unicode(self.display_value))

        self.flagContent(self.get_flag())

    @property
    def value(self):
        return 0

    @property
    def display_value(self):
        return unicode(self.value)

    @property
    def value(self):
        return int(self.data(QtCore.Qt.EditRole).toPyObject())

    def get_flag(self):
        return None

    def is_error(self):
        return self.get_flag() == self.ERROR

    def is_warning(self):
        return self.get_flag() == self.WARNING

    def is_info(self):
        return self.get_flag() == self.INFO


class ReportAutoField(ReportField, FlexibleReadOnlyWidget):

    def __init__(self, parent, report, age, *args, **kwargs):
        super(ReportAutoField, self).__init__("0")
        
        self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.setFlags(QtCore.Qt.NoItemFlags)

        #self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)

        self.parent_table = parent
        self.report = report
        self.age = age

        # calculate content
        self.live_refresh()

    @property
    def value(self):
        self.value = int(self.data(QtCore.Qt.EditRole).toPyObject())

    def get_flag(self):
        if self.value > 10:
            return self.WARNING
        return None

class ReportAutoBeginingTotal(ReportAutoField):

    @property
    def value(self):
        m = self.parent_table.get_field_value('%s_total_beginning_m' % self.age)
        f = self.parent_table.get_field_value('%s_total_beginning_f' % self.age)
        return m + f

class ReportAutoAdmissionTotal(ReportAutoField):

    @property
    def value(self):
        return sum([self.parent_table.get_field_value('%s_%s'
                                                      % (self.age, fname))
                    for fname in ('hw_u70_bmi_u16',
                                  'muac_u11_muac_u18',
                                  'oedema',
                                  'other')])

class ColumnSumItem(ReportAutoField):

    def __init__(self, parent, report, age, *args, **kwargs):
        super(ColumnSumItem, self).__init__(parent, report, age, *args, **kwargs)
        
        #self.column = column
        #self.parent_table = parent

        #self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.live_refresh()

    '''def live_refresh(self):
        value = 0
        for row in self._parent.data[:-1]:
            value += row[self._column].value
        
        self.setText(str(value))
        self.setData(QtCore.Qt.DisplayRole, str(value))
    '''
    @property
    def value(self):
        value = 0
        # loop on all rows but last (this one supposedly)
        for rowid in range(0, self.parent_table.rowCount() - 1):
            value += self.parent_table.item(rowid, self.column()).value
            print('row %d: %d' % (rowid, value))
        return value

####################### ?


class ContinueWidget(QtGui.QWidget):

    def __init__(self, parent):

        super(ContinueWidget, self).__init__(parent)
        self.box = QtGui.QHBoxLayout()
        self.box.addStretch()
        self.box.addWidget(ContinueButton(self))
        self.setLayout(self.box)

class ContinueButton(QtGui.QPushButton):

    def __init__(self, parent):

        icon = QtGui.QIcon('images/emblem-default.png')
        super(ContinueButton, self).__init__(icon, 
                                             u"En&registrer && Continuer",
                                             parent)


class ReportValueEdit(QtGui.QLineEdit):
    """  """

    def __init__(self, parent, table, report, field):
        
        QtGui.QLineEdit.__init__(self, parent)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self._table = table
        self._report = report
        self._field = field

        value = str(getattr(self._report, self._field))
        
        if self._report.status == self._report.STATUS_CREATED:
            self.setPlaceholderText(value)
        else:
            self.setText(value)

        self.setValidator(QtGui.QIntValidator(0, 100000, self))

        self.editingFinished.connect(self.notify_parent)

    @property
    def value(self):
        v = self.text()
        if not v:
            v = self.placeholderText()
        return int(v)

    def notify_parent(self):
        print('notify_parent: ' % self)
        self._table.cell_updated(self)


class ReportValueEditItem(QtGui.QTableWidgetItem):

    def __init__(self, parent, report, field):
        QtGui.QTableWidgetItem.__init__(self, "?", 0)
        
        self._parent = parent
        self._report = report
        self._field = field
        self._must_valid = True

        self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.setToolTip(self._field)
        self.setWhatsThis(self._field)
        #self.setStatusTip(self._field)

        value = getattr(self._report, self._field)
        self.set_value(value)

    @property
    def value(self):
        return int(self.data(QtCore.Qt.EditRole).toPyObject())

    def set_value(self, value):
        self.setData(QtCore.Qt.EditRole, str(value))
        self.setData(QtCore.Qt.DisplayRole, str(value))


class ReportItemEditorFactory(QtGui.QItemDelegate):

    def createEditor(self, parent, option, index):
        report = parent.parent().get_report_for(index.row(), index.column())
        field = parent.parent().get_field_for(index.row(), index.column())
        edit = ReportValueEdit(parent, parent.parent(), report, field)
        edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        return edit

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

    def setEditorData(self, editor, index):
        ds = index.model().data(index, QtCore.Qt.DisplayRole).toString()
        editor.setText(ds)
    
    def commitAndCloseEditor(self, sender):
        #QDateEdit *editor = qobject_cast<QDateEdit*>(sender());
        print('commitAndCloseEditor')
        self.commitData.emmit(editor)
        self.closeEditor.emmit(editor)


class TableSectionHead(QtGui.QTableWidgetItem):

    def __init__(self, *args, **kwargs):
        super(TableSectionHead, self).__init__(*args, **kwargs)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)


class ReportValueLabel(QtGui.QLabel):

    def __init__(self, parent, report, field):

        QtGui.QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        if not report or not field:
            self.setText('')
        else:
            self.setText(str(getattr(self._report, self._field)))

class ReportAutoValueLabel(QtGui.QLabel):

    def __init__(self, parent, report, field):

        QtGui.QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

    def refresh(self):
        pass



class BlankCell(QtGui.QTableWidgetItem):

    def __init__(self, parent):
        QtGui.QTableWidgetItem.__init__(self)
        self.setBackground(QtGui.QBrush(QtCore.Qt.darkGray,
                                        QtCore.Qt.Dense4Pattern))
        self.setFlags(QtCore.Qt.NoItemFlags)

    @property
    def value(self):
        return 0