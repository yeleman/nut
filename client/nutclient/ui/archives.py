#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from PyQt4 import QtGui, QtCore

from common import (NUTWidget, PageTitle, PageIntro, InfoTable,
                    LinkButton, PageSection, fixed_size_table, 
                    FlexibleReadOnlyTable, FlexibleReadOnlyWidget)
from database import Report, InputOrderReport


class PECTable(FlexibleReadOnlyTable):

    def __init__(self, parent, report):
        super(PECTable, self).__init__(parent)

        self.data.append((report.all_total_beginning,
                          report.all_total_admitted,
                          report.all_total_out,
                          report.all_total_end))
        self.hheaders = [u"Début mois", u"Admissions",
                         u"Sorties", u"Fin du mois"]
        #self.display_vheaders = False
        self.vheaders = [u"PRISE EN CHARGE"]
        self.stretch_columns = [0,]
        self.max_rows = 1
        self.refresh()


class CONSOTable(FlexibleReadOnlyTable):

    def __init__(self, parent, report, order_report):
        super(CONSOTable, self).__init__(parent)

        for icr in report.nutinput_reports:

            ior = InputOrderReport.filter(order_report=order_report,
                                          nut_input=icr.nut_input).get()
            self.vheaders.append(icr.nut_input.name.upper())
            self.data.append((icr.initial,
                              icr.received,
                              icr.used,
                              icr.lost,
                              icr.left,
                              ior.quantity))
        self.hheaders = [u"Début mois", u"Reçus",
                         u"Utilisés", u"Perdus",
                         u"Restants", u"Commandés"]
        self.refresh()


class ReportPreview(QtGui.QDialog, NUTWidget):

    def __init__(self, report, parent=0, *args, **kwargs):

        QtGui.QWidget.__init__(self, parent)

        self.resize(600, 400)

        self.report = report
        
        self.setWindowTitle(u"Aperçu du rapport %(period)s (%(status)s)" % {'period': self.report.period, 'status': self.report.verbose_status()})

        self.intro = PageIntro(u"Ci-dessous, un aperçu des données du rapport.")

        vbox = QtGui.QVBoxLayout()

        # page title
        vbox.addWidget(self.intro)

        for cap in self.report.caps():

            if not getattr(self.report, 'is_%s' % cap):
                continue

            # PEC TABLE
            section = QtGui.QGroupBox(cap.upper(), self) #PageSection(cap.upper())
            section_box = QtGui.QVBoxLayout()

            pec_table = PECTable(self, getattr(self.report, 'pec_%s_report' % cap))
            conso_table = CONSOTable(self, 
                                     getattr(self.report, 'cons_%s_report' % cap),
                                     getattr(self.report, 'order_%s_report' % cap))

            section_box.addWidget(pec_table)
            section_box.addWidget(conso_table)
            section_box.addStretch(50)
            section.setLayout(section_box)

            vbox.addWidget(section)
            
        
        self.setLayout(vbox)


class ArchivesTable(FlexibleReadOnlyTable):

    def __init__(self, parent):

        def edit_report(ident):
            from report import ReportWidget
            self.parentWidget().change_main_context(ReportWidget, 
                                                    report=Report.filter(id=ident).get())

        def preview(ident):
            self.parentWidget().open_dialog(ReportPreview,
                                            modal=True,
                                            report=Report.filter(id=ident).get())

        super(ArchivesTable, self).__init__(parent)

        self.hheaders = [u"Période",
                        u"Statut",
                        u"UREN",
                        u"Dernière modif.",
                        u"PEC début",
                        u"PEC fin",
                        u"Aperçu",
                        u"Éditer"]

        for report in Report.select():
            self.data.append((report.period.__unicode__(),
                           report.verbose_status(),
                           report.verbose_caps(),
                           report.modified_on.strftime('%d %B, %H:%M'),
                           report.sum_for_field('all_total_beginning'),
                           report.sum_for_field('all_total_end'),
                           LinkButton(u"Aperçu", preview, report.id),
                           LinkButton(u"Éditer", edit_report, report.id)))
        
        self.display_vheaders = False
        self.stretch_columns = [0,]
        self.align_map = {0: 'l', 1: 'l'}
        self.refresh()


class ArchivesWidget(NUTWidget):

    title = u"Archives"

    def __init__(self, parent=0, *args, **kwargs):

        super(ArchivesWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        self.title = PageTitle(u"Archives des rapports")
        self.intro = PageIntro(u"")

        self.table = ArchivesTable(self)

        vbox.addWidget(self.title)
        vbox.addWidget(self.table)
        vbox.addStretch(50)


        self.setLayout(vbox)
