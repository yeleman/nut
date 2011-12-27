#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui

from common import NUTWidget, PageTitle


class DashboardWidget(NUTWidget):

    def __init__(self, parent=0, *args, **kwargs):

        super(DashboardWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        self.title = PageTitle(_(u"Dashboard %s") % self.parent.user)
        vbox.addWidget(self.title)

        self.setLayout(vbox)
