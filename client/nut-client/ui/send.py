#!/usr/bin/env python
# encoding=utf-8
# maintainer: Alou

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from common import REDEWidget, PageTitle, PageIntro, FormLabel


class SendWidget(REDEWidget):

    def __init__(self, parent=0, *args, **kwargs):

        super(SendWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        gridbox = QtGui.QGridLayout()

        self.title = PageTitle(_(u"Send your report."))
        self.intro = PageIntro(_(u"Your report is ready for sending.\nYou" \
                                  u"need to choose a sending method" \
                                  u" depending on your device and plan."))
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        self.combobox = QtGui.QComboBox()
        self.combobox.addItem(_(u'SMS'))
        self.combobox.addItem(_(u'Internet (EDGE Data)'))
        gridbox.addWidget(FormLabel(_(u"Transfer Type:")), 1, 0)
        gridbox.addWidget(self.combobox, 1, 1)

        gridbox.addWidget(FormLabel(_(u"Estimation Cost:")), 2, 0)
        gridbox.addWidget(QtGui.QLabel(_(u"Sending this report would cost" \
                                         u" you 4 SMS.")), 2, 1)

        cancel_but = QtGui.QPushButton(_(u"Cancel"))
        send_but = QtGui.QPushButton(_(u"Send"))
        gridbox.addWidget(send_but, 3, 1)
        gridbox.addWidget(cancel_but, 4, 1)
        send_but.clicked.connect(self.send)
        cancel_but.clicked.connect(self.cancel)

        gridbox.setColumnStretch(2, 1)
        gridbox.setRowStretch(5, 10)

        vbox.addLayout(gridbox)
        self.setLayout(vbox)

    def send(self):
        pass

    def cancel(self):
        self.close()
