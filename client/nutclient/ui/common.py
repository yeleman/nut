#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

MAIN_WIDGET_SIZE = 900


class NUTWidget(QtGui.QWidget):

    title = "?"

    def __init__(self, parent=0, *args, **kwargs):

        QtGui.QWidget.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent

        self.setMaximumWidth(MAIN_WIDGET_SIZE)

        self.main_window.setWindowTitle(self.title)

    def refresh(self):
        pass

    def get_main_prop(self, name):
        if hasattr(self.main_window, name):
            return getattr(self.main_window, name)
        else:
            return None

    @property
    def user(self):
        return self.get_main_prop('_user')

    @property
    def main_window(self):
        w = self
        while w:
            if w.__class__.__name__ == 'MainWindow':
                return w
            if hasattr(w, 'parent'):
                w = w.parent
                continue
            else:
                return None
        return None

    @classmethod
    def require_logged_user(self):
        return True

    def process_event(self, event):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        return self.parentWidget()\
                          .change_context(context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(dialog, \
                                               modal=modal, *args, **kwargs)

    def default_focus(self):
        """ widget which should receive focus on NUTWidget display

            Called from MainWindows as FocusProxy is buggy. """
        return None

    @classmethod
    def has_pagination(cls):
        return False

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


class EnterDoesTab(QtGui.QWidget):

    def keyReleaseEvent(self, event):
        super(EnterDoesTab, self).keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key_Return:
            self.focusNextChild()


class EnterTabbedLineEdit(QtGui.QLineEdit, EnterDoesTab):
    pass


class PageTitle(QtGui.QLabel):
    """ Formatage du titre de page """

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 16)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class PageIntro(QtGui.QLabel):
    """ Formatage de l'introduction de page """

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 12)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class FormLabel(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

class ErrorLabel(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont()
        self.setFont(font)
        red = QtGui.QColor(QtCore.Qt.red)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, red)
        self.setPalette(palette)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

class IntLineEdit(QtGui.QLineEdit):
    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.setValidator(QtGui.QIntValidator(0, 100000, self))


class FloatLineEdit(QtGui.QLineEdit):
    """ Accepter que des nombre positif et les nombre avec virgule """

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.setValidator(QtGui.QDoubleValidator(0, 100000, 2, self))


class DateEdit(QtGui.QDateEdit):
    """ Accepter que une date """

    def __init__(self, parent=None):
        QtGui.QDateEdit.__init__(self, parent)
        self.setDisplayFormat("MMMM yyyy")
        self.setDateRange(QtCore.QDate(1999, 1, 1), QtCore.QDate(2100, 1, 1))


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

class ReportAutoField(QtGui.QLabel):

    def __init__(self, parent, report, age):
        QtGui.QLabel.__init__(self, parent)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # prevent tabs focus on cell
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.parent().setFocusPolicy(QtCore.Qt.NoFocus)

        #self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)

        self._parent = parent
        self._report = report
        self._age = age

        # calculate content
        self.live_refresh()

    def live_refresh(self):
        pass

class ReportAutoAdmissionTotal(ReportAutoField):

    @property
    def value(self):
        return sum([self._parent.get_field_value('%s_%s'
                                                  % (self._age, fname))
                     for fname in ('total_beginning_m',
                                   'total_beginning_f',
                                   'hw_u70_bmi_u16',
                                   'muac_u11_muac_u18',
                                   'oedema',
                                   'other')])

    def live_refresh(self):
        self.setText(str(self.value))

class ReportAutoBeginingTotal(ReportAutoField):    

    def live_refresh(self):
        self.setText(str(self.value))

    @property
    def value(self):
        m = self._parent.get_field_value('%s_total_beginning_m' % self._age)
        f = self._parent.get_field_value('%s_total_beginning_f' % self._age)
        return m + f

class BlankCell(QtGui.QTableWidgetItem):

    def __init__(self, parent):
        QtGui.QTableWidgetItem.__init__(self)
        self.setBackground(QtGui.QBrush(QtCore.Qt.darkGray,
                                        QtCore.Qt.Dense4Pattern))
        self.setFlags(QtCore.Qt.NoItemFlags)

    @property
    def value(self):
        return 0
      

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

class ColumnSumItem(QtGui.QTableWidgetItem):

    def __init__(self, column, parent, *args, **kwargs):
        super(ColumnSumItem, self).__init__(*args, **kwargs)
        
        self._column = column
        self._parent = parent

        self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.live_refresh()

    def live_refresh(self):
        value = 0
        for row in self._parent.data[:-1]:
            value += row[self._column].value
        
        self.setText(str(value))
        self.setData(QtCore.Qt.DisplayRole, str(value))


class ReportTable(QtGui.QTableWidget, NUTWidget):

    def __init__(self, parent, report=None, type=None, *args, **kwargs):

        QtGui.QTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self._type = type # PAGE NAME
        self._report = report
        self._parent = parent
        self.header = []
        self.data = []

        self.setAlternatingRowColors(True)
        
        self.setShowGrid(True)
        self.setWordWrap(True)

        self.horizontalHeader().setVisible(True)
        self.horizontalHeader().setDefaultSectionSize(78)
        self.horizontalHeader().setHighlightSections(True)
        self.horizontalHeader().setFont(QtGui.QFont("Courier New", 10))
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        
        #self.horizontalHeader().setHighlightSections(True)
        #self.verticalHeader().setHighlightSections(True)
        self.horizontalHeader().setStretchLastSection(True)

        self.verticalHeader().setVisible(True)
        self.verticalHeader().setDefaultSectionSize(30)
        self.verticalHeader().setHighlightSections(True)
        self.verticalHeader().setFont(QtGui.QFont("Courier New", 10))
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)

        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        #self.setFont(QtGui.QFont("Courier New", 10))

        # set delegate factory for all data rows
        deleg = ReportItemEditorFactory()
        for row in self.get_data_rows():
            self.setItemDelegateForRow(row, deleg)

    def get_data_rows(self):
        rows = []
        caps = self.get_caps_from(self._report)
        i = 0
        for cap in caps:
            i += 1
            for row in range(i, i + 4):
                rows.append(row)
                i += 1
        return rows

    def setdata(self, value):
        if not isinstance(value, (list, None.__class__)):
            raise ValueError
        self._data = value

    def getdata(self):
        return self._data

    data = property(getdata, setdata)

    def setheader(self, value):
        if not isinstance(value, (list, None.__class__)):
            raise ValueError
        self._header = value

    def getheader(self):
        return self._header

    header = property(getheader, setheader)

    def _reset(self):
        for index in range(self.rowCount(), -1, -1):
            self.removeRow(index)

    def refresh(self, resize=False):
        if not self.data: # or not self.header:
            return

        # increase rowCount by one if we have to display total row
        rc = self.data.__len__()
        #if self._display_total:
        #    rc += 1
        self.setRowCount(rc)
        #self.setColumnCount(self.header.__len__())
        #self.setHorizontalHeaderLabels(self.header)

        n = 0
        for row in self.data:
            m = 0
            for item in row:
                ui_item = self._item_for_data(n, m, item, row)
                if isinstance(item, QtGui.QTableWidgetItem):
                    self.setItem(n, m, item)
                elif isinstance(item, QtGui.QWidget):
                    self.setCellWidget(n, m, item)
                elif isinstance(ui_item, QtGui.QTableWidgetItem):
                    self.setItem(n, m, ui_item)
                elif isinstance(ui_item, QtGui.QWidget):
                    self.setCellWidget(n, m, ui_item)
                else:
                    self.setItem(QtGui.QTableWidgetItem(u"%s" % ui_item))
                m += 1
            n += 1

        # call subclass extemsion
        self.extend_rows()

        # only resize columns at initial refresh
        if resize:
            self.resizeColumnsToContents()

        self.live_refresh()


    def extend_rows(self):
        ''' called after cells have been created/refresh.

            Use for adding/editing cells '''
        pass

    def _item_for_data(self, row, column, data, context=None):
        ''' returns QTableWidgetItem or QWidget to add to a cell '''
        return QtGui.QTableWidgetItem(self._format_for_table(data))

    def _format_for_table(self, value):
        ''' formats input value for string in table widget '''
        if isinstance(value, basestring):
            return value

        if isinstance(value, (int, float, long)):
            return formatted_number(value)

        if isinstance(value, QtGui.QTableWidgetItem):
            return value

        if value == None:
            return ''

        return u"%s" % value

    def get_field(self, field):
        for row in self.data:
            for cell in row:
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
            ind = (row/ 3) - 1
            ind = 0 if ind < 0 else ind
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
        print('live_refresh')
        for row in self.data:
            for cell in row:
                if hasattr(cell, 'live_refresh'):
                    getattr(cell, 'live_refresh')()
