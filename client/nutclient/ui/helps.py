#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui

from common import NUTWidget, PageTitle, PageIntro


class HelpWidget(NUTWidget):

    title = u"Help"

    def __init__(self, parent=0, topic=None, *args, **kwargs):

        super(HelpWidget, self).__init__(parent=parent, *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        
        self.title = PageTitle(_(u"Help"))
        vbox.addWidget(self.title)

        vbox.addWidget(self.get_content(topic))
        self.topic = topic

        self.setLayout(vbox)

    def get_content(self, topic):
        intro = {'general': _(u"General HELP"),
                 'login': _(u"Type in your username and blabla"),
                 'dashboard': _(u"List of recent events")}
        if intro.has_key(topic):
            return PageIntro(intro[topic])
        else:
            return PageIntro(intro['general'])

    @classmethod
    def require_logged_user(cls):
        return False
