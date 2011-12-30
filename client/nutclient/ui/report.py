#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore

from common import NUTWidget, PageTitle, PageIntro, FormLabel, ErrorLabel, EnterTabbedLineEdit, ReportTable
from nutclient.exceptions import *
from nutclient.utils import offline_login
from dashboard import DashboardWidget


class ReportWidget(NUTWidget):

    title = u"Nutrition Monthly Report"

    def __init__(self, parent=0, *args, **kwargs):

        super(ReportWidget, self).__init__(parent=parent, *args, **kwargs)

        
        self.title = PageTitle(_(u"Monthly Nutrition Report"))
        self.intro = PageIntro(_(u""))

        vbox = QtGui.QVBoxLayout()
        #gridbox = QtGui.QGridLayout()

        # page title
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        # Table
        self.table = ReportTable(self, 8, 10)
        self.table.setHorizontalHeaderLabels([u"Total au\ndébut du\nmois",
                                              u"Dont\nSexe\nM", u"Dont\nSexe\nF",
                                              u"P/T≥70\n<80%\nIMC<18",
                                              u"PB<120\nou\nPB<210",
                                              u"P/T<70%\nou\nIMC<16",
                                              u"PB<11cm\nou\nPB<18cm",
                                              u"Œdeme", u"Autre", "TOTAL\nADMIS"])
        self.table.setVerticalHeaderLabels([u"URENAS 2",
                                            u"6-59 mois", u"> 59 mois",
                                            u"Suivi URENI", u"URENAM 3",
                                            u"6-59 mois", u"FE/FA",
                                            u"Suivi 1&2"])



        vbox.addWidget(self.table)
        self.setLayout(vbox)

        # set focus to username field
        self.setFocusProxy(self.table)

    ############ DEBUG
    @classmethod
    def require_logged_user(self):
        return False
