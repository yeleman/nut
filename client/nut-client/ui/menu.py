#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore, Qt

from send import SendWidget
from helps import HelpWidget
from sim_management import SIM_managementWidget
from data_entry import DataEntryWidget
from preferences import PreferencesWidget


class REDEMenu(QtGui.QToolBar):

    def __init__(self, parent):

        QtGui.QToolBar.__init__(self, parent)

        self.parent = parent

        self._items = []

    @property
    def ident(self):
        return None

    @property
    def items(self):
        return []

    def build(self):
        self.clear()
        for item in self.items():
            icon = QtGui.QIcon(QtGui.QPixmap("images/f%d.png" % item.shortcut))
            btn = ToolBarButton(self)
            btn.setDefaultAction(QtGui.QAction(icon, item.name, self))
            btn.setTarget(item.action)
            self.addWidget(btn)
            QtGui.QShortcut(QtGui.QKeySequence(QtCore\
                                 .QCoreApplication.translate('', "F%d" \
                                 % item.shortcut)), self, item.action)

    def goto(self, action):
        pass


class ToolBarButton(QtGui.QToolButton):

    def __init__(self, parent):
        QtGui.QToolButton.__init__(self, parent)
        self.setToolButtonStyle(2)
        self._target = None

    def setTarget(self, func):
        self._target = func

    def mouseReleaseEvent(self, event):
        QtGui.QToolButton.mouseReleaseEvent(self, event)
        if self._target:
            self._target.__call__()


class MainMenu(REDEMenu):

    def __init__(self, parent):
        REDEMenu.__init__(self, parent)

    def ident(self):
        return 'main'

    def items(self):
        return [
            REDEMenuItem(1, _(u"Help"), self.help),
            REDEMenuItem(2, _(u"Next"), self.next),
            REDEMenuItem(3, _(u"Previous"), self.previous),
            REDEMenuItem(4, _(u"Data Entry"), self.data_entry),
            REDEMenuItem(5, _(u"SIM Management"), self.sim_mgmt),
            REDEMenuItem(6, _(u"Send"), self.send),
            REDEMenuItem(7, _(u"Preferences"), self.preferences),
            REDEMenuItem(12, _(u"Quit"), self.quit),
        ]

    def help(self):
        print "help"
        self.parent.change_context(HelpWidget)

    def next(self):
        print "next"

    def previous(self):
        print "previous"

    def data_entry(self):
        print "data entry"
        self.parent.setWindowTitle(_(u"Data Entry"))
        self.parent.change_context(DataEntryWidget)

    def sim_mgmt(self):
        print "sim"
        self.parent.setWindowTitle(_(u"SIM Management"))
        self.parent.change_context(SIM_managementWidget)

    def preferences(self):
        print "pref"
        self.parent.setWindowTitle(_(u"Preferences"))
        self.parent.change_context(PreferencesWidget)

    def send(self):
        self.parent.setWindowTitle(_(u"Send"))
        self.parent.change_context(SendWidget)

    def quit(self):
        self.parent.close()
        pass


class REDEMenuItem:

    def __init__(self, shortcut, name, action, *action_args):
        self.name = name
        self.action = action
        self.shortcut = shortcut
        self.action_args = action_args
