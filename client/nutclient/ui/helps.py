#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui

from common import NUTWidget, PageTitle


class HelpWidget(NUTWidget):

    def __init__(NUT, parent=0, *args, **kwargs):

        super(HelpWidget, NUT).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        # Le titre
        NUT.title = PageTitle(_(u"Help"))
        vbox.addWidget(NUT.title)

        NUT.setLayout(vbox)
