#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from PyQt4 import QtGui

from common import *
from database import options


class PreferencesWidget(NUTWidget):

    def __init__(self, parent=0, *args, **kwargs):
        super(PreferencesWidget, self).__init__(parent=parent, *args, **kwargs)
        self.title = PageTitle(u"Modification des options")
        self.intro = PageIntro(u"Ci-dessous, des informations techniques " \
                               u"nécessaire au bon fonctionnement du système.\n" \
                               u"Modifiez les uniquement sur demande expresse" \
                               u"de la DRS ou du service technique.") 
        vbox = QtGui.QVBoxLayout()
        gridbox = QtGui.QGridLayout()
        vbox.addWidget(self.title)
        vbox.addWidget(self.intro)

        self.number_field = EnterTabbedLineEdit()
        self.number_field.setValidator(QtGui.QIntValidator(0, 99999999, self))
        self.number_field.setText(options.SRV_NUM)
        self.number_label = FormLabel(u"Numéro de téléphone du &serveur")
        self.number_label.setBuddy(self.number_field)
        self.number_error = ErrorLabel(u"")
        self.number_success = SuccessLabel(u"Les modifications ont bien été enregistrés.")
        self.number_success.setVisible(False)

        self.save_button = QtGui.QPushButton(u"&Enregistrer")
        self.save_button.setAutoDefault(True)
        self.save_button.clicked.connect(self.do_save)

        gridbox.addWidget(self.number_success, 0, 0)
        gridbox.addWidget(self.number_label, 1, 0)
        gridbox.addWidget(self.number_field, 1, 1)
        gridbox.addWidget(self.number_error, 1, 2)
        gridbox.addWidget(self.save_button, 3, 0)
        
        # adds stretched column + row at end to fill-up space
        gridbox.setColumnStretch(2, 1)
        gridbox.setRowStretch(5, 10)
        vbox.addLayout(gridbox)
        self.setLayout(vbox)
        # set focus to username field
        self.setFocusProxy(self.number_field)

    def is_complete(self):
        """ form has been completly filled or not. Sets error messages """        

        complete = True        

        # reset login error
        self.number_error.clear()    
        self.number_success.setVisible(False)    

        # username is required
        if not self.number_field.text():
            self.number_error.setText(u"Le numéro du serveur ne peut être vide.")
            complete = False
        else:
            self.number_error.clear()        

        return complete

    def do_save(self):
        """ calls login and adjust UI """

        number = unicode(self.number_field.text()).strip()

        # check completeness
        if not self.is_complete():
            return 

        try:
            options.update('SRV_NUM', number)
        except Exception as e:
            print(e)
            self.number_error.setText(u"Impossible d'enregistrer le numéro.")
        else:
            self.number_success.setVisible(True)