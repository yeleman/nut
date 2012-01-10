#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from utils import formatted_number

MAIN_WIDGET_SIZE = 900


def fixed_size_table(row, col, hheader, vheader):

    header_row_height = 25
    row_height = 28
    header_col_width = 120
    col_width = 101

    width = col_width * col
    if hheader:
        width += header_col_width

    height = row_height * row
    if vheader:
        height += header_row_height

    return QtCore.QSize(width, height)


class FlexibleTable(QtGui.QTableWidget):

    # Arbitrary values to play with
    # TODO: find a way to calculate those
    MARGIN_FOR_PARENT_MAX = 20
    SCROLL_WIDTH = 17

    def __init__(self, parent=0):
        super(FlexibleTable, self).__init__(parent)

        self.data = []  # main data holder
        self.hheaders = []  # horizontal headers
        self.vheaders = []  # vertical headers
        self.max_width = 0
        self.max_height = 0
        self.max_rows = 0
        self.stretch_columns = []

        # vHeaders to Content (default)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        #self.verticalHeader().setStretchLastSection(True)

        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        #self.horizontalHeader().setStretchLastSection(True)

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                             QtGui.QSizePolicy.Preferred))

    def max_width():
        def fget(self):
            return self._max_width
        def fset(self, value):
            self._max_width = value
        def fdel(self):
            del self._max_width
        return locals()
    max_width = property(**max_width())

    def max_height():
        def fget(self):
            return self._max_height
        def fset(self, value):
            self._max_height = value
        def fdel(self):
            del self._max_height
        return locals()
    max_height = property(**max_height())

    def max_rows():
        def fget(self):
            return self._max_rows
        def fset(self, value):
            self._max_rows = value
        def fdel(self):
            del self._max_rows
        return locals()
    max_rows = property(**max_rows())

    def stretch_columns():
        def fget(self):
            return self._stretch_columns
        def fset(self, value):
            self._stretch_columns = value
        def fdel(self):
            del self._stretch_columns
        return locals()
    stretch_columns = property(**stretch_columns())

    def data():
        def fget(self):
            return self._data
        def fset(self, value):
            self._data = value
        def fdel(self):
            del self._data
        return locals()
    data = property(**data())

    def _item_for_data(self, row, column, data, context=None):
        ''' returns QTableWidgetItem or QWidget to add to a cell

            override it to add new type of data '''
        return QtGui.QTableWidgetItem(self._format_for_table(data))

    def _format_for_table(self, value):
        ''' formats input value for string in table widget 

            override it to add more formats'''

        if isinstance(value, basestring):
            return value

        if isinstance(value, (int, float, long)):
            return formatted_number(value)

        if value == None:
            return ''

        return u"%s" % value

    def extend_rows(self):
        ''' override this to add more rows/data ar refresh() '''
        pass

    def live_refresh(self):
        ''' calls live-refresh method on each cell. '''
        pass

    def refresh(self):
        # don't refresh if there's no data #TODO: sure?
        if not self.data:
            return

        # set row count
        self.setRowCount(len(self.data))
        self.setColumnCount(len(self.hheaders))
        self.setHorizontalHeaderLabels(self.hheaders)
        self.setVerticalHeaderLabels(self.vheaders)

        rowid = 0
        for row in self.data:
            colid = 0
            for item in row:
                
                # item is already a QTableWidgetItem, display it
                if isinstance(item, QtGui.QTableWidgetItem):
                    self.setItem(rowid, colid, item)
                # item is QWidget, display it
                elif isinstance(item, QtGui.QWidget):
                    self.setCellWidget(rowid, colid, item)
                # item is not ready for display, try to format it
                else:
                    ui_item = self._item_for_data(rowid, colid, item, row)

                    # new item is a QTableWidgetItem or QWidget
                    if isinstance(ui_item, QtGui.QTableWidgetItem):
                        self.setItem(rowid, colid, ui_item)
                    elif isinstance(ui_item, QtGui.QWidget):
                        self.setCellWidget(rowid, colid, ui_item)
                    # something failed, let's build a QTableWidgetItem
                    else:
                        self.setItem(QtGui.QTableWidgetItem(u"%s" % ui_item))
                colid += 1
            rowid += 1

        # call subclass extension
        self.extend_rows()

        # apply resize rules
        self.apply_resize_rules()
        print(self.sizeHint())
        self.updateGeometry()

        # emit post-refresh signal
        self.live_refresh()

    def apply_resize_rules(self):
        # set a fixed outbox
        if self.max_width:
            self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        else:
            # let parent & all set appropriate
            self.max_width = self.parentWidget().maximumWidth() - self.MARGIN_FOR_PARENT_MAX

        self.resize(self.max_width, self.size().height())

        ### WIDTH
        # width is adjusted to the max_size/width of the table
        # each cell gets resized to content.
        # if there is more space available, designed columns are streched.

        # get width once resized to content
        contented_width = 0 ##self.width()
        for ind in range(0, self.horizontalHeader().count()):
            contented_width += self.horizontalHeader().sectionSize(ind)

        # get content-sized with of header
        vheader_width = self.verticalHeader().width()
        extra_width = self.max_width - contented_width

        # space filled-up.
        if extra_width:
            remaining_width = extra_width - vheader_width
            try:
                indiv_extra = remaining_width / len(self.stretch_columns)
            except ZeroDivisionError:
                indiv_extra = 0

            self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
            for colnum in self.stretch_columns:
                self.horizontalHeader().resizeSection(colnum, self.horizontalHeader().sectionSize(colnum) + indiv_extra)

        self.horizontalHeader().update()
        self.update()
        new_width = self.size().width()

        ### HEIGHT
        # table height stops at last row.
        # if max_row/max_height specified and rows above it,
        # it it shrink to this height.

        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.resize(new_width, self.size().height())

        hheader_height = self.horizontalHeader().height()
        
        #total_rows_height = self.size().height() - hheader_height
        total_rows_height = 0 ##self.width()
        for ind in range(0, self.verticalHeader().count()):
            total_rows_height += self.verticalHeader().sectionSize(ind)

        total_height = hheader_height + total_rows_height
        
        max_height = 0
        if not self.max_height and self.max_rows:
            max_height = hheader_height
            for ind in range(0, self.max_rows):
                max_height += self.verticalHeader().sectionSize(ind)

        # user-defined max_height has precedence
        if self.max_height:
            max_height = self.max_height

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                             QtGui.QSizePolicy.Fixed))

        if max_height and total_height > max_height:
            new_height = max_height
        else:
            new_height = total_height

        rows_with_widgets = []
        for rowid in range(0, len(self.data)):
            for colid in range(0, len(self.data[rowid])):
                if not isinstance(self.item(rowid, colid), QtGui.QTableWidgetItem) and not rowid in rows_with_widgets:
                    rows_with_widgets.append(rowid)

        print('rows_with_widgets: %s' % rows_with_widgets)

        if len(rows_with_widgets) >= 1:
            if len(rows_with_widgets) <= 2:
                new_height += 4 * len(rows_with_widgets)
            else:
                new_height += (3 * (len(rows_with_widgets) + 1)) - 1

        # content is trimed and a scroll bar will appear
        # let's have its size supported by strecthed (if any)
        # or equally across all fields
        if new_height < total_height:
            if len(self.stretch_columns):
                share = self.SCROLL_WIDTH / len(self.stretch_columns)
                for colid in self.stretch_columns:
                    self.horizontalHeader().resizeSection(colid, self.horizontalHeader().sectionSize(colid) - share)
            else:
                share = self.SCROLL_WIDTH / self.horizontalHeader().count()
                for colid in range(0, self.horizontalHeader().count()):
                    self.horizontalHeader().resizeSection(colid, self.horizontalHeader().sectionSize(colid) - share)

        self.resize(new_width, new_height)
        self.setMaximumSize(new_width + 2, new_height + 0)
        self.setMinimumSize(new_width - 2, new_height + 0)

        self.verticalHeader().update()
        self.update()

