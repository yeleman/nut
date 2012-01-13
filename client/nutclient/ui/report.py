#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin
import weakref
import gc

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
    def blank_line():
        return [BlankCell(parent) for x in range(0, cols)]

    # Add SAMP section
    if report.is_samp:
        # add blank line for SAM section header
        data.append(blank_line())

        # retrieve sam report
        sampr = report.pec_samp_report
        #parent.

        for age in ('u6', 'u59', 'o59'):

            cells = []
            cells.append(ReportAutoBeginingTotal(parent, samr, age))
            cells.append(ReportValueEditItem(parent, 
                                         samr, '%s_total_beginning_m' % age))
            cells.append(ReportValueEditItem(parent,
                                         samr, '%s_total_beginning_f' % age))
            cells.append(BlankCell(parent))
            cells.append(BlankCell(parent))
            for fname in ('hw_u70_bmi_u16', 'muac_u11_muac_u18',
                          'oedema', 'other'):
                cells.append(ReportValueEditItem(parent, 
                                             samr, '%s_%s' % (age, fname)))
            cells.append(ReportAutoAdmissionTotal(parent, samr, age))
            
            data.append(cells)

    # Add SAM section
    if report.is_sam:
        # add blank line for SAM section header
        data.append(blank_line())

        # retrieve sam report
        samr = report.pec_sam_report
        #parent.

        for age in ('u59', 'o59', 'fu1'):

            cells = []
            cells.append(ReportAutoBeginingTotal(parent, samr, age))
            cells.append(ReportValueEditItem(parent, 
                                         samr, '%s_total_beginning_m' % age))
            cells.append(ReportValueEditItem(parent,
                                         samr, '%s_total_beginning_f' % age))
            cells.append(BlankCell(parent))
            cells.append(BlankCell(parent))
            for fname in ('hw_u70_bmi_u16', 'muac_u11_muac_u18',
                          'oedema', 'other'):
                cells.append(ReportValueEditItem(parent, 
                                             samr, '%s_%s' % (age, fname)))
            cells.append(ReportAutoAdmissionTotal(parent, samr, age))
            
            data.append(cells)

    # Add MAM section
    if report.is_mam:
        # add blank line for SAM section header
        data.append(blank_line())

        # retrieve sam report
        samr = report.pec_mam_report
        #parent.

        print('MAM REPORT: %s' % samr)

        for age in ('u59', 'pw', 'fu12'):

            cells = []
            cells.append(ReportAutoBeginingTotal(parent, samr, age))
            if age == 'pw':
                cells.append(BlankCell(parent))
            else:
                cells.append(ReportValueEditItem(parent, 
                                         samr, '%s_total_beginning_m' % age))
            cells.append(ReportValueEditItem(parent,
                                         samr, '%s_total_beginning_f' % age))

            cells.append(ReportValueEditItem(parent, 
                                             samr, '%s_%s' % (age, 'hw_b7080_bmi_u18')))

            cells.append(ReportValueEditItem(parent, 
                                             samr, '%s_%s' % (age, 'muac_u120')))

            cells.append(BlankCell(parent))
            cells.append(BlankCell(parent))
            cells.append(BlankCell(parent))

            cells.append(ReportValueEditItem(parent, 
                                             samr, '%s_%s' % (age, 'other')))

            cells.append(ReportAutoAdmissionTotal(parent, samr, age))
            
            data.append(cells)

    # add total line
    data.append([ColumnSumItem(parent, None, None) for x in range(0, cols)])

    return data

