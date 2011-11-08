#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4 import QtGui, QtCore

from common import REDEWidget, PageTitle, FormLabel, IntLineEdit


class SIM_managementWidget(REDEWidget):
    """Pöur la recharge de la carte SIM
    """

    def __init__(self, parent=0, *args, **kwargs):

        super(SIM_managementWidget, self).__init__(parent=parent,
                                                        *args, **kwargs)

        vbox = QtGui.QVBoxLayout()
        # Le titre
        self.label = PageTitle(_(u"Reload SIM card."))
        vbox.addWidget(self.label)

        self.carte_number = IntLineEdit()
        self.cb = QtGui.QCheckBox()
        self.combo = QtGui.QComboBox(self)
        self.combo.addItem(u"Orange")
        self.combo.addItem(u"Malitel")
        self.button = QtGui.QPushButton(_(u"ok"))

        # Grid
        gridbox = QtGui.QGridLayout()
        gridbox.addWidget(FormLabel(_(u"Number of the SIM card")), 0, 1)
        gridbox.addWidget(self.carte_number, 0, 2)
        gridbox.addWidget(FormLabel(_(u"Internet package everywere")), 1, 1)
        gridbox.addWidget(self.cb, 1, 2)
        gridbox.addWidget(FormLabel(_(u"Operator")), 2, 1)
        gridbox.addWidget(self.combo, 2, 2)
        gridbox.addWidget(self.button, 3, 2)
        # Agrandir la taille de la colonne 3
        gridbox.setColumnStretch(3, 1)
        # Agrandir la taille de la ligne 3
        gridbox.setRowStretch(5, 10)

        vbox.addLayout(gridbox)
        self.setLayout(vbox)