class NUTWidget(QtGui.QWidget):

    title = "?"

    def __init__(self, parent, *args, **kwargs):

        super(NUTWidget, self).__init__(*args, **kwargs)

        self._parent = parent

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
            if hasattr(w, '_parent'):
                w = w._parent
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

class PageSection(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 14)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

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


class LinkButton(QtGui.QPushButton):

    def __init__(self, text, handler, ident):

        super(LinkButton, self).__init__(text)

        self.ident = ident
        self.handler = handler
        self.clicked.connect(self.on_command)

    def on_command(self):
        self.handler(self.ident)


class InfoTable(QtGui.QTableWidget, NUTWidget):

    def __init__(self, *args, **kwargs):

        QtGui.QTableWidget.__init__(self, *args, **kwargs)

        self._data = []

        self.setAlternatingRowColors(True)
        
        self.setShowGrid(True)
        #self.setWordWrap(True)

        self.horizontalHeader().setVisible(True)
        #self.horizontalHeader().setDefaultSectionSize(78)
        self.horizontalHeader().setHighlightSections(True)
        self.horizontalHeader().setFont(QtGui.QFont("Courier New", 10))
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        
        #self.horizontalHeader().setStretchLastSection(True)

        self.verticalHeader().setVisible(False)
        #self.verticalHeader().setDefaultSectionSize(30)
        self.verticalHeader().setHighlightSections(True)
        self.verticalHeader().setFont(QtGui.QFont("Courier New", 10))
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #self.setFont(QtGui.QFont("Courier New", 10))

    def refresh(self, resize=False):
        if not self.data: # or not self.header:
            return

        # increase rowCount by one if we have to display total row
        rc = self.data.__len__()

        self.setRowCount(rc)

        n = 0
        for row in self.data:
            m = 0
            for item in row:
                ui_item = self._item_for_data(n, m, item, row)
                ui_item.setFlags(QtCore.Qt.ItemIsEnabled)
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

        # only resize columns at initial refresh
        if resize:
            self.resizeColumnsToContents()

    def datap():
        def fget(self):
            return self._data
        def fset(self, value):
            self._data = value
        def fdel(self):
            del self._data
        return locals()
    data = property(**datap())

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