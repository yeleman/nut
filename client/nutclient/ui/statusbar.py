#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from PyQt4 import QtGui, QtCore
import thread
import time
from datetime import datetime
from acpi import ACPIBatteryStatus

class NUTStatusBar(QtGui.QStatusBar):

    def __init__(self, parent):

        QtGui.QStatusBar.__init__(self, parent)

        self.showMessage(u"السلام عليكم", 2000)
        self.batt = BatteryIndicator(self)
        self.addPermanentWidget(self.batt)


class BatteryIndicator(QtGui.QWidget):

    def __init__(self, parent):

        QtGui.QWidget.__init__(self, parent)

        self.hbox = QtGui.QHBoxLayout()
        self.batt_label = QtGui.QLabel(u"Alimentation:")
        self.batt_icon = QtGui.QLabel()
        self.batt_icon.setPixmap(QtGui.QPixmap())
        self.batt_text = QtGui.QLabel()

        self.hbox.addWidget(self.batt_label)
        self.hbox.addWidget(self.batt_text)
        self.hbox.addWidget(self.batt_icon)

        self.battery = ACPIBatteryStatus(10)

        self.update()
        self.startTimer(2000)

        self.setLayout(self.hbox)

    def icon(self, percent):
        if percent == ACPIBatteryStatus.P_UNKNOWN:
            return QtGui.QPixmap()
        else:
            return QtGui.QPixmap('images/battery-%s.png' % str(self.icon_name(percent)).zfill(3))

    def icon_name(self, percent):
        ret = percent % 10
        if ret <= 5:
            return percent - ret
        else:
            return (percent - ret) + 10


    def status_text(self, status, percent):
        if status == ACPIBatteryStatus.DESKTOP:
            return u"Secteur"
        if status == ACPIBatteryStatus.UNKNOWN:
            if percent != ACPIBatteryStatus.P_UNKNOWN:
                return u"Secteur (%d%%)" % percent
            else:
                return u"Inconnu"
        if status == ACPIBatteryStatus.ONLINE:
            return u"Secteur (%d%%)" % percent
        if status == ACPIBatteryStatus.OFFLINE:
            return u"Batterie (%d%%)" % percent

    def timerEvent(self, event):
        self.update()

    def update(self):

        self.batt_text.setText(self.status_text(self.battery.status, self.battery.percent))
        self.batt_icon.setToolTip(self.status_text(self.battery.status, self.battery.percent))
        self.batt_icon.setPixmap(self.icon(self.battery.percent))
