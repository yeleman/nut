#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from nutclient.utils import formatted_number


class FlexibleTable(QtGui.QTableWidget):

    # Arbitrary values to play with
    # TODO: find a way to calculate those
    MARGIN_FOR_PARENT_MAX = 20
    MARGIN_FOR_PARENT_MAX2 = 50
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
        self.display_hheaders = True
        self.display_vheaders = True

        self.setAlternatingRowColors(True)
        self.setShowGrid(True)
        self.setWordWrap(True)

        #self.horizontalHeader().setFont(QtGui.QFont("Courier New", 10))
        self.horizontalHeader().setHighlightSections(True)
        self.verticalHeader().setHighlightSections(True)
        #self.verticalHeader().setFont(QtGui.QFont("Courier New", 10))
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        # vHeaders to Content (default)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        #self.verticalHeader().setStretchLastSection(True)

        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        #self.horizontalHeader().setStretchLastSection(True)

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                             QtGui.QSizePolicy.Preferred))

    def display_hheaders():
        def fget(self):
            return self._display_hheaders
        def fset(self, value):
            self._display_hheaders = value
        def fdel(self):
            del self._display_hheaders
        return locals()
    display_hheaders = property(**display_hheaders())

    def display_vheaders():
        def fget(self):
            return self._display_vheaders
        def fset(self, value):
            self._display_vheaders = value
        def fdel(self):
            del self._display_vheaders
        return locals()
    display_vheaders = property(**display_vheaders())

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
        # set row count
        self.setRowCount(len(self.data))
        self.setColumnCount(len(self.hheaders))
        #self.setHorizontalHeaderLabels(self.hheaders)
        for col in xrange(len(self.hheaders)):
            self.setHorizontalHeaderItem(col, QtGui.QTableWidgetItem(self.hheaders[col]))
        #self.setVerticalHeaderLabels(self.vheaders)
        for row in xrange(len(self.vheaders)):
            self.setVerticalHeaderItem(row, QtGui.QTableWidgetItem(self.vheaders[row]))
        

        # don't refresh if there's no data #TODO: sure?
        if not self.data:
            pass
            #return

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
                        self.setItem(rowid, colid, 
                                     QtGui.QTableWidgetItem(u"%s" % ui_item))
                colid += 1
            rowid += 1

        # call subclass extension
        self.extend_rows()

        # apply resize rules
        self.apply_resize_rules()

        self.updateGeometry()

        # emit post-refresh signal
        self.live_refresh()

    def apply_resize_rules(self):
        print('begin')

        # set headers visibility according to our prop
        self.verticalHeader().setVisible(self.display_vheaders)
        self.horizontalHeader().setVisible(self.display_hheaders)

        # set a fixed outbox
        if self.max_width:
            self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        else:
            # let parent & all set appropriate
            self.max_width = self.parentWidget().maximumWidth() - self.MARGIN_FOR_PARENT_MAX
        
        if self.max_width > 10000:
            self.max_width = self.parentWidget().width() - self.MARGIN_FOR_PARENT_MAX2

        self.resize(self.max_width, self.size().height())

        ### WIDTH
        # width is adjusted to the max_size/width of the table
        # each cell gets resized to content.
        # if there is more space available, designed columns are streched.

        # get width once resized to content
        contented_width = 0 ##self.width()
        for ind in range(0, self.horizontalHeader().count()):
            contented_width += self.horizontalHeader().sectionSize(ind)

        self.verticalHeader().adjustSize()
        # get content-sized with of header
        if self.display_vheaders:
            vheader_width = self.verticalHeader().width()
        else:
            vheader_width = 0
        print('vheader_width: %d' % vheader_width)
        extra_width = self.max_width - contented_width ## - vheader_width

        # space filled-up.
        if extra_width:
            print('extra_width: %d' % extra_width)
            remaining_width = extra_width - vheader_width
            try:
                to_stretch = self.stretch_columns
                indiv_extra = remaining_width / len(to_stretch)
            except ZeroDivisionError:
                to_stretch = range(0, self.horizontalHeader().count())
                indiv_extra = remaining_width / len(to_stretch)
            except:
                indiv_extra = 0

            self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
            for colnum in to_stretch:
                self.horizontalHeader().resizeSection(colnum, self.horizontalHeader().sectionSize(colnum) + indiv_extra)

        self.horizontalHeader().update()
        self.update()

        # don't update size if not data
        new_width = self.size().width()
        print('new_width: %d' % new_width)

        print('height')
        ### HEIGHT
        # table height stops at last row.
        # if max_row/max_height specified and rows above it,
        # it it shrink to this height.

        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.resize(new_width, self.size().height())

        self.horizontalHeader().adjustSize()
        hheader_height = self.horizontalHeader().height()
        
        #total_rows_height = self.size().height() - hheader_height
        total_rows_height = 0 ##self.width()
        for ind in range(0, self.verticalHeader().count()):
            total_rows_height += self.rowHeight(ind)

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
                #if not isinstance(self.item(rowid, colid), QtGui.QTableWidgetItem) and not rowid in rows_with_widgets:
                if isinstance(self.item(rowid, colid), (QtGui.QPushButton, None.__class__)) and not rowid in rows_with_widgets:
                    rows_with_widgets.append(rowid)
                print('%d %s' % (colid, self.item(rowid, colid)))
                try:
                    print('%d %s' % (colid, self.item(rowid, colid)._field))
                except:
                    pass

        print('rows_with_widgets: %s' % rows_with_widgets)
        
        if len(rows_with_widgets) >= 1:
            if len(rows_with_widgets) <= 2:
                new_height += 4 * len(rows_with_widgets)
            else:
                new_height += (3 * (len(rows_with_widgets) + 1)) - 1
        

        if self.display_vheaders and self.vheaders:
            new_height += 2

        # add extra space if table is empty
        if not len(self.data):
            new_height += 3 + hheader_height
            new_width += 4

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


        print((new_width, new_height))
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setStretchLastSection(True)
        self.resize(new_width, new_height)
        self.setMaximumSize(new_width + 2, new_height + 0)
        self.setMinimumSize(new_width - 2, new_height + 0)

        self.verticalHeader().update()
        self.update()
        print('done')


