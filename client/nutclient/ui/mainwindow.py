#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
import threading
import Queue

from PyQt4 import QtGui, QtCore

from dashboard import DashboardWidget
from common import NUTWidget
from login import LoginWidget
from menu import *
from statusbar import NUTStatusBar
from nutclient.exceptions import UnableToCompleteWidget

import zmq
import random
import time

class ZmqServer(threading.Thread):

    """ ZeroMQ server (REQ) receiving incoming events (events.Event objects) """

    def __init__(self, target):
        self._target = target
        self.is_running = True

        threading.Thread.__init__ ( self )

    def run(self):
        # setup zmq server
        try:
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://*:5555")
        except:
            # something went wrong, better drop event support than
            # freeze the UI.
            self.is_running = False

        while self.is_running:
            try:
                # grab event or dismiss
                event = socket.recv_pyobj(zmq.NOBLOCK)
            except zmq.ZMQError:
                # raises on no-message to poll
                time.sleep(2)
                continue
            if event:
                # send event to main window
                self._target.add_event(event)
                #socket.send('200')
            time.sleep(2)

    def stop(self):
        self.is_running = False

class MainWindow(QtGui.QMainWindow):
    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)

        # QApplication
        self.app = app

        # events queue
        self._events = Queue.Queue(0)

        # modal dialog holder
        self.dialog = None

        # store User in session
        self._user = None

        self.resize(900, 650)
        self.setWindowTitle(_(u"NUT Client"))
        self.setWindowIcon(QtGui.QIcon('images/icon32.png'))

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.QCoreApplication.translate('', "Ctrl+q")), self, self.close)

        self.menu = MainMenu(self)
        self.menu.build()
        self.addToolBar(self.menu)

        self.statusbar = NUTStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.view_widget = NUTWidget(self)

        self.change_context(LoginWidget)

        self.thread = ZmqServer(self)
        self.thread.start()

        self.timer = None

    def change_context(self, context_widget, *args, **kwargs):

        # check permissions
        if context_widget.require_logged_user() and not self.is_logged():
            self.change_context(LoginWidget)
            return

        # remove focus from previous page
        self.view_widget.clearFocus()

        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # attach context to window
        self.setCentralWidget(self.view_widget)

        # set focus to default widget on target
        focus = self.view_widget.default_focus()
        if focus:
            focus.setFocus()

    """def change_context_id(self, context_id, *args, **kwargs):
        contexts = {'help': {'widget': DashboardWidget, 'menu': None}}
        self.change_context(contexts[context_id]['widget'], args, kwargs)"""

    def open_dialog(self, dialog, modal=False, *args, **kwargs):
        self.dialog = dialog(parent=self, *args, **kwargs)
        self.dialog.setModal(modal)
        self.dialog.exec_()
        self.dialog = None

    def process_event(self, event):
        # discard if event expired
        if not event.alive:
            return

        # send event to modal dialog if exist
        if self.dialog:
            self.dialog.process_event(event)

        # has event been discarded?
        if not event.alive:
            return

        # send event to current widget
        self.view_widget.process_event(event)

        # has event been discarded?
        if not event.alive:
            return

        # nobody handled event. Use default notification
        self.default_event_handler(event)
        event.discard()

    def default_event_handler(self, event):
        #rep = QtGui.QMessageBox.question(self, u"Incoming SMS", event.detail)
        self.statusbar.showMessage(event.verbose())
        event.discard()

    def add_event(self, event):
        # add event to queue and launch a timer
        # this way we can process event on the QtGui thread.
        self._events.put(event)
        self.timer = self.startTimer(1000)

    def timerEvent(self, qt_event):
        # retrieve event from queue
        # delete timer
        # process event gui-wise
        event = self._events.get()
        if event:
            self.killTimer(self.timer)
            self.process_event(event)

    def closeEvent(self, event):
        # make sure we kill ZMQ thread before leaving
        self.thread.stop()
        event.accept()

    def is_logged(self):
        return self._user and self._user.active
