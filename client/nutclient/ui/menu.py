#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore, Qt

from dashboard import DashboardWidget
from report import ReportWidget
from help import HelpWidget
from sim_management import SIMManagementWidget
from preferences import PreferencesWidget
from archives import ArchivesWidget


class NUTMenu(QtGui.QToolBar):

    def __init__(self, parent):

        QtGui.QToolBar.__init__(self, parent)

        self.parent = parent

        self.setMovable(False)
        self.setToolButtonStyle(0)

        self._items = []
        self.has_pagination = False

    @property
    def ident(self):
        return None

    @property
    def items(self):
        return []

    def setPagination(self, activate):
        self.has_pagination = activate
        self.build()

    def build(self):
        self.clear()
        for item in self.items():
            icon = QtGui.QIcon(QtGui.QPixmap("images/f%d.png" % item.shortcut))
            btn = ToolBarButton(self)
            btn.setToolButtonStyle(2)
            action = QtGui.QAction(icon, item.name, self)
            action.setEnabled(item.enabled)
            action.setToolTip(item.description)
            btn.setDefaultAction(action)
            btn.setTarget(item.action)
            self.addWidget(btn)
            self.SHORTCUTS[eval('QtCore.Qt.Key_F%d'
                                % item.shortcut)] = item.action

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
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.QCoreApplication.translate('', "Ctrl+q")), self, self.quit)

        self.SHORTCUTS = {}

    def ident(self):
        return 'main'

    def items(self):
        return [
            NUTMenuItem(1, u"Tableau de bord", self.dashboard, u"Tableau de bord"),
            NUTMenuItem(2, u"Archives", self.archives, u"Liste des rapports créés et envoyés"),
            NUTMenuItem(3, u"Rapport", self.data_entry, u"Créer (ou reprendre) le rapport courant"),
            NUTMenuItem(5, u"↢", self.previous, u"Page précédente", self.has_pagination),
            NUTMenuItem(6, u"↣", self.next, u"Page suivante", self.has_pagination),
            NUTMenuItem(8, u"Gestion SIM", self.sim_mgmt, u"Gestion du crédit téléphone"),
            NUTMenuItem(9, u"Options", self.preferences, u"Regler les paramètres"),
            #NUTMenuItem(10, u"?", self.whatis, u"Obtenir des informations sur un élément"),
            NUTMenuItem(11, u"Aide", self.help),
            NUTMenuItem(12, u"Quitter", self.quit, u"Quitter et éteindre la machine"),
        ]

    def dashboard(self):
        self.parent.change_context(DashboardWidget)

    def archives(self):
        self.parent.change_context(ArchivesWidget)

    def help(self):
        #self.parent.change_context(HelpWidget, 
        self.parentWidget().open_dialog(HelpWidget,
                                   topic=self.parent.view_widget \
                                             .__class__.__name__ \
                                             .lower().replace('widget', ''))

    def next(self):
        if hasattr(self.parent.view_widget, 'next'):
            return self.parent.view_widget.next()

    def previous(self):
        if hasattr(self.parent.view_widget, 'previous'):
            return self.parent.view_widget.previous()

    def data_entry(self):
        self.parent.change_context(ReportWidget)

    def sim_mgmt(self):
        self.parent.change_context(SIMManagementWidget)

    def preferences(self):
        self.parent.change_context(PreferencesWidget)

    def quit(self):
        if self.parent.view_widget.prevent_close():
            if self.parent.view_widget.attempt_close():
                self.parent.close()
        else:
            self.parent.close()

    def whatis(self):
        if QtGui.QWhatsThis.inWhatsThisMode():
            QtGui.QWhatsThis.leaveWhatsThisMode()
        else:
            QtGui.QWhatsThis.enterWhatsThisMode()

class NUTMenuItem:

    def __init__(self, shortcut, name, action,
                 description=None, enabled=True, *action_args):
        self.name = name
        self.action = action
        self.shortcut = shortcut
        self.enabled = enabled
        self.description = description if description else name
        self.action_args = action_args
