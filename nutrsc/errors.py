#!/usr/bin/env python
# encoding=utf-8

LOGIN_ERRORS = {
    'NO_ACC': u"Cet identifiant n'existe pas.",
    'BAD_PASS': u"Le mot de passe est incorrect pour cet identifiant.",
    'ACC_DIS': u"Cet identifiant a été désactivé.",
    'OTHER': u"Erreur inconnue."
}

REPORT_ERRORS = {
    'NO_ACC': u"Cet identifiant n'existe pas.",
    'NO_PERM': u"Cet identifian n'est pas autorisé "
               u"à envoyer des rapports pour ce centre",
    'BAD_PASS': u"Le mot de passe est incorrect pour cet identifiant.",
    'ACC_DIS': u"Cet identifiant a été désactivé.",
    'OTHER': u"Erreur inconnue.",
    'BAD_FORM': u"Format SMS incorrect (sections).",
    'BAD_FORM_PEC': u"Format SMS incorrect (PEC).",
    'BAD_FORM_CONS': u"Format SMS incorrect (CONS).",
    'BAD_FORM_ORDER': u"Format SMS incorrect (ORDER).",
    'BAD_FORM_INFO': u"Format SMS incorrect (infos).",
    'BAD_FORM_PERIOD': u"Format SMS incorrect (period).",
    'BAD_FORM_OTHER': u"Format SMS incorrect (others).",
    'BAD_PERIOD': u"Impossible d'enregistrer des données "
                  u"pour cette période actuellement.",
    'NOT_ENT': u"Cet identifiant n'est lié à aucun centre de santé.",
    'BAD_CAP': u"Le rapport ne correspond pas aux types d'UREN du centre. "
               u"Essayez de vous re-identifier à distance.",
    'PEC': u"PEC: Données incorrectes.",
    'PEC_MAM': u"PEC MAM: Données incorrectes.",
    'PEC_SAM': u"PEC SAM: Données incorrectes.",
    'PEC_SAMP': u"PEC SAM+: Données incorrectes.",
    'CONS': u"CONS: Données incorrectes.",
    'CONS_MAM': u"CONS MAM: Données incorrectes.",
    'CONS_SAM': u"CONS SAM: Données incorrectes.",
    'CONS_SAMP': u"CONS SAM+: Données incorrectes.",
    'ORDER': u"ORDER: Données incorrectes.",
    'ORDER_MAM': u"ORDER MAM: Données incorrectes.",
    'ORDER_SAM': u"ORDER SAM: Données incorrectes.",
    'ORDER_SAMP': u"ORDER SAM+: Données incorrectes.",
    'OTHER_INT': u"Les données Autres ne correspondent pas aux données PEC.",
    'SRV': u"Une erreur technique s'est produite. "
           u"Contactez le support technique.",
    'UNIQ': u"Ce centre de santé a déjà un rapport pour cette période.",
    'MISS': u"Impossible de mettre à jour le rapport. Il n'existe pas.",
}
