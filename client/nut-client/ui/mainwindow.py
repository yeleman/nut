#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from PyQt4 import QtGui, QtCore

from dashboard import DashboardWidget
from menu import *
from statusbar import REDEStatusBar

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(900, 650)
        self.setWindowTitle(_(u"Remote Excel Data Entry"))
        self.setWindowIcon(QtGui.QIcon('images/icon32.png'))

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.QCoreApplication.translate('', "Ctrl+q")), self, self.close)

        self.menu = MainMenu(self)
        self.menu.build()
        self.addToolBar(self.menu)

        self.statusbar = REDEStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.change_context(DashboardWidget)

    def change_context(self, context_widget, *args, **kwargs):

        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # attach context to window
        self.setCentralWidget(self.view_widget)
        self.view_widget.setFocus()

    def change_context_id(self, context_id, *args, **kwargs):
        contexts = {'help': {'widget': DashboardWidget, 'menu': None}}
        self.change_context(contexts[context_id]['widget'], args, kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        d = dialog(parent=self, *args, **kwargs)
        d.setModal(modal)
        d.exec_()
