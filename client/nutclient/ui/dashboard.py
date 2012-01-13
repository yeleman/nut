#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui

from common import (NUTWidget, PageTitle, PageIntro, PageSection,
                    LinkButton, FlexibleReadOnlyTable)
from database import Report, Message


class InProgressTable(FlexibleReadOnlyTable):

    def __init__(self, parent):
        super(InProgressTable, self).__init__(parent)

        def edit_report(ident):
            from report import ReportWidget
            self.parentWidget().change_main_context(ReportWidget, 
                                     report=Report.filter(id=ident).get())

        date_fmt = '%d %B, %Hh%M'
        for report in Report.opened():               
            self.data.append((report.verbose_status(),
                              report.__unicode__(),
                              report.created_on.strftime(date_fmt),
                              report.modified_on.strftime(date_fmt),                            
                              LinkButton(u"Éditer", edit_report, report.id)))
        self.hheaders = [u"Statut", u"Rapport", 
                         u"Créé le", u"Modifié le", u"Action"]
        self.stretch_columns = [1,]
        self.align_map = {0: 'l', 1: 'l'}
        self.max_rows = 5
        self.refresh()

class MessagesTable(FlexibleReadOnlyTable):

    def __init__(self, parent):
        super(MessagesTable, self).__init__(parent)

        date_fmt = '%d %B, %Hh%M'
        for message in Message.select().order_by(('date', 'desc')).limit(10):
            self.data.append((message.date.strftime('%d %B, %Hh%M'),
                              message.identity,
                              message.text))
        self.hheaders = [u"Date", u"From", u"Message"]
        self.display_vheaders = False
        self.stretch_columns = [2,]
        self.max_rows = 8
        self.align_map = {0: 'l', 1: 'l', 2:'l'}
        self.refresh()


class DashboardWidget(NUTWidget):

    title = u"Dashboard"

    def __init__(self, parent=0, *args, **kwargs):

        super(DashboardWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        self.title = PageTitle(_(u"Résumé"))
        self.title = PageTitle(u"%(user)s de %(hc)s/%(hcc)s (%(hccap)s)" \
                             % {'user': self.user,
                                'hc': self.user.hc,
                                'hcc': self.user.hc_code,
                                'hccap': self.user.verb_caps()})


        self.in_progress_label = PageSection(u"En cours")

        self.in_progress_table = InProgressTable(self)
        
        self.messages_label = PageSection(u"Derniers messages")
        self.messages_table = MessagesTable(self)

        vbox.addWidget(self.title)
        vbox.addWidget(self.in_progress_label)
        vbox.addWidget(self.in_progress_table)

        vbox.addWidget(self.messages_label)
        vbox.addWidget(self.messages_table)
        vbox.addStretch(50)
        


        self.setLayout(vbox)
