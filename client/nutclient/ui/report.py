#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from datetime import date, datetime

from PyQt4 import QtGui, QtCore

from common import *
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

        # a report exist for that period.
        if Report.filter(period=period).count() == 1:
            report = Report.filter(period=period).get()
        else:
            report = Report.create_safe(period=period, user=self.user)

        self.parent.view_widget.report = report

        self.close()


def build_data_from(parent, report, readonly):

    data = []
    cols = 10
    blank_line = [BlankCell(parent) \
                  for x in range(0, cols)]

    # Add SAM section
    if report.is_sam:
        # add blank line for SAM section header
        data.append(blank_line)

        # retrieve sam report
        samr = report.pec_sam_report

        for age in ('u59', 'o59', 'fu1'):

            cells = []
            cells.append(ReportAutoBeginingTotal(parent, samr, age))
            cells.append(ReportValueEdit(parent, 
                                         samr, '%s_total_beginning_m' % age))
            cells.append(ReportValueEdit(parent,
                                         samr, '%s_total_beginning_f' % age))
            cells.append(BlankCell(parent))
            cells.append(BlankCell(parent))
            for fname in ('hw_u70_bmi_u16', 'muac_u11_muac_u18',
                          'oedema', 'other'):
                cells.append(ReportValueEdit(parent, 
                                             samr, '%s_%s' % (age, fname)))
            cells.append(ReportAutoAdmissionTotal(parent, samr, age))
            
            data.append(cells)

    return data

class ReportWidget(NUTWidget):

    title = u"Nutrition Monthly Report"
    report = None

    def __init__(self, parent=0, *args, **kwargs):

        super(ReportWidget, self).__init__(parent=parent, *args, **kwargs)

        self.init_timer = self.startTimer(0)

    def build_pec_ui(self):
        self.title = PageTitle(_(u"Rapport Statistique Mensuel - Traitement de la malnutrition aiguë") % self.report.period)
        self.intro = PageIntro(_(u"%(period)s") % {'period': self.report.period})

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

        self.table.data = build_data_from(self.table, self.report, self.readonly)
        self.table.refresh()    

        vbox.addWidget(self.table)
        self.setLayout(vbox)

        # set focus to username field
        self.setFocusProxy(self.table)
        

    def gen_ui(self):

        # What do we display now?
        self.build_pec_ui()


    @property
    def readonly(self):
        return not self.report.can_edit()

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

