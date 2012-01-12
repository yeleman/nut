#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore

from common import NUTWidget, PageTitle, PageIntro, FormLabel, ErrorLabel, EnterTabbedLineEdit
from nutclient.exceptions import *
from nutclient.utils import offline_login, remote_login_request
from dashboard import DashboardWidget


class LoginWidget(NUTWidget):

    title = u"Please log-in"

    def __init__(self, parent=0, *args, **kwargs):

        super(LoginWidget, self).__init__(parent=parent, *args, **kwargs)

        
        self.title = PageTitle(_(u"Log-in to the system"))
        self.intro = PageIntro(_(u"You need to log into the system before " \
                                 u"you are allowed to access it.\n" \
                                 u"If you never logged-in, you will have to " \
                                 u"do a remote login which will take about " \
                                 u"3mn."))

        vbox = QtGui.QVBoxLayout()
        gridbox = QtGui.QGridLayout()

        # page title
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        # username field
        self.username_field = EnterTabbedLineEdit()
        self.username_label = FormLabel(u"&Identifiant")
        self.username_label.setBuddy(self.username_field)
        self.username_error = ErrorLabel(u"")

        # password field
        self.password_field = EnterTabbedLineEdit()
        self.password_field.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        self.password_label = FormLabel(u"Mot de &passe")
        self.password_label.setBuddy(self.password_field)
        self.password_error = ErrorLabel(u"")

        # login button
        self.login_buttun = QtGui.QPushButton(_(u"&Log in"))
        self.login_buttun.setAutoDefault(True)
        self.login_buttun.clicked.connect(self.do_login)

        # login error
        self.login_error = ErrorLabel("")

        # grid layout
        gridbox.addWidget(self.username_label, 0, 0)
        gridbox.addWidget(self.username_field, 0, 1)
        gridbox.addWidget(self.username_error, 0, 2)
        gridbox.addWidget(self.password_label, 1, 0)
        gridbox.addWidget(self.password_field, 1, 1)
        gridbox.addWidget(self.password_error, 1, 2)
        gridbox.addWidget(self.login_buttun, 2, 0)
        gridbox.addWidget(self.login_error, 3, 1)

        # adds stretched column + row at end to fill-up space
        gridbox.setColumnStretch(2, 1)
        gridbox.setRowStretch(5, 10)

        vbox.addLayout(gridbox)
        self.setLayout(vbox)

        # set focus to username field
        self.setFocusProxy(self.username_field)

    def default_focus(self):
        # direct focus to username field
        return self.username_field

    @classmethod
    def require_logged_user(self):
        return False

    def is_complete(self):
        """ form has been completly filled or not. Sets error messages """

        complete = True

        # reset login error
        self.login_error.clear()

        # username is required
        if not self.username_field.text():
            self.username_error.setText(_(u"Username is required."))
            complete = False
        else:
            self.username_error.clear()

        # password is required
        if not self.password_field.text():
            self.password_error.setText(_(u"Password is required."))
            complete = False
        else:
            self.password_error.clear()
        return complete

    def do_login(self):
        """ calls login and adjust UI """

        username = unicode(self.username_field.text()).strip()
        password = unicode(self.password_field.text()).strip()

        # check completeness
        if not self.is_complete():
            return

        try:
            user = offline_login(username=username,
                                 password=password)
        except UsernameNotFound:
            # Username is not in database.
            # ask user whether to retype or perform remote login
            box = QtGui.QMessageBox.question(self, _(u"Are you sure?"),
                    _(u"You typed “%s” as username. " \
                      u"That username is unknown on this computer (which " \
                      u"is normal if this is your first log in).\n" \
                      u"Do you want to re-type your username (cancel this) " \
                      u"or do you want to perform a remote login on the " \
                      u"server?\n\nContinue with a remote login?") % username,
                    QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)
            if box == QtGui.QMessageBox.Cancel:
                return
            else:
                # trigger online_login
                dialog = self.open_dialog(RemoteLogin,
                                          username=username,
                                          password=password)
                return

        if not user:
            self.login_error.setText(_(u"Provided password is wrong"))
            return

        # store User object to main window
        self.main_window._user = user

        # go to dashboard
        self.change_main_context(DashboardWidget)

    def process_event(self, event):
        if event.type == event.LOGIN_SUCCESS \
           or event.type == event.LOGIN_FAILED:
            box = QtGui.QMessageBox.information(self,
                                                _(u"Successfully logged-in"),
                    _(u"Congratulations!\nThe server positively recognized " \
                      u"you and sent your Health Center informations.\nFrom " \
                      u"now, you will be able to log-in instantly with that " \
                      u"username."))
            event.discard()
            self.do_login()


class RemoteLogin(QtGui.QDialog, NUTWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent)

        self.username = None
        self.password = None

        if kwargs.has_key('username'):
            self.username = kwargs['username']

        if kwargs.has_key('password'):
            self.password = kwargs['password']

        self.setWindowTitle(_(u"Remote Login"))

        self.title = PageTitle(_(u"Send a remote login request"))
        self.intro = PageIntro(_(u"A remote login is performed by sending " \
                                 u"your username and password to the server," \
                                 u"\nand waiting for it to acknowledge your " \
                                 u"access.\n\nThis process can take up to " \
                                 u"5mn.\nYou can interrupt the process and" \
                                 u"try to login normally at a later time.\n\n" \
                                 u"Make sure your types your username and " \
                                 u"password properly before starting."))

        vbox = QtGui.QVBoxLayout()

        # page title
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        # progress bar is loading-animated (no progress)
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.progress_label = QtGui.QLabel(_(u"Waiting for server " \
                                             u"to respond…"))
        self.progress_label.setVisible(False)

        # continue sends sms
        self.continue_button = QtGui.QPushButton(_(u"&Continue"))
        self.continue_button.clicked.connect(self.send_request)

        # cancel closes window
        self.cancel_button = QtGui.QPushButton(_(u"&Abort"))
        self.cancel_button.clicked.connect(self.close)

        # layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.progress_bar)
        hbox.addStretch()
        hbox.addWidget(self.continue_button)
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.progress_label)
        self.setLayout(vbox)

        # set focus to username field
        self.setFocusProxy(self.cancel_button)
        self.cancel_button.setFocus()

    def send_request(self):
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.continue_button.setVisible(False)
        remote_login_request(self.username, self.password)

    def process_event(self, event):
        # login success/failure close pending dialog
        # keep event alive so that parent will process
        if event.type == event.LOGIN_SUCCESS \
           or event.type == event.LOGIN_FAILED:
            self.close()