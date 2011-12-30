#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore, Qt

from dashboard import DashboardWidget
from report import ReportWidget
from send import SendWidget
from helps import HelpWidget
from sim_management import SIM_managementWidget
from data_entry import DataEntryWidget
from preferences import PreferencesWidget


class NUTMenu(QtGui.QToolBar):

    def __init__(self, parent):

        QtGui.QToolBar.__init__(self, parent)

        self.parent = parent

        self.setMovable(False)
        self.setToolButtonStyle(0)

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
            btn.setToolButtonStyle(2)
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
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def setTarget(self, func):
        self._target = func

    def mouseReleaseEvent(self, event):
        QtGui.QToolButton.mouseReleaseEvent(self, event)
        if self._target:
            self._target.__call__()


class MainMenu(NUTMenu):

    def __init__(self, parent):
        NUTMenu.__init__(self, parent)

    def ident(self):
        return 'main'

    def items(self):
        return [
            NUTMenuItem(1, _(u"Dashboard"), self.dashboard),
            NUTMenuItem(2, _(u"Archives"), self.help),
            NUTMenuItem(3, _(u"Data Entry"), self.data_entry),
            #NUTMenuItem(5, _(u"Previous"), self.previous),
            #NUTMenuItem(6, _(u"Next"), self.next),
            NUTMenuItem(8, _(u"SIM Mgmt"), self.sim_mgmt),
            NUTMenuItem(9, _(u"Options"), self.preferences),
            #NUTMenuItem(10, _(u"Send"), self.send),
            NUTMenuItem(11, _(u"Help"), self.help),
            NUTMenuItem(12, _(u"Quit"), self.quit),
        ]

    def dashboard(self):
        self.parent.change_context(DashboardWidget)

    def help(self):
        self.parent.change_context(HelpWidget, topic=self.parent.view_widget.__class__.__name__.lower().replace('widget', ''))

    def next(self):
        print "next"

    def previous(self):
        print "previous"

    def data_entry(self):
        self.parent.change_context(ReportWidget)

    def sim_mgmt(self):
        self.parent.change_context(SIM_managementWidget)

    def preferences(self):
        self.parent.change_context(PreferencesWidget)

    def send(self):
        self.parent.setWindowTitle(_(u"Send"))
        self.parent.change_context(SendWidget)

    def quit(self):
        self.parent.close()
        pass


class NUTMenuItem:

    def __init__(self, shortcut, name, action, *action_args):
        self.name = name
        self.action = action
        self.shortcut = shortcut
        self.action_args = action_args
