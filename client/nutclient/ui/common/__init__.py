#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from report import *
from table import *
from elements import *



# class ReportTable(QtGui.QTableWidget, NUTWidget):

#     def __init__(self, parent, report=None, type=None, *args, **kwargs):

#         QtGui.QTableWidget.__init__(self, parent=parent, *args, **kwargs)

#         self._type = type # PAGE NAME
#         self._report = report
#         self._parent = parent
#         self.header = []
#         self.data = []

#         self.setAlternatingRowColors(True)
        
#         self.setShowGrid(True)
#         #self.setWordWrap(True)

#         self.horizontalHeader().setVisible(True)
#         self.horizontalHeader().setDefaultSectionSize(78)
#         self.horizontalHeader().setHighlightSections(True)
#         self.horizontalHeader().setFont(QtGui.QFont("Courier New", 10))
#         self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        
#         #self.horizontalHeader().setHighlightSections(True)
#         #self.verticalHeader().setHighlightSections(True)
#         self.horizontalHeader().setStretchLastSection(True)

#         self.verticalHeader().setVisible(True)
#         self.verticalHeader().setDefaultSectionSize(30)
#         self.verticalHeader().setHighlightSections(True)
#         self.verticalHeader().setFont(QtGui.QFont("Courier New", 10))
#         self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)

#         self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
#         #self.setFont(QtGui.QFont("Courier New", 10))

#         # set delegate factory for all data rows
#         deleg = ReportItemEditorFactory()
#         for row in self.get_data_rows():
#             self.setItemDelegateForRow(row, deleg)

#     def get_data_rows(self):
#         rows = []
#         caps = self.get_caps_from(self._report)
#         i = 0
#         for cap in caps:
#             i += 1
#             for row in range(i, i + 4):
#                 rows.append(row)
#                 i += 1
#         return rows

#     def setdata(self, value):
#         if not isinstance(value, (list, None.__class__)):
#             raise ValueError
#         self._data = value

#     def getdata(self):
#         return self._data

#     data = property(getdata, setdata)

#     def setheader(self, value):
#         if not isinstance(value, (list, None.__class__)):
#             raise ValueError
#         self._header = value

#     def getheader(self):
#         return self._header

#     header = property(getheader, setheader)

#     def _reset(self):
#         for index in range(self.rowCount(), -1, -1):
#             self.removeRow(index)

#     def refresh(self, resize=False):
#         if not self.data: # or not self.header:
#             return

#         # increase rowCount by one if we have to display total row
#         rc = self.data.__len__()
#         #if self._display_total:
#         #    rc += 1
#         self.setRowCount(rc)
#         #self.setColumnCount(self.header.__len__())
#         #self.setHorizontalHeaderLabels(self.header)

#         n = 0
#         for row in self.data:
#             m = 0
#             for item in row:
#                 ui_item = self._item_for_data(n, m, item, row)
#                 if isinstance(item, QtGui.QTableWidgetItem):
#                     self.setItem(n, m, item)
#                 elif isinstance(item, QtGui.QWidget):
#                     self.setCellWidget(n, m, item)
#                 elif isinstance(ui_item, QtGui.QTableWidgetItem):
#                     self.setItem(n, m, ui_item)
#                 elif isinstance(ui_item, QtGui.QWidget):
#                     self.setCellWidget(n, m, ui_item)
#                 else:
#                     self.setItem(QtGui.QTableWidgetItem(u"%s" % ui_item))
#                 m += 1
#             n += 1

#         # call subclass extemsion
#         self.extend_rows()

#         # only resize columns at initial refresh
#         if resize:
#             self.resizeColumnsToContents()

#         self.live_refresh()


#     def extend_rows(self):
#         ''' called after cells have been created/refresh.

#             Use for adding/editing cells '''
#         pass

#     def _item_for_data(self, row, column, data, context=None):
#         ''' returns QTableWidgetItem or QWidget to add to a cell '''
#         return QtGui.QTableWidgetItem(self._format_for_table(data))

#     def _format_for_table(self, value):
#         ''' formats input value for string in table widget '''
#         if isinstance(value, basestring):
#             return value

#         if isinstance(value, (int, float, long)):
#             return formatted_number(value)

#         if isinstance(value, QtGui.QTableWidgetItem):
#             return value

#         if value == None:
#             return ''

#         return u"%s" % value

#     def get_field(self, field):
#         for row in self.data:
#             for cell in row:
#                 if hasattr(cell, '_field'):
#                     if getattr(cell, '_field') == field:
#                         return cell
#         return None

#     def get_caps_from(self, report):
#         caps = []
#         if report.is_samp:
#             caps.append('samp')
#         if report.is_sam:
#             caps.append('sam')
#         if report.is_mam:
#             caps.append('mam')
#         return caps

