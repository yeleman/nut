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


class ReportWidget(NUTWidget):

    title = u"Nutrition Monthly Report"
    report = None

    # Report U.I pages. Switch with next() previous()
    PEC_ADM_CRIT = 'pec_adm_crit'
    PEC_ADM_TYP = 'pec_adm_typ'
    PEC_OUT = 'pec_out'
    PEC_RECAP = 'pec_recap'
    CONS_ORDER = 'cons_order'
    PAGES = [PEC_ADM_CRIT, PEC_ADM_TYP, PEC_OUT, PEC_RECAP, CONS_ORDER]

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
            QtGui.QMessageBox.warning(self, u"Impossible de changer de page.",
                              u"Les données en cours ne sont pas correctes." \
                              u"\nVous devez les corriger pour continuer."),
            return False

        print('changing from %s to %s' % (self.current_page, new_page))
        
        index = self.PAGES.index(new_page)
        self.stacked_table.setCurrentIndex(index)
        self.table.load_data(self.readonly)
        self.table.refresh()

        # set current page pointer
        self.current_page = new_page

        return True

    @property
    def table(self):
        return self.stacked_table.currentWidget().table

    @property
    def instructions(self):
        return self.stacked_table.currentWidget().instructions

    def clear_vbox(self):
        return
        for i in range(self.vbox.count()):
            w = self.vbox.itemAt(i).widget()
            if hasattr(w, 'close'):
                w.close()
        
    def get_widgets_for(self, page):

        return [self.table, self.title, self.intro]

    def build_ui(self):

        self.stacked_table = QtGui.QStackedWidget()

        for lpage in self.PAGES:
            self.stacked_table.addWidget(getattr(self, 'build_%s' % lpage.lower())(lpage))

        self.current_page = self.PAGES[0]
        self.table.load_data(self.readonly)
        self.table.refresh()

        self.continue_button = ContinueWidget(self)
        #self.continue_button.clicked.connect(self.next)
        self.vbox.addWidget(self.stacked_table)
        self.vbox.addStretch(100)
        #self.vbox.addWidget(self.continue_button)

    def can_change_page(self):
        # check if data validates
        # if YES, save and move
        # else trigger alert
        return self.save_and_validate_current_page()

    def save_and_validate_current_page(self):
        
        if self.current_page in (self.PEC_ADM_CRIT, self.PEC_ADM_TYP):
            if self.table.validate():
                self.table.save()
                return True
            else:
                return False

        # don't know where we at
        return False
            

    def __init__(self, parent=0, *args, **kwargs):

        if 'report' in kwargs:
            self.report = kwargs['report']
            del kwargs['report']

        super(ReportWidget, self).__init__(parent=parent, *args, **kwargs)

        self.init_timer = self.startTimer(0)

        self.vbox = QtGui.QVBoxLayout()

        self.setLayout(self.vbox)

    def build_pec_adm_crit(self, page):

        widget = NUTWidget(self)
        vbox = QtGui.QVBoxLayout()
        title = PageTitle(_(u"Rapport Statistique Mensuel - Traitement de la malnutrition aiguë") % self.report.period)
        intro = PageIntro(_(u"%(period)s – PRISE EN CHARGE: Critère d'admissions") % {'period': self.report.period})

        # Table
        widget.table = PECADMCRITReportTable(widget, self.report, page)
        
        widget.instructions = PECADMCRITInstructions(self, widget.table, self.report, page)

        widget.setFocusProxy(widget.table)

        vbox.addWidget(title)
        vbox.addWidget(intro)
        vbox.addWidget(widget.table)
        vbox.addWidget(widget.instructions)
        vbox.addStretch(50)
        widget.setLayout(vbox)

        return widget

    def build_pec_adm_typ(self, page):

        widget = NUTWidget(self)
        vbox = QtGui.QVBoxLayout()

        title = PageTitle(_(u"Rapport Statistique Mensuel - Traitement de la malnutrition aiguë") % self.report.period)
        intro = PageIntro(_(u"%(period)s – PRISE EN CHARGE: Type d'admissions") % {'period': self.report.period})

        widget.table = PECADMTYPReportTable(widget, self.report, page)
        widget.instructions = PECADMTYPInstructions(self, widget.table, self.report, page)

        vbox.addWidget(title)
        vbox.addWidget(intro)
        vbox.addWidget(widget.table)
        vbox.addWidget(widget.instructions)
        vbox.addStretch(50)
        widget.setLayout(vbox)

        return widget

    def build_pec_out(self, page):
        widget = NUTWidget(self)
        vbox = QtGui.QVBoxLayout()

        title = PageTitle(_(u"Rapport Statistique Mensuel - Traitement de la malnutrition aiguë") % self.report.period)
        intro = PageIntro(_(u"%(period)s – PRISE EN CHARGE: Type d'admissions") % {'period': self.report.period})

        widget.table = PECOUTReportTable(widget, self.report, page)
        widget.instructions = PECOUTInstructions(self, widget.table, self.report, page)

        vbox.addWidget(title)
        vbox.addWidget(intro)
        vbox.addWidget(widget.table)
        vbox.addWidget(widget.instructions)
        vbox.addStretch(50)
        widget.setLayout(vbox)
        return widget

    def build_pec_recap(self, page):
        widget = NUTWidget(self)
        vbox = QtGui.QVBoxLayout()
        widget.setLayout(vbox)
        return widget

    def build_cons_order(self, page):
        widget = NUTWidget(self)
        vbox = QtGui.QVBoxLayout()
        widget.setLayout(vbox)
        return widget

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
        self.build_ui()


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

