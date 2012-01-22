#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from nutrsc.mali import *
from table import *


class ReportFlexibleTable(FlexibleTable):

    def __init__(self, parent, report, page):
        super(ReportFlexibleTable, self).__init__(parent)

        self.report = report
        self.type = page

        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)

        # set delegate factory for all data rows
        deleg = ReportItemEditorFactory()
        self.setItemDelegate(deleg)

    def get_field(self, field, cap, *args):
        for rowid in self.rows_for_cap(cap):
            for colid in xrange(0, self.columnCount()):
                cell = self.item(rowid, colid)
                if hasattr(cell, '_field'):
                    if getattr(cell, '_field') == field:
                        return cell
        return None

    def rows_for_cap(self, cap):
        index = self.report.caps().index(cap)
        s = index * 4
        return xrange(s, s + 4)

    def get_caps_from(self, report):
        return self.report.caps()

    def get_report_for(self, row, column):
        return self.item(row, column)._report

    def get_field_for(self, row, column):
        return self.item(row, column)._field

    '''def get_report_for(self, row, column):
        if self.type in ('pec_adm_crit', 'pec_adm_typ', 'pec_out', 'pec_recap'):
            ind = row / 4
            cap = self.get_caps_from(self.report)[ind]
            return getattr(self.report, 'pec_%s_report' % cap)
        return None

    def get_age_for(self, row, column):
        table = [None] + POPULATIONS_CAP[SEVERE_COMP] + \
                [None] + POPULATIONS_CAP[SEVERE] + \
                [None] + POPULATIONS_CAP[MODERATE]
       
        if not self.report.is_samp:
            table = table[4:]

        if not self.report.is_sam:
            table = table[4:]

        if not self.report.is_mam:
            table = table[4:]
        return table[row]        

    def get_field_for(self, row, column):

        age = self.get_age_for(row, column)
        return '%s_%s' % (age, self.report_fields[column])'''

    def get_field_value(self, fname, cap, *args):
        field = self.get_field(fname, cap, *args)
        if not field:
            return 0
        try:
            return field.value
        except:
            raise

    def cell_updated(self, item):
        """ a child cell has been updated """
        self.live_refresh()

    def live_refresh(self):
        for rowid in range(0, self.rowCount()):
            for colid in range(0, self.columnCount()):
                cell = self.item(rowid, colid)
                if hasattr(cell, 'live_refresh'):
                    getattr(cell, 'live_refresh')()

    def refresh(self):
        super(ReportFlexibleTable, self).refresh()


class ReportField(FlexibleWidget):

    INFO = 0
    WARNING = 1
    ERROR = 2
    COLORS = {INFO: (121, 143, 155),
              WARNING: (231, 161, 22),
              ERROR: (115,16,31)}
    ICONS = {}  #{ERROR: 'error'}

    def __init__(self, *args, **kwargs):
        super(ReportField, self).__init__(*args, **kwargs)
        self.default_brush = self.background()
        self.default_text_brush = self.foreground()

    def flagContent(self, flag):
        if not flag in self.COLORS:
            self.setBackground(self.default_brush)
            self.setForeground(self.default_text_brush)
        else:
            if isinstance(self.COLORS[flag], basestring):
                brush = QtGui.QBrush(eval('QtCore.Qt.%s' % self.COLORS[flag]))
            elif self:
                brush = QtGui.QBrush(QtGui.QColor(*self.COLORS[flag]))
            if flag == self.ERROR:
                self.setForeground(brush)
            else:
                self.setBackground(brush)

        if not flag in self.ICONS:
            self.setIcon(QtGui.QIcon())
        else:
            self.setIcon(QtGui.QIcon('images/%s.png' % self.ICONS[flag]))

    def live_refresh(self):
        self.setData(QtCore.Qt.EditRole, unicode(self.value))
        self.setData(QtCore.Qt.DisplayRole, unicode(self.display_value))

        self.flagContent(self.get_flag())

    @property
    def display_value(self):
        return unicode(self.value)

    @property
    def value(self):
        try:
            return int(self.data(QtCore.Qt.EditRole).toPyObject())
        except Exception as e:
            return 0

    def get_flag(self):
        return None

    def is_error(self):
        return self.get_flag() == self.ERROR

    def is_warning(self):
        return self.get_flag() == self.WARNING

    def is_info(self):
        return self.get_flag() == self.INFO


