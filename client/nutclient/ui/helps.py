#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui

from common import NUTWidget, PageTitle, PageIntro


class HelpWidget(QtGui.QDialog, NUTWidget):

    def __init__(self, parent=0, topic=None, *args, **kwargs):

        super(HelpWidget, self).__init__(parent=parent, *args, **kwargs)

        self.topic = topic

        self.resize(600, 400)
        self.setWindowTitle(u"Aide – Système Nutrition")

        vbox = QtGui.QVBoxLayout()
        self.title = PageTitle(u"Aide – Système Nutrition")
        vbox.addWidget(self.title)
        vbox.addWidget(self.get_content(topic))

        vbox.addStretch(50)
        self.setLayout(vbox)

    def get_content(self, topic):
        intro = {'general': u"Aide générale",
                 'login': u"Tapez ",
                 'dashboard': u"Le tableau de bord présente la liste des derniers événnements."}
        if intro.has_key(topic):
            if isinstance(topic, basestring):
                return PageIntro(intro[topic])
            else:
                return intro[topic]
        else:
            return GeneralHelpWidget()

    @classmethod
    def require_logged_user(cls):
        return False


class GeneralHelpWidget(NUTWidget):

    def __init__(self, parent=0):
        super(GeneralHelpWidget, self).__init__(parent)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(PageIntro(u"Aide générale à développer."))
        vbox.addStretch(50)
        self.setLayout(vbox)