class ReportWidget(NUTWidget):

    title = u"Nutrition Monthly Report"
    report = None

    # Report U.I pages. Switch with next() previous()
    PEC_ADM_CRIT = 'pec_adm_crit'
    PEC_ADM_TYPE = 'pec_adm_type'
    PEC_OUT = 'pec_out'
    PEC_RECAP = 'pec_recap'
    CONS_ORDER = 'cons_order'
    PAGES = [PEC_ADM_CRIT, PEC_ADM_TYPE, PEC_OUT, PEC_RECAP, CONS_ORDER]

    def next(self):
        # can't go next if on last page
        if self.current_page == self.PAGES[-1]:
            return False

        ind = self.PAGES.index(self.current_page)
        return self.change_page(self.PAGES[ind + 1])

    def previous(self):
        # can't go next if on last page
        if self.current_page == self.PAGES[0]:
            return False

        ind = self.PAGES.index(self.current_page)
        return self.change_page(self.PAGES[ind - 1])

    def change_page(self, new_page):
        if not self.can_change_page():
            return False

        print('changing from %s to %s' % (self.current_page, new_page))
        
        # removes all widgets
        self.clear_vbox()
        
        # build new page UI
        self.build_ui(new_page)

        # set current page pointer
        self.current_page = new_page

        return True

    def clear_vbox(self):
        for i in range(self.vbox.count()): self.vbox.itemAt(i).widget().close()
        
    def get_widgets_for(self, page):

        return [self.table, self.title, self.intro]

    def build_ui(self, page):

        # launch build_xx method for page
        if page in self.PAGES:
            getattr(self, 'build_%s' % page.lower())()


    def can_change_page(self):
        # check if data validates
        # if YES, save and move
        # else trigger alert
        return True

    def __init__(self, parent=0, *args, **kwargs):

        if 'report' in kwargs:
            self.report = kwargs['report']
            del kwargs['report']

        super(ReportWidget, self).__init__(parent=parent, *args, **kwargs)

        self.init_timer = self.startTimer(0)

        self.vbox = QtGui.QVBoxLayout()

        self.continue_button = ContinueWidget(self)

        

    def build_pec_adm_crit(self, do=False):

        self.title = PageTitle(_(u"Rapport Statistique Mensuel - Traitement de la malnutrition aiguë") % self.report.period)
        self.intro = PageIntro(_(u"%(period)s") % {'period': self.report.period})

        # Table
        self.table = PECADMCRITReportTable(self, self.report, self.current_page)
        self.table.data = build_data_from(self.table, self.report, self.readonly)
        self.table.refresh()


        # page title
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.intro)
        self.vbox.addWidget(self.table)
        self.vbox.addStretch(50)
        self.vbox.addWidget(self.continue_button)

        # try to set layout (will silently fail if exist)
        self.setLayout(self.vbox)

        # set focus to username field
        self.setFocusProxy(self.table)

    def build_pec_adm_type(self):

        self.title = PageTitle(u"-")
        self.intro = PageIntro(_(u"%(period)s") % {'period': self.report.period})
        self.table = ReportTable(self, self.report, self.current_page, 8, 10)
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
                                            u"Suivi 1&2", u"TOTAL"])

        # page title
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.intro)
        self.vbox.addWidget(self.table)
        self.vbox.addStretch(50)

        # try to set layout (will silently fail if exist)
        self.setLayout(self.vbox)

        # set focus to username field
        self.setFocusProxy(self.table)
        

    def setup_report_ui(self):

        # ask User to select a period
        if not self.report:
            period_widget = self.open_dialog(ReportPeriodWidget)

        # report *should* be set by dialog.
        # if not, go back to Dashboard.
        if not self.report:
            QtGui.QMessageBox.warning(self, u"pas de periode", u"boo")
            self.change_main_context(DashboardWidget)
            return

        print(self.report.is_mam)
        print(self.report.is_sam)
        print(self.report.is_samp)

        # we now have a report, setup shortcuts
        self.pec_mam_report = self.report.pec_mam_report
        self.pec_sam_report = self.report.pec_sam_report
        self.pec_samp_report = self.report.pec_samp_report
        self.cons_mam_report = self.report.cons_mam_report
        self.cons_sam_report = self.report.cons_sam_report
        self.cons_samp_report = self.report.cons_samp_report
        self.order_mam_report = self.report.order_mam_report
        self.order_sam_report = self.report.order_sam_report
        self.order_samp_report = self.report.order_samp_report

        # setup default page
        self.current_page = self.PEC_ADM_CRIT


        # What do we display now?
        self.build_ui(self.current_page)


    @property
    def readonly(self):
        return not self.report.can_edit()

    # TODO: Return True
    @classmethod
    def require_logged_user(self):
        return False

    @classmethod
    def has_pagination(cls):
        return True

    def cancel_period_request(self):
        self.change_context(DashboardWidget)

    def timerEvent(self, event):
        self.killTimer(self.init_timer)
        self.setup_report_ui()

