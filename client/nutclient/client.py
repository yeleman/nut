#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
import gettext
import locale

from PyQt4 import QtGui

from ui.mainwindow import MainWindow
from ui.window import NUTWindow


def main():

    #gettext_windows.setup_env()

    locale.setlocale(locale.LC_ALL, '')

    gettext.install('nut', localedir='locale', unicode=True)

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(app)
    setattr(NUTWindow, 'window', window)
    window.show()
    #window.showMaximized()
    #window.showNormal()
    #window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
