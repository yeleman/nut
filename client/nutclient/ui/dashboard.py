#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui

from common import NUTWidget, PageTitle, PageIntro


class DashboardWidget(NUTWidget):

    title = u"Dashboard"

    def __init__(self, parent=0, *args, **kwargs):

        super(DashboardWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        self.title = PageTitle(_(u"Welcome %(user)s, %(hc)s (%(hccap)s)") \
                               % {'user': self.parent.user,
                                  'hc': self.parent.user.hc,
                                  'hccap': self.parent.user.verb_caps()})
        self.intro = PageIntro(u"")

        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        self.setLayout(vbox)