#     def get_report_for(self, row, column):
#         if self._type in ('pec_adm_crit', 'pec_adm_typ', 'pec_out', 'pec_recap'):
#             ind = (row/ 3) - 1
#             ind = 0 if ind < 0 else ind
#             cap = self.get_caps_from(self._report)[ind]
#             return getattr(self._report, 'pec_%s_report' % cap)
#         return None

#     def get_age_for(self, row, column):
#         table = [None, 'u6', 'u59', 'o59', 
#                  None, 'u59', 'o59', 'fu1',
#                  None, 'u59', 'pw', 'fu12']
       
#         if not self._report.is_samp:
#             table = table[4:]

#         if not self._report.is_sam:
#             table = table[4:]

#         if not self._report.is_mam:
#             table = table[4:]
#         return table[row]        

#     def get_field_for(self, row, column):
#         table = {
#             'pec_adm_crit': [(None, u""),
#                              ('total_beginning_m', u"Total debut"),
#                              ('total_beginning_f', u""),
#                              ('hw_b7080_bmi_u18', u""),
#                              ('muac_u120', u""),
#                              ('hw_u70_bmi_u16', u""),
#                              ('muac_u11_muac_u18', u""),
#                              ('oedema', u""),
#                              ('other', u""),
#                              (None, u"")]
#         }

#         if self._type in ('pec_adm_crit', 'pec_adm_typ', 'pec_out', 'pec_recap'):
#             age = self.get_age_for(row, column)
#             return '%s_%s' % (age, table[self._type][column][0])

#     def get_field_value(self, field):
#         field = self.get_field(field)
#         if not field:
#             return 0
#         try:
#             return field.value
#         except:
#             return -9

#     def click_item(self, row, column, *args):
#         pass

#     def cell_updated(self, item):
#         print('cell_updated: %s' % item)
#         self.live_refresh()

#     def live_refresh(self):
#         print('live_refresh')
#         for row in self.data:
#             for cell in row:
#                 if hasattr(cell, 'live_refresh'):
#                     getattr(cell, 'live_refresh')()


# class InfoTable(QtGui.QTableWidget, NUTWidget):

#     def __init__(self, *args, **kwargs):

#         QtGui.QTableWidget.__init__(self, *args, **kwargs)

#         self._data = []

#         self.setAlternatingRowColors(True)
        
#         self.setShowGrid(True)
#         #self.setWordWrap(True)

#         self.horizontalHeader().setVisible(True)
#         #self.horizontalHeader().setDefaultSectionSize(78)
#         self.horizontalHeader().setHighlightSections(True)
#         self.horizontalHeader().setFont(QtGui.QFont("Courier New", 10))
#         self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        
#         #self.horizontalHeader().setStretchLastSection(True)

#         self.verticalHeader().setVisible(False)
#         #self.verticalHeader().setDefaultSectionSize(30)
#         self.verticalHeader().setHighlightSections(True)
#         self.verticalHeader().setFont(QtGui.QFont("Courier New", 10))
#         self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

#         self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
#         self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
#         #self.setFont(QtGui.QFont("Courier New", 10))

#     def refresh(self, resize=False):
#         if not self.data: # or not self.header:
#             return

#         # increase rowCount by one if we have to display total row
#         rc = self.data.__len__()

#         self.setRowCount(rc)

#         n = 0
#         for row in self.data:
#             m = 0
#             for item in row:
#                 ui_item = self._item_for_data(n, m, item, row)
#                 ui_item.setFlags(QtCore.Qt.ItemIsEnabled)
#                 if isinstance(item, QtGui.QTableWidgetItem):
#                     self.setItem(n, m, item)
#                 elif isinstance(item, QtGui.QWidget):
#                     self.setCellWidget(n, m, item)
#                 elif isinstance(ui_item, QtGui.QTableWidgetItem):
#                     self.setItem(n, m, ui_item)
#                 elif isinstance(ui_item, QtGui.QWidget):
#                     self.setCellWidget(n, m, ui_item)
#                 else:
#                     self.setItem(QtGui.QTableWidgetItem(u"%s" % ui_item))
#                 m += 1
#             n += 1

#         # only resize columns at initial refresh
#         if resize:
#             self.resizeColumnsToContents()

#     def datap():
#         def fget(self):
#             return self._data
#         def fset(self, value):
#             self._data = value
#         def fdel(self):
#             del self._data
#         return locals()
#     data = property(**datap())

#     def _item_for_data(self, row, column, data, context=None):
#         ''' returns QTableWidgetItem or QWidget to add to a cell '''
#         return QtGui.QTableWidgetItem(self._format_for_table(data))

#     def _format_for_table(self, value):
#         ''' formats input value for string in table widget '''
#         if isinstance(value, basestring):
#             return value

#         if isinstance(value, (int, float, long)):
#             return formatted_number(value)

#         if isinstance(value, QtGui.QTableWidgetItem):
#             return value

#         if value == None:
#             return ''

#         return u"%s" % value

