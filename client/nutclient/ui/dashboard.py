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
      self.title = PageTitle(_(u"Résumé"))
      self.intro = PageIntro(u"Welcome %(user)s, %(hc)s (%(hccap)s)" \
                           % {'user': self.user,
                              'hc': self.user.hc,
                              'hccap': self.user.verb_caps()})


      self.in_progress_label = QtGui.QLabel(u"En cours")
      self.in_progress_table = QtGui.QTableWidget(1, 4, self)
      self.in_progress_table.setHorizontalHeaderLabels([u"Rapport", u"Statut", u"Créé le", u"Modifié le"])
      
      self.last_events_label = QtGui.QLabel(u"Derniers évennements")
      self.last_events_table = QtGui.QTableWidget(4, 4, self)
      self.last_events_table.setHorizontalHeaderLabels([u"Évennement", u"Date"])

      self.messages_label = QtGui.QLabel(u"Derniers évennements")
      self.messages_table = QtGui.QTableWidget(4, 2, self)
      self.messages_table.setHorizontalHeaderLabels([u"Date", u"Message"])

      vbox.addWidget(self.title)
      vbox.addWidget(self.intro)
      vbox.addWidget(self.in_progress_label)
      vbox.addWidget(self.in_progress_table)
      vbox.addWidget(self.last_events_label)
      vbox.addWidget(self.last_events_table)
      vbox.addWidget(self.messages_label)
      vbox.addWidget(self.messages_table)


      self.setLayout(vbox)
