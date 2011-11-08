#!/usr/bin/env python
# encoding=utf-8
# maintainer: Alou

from PyQt4 import QtGui

from common import REDEWidget, PageTitle, PageIntro


class PreferencesWidget(REDEWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(PreferencesWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        gridbox = QtGui.QGridLayout()

        self.title = PageTitle(_(u"Change your preferences."))
        self.intro = PageIntro(_(u""))
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        vbox.addLayout(gridbox)
        self.setLayout(vbox)
