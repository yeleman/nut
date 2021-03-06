#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin
import weakref
import gc

from datetime import date, datetime

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

from utils import send_report
from common import *
from nutclient.exceptions import *
from nutclient.utils import offline_login
from dashboard import DashboardWidget
from database import Report, Period


class ReportPeriodWidget(QtGui.QDialog, NUTWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent)

        self.parent = parent

        self.setWindowTitle(u"Période des données")

        self.title = PageTitle(u"Indiquez la période correspondante.")
        self.intro = PageIntro(u"Indiquez ci-dessous la période (mois et " \
                                 u"année qui correspond aux données.\n" \
                                 u"Cela doit être le mois passé.\n\n" \
                                 u"Vous ne pouvez pas saisir les données du " \
                                 u"rapport sans renseigner la période.")

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
        self.confirm_button = QtGui.QPushButton(u"&Continuer")
        self.confirm_button.setAutoDefault(True)
        self.confirm_button.clicked.connect(self.confirm)

        # cancel closes window
        self.cancel_button = QtGui.QPushButton(u"&Annuler")
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

    title = u"Rapport Statistique Mensuel"
    report = None

    # Report U.I pages. Switch with next() previous()
    PEC_ADM_CRIT = 'pec_adm_crit'
    PEC_ADM_TYP = 'pec_adm_typ'
    PEC_OUT = 'pec_out'
    PEC_RECAP = 'pec_recap'
    CONS_ORDER = 'cons_order'
    PAGES = [PEC_ADM_CRIT, PEC_ADM_TYP, PEC_OUT, PEC_RECAP, CONS_ORDER]

    def prevent_close(self):
        return True
    
    def attempt_close(self):
        # don't bother if there's not Report
        if not self.report:
            return True

        resp = QtGui.QMessageBox.question(self, u"Voulez-vous quitter ?",
                            u"Si vous quitter l'édition du rapport maintenant,"
                            u" vos modfications sur cette page seront perdues."
                            u"\n\nQuitter le rapport ?",
                            QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                            QtGui.QMessageBox.Cancel)
        if resp == QtGui.QMessageBox.Ok:
            self.report = None
            return True
        else:
            return False

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
        if (self.PAGES.index(new_page)
            >= self.PAGES.index(self.current_page)):
            if not self.can_change_page():
                QtGui.QMessageBox.warning(self, u"Impossible de changer de page.",
                                u"Les données en cours ne sont pas correctes."
                                u"\nVous devez les corriger pour continuer.")
                return False

        print('changing from %s to %s' % (self.current_page, new_page))
        
        # close previous properly
        self.instructions.stop()

        index = self.PAGES.index(new_page)
        self.stacked_table.setCurrentIndex(index)
        self.table.load_data(self.readonly)
        self.table.refresh()
        self.instructions.start()

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
            self.stacked_table.addWidget(getattr(self, 'build_%s' 
                                                       % lpage.lower())(lpage))

        self.current_page = self.PAGES[0]
        self.table.load_data(self.readonly)
        self.table.refresh()
        self.instructions.start()

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
        # don't bother on read only
        if self.readonly:
            return True
        if self.current_page in (self.PEC_ADM_CRIT, 
                                 self.PEC_ADM_TYP,
                                 self.PEC_OUT, self.PEC_RECAP, self.CONS_ORDER):
            if self.table.validate():
                self.report.touch()
                self.table.save()
                # check completeness on last page
                if self.current_page == self.PAGES[-1]:
                    if self.report.is_valid():
                        self.report.mark_as_complete()
                        return True
                    else:
                        return False
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

    def save(self):
        if not self.save_and_validate_current_page():
            QtGui.QMessageBox.warning(self, u"Impossible d'enregistrer.",
                              u"Impossible d'enregistrer "
                              u"les données. Les données ne sont pas correctes."
                              u"\nVous devez les corriger pour re-essayer."),
            return False
        return True

    def transmit(self):
        # disable send button to prevent accidental double sending
        self.transmit_button.disable()

        if not self.save_and_validate_current_page():
            QtGui.QMessageBox.warning(self, u"Impossible de transmettre.",
                              u"Impossible de transmettre "
                              u"le rapport. Les données ne sont pas correctes."
                              u"\nVous devez les corriger pour re-essayer.")
            self.transmit_button.enable()
            return False

        if send_report(self.report, self.user):
            QtGui.QMessageBox.information(self, u"Transmission en cours...",
                                                u"Le rapport est en cours de "
                                                u"Transmission.\n\n"
                                                u"Veuillez attendre la "
                                                u"confirmation du serveur.")
            return True
        return False

    def build_default_layout(self, page):

        titles = {self.PEC_ADM_CRIT: u"PRISE EN CHARGE: Critère d'admissions",
                  self.PEC_ADM_TYP: u"PRISE EN CHARGE: Type d'admissions",
                  self.PEC_OUT: u"PRISE EN CHARGE: Sorties",
                  self.PEC_RECAP: u"PRISE EN CHARGE: Récapitulatif",
                  self.CONS_ORDER: u"Consommation/commande d'intrants"}
        pname = page.upper().replace('_', '')
        table_widget = eval('%sReportTable' % pname)
        instr_widget = eval('%sInstructions' % pname)

        widget = NUTWidget(self)
        vbox = QtGui.QVBoxLayout()
       
        title = PageIntro(u"<b>Rapport de %(period)s</b>. %(title)s – "
                          u"<b>%(cur)d/%(tot)d</b>" 
                          % {'period': self.report.period,
                             'title': titles[page],
                             'cur': self.PAGES.index(page) + 1,
                             'tot': len(self.PAGES)})

        # Table
        widget.table = table_widget(widget, self.report, page)
        
        widget.instructions = instr_widget(self, widget.table, self.report, page)

        widget.setFocusProxy(widget.table)

        head_box = QtGui.QHBoxLayout()
        if page == self.PAGES[-1]:
            self.transmit_button = TransmitButton()
            self.transmit_button.clicked.connect(self.transmit)
            if not self.report.can_send:
                self.transmit_button.disable()
        else:
            self.transmit_button = SaveButton()
            self.transmit_button.clicked.connect(self.save)
            if self.readonly:
                self.transmit_button.disable()
        head_line = QtGui.QWidget()
        head_box.addWidget(title)
        head_box.addStretch()
        head_box.addWidget(self.transmit_button)
        head_line.setLayout(head_box)
        vbox.addWidget(head_line)

        vbox.addWidget(widget.table)

        if page == self.PEC_RECAP:
            others_box = QtGui.QHBoxLayout()

            others_label = BoldLabel(u"Spécifier Autres:")

            widget.others_tb_field = ReportValueEdit(widget, None, self.report, 'others_tb')
            others_tb_label = BoldLabel(u"Tuberculeux")
            others_tb_label.setBuddy(widget.others_tb_field)

            widget.others_hiv_field = ReportValueEdit(widget, None, self.report, 'others_hiv')
            others_hiv_label = BoldLabel(u"PV VIH")
            others_hiv_label.setBuddy(widget.others_hiv_field)

            widget.others_lwb_field = ReportValueEdit(widget, None, self.report, 'others_lwb')
            others_lwb_label = BoldLabel(u"Petits poids de naissance")
            others_lwb_label.setBuddy(widget.others_lwb_field)

            others_line = QtGui.QWidget()
            others_box.addWidget(others_label)
            others_box.addWidget(others_tb_label)
            others_box.addWidget(widget.others_tb_field)
            others_box.addWidget(others_hiv_label)
            others_box.addWidget(widget.others_hiv_field)
            others_box.addWidget(others_lwb_label)
            others_box.addWidget(widget.others_lwb_field)
            others_box.addStretch()
            others_line.setLayout(others_box)

            vbox.addWidget(others_line)

        vbox.addWidget(widget.instructions)
        vbox.addStretch(50)
        widget.setLayout(vbox)

        return widget
        

    def build_pec_adm_crit(self, page):
        return self.build_default_layout(page)

    def build_pec_adm_typ(self, page):
        return self.build_default_layout(page)

    def build_pec_out(self, page):
        return self.build_default_layout(page)

    def build_pec_recap(self, page):
        return self.build_default_layout(page)

    def build_cons_order(self, page):
        return self.build_default_layout(page)

    def setup_report_ui(self):

        # ask User to select a period
        if not self.report:
            self.open_dialog(ReportPeriodWidget)

        # report *should* be set by dialog.
        # if not, go back to Dashboard.
        if not self.report:
            self.change_main_context(DashboardWidget)
            return

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

    @classmethod
    def require_logged_user(self):
        return True

    @classmethod
    def has_pagination(cls):
        return True

    def cancel_period_request(self):
        self.change_context(DashboardWidget)

    def timerEvent(self, event):
        self.killTimer(self.init_timer)
        self.setup_report_ui()

