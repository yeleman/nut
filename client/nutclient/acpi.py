#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from subprocess import Popen, PIPE
import thread
import time

class ACPIBatteryStatus:

    ACPI = '/usr/bin/acpi'
    AC = 'a'
    BATT = 'b'

    UNKNOWN = 0
    ONLINE = 1
    OFFLINE = 2
    DESKTOP = 3

    P_UNKNOWN = -1
    P_EMPTY = 0
    P_FULL = 100

    def __init__(self, interval):
        self.interval = interval
        self._status = self.UNKNOWN
        self._percent = self.P_UNKNOWN

        thread.start_new_thread(self.loop, ())

    @property
    def status(self):
        return self._status

    @property
    def percent(self):
        return self._percent

    def update(self):
        ac_power = self.fetch(self.AC)
        battery = self.fetch(self.BATT)

        # we should never have no info on AC.
        if not ac_power:
            self._status = self.UNKNOWN
            self._percent = self.UNKNOWN
            return

        # desktop without battery
        if not battery:
            self._status = self.DESKTOP
            self._percent = self.P_UNKNOWN
            return

        self._status = battery['status']
        self._percent = battery['percent']

    def loop(self):
        self.update()
        time.sleep(self.interval)
        self.loop()

    def fetch(self, device):
        # launch acpi bin with device parameter.
        output = Popen([self.ACPI, '-%s' % device], stdout=PIPE).communicate()[0]
        output = output.strip().split('\n')[0]

        # acpi returns nothing if device is not present
        if not ':' in output:
            return None

        # result line
        try:
            status_str = output.split(':')[1].strip()
        except:
            return None

        status = self.UNKNOWN
        percent = self.P_UNKNOWN

        if status_str == 'on-line' or status_str.startswith('Charging') \
           or status_str.startswith('Full'):
            status = self.ONLINE
        if status_str == 'off-line' or status_str.startswith('Discharging'):
            status = self.OFFLINE
        if status_str.startswith('Discharging'):
            status = self.OFFLINE

        # we have a %age and time
        if ',' in status_str:
            try:
                percent = int(status_str.split(',')[1].strip().replace('%', ''))
            except: pass

        return {'status': status, 'percent': percent}
