#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

import os
import re
import time
import subprocess
import threading

import envoy
from PyQt4 import QtGui, QtCore

from common import (NUTWidget, PageTitle, FormLabel, PageIntro,
                    ErrorLabel, EnterTabbedLineEdit)
from nutrsc.mali import OPERATORS, parse_ussd


class SIMManagementWidget(NUTWidget):

    title = u"Gestion SIM"

    def __init__(self, parent=0, *args, **kwargs):

        super(SIMManagementWidget, self).__init__(parent=parent,
                                                  *args, **kwargs)

        self.title = PageTitle(u"Gestion de la carte SIM")
        self.intro = PageIntro(u"Afin de pouvoir transmettre les rapports par "
                               u"SMS, vous devez vérifier que la carte SIM "
                               u"du modem dispose de crédit.\n"
                               u"Indiquez l'opérateur de la carte SIM et le "
                               u"numéro de la carte de recharge.\n\n"
                               u"Vous pouvez aussi transférer du crédit sur "
                               u"le numéro de la carte SIM.")

        vbox = QtGui.QVBoxLayout()
        gridbox = QtGui.QGridLayout()

        # page title
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        # operator choice
        self.operator_field = QtGui.QComboBox(self)
        for operator in OPERATORS:
            self.operator_field.addItem(operator.get('name', u'?'))
        self.operator_label = FormLabel(u"&Opérateur")
        self.operator_label.setBuddy(self.operator_field)
        self.operator_error = ErrorLabel(u"")

        # balance button
        self.balance_button = QtGui.QPushButton(u"&Vérifier le solde")
        self.balance_button.setAutoDefault(True)
        self.balance_button.clicked.connect(self.do_balance)
        self.balance_button.setVisible(True)
        self.balance_label = FormLabel(u"&Crédit disponible")
        self.balance_label.setBuddy(self.balance_button)
        self.balance_response = ErrorLabel(u"")

        # card field
        self.card_field = EnterTabbedLineEdit()
        regexp = QtCore.QRegExp(u'\d{1,18}')
        self.card_field.setValidator(QtGui.QRegExpValidator(regexp, self))
        self.card_label = FormLabel(u"&Numéro de la carte")
        self.card_label.setBuddy(self.card_field)
        self.card_error = ErrorLabel(u"")

        # submit button
        self.send_button = QtGui.QPushButton(u"&Envoyer")
        self.send_button.setAutoDefault(False)
        self.send_button.clicked.connect(self.do_send)

        # submit error
        #self.send_response = ErrorLabel("")

        # progress bar is loading-animated (no progress)
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.progress_label = QtGui.QLabel(u"En attente de la réponse du " \
                                             u"serveur…")
        self.progress_label.setVisible(False)

        # grid layout
        gridbox.addWidget(self.balance_label, 0, 0)
        gridbox.addWidget(self.balance_button, 0, 1)
        gridbox.addWidget(self.balance_response, 0, 2)

        gridbox.addWidget(self.operator_label, 1, 0)
        gridbox.addWidget(self.operator_field, 1, 1)
        gridbox.addWidget(self.operator_error, 1, 2)
        gridbox.addWidget(self.card_label, 2, 0)
        gridbox.addWidget(self.card_field, 2, 1)
        gridbox.addWidget(self.card_error, 2, 2)
        gridbox.addWidget(self.send_button, 3, 1)
        #gridbox.addWidget(self.send_response, 4, 2)

        # adds stretched column + row at end to fill-up space
        gridbox.setColumnStretch(2, 1)
        gridbox.setRowStretch(5, 10)

        vbox.addLayout(gridbox)
        self.setLayout(vbox)

        # set focus to username field
        self.setFocusProxy(self.card_field)

    def display_balance(self, balance):
        self.balance_response.setText(balance)
        self.balance_response.setVisible(True)
    
    def hide_balance(self):
        self.balance_response.setVisible(False)

    def display_topup(self, topup):
        self.card_error.setText(topup)
        self.card_error.setVisible(True)
    
    def hide_topup(self):
        self.card_error.clear()
        
    def default_focus(self):
        # direct focus to username field
        return self.card_field

    @classmethod
    def require_logged_user(self):
        return False

    def do_balance(self):
        operator = OPERATORS[self.operator_field.currentIndex()]
        self.open_dialog(UssdDialog,
                         action='balance',
                         operator=operator,
                         peer=self)
        return

    def is_complete(self):
        """ form has been completly filled or not. Sets error messages """

        complete = True

        # reset send error
        #self.send_response.clear()

        # card number is required
        if not self.card_field.text():
            self.card_error.setText(u"Le numéro de carte de recharge"
                                    u" est requis.")
            complete = False
        else:
            self.card_error.clear()

        return complete

    def do_send(self):

        # check completeness
        if not self.is_complete():
            return

        operator = OPERATORS[self.operator_field.currentIndex()]
        card = int(self.card_field.text())
        
        self.open_dialog(UssdDialog,
                         action='topup',
                         operator=operator,
                         card=card,
                         peer=self)
        return


