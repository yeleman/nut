#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


MAIN_WIDGET_SIZE = 1020


class NUTWidget(QtGui.QWidget):

    title = None

    def __init__(self, parent, *args, **kwargs):

        super(NUTWidget, self).__init__(*args, **kwargs)

        self._parent = parent

        self.setMaximumWidth(MAIN_WIDGET_SIZE)

        if self.title:
            self.main_window.setWindowTitle(self.title)

    def refresh(self):
        pass

    def get_main_prop(self, name):
        if hasattr(self.main_window, name):
            return getattr(self.main_window, name)
        else:
            return None

    @property
    def user(self):
        return self.get_main_prop('_user')

    @property
    def main_window(self):
        w = self
        while w:
            if w.__class__.__name__ == 'MainWindow':
                return w
            if hasattr(w, '_parent'):
                w = w._parent
                continue
            elif hasattr(w, 'parentWidget'):
                w = w.parentWidget()
                continue
            else:
                return None
        return None

    @classmethod
    def require_logged_user(self):
        return True

    def process_event(self, event):
        pass

    def change_main_context(self, context_widget, *args, **kwargs):
        return self.main_window\
                          .change_context(context_widget, *args, **kwargs)

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        return self.main_window.open_dialog(dialog, \
                                               modal=modal, *args, **kwargs)

    def default_focus(self):
        """ widget which should receive focus on NUTWidget display

            Called from MainWindows as FocusProxy is buggy. """
        return None

    @classmethod
    def has_pagination(cls):
        return False

    def prevent_close(self):
        ''' whether or not exit should be blocked '''
        return False

    def attempt_close(self):
        ''' override to add logic on widget leave.return True if OK to leave '''
        return True

class PageTitle(QtGui.QLabel):
    """ Formatage du titre de page """

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 16)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class PageIntro(QtGui.QLabel):
    """ Formatage de l'introduction de page """

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 12)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class FormLabel(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

class ErrorLabel(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont()
        self.setFont(font)
        red = QtGui.QColor(QtCore.Qt.red)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, red)
        self.setPalette(palette)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class PageSection(QtGui.QLabel):

    def __init__(self, text, parent=None):
        QtGui.QLabel.__init__(self, text, parent)
        font = QtGui.QFont("Times New Roman", 14)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class LinkButton(QtGui.QPushButton):

    def __init__(self, text, handler, ident):

        super(LinkButton, self).__init__(text)

        self.ident = ident
        self.handler = handler
        self.clicked.connect(self.on_command)

    def on_command(self):
        self.handler(self.ident)


class BoldLabel(QtGui.QLabel):

    def __init__(self, text, parent=None):
        super(BoldLabel, self).__init__(text, parent)
        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        

class SuccessLabel(QtGui.QWidget):

    def __init__(self, text, parent=None):
        super(SuccessLabel, self).__init__(parent)

        hbox = QtGui.QHBoxLayout()
        iconl = QtGui.QLabel('', self)
        iconl.setPixmap(QtGui.QPixmap('images/accept.png'))
        textl = QtGui.QLabel(text, self)
        textl.setText(text)
        textl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hbox.addWidget(iconl)
        hbox.addWidget(textl)
        self.setLayout(hbox)


class IconLabel(QtGui.QLabel):

    def __init__(self, icon, parent=None):
        super(IconLabel, self).__init__('', parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setPixmap(icon)


class TransmitButton(QtGui.QPushButton):

    def __init__(self, parent=None):
        super(TransmitButton, self).__init__(QtGui.QIcon('images/phone.png'),
                                             u"&Transmettre le rapport", parent)

    def disable(self):
        self.setEnabled(False)

    def enable(self):
        self.setEnabled(True)


class SaveButton(QtGui.QPushButton):

    def __init__(self, parent=None):
        super(SaveButton, self).__init__(QtGui.QIcon('images/table_save.png'), 
                                                     u"&Enregistrer", parent)

    def disable(self):
        self.setEnabled(False)

    def enable(self):
        self.setEnabled(True)