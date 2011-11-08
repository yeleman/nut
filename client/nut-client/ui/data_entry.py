#!/usr/bin/env python
# encoding=utf-8
# maintainer: Alou

from PyQt4 import QtGui, QtCore

from common import REDEWidget, PageTitle, PageIntro, FormLabel,\
                                    DateEdit, IntLineEdit, FloatLineEdit


class DataEntryWidget(REDEWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(DataEntryWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        gridbox = QtGui.QGridLayout()

        self.title = PageTitle(_(u"Data Entry."))
        self.intro = PageIntro(_(u""))
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        self.floatlineedit = FloatLineEdit()
        self.inttlineedit = IntLineEdit()
        self.date = DateEdit(QtCore.QDate.currentDate())

        gridbox.addWidget(FormLabel(_(u"Nombre positif")), 0, 1)
        gridbox.addWidget(self.inttlineedit, 0, 2)
        gridbox.addWidget(FormLabel(_(u"Nombre positif avec virgule")), 1, 1)
        gridbox.addWidget(self.floatlineedit, 1, 2)
        gridbox.addWidget(FormLabel(_(u"Date")), 2, 1)
        gridbox.addWidget(self.date, 2, 2)
        vbox.addLayout(gridbox)
        self.setLayout(vbox)
