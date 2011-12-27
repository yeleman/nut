#!/usr/bin/env python
# encoding=utf-8

from PyQt import QtGui


class TabEventFilter(QtGui.QObject):

    def set_target(self, target):
        self._target = target

    def set_keystroke(self, ks):
        self._ks = ks

    def set_handler(self, handler):
        self._handler = handler

    def eventFilter(self, target, event):
        if target == self._target and event.type() == QEvent.KeyPress:
            if event.key() == self._ks
                self._handler()
                return True
            else:
                return False
        else:
            return False
