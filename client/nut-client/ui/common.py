#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

MAIN_WIDGET_SIZE = 900


class REDEWidget(QtGui.QWidget):

    def __init__(self, parent=0, *args, **kwargs):

        QtGui.QWidget.__init__(self, parent=parent, *args, **kwargs)

        self.setMaximumWidth(MAIN_WIDGET_SIZE)

    def refresh(self):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        return self.parentWidget()\
                          .change_context(context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.parentWidget().open_dialog(dialog, \
                                               modal=modal, *args, **kwargs)

class PageTitle(QtGui.QLabel):
    """ Formatage du titre de page """

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 16)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)


class PageIntro(QtGui.QLabel):
    """ Formatage de l'introduction de page """

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 12)
        self.setAlignment(Qt.AlignLeft)


class FormLabel(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft)


class IntLineEdit(QtGui.QLineEdit):
    """Accepter que des nombre positive """

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.setValidator(QtGui.QIntValidator(0, 100000, self))


class FloatLineEdit(QtGui.QLineEdit):
    """ Accepter que des nombre positif et les nombre avec virgule """

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.setValidator(QtGui.QDoubleValidator(0, 100000, 2, self))


class DateEdit(QtGui.QDateEdit):
    """ Accepter que une date """

    def __init__(self, parent=None):
        QtGui.QDateEdit.__init__(self, parent)
        self.setDisplayFormat("MMMM yyyy")
        self.setDateRange(QtCore.QDate(1999, 1, 1), QtCore.QDate(2100, 1, 1))