class ReportAutoField(ReportField, FlexibleReadOnlyWidget):

    def __init__(self, parent, report, field, age, *args, **kwargs):
        super(ReportAutoField, self).__init__("2000")
        
        self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        #self.setFlags(QtCore.Qt.ItemIsEnabled)
        self.setFlags(QtCore.Qt.NoItemFlags)

        #self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)

        self.default_text_brush = QtGui.QBrush(QtGui.QColor(121, 143, 155))

        self.parent_table = parent
        self.report = report
        self.field = field
        self.age = age

        # calculate content
        self.live_refresh()

    @property
    def value(self):
        return int(self.data(QtCore.Qt.EditRole).toPyObject())

    def get_flag(self):
        if compare_expected_value(self.report, self.field, self.value):
            return self.WARNING
        return None

class ReportAutoBeginingTotal(ReportAutoField):

    @property
    def value(self):
        m = self.parent_table.get_field_value('%s_total_beginning_m' % self.age, self.report.CAP)
        f = self.parent_table.get_field_value('%s_total_beginning_f' % self.age, self.report.CAP)
        return m + f


class ReportAutoOutTotal(ReportAutoField):

    @property
    def value(self):
        return sum([self.parent_table.get_field_value('%s_%s'
                                          % (self.age, fname), self.report.CAP)
                    for fname in ('healed', 'referred_out',
                                  'deceased',
                                  'aborted',
                                  'non_respondant',
                                  'medic_transfered_out',
                                  'nut_transfered_out')])

    def begining_value(self, sex=None):
        if sex:
            return getattr(self.report, '%s_total_beginning_%s' % (self.age, sex), 0)
        return self.report.male_female_sum('%s_total_beginning' % self.age)

    def admitted_value(self, sex=None):
        if sex:
            return getattr(self.report, '%s_admitted_%s' % (self.age, sex), 0)
        return self.report.male_female_sum('%s_admitted' % self.age)

    def max_value(self, sex=None):
        return self.begining_value(sex) + self.admitted_value(sex)

    def gender_value(self, sex=None):
        m = self.parent_table.get_field_value('%s_total_out_m' % self.age, self.report.CAP)
        f = self.parent_table.get_field_value('%s_total_out_f' % self.age, self.report.CAP)
        if sex:
            if sex.lower() == 'm':
                return m
            if sex.lower() == 'f':
                return f
        return m + f

    def is_gender_mismatch(self):
        return self.value != self.gender_value()

    def is_global_invalid(self):
        return (self.is_global_invalid_number()
                or self.is_global_invalid_gender('m')
                or self.is_global_invalid_gender('f'))
    
    def is_global_invalid_number(self):
        return self.value > self.max_value

    def is_global_invalid_gender(self, sex):
        return self.gender_value(sex) > self.max_value(sex)

    def get_flag(self):
        if self.is_gender_mismatch() \
            or self.is_global_invalid():
            return self.ERROR
        else:
            return None


class ReportAutoValueRO(ReportAutoField):

    @property
    def value(self):
        return getattr(self.report, self.field, 0)


class ReportAutoAdmissionTotal(ReportAutoField):

    @property
    def value(self):
        return sum([self.parent_table.get_field_value('%s_%s'
                                                      % (self.age, fname), self.report.CAP)
                    for fname in ('hw_u70_bmi_u16',
                                  'muac_u11_muac_u18',
                                  'oedema',
                                  'other')])


class ReportAutoQuantitiesLeft(ReportAutoField):

    @property
    def possessed(self):
        return sum([self.parent_table.get_field_value(fname, self.report.CAP, self.report.nut_input.slug)
                    for fname in ('initial', 'received')])
    @property
    def consumed(self):
        return sum([self.parent_table.get_field_value(fname, self.report.CAP, self.report.nut_input.slug)
                    for fname in ('used', 'lost')])

    @property
    def value(self):
        return self.possessed - self.consumed

    @property
    def is_invalid(self):
        return self.value < 0

    def get_flag(self):
        if self.is_invalid:
            return self.ERROR
        else:
            return None


