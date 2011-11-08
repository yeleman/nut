#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui

from common import REDEWidget, PageTitle


class DashboardWidget(REDEWidget):

    def __init__(self, parent=0, *args, **kwargs):

        super(DashboardWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        # Le titre
        self.title = PageTitle(_(u"Dashboard"))
        vbox.addWidget(self.title)

        self.setLayout(vbox)
