#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys
import gettext
import locale

from PyQt4 import QtGui, QtCore

from ui.mainwindow import MainWindow
from ui.window import NUTWindow


def main(args):

    halt_on_quit = False
    fullscreen = False

    if 'fullscreen' in args:
        fullscreen = True
    
    if 'halt_on_quit' in args:
        halt_on_quit = True

    locale.setlocale(locale.LC_ALL, '')

    gettext.install('nut', localedir='locale', unicode=True)

    app = QtGui.QApplication(sys.argv)

    # translation file for Qt (QT's widgets)
    loc = QtCore.QLocale.system()
    trans = QtCore.QTranslator(app)
    sLocName = "qt_" + loc.name()
    sLocPath = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    if trans.load(sLocName, sLocPath):
        app.installTranslator(trans)

    window = MainWindow(app)

    setattr(NUTWindow, 'window', window)
    setattr(NUTWindow, 'halt_on_quit', halt_on_quit)

    if fullscreen:
        window.showFullScreen()
    else:
        window.show()
    
    ret = app.exec_()
    if halt_on_quit:
        import subprocess
        subprocess.call(' '.join(['/usr/bin/sudo', '/sbin/halt']), shell=True)
    sys.exit(ret)

if __name__ == "__main__":
    main([arg.replace('-', '').lower() for arg in sys.argv])