class FlexibleWidget(QtGui.QTableWidgetItem):

    def __init__(self, *args, **kwargs):
        super(FlexibleWidget, self).__init__(*args, **kwargs)
        
        #self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.setFlags(QtCore.Qt.ItemIsEnabled | 
                      QtCore.Qt.ItemIsSelectable |
                      QtCore.Qt.ItemIsEditable)

    def live_refresh(self):
        print('live refreshing editable %s' % self)
        pass


class FlexibleReadOnlyTable(FlexibleTable):

    def __init__(self, parent=0):
        super(FlexibleReadOnlyTable, self).__init__(parent)
        self.align_map = {}

    def align_map():
        def fget(self):
            return self._align_map
        def fset(self, value):
            self._align_map = value
        def fdel(self):
            del self._align_map
        return locals()
    align_map = property(**align_map())

    def _item_for_data(self, row, column, data, context=None):
        if isinstance(data, (basestring, int)):
            if column in self.align_map.keys():
                widget = self.widget_from_align(self.align_map[column])
            else:
                widget = FlexibleReadOnlyWidget
            return widget(self._format_for_table(data))
        else:
            super(FlexibleReadOnlyTable, self)._item_for_data(row, column, data, context)

    def widget_from_align(self, align):
        if align.lower() == 'l':
            return FlexibleReadOnlyWidgetAL
        elif align.lower() == 'r':
            return FlexibleReadOnlyWidgetAR
        else:
            return FlexibleReadOnlyWidget


class FlexibleReadOnlyWidget(FlexibleWidget):

    def __init__(self, *args, **kwargs):
        super(FlexibleReadOnlyWidget, self).__init__(*args, **kwargs)
        
        self.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def live_refresh(self):
        print('live refreshing %s' % self)
        pass


class FlexibleReadOnlyWidgetAL(FlexibleReadOnlyWidget):
    def __init__(self, *args, **kwargs):
        super(FlexibleReadOnlyWidgetAL, self).__init__(*args, **kwargs)
        self.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class FlexibleReadOnlyWidgetAR(FlexibleReadOnlyWidget):
    def __init__(self, *args, **kwargs):
        super(FlexibleReadOnlyWidgetAR, self).__init__(*args, **kwargs)
        self.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)


class EnterDoesTab(QtGui.QWidget):

    def keyReleaseEvent(self, event):
        super(EnterDoesTab, self).keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key_Return:
            self.focusNextChild()


class EnterTabbedLineEdit(QtGui.QLineEdit, EnterDoesTab):
    pass