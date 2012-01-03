#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date, datetime

from PyQt4 import QtGui, QtCore

from common import NUTWidget, PageTitle, PageIntro, FormLabel, ErrorLabel, EnterTabbedLineEdit, ReportTable
from nutclient.exceptions import *
from nutclient.utils import offline_login
from dashboard import DashboardWidget
from database import Report, Period

class ReportPeriodWidget(QtGui.QDialog, NUTWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent)

        self.parent = parent

        self.setWindowTitle(_(u"Période des données"))

        self.title = PageTitle(_(u"Indiquez la période correspondante."))
        self.intro = PageIntro(_(u"Indiquez ci-dessous la période (mois et " \
                                 u"année qui correspond aux données.\n" \
                                 u"Cela doit être le mois passé.\n\n" \
                                 u"Vous ne pouvez pas saisir les données du " \
                                 u"rapport sans renseigner la période."))

        vbox = QtGui.QVBoxLayout()
        gridbox = QtGui.QGridLayout()

        # page title
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        # date field
        self.date_field = QtGui.QDateEdit(self)
        #self.date_field.setReadOnly(True)
        self.date_field.setMinimumDate(date(2012, 1, 1))
        self.date_field.setMaximumDate(date(2020, 12, 1))
        self.date_field.setDisplayFormat('MMMM yyyy')
        self.date_label = FormLabel(u"Période")
        self.date_label.setBuddy(self.date_field)

        # confirm button
        self.confirm_button = QtGui.QPushButton(_(u"&Continuer"))
        self.confirm_button.setAutoDefault(True)
        self.confirm_button.clicked.connect(self.confirm)

        # cancel closes window
        self.cancel_button = QtGui.QPushButton(_(u"&Annuler"))
        self.cancel_button.clicked.connect(self.cancel)

        # login error
        self.period_error = ErrorLabel("")

        # grid layout
        gridbox.addWidget(self.date_label, 0, 0)
        gridbox.addWidget(self.date_field, 0, 1)
        gridbox.addWidget(self.period_error, 1, 1)

        # adds stretched column + row at end to fill-up space
        gridbox.setColumnStretch(2, 1)
        gridbox.setRowStretch(5, 10)
        
        # layout
        vbox.addLayout(gridbox)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.cancel_button)
        hbox.addWidget(self.confirm_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        # set focus to username field
        self.setFocusProxy(self.confirm_button)
        self.confirm_button.setFocus()

    def cancel(self):
        self.close()

    def confirm(self):
        period_date = self.date_field.date().toPyDate()
        period = Period.from_date(period_date)
        
        report = period

        self.parent.view_widget.report = report

        self.close()

class ReportWidget(NUTWidget):

    title = u"Nutrition Monthly Report"
    report = None

    def __init__(self, parent=0, *args, **kwargs):

        super(ReportWidget, self).__init__(parent=parent, *args, **kwargs)

        report = None

        self.init_timer = self.startTimer(0)

    def gen_ui(self):
        self.title = PageTitle(_(u"Monthly Nutrition Report"))
        self.intro = PageIntro(_(u"%s") % self.report)

        vbox = QtGui.QVBoxLayout()
        #gridbox = QtGui.QGridLayout()

        # page title
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        # Table
        self.table = ReportTable(self, None, 8, 10)
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

    def cancel_period_request(self):
        self.change_context(DashboardWidget)

    def timerEvent(self, event):
        self.killTimer(self.init_timer)

        if not self.report:
            period_widget = self.open_dialog(ReportPeriodWidget)

        # report *should* be set by dialog.
        # if not, go back to Dashboard.
        if not self.report:
            QtGui.QMessageBox.warning(self, u"pas de periode", u"boo")
            self.change_main_context(DashboardWidget)
            return

        self.gen_ui()