class UssdDialog(QtGui.QDialog, NUTWidget):

    def __init__(self, parent=0, *args, **kwargs):
        QtGui.QWidget.__init__(self, parent)

        self.action = kwargs.get('action', 'balance')
        self.operator = kwargs.get('operator', OPERATORS[-1])
        self.card = kwargs.get('card', None)
        self.peer = kwargs.get('peer', None)

        if self.action == 'topup':
            self.ussd_cmd = self.operator.get('ussd_topup') % self.card
            title = u"Recharge %s" % self.operator.get('name')
        else:
            self.ussd_cmd = self.operator.get('ussd_balance')
            title = u"Demande du solde %s" % self.operator.get('name')

        self.setWindowTitle(title)

        self.intro = PageIntro(title + u"\n\n" +
                               u"En attente de la réponse du serveur.\n"
                               u"Vous pouvez annuler et trouverez la réponse\n"
                               u"dans la zone messages du tableau "
                               u"de bord.\n\n")

        vbox = QtGui.QVBoxLayout()

        vbox.addWidget(self.intro)

        # progress bar is loading-animated (no progress)
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)

        self.progress_label = QtGui.QLabel(u"En attente de la réponse du " \
                                           u"serveur…")

        # cancel closes window
        self.cancel_button = QtGui.QPushButton(u"&Annuler")
        self.cancel_button.clicked.connect(self.cancel)

        # layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.progress_bar)
        hbox.addStretch()
        hbox.addWidget(self.cancel_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.progress_label)
        self.setLayout(vbox)

        # set focus to username field
        self.setFocusProxy(self.cancel_button)
        self.cancel_button.setFocus()


        self.cmd = ['/usr/bin/gammu', 'getussd', self.ussd_cmd]
        self.process = None
        self.out = None
        self.err = None
        self.returncode = None
        self.data = None
        self.running = False
        self.timeout = 30
        self.countdown = 0
        self.loop = 2

        self.ussd_launched = False
        self.timer = self.startTimer(1)

    def cancel(self):
        try:
            self.thread.stop()
        except:
            pass
        self.close()

    def success(self, text=u"Impossible d'obtenir une réponse. "
                           u"Réessayez plus tard"):
        try:
            self.thread.stop()
        except:
            pass
        if self.action == 'topup':
            self.peer.display_topup(text)
        else:
            self.peer.display_balance(text)
        self.close()

    def process_event(self, event):
        # login success/failure close pending dialog
        # keep event alive so that parent will process
        if event.type == event.USSD_SUCCESS:
            self.success(event.detail)
        elif event.type == event.USSD_FAILED:
            self.success()
    
    def timerEvent(self, event):
        if not self.ussd_launched:
            self.ussd_launched = True
            self.killTimer(event.timerId())

            self.run()
        else:
            if not self.process:
                return

            self.process.poll()
            if (self.process.returncode is None
                and self.running
                and self.countdown < self.timeout):

                self.countdown += self.loop
            else:
                self.killTimer(event.timerId())
                self.end()

    def run(self):
        
        # stop Gammu-SMSD
        envoy.run('sudo /etc/init.d/gammu-smsd stop')

        environ = dict(os.environ)

        def target():
            self.process = subprocess.Popen(self.cmd,
                universal_newlines=True,
                shell=False,
                env=environ,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0,
            )

            self.out, self.err = self.process.communicate()

        self.thread = threading.Thread(target=target)
        self.thread.start()
        self.running = True

        self.timer = self.startTimer(self.loop * 1000)

    def stop(self):
        print('stop')
        self.running = False
        self.process.terminate()

    def end(self):
        print('end')
        if self.thread.is_alive():
            self.process.terminate()
            self.thread.join()
        self.returncode = self.process.returncode

        print('OUT: %s' % self.out)
        print('ERR: %s' % self.err)
        
        # Restart Gammu-SMSD
        envoy.run('sudo /etc/init.d/gammu-smsd start')

        self.success(parse_ussd(self.out))
