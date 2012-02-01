#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import pickle
import threading
import Queue
import time

import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message
from PyQt4 import QtGui, QtCore

from nutclient.event import Event
from dashboard import DashboardWidget
from common import NUTWidget
from login import LoginWidget
from menu import *
from statusbar import NUTStatusBar
from nutclient.exceptions import UnableToCompleteWidget


class SnakeMQServer():

    def __init__(self, target):
        self._target = target
        self.is_running = False

        self.my_link = snakemq.link.Link()
        self.my_packeter = snakemq.packeter.Packeter(self.my_link)
        self.my_messaging = snakemq.messaging.Messaging('server', "",
                                                        self.my_packeter)

        self.my_link.add_listener(("", 4000))

        def on_recv(conn, ident, message):
            event = Event.from_dict(pickle.loads(message.data))
            self._target.add_event(event)

        self.my_messaging.on_message_recv.add(on_recv)

        self.thread = None

    def start(self, *args, **kwargs):
        if not self.is_running:
            self.run()

    def run(self):
        self.thread = threading.Thread(target=self.my_link.loop)
        self.thread.start()
    
    def stop(self):
        self.is_running = False
        if self.thread:
            self.my_link.stop()
            self.thread.join()


class MainWindow(QtGui.QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()

        # QApplication
        self.app = app

        # events queue
        self._events = Queue.Queue(0)

        # modal dialog holder
        self.dialog = None

        # store User in session
        self._user = None

        self.resize(1024, 600)
        self.setWindowTitle(u"Malnutrition Aigüe au Mali")
        self.setWindowIcon(QtGui.QIcon('images/icon32.png'))

        self.menu = MainMenu(self)
        self.menu.build()
        self.addToolBar(self.menu)

        self.statusbar = NUTStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.view_widget = NUTWidget(self)

        self.change_context(LoginWidget)

        self.thread = SnakeMQServer(self)
        self.thread.start()

        self.timer = None

    def change_context(self, context_widget, *args, **kwargs):
        if self.view_widget.prevent_close():
            if not self.view_widget.attempt_close():
                return

        # check permissions
        if context_widget.require_logged_user() and not self.is_logged():
            self.change_context(LoginWidget)
            return

        # remove focus from previous page
        self.view_widget.clearFocus()

        # instanciate context
        self.view_widget = context_widget(parent=self, *args, **kwargs)

        # adjust menu pagination
        self.menu.setPagination(context_widget.has_pagination())

        # attach context to window
        self.setCentralWidget(self.view_widget)

        # set focus to default widget on target
        focus = self.view_widget.default_focus()
        if focus:
            focus.setFocus()

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