class ReportMultipleAutoAdmissionTotal(ReportAutoField):

    """ Admission Total fields for Admission Type page.

        Values to type sum.
        Displays all data (criteria, type, genders) """

    @property
    def value(self):
        return sum([self.parent_table.get_field_value('%s_%s'
                                          % (self.age, fname), self.report.CAP)
                    for fname in ('new_case',
                                  'relapse',
                                  'returned',
                                  'nut_transfered_in',
                                  'nut_referred_in')])

    @property
    def criteria_value(self):
        return sum([getattr(self.report, '%s_%s' % (self.age, fname), 0)
                    for fname in ('hw_b7080_bmi_u18',
                                  'muac_u120',
                                  'hw_u70_bmi_u16',
                                  'muac_u11_muac_u18',
                                  'oedema',
                                  'other')])

    @property
    def gender_value(self):
        return sum([self.parent_table.get_field_value('%s_%s'
                                          % (self.age, fname), self.report.CAP)
                    for fname in ('admitted_m',
                                  'admitted_f')])

    @property
    def display_value(self):
        # champagne!
        if self.value == self.criteria_value \
           and self.value == self.gender_value:
            return unicode(self.value)
        else:
            return unicode(self.value)
            '''return unicode(u"%d | %d | %d" % (self.value,
                                              self.criteria_value,
                                              self.gender_value))'''

    def get_flag(self):
        if self.value == self.criteria_value \
           and self.value == self.gender_value:
            return None
        else:
            return self.ERROR

class ColumnSumItem(ReportAutoField):

    def __init__(self, parent, report, age, *args, **kwargs):
        super(ColumnSumItem, self).__init__(parent, report, None, age, *args, **kwargs)

        self.live_refresh()

    @property
    def value(self):
        value = 0
        # loop on all rows but last (this one supposedly)
        for rowid in range(0, self.parent_table.rowCount() - 1):
            try:
                value += self.parent_table.item(rowid, self.column()).value
            except AttributeError:
                # might be a BlankCell
                pass
        return value


class ReportAutoCustomField(ReportField, FlexibleReadOnlyWidget):

    def __init__(self, parent, report, field, age, *args, **kwargs):
        super(ReportAutoCustomField, self).__init__("0")
        
        self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.setFlags(QtCore.Qt.NoItemFlags)

        self.parent_table = parent
        self.report = report
        self._field = field
        self.age = age

        # calculate content
        self.live_refresh()

    @property
    def value(self):
        return getattr(self.report, self._field)


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
        
        #if self._report.status == self._report.STATUS_CREATED:
        #    self.setPlaceholderText(value)
        #else:
        self.setText(value)

        self.setValidator(QtGui.QIntValidator(0, 9999, self))

        self.editingFinished.connect(self.notify_parent)

    @property
    def value(self):
        v = self.text()
        if not v:
            v = self.placeholderText()
        return int(v)

    def notify_parent(self):
        if not self.text():
            self.setText(0)
        self._table.cell_updated(self)


class ReportValueEditItem(QtGui.QTableWidgetItem):

    def __init__(self, parent, report, field, age):
        QtGui.QTableWidgetItem.__init__(self, "?", 0)
        
        self._parent = parent
        self._report = report
        self._field = field
        self._age = age
        self._must_valid = True

        self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.setToolTip(self._field)
        self.setWhatsThis(self._field)
        #self.setStatusTip(self._field)

        self.live_refresh()

    def live_refresh(self):
        self.setData(QtCore.Qt.EditRole, str(self.value))
        self.setData(QtCore.Qt.DisplayRole, str(self.value))

    @property
    def value(self):
        try:
            return int(self.data(QtCore.Qt.EditRole).toPyObject())
        except:
            return getattr(self._report, self._field)
        


class ReportItemEditorFactory(QtGui.QItemDelegate):

    def createEditor(self, parent, option, index):
        report = parent.parent().get_report_for(index.row(), index.column())
        field = parent.parent().get_field_for(index.row(), index.column())
        edit = ReportValueEdit(parent, parent.parent(), report, field)
        edit.setFocusPolicy(QtCore.Qt.StrongFocus)
        return edit


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