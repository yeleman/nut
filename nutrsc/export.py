#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import sys
import StringIO

import xlwt

from nutrsc.mali import HC_CAPS, CONSUMPTION_TABLE, DEFAULT_VERSION, CAPS
from nutrsc.constants import MODERATE, SEVERE, SEVERE_COMP
try:
    from nutclient.database import InputOrderReport
except ImportError:
    pass

font_gras = xlwt.Font()
font_gras.bold = True
font_gras.height = 10 * 0x14

font = xlwt.Font()
font.name = 'Verdana'
font.bold = True
font.height = 12 * 0x14

borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

al = xlwt.Alignment()
al.horz = xlwt.Alignment.HORZ_CENTER
al.vert = xlwt.Alignment.VERT_CENTER

left_al = xlwt.Alignment()
left_al.vert = xlwt.Alignment.HORZ_LEFT

pat2 = xlwt.Pattern()
pat2.pattern = xlwt.Pattern.SOLID_PATTERN
pat2.pattern_fore_colour = 23

style_title = xlwt.XFStyle()
style_title.font = font
style_title.alignment = al

styleheader = xlwt.XFStyle()
styleheader.borders = borders
styleheader.alignment = al
styleheader.font = font_gras

styleheader_ = xlwt.XFStyle()
styleheader_.borders = borders
styleheader_.alignment = al

styleheader_left = xlwt.XFStyle()
styleheader_left.borders = borders

style_without_border = xlwt.XFStyle()

style_value = xlwt.XFStyle()
style_value.borders = borders
style_value.alignment = al

styleblack = xlwt.XFStyle()
styleblack.pattern = pat2
styleblack.borders = borders

styleheader_left_g = xlwt.XFStyle()
styleheader_left_g.borders = borders
styleheader_left_g.font = font_gras
styleheader_left_g.alignment = left_al


def val(report, field):
    return getattr(report, field, None)


def empty(nb=10, var=None):
    l = []; [l.append(var) for x in range(0, nb + 1)]
    return l


def export_report_stream(report):

    book = xlwt.Workbook(encoding='utf-8')

    sheet = book.add_sheet(u"PEC")
    sheet.col(0).width = 0x0d00 * 1.5
    sheet.row(8).height = 790
    sheet.row(26).height = 400

    # define if django report or peewee (client)
    is_django = report.__class__.__name__ == 'NutritionReport'

    # setup some variables
    if is_django:
        hc_name = report.entity.name
        issamp = report.is_samp
        issam = report.is_sam
        ismam = report.is_mam
        others_hiv = report.pec_other_report.other_hiv
        others_tb = report.pec_other_report.other_tb
        others_lwb = report.pec_other_report.other_lwb
        # retrieve InputOrderReport.objects.filter without importing
        ior_class = list(report.order_reports()[0].input_order_reports.all())[0].__class__.objects.filter
    else:
        hc_name = report.hc_name
        issamp = report.hc_issamp
        issam = report.hc_issam
        ismam = report.hc_ismam
        others_hiv = report.others_hiv
        others_tb = report.others_tb
        others_lwb = report.others_lwb
        ior_class = InputOrderReport.filter

    def write_merge_p(liste, style):
        
        for index in liste:
            label = index.keys()[0]
            row, row1, col, col1 = index.values()[0]
            sheet.write_merge(row, row1, col, col1, label, style)

    def write_p(liste, on_row, i_row, on_col, i_col, style=style_value):

        for index in liste:
            style_ = style
            if index == None:
                style_ = styleblack
            if on_row < 40 and on_row > 26 and on_col == 1:
                sheet.write_merge(on_row, on_row, on_col, on_col + 2,
                                  index, style_)
                on_col += 3
            else:
                sheet.write(on_row, on_col, index, style_)
                on_col += i_col
            on_row += i_row

    def create_values(hc, liste, prefix):
        liste_val = [val(hc, "%s%s" % (prefix, i)) for i in liste]
        return liste_val

    def type_center():
        type_ = []
        if issam:
            type_.append(HC_CAPS[SEVERE])
        if issamp:
            type_.append(HC_CAPS[SEVERE_COMP])
        if ismam:
            type_.append(HC_CAPS[MODERATE])
        return " + ".join(type_)

    # Titres
    sheet.write_merge(0, 0, 0, 17,
                      u"RAPPORT STATISTIQUE MENSUEL - TRAITEMENT DE "
                      u"LA MALNUTRITION AIGUE", style_title)
    # En-tête gauche
    sheet.write(1, 0, u"REGION")
    sheet.write(1, 1, u"Gao")
    sheet.write(2, 0, u"District")
    sheet.write(2, 1, u"")
    sheet.write(3, 0, u"CSCom")
    sheet.write(3, 1, u"%s" % hc_name)

    sheet.write_merge(4, 4, 0, 1, u"TYPE DE CENTRE")
    sheet.write_merge(4, 4, 2, 3, u"%s" % type_center())
    sheet.write_merge(5, 5, 0, 1, u"DATE D'OUVERTURE")

    #  En-tête droite
    sheet.write_merge(2, 2, 13, 14, u"Rapport préparé par  ")
    sheet.write_merge(2, 2, 15, 17, u"%s" % report.created_by)
    sheet.write_merge(3, 3, 13, 15, u"MOIS / ANNEE du rapport")
    sheet.write(4, 13, u"Mois")
    sheet.write_merge(4, 4, 14, 15, "%s" % report)

    type_centers = ["URENI 1", "URENAS 2", "URENAM 3", "TOTAL"]
    write_p(type_centers, 9, 4, 0, 0, styleheader_left_g)
    write_p(type_centers, 27, 4, 0, 0, styleheader_left_g)

    #Tableau1 header
    header1 = [{u"Groupe \nd'age": [6, 8, 0, 0]},
               {u"Total au \ndébut \nmois(A1)": [6, 8, 1, 1]},
               {u"Sexe(A2)": [6, 7, 2, 3]},
               {u"Admissions(B)": [6, 6, 4, 17]},
               {u"Critere d'admissions (B1)": [7, 7, 4, 9]},
               {u"Autre": [8, 8, 9, 9]},
               {u"Type d'admission (B2)": [7, 7, 10, 14]},
               {u"Total \nAdmissions \n (B3)": [7, 8, 15, 15]},
               {u"Sexe (B4)": [7, 7, 16, 17]},]
    write_merge_p(header1, styleheader)

    header1_ = [{u"M": [8, 8, 2, 2]},
               {u"F": [8, 8, 3, 3]},
               {u"P/T \n≥70< 80% \nou\nIMC<18": [8, 8, 4, 4]},
               {u"PB <120\nmm (ou PB\n<210 mm)": [8, 8, 5, 5]},
               {u"P/T <70%\nou IMC\n<16 ": [8, 8, 6, 6]},
               {u"PB <11 cm\n(ou PB\n<18cm) ": [8, 8, 7, 7]},
               {u"Oedemes": [8, 8, 8, 8]},
               {u"Nouveau\ncas": [8, 8, 10, 10]},
               {u"Rechute\n(après\ngueris)": [8, 8, 11, 11]},
               {u"Réadmission\n(après\nabandons)\nou Medica": [8, 8, 12, 12]},
               {u"Transfert\nnutritionnel": [8, 8, 13, 13]},
               {u"Référence\nnutritionnelle": [8, 8, 14, 14]},
               {u"M": [8, 8, 16, 16]},
               {u"F": [8, 8, 17, 17]},]
    write_merge_p(header1_, styleheader_)

    type_ureni_1 = ["< 6 mois", "6-59 mois", ">59 mois"]
    write_p(type_ureni_1, 10, 1, 0, 0, styleheader_left)
    write_p(type_ureni_1, 28, 1, 0, 0, styleheader_left)
    type_ureni_2 = [" 6-59 mois", ">59 mois", "Suivi de URENI 1"]
    write_p(type_ureni_2, 14, 1, 0, 0, styleheader_left)
    write_p(type_ureni_2, 32, 1, 0, 0, styleheader_left)
    type_ureni_3 = ["6-59 mois", "FE/FA"]
    write_p(type_ureni_3, 18, 1, 0, 0, styleheader_left)
    write_p(type_ureni_3, 36, 1, 0, 0, styleheader_left)
    sheet.write(20, 0, u"Suivi de 1 et 2", styleheader_left)
    sheet.write(38, 0, u"Suivi de 3 et 2", styleheader_left)
    l_val = ['_total_beginning', '_total_beginning_m', '_total_beginning_f',
        '_hw_b7080_bmi_u18', '_muac_u120', '_hw_u70_bmi_u16',
        '_muac_u11_muac_u18', '_oedema', '_other', '_new_case', '_relapse',
        '_returned', '_nut_transfered_in', '_nut_referred_in', '_admitted',
        '_admitted_m', '_admitted_f']
    # Valeurs tableau1
    # URENI 1
    write_p(empty(16), 9, 0, 1, 1)
    # < 6 mois
    u6_pec_samp_reports = create_values(report.pec_samp_report, l_val, 'u6')
    write_p(u6_pec_samp_reports, 10, 0, 1, 1, style_value)
    # 6-59 mois
    u59_pec_samp_reports = create_values(report.pec_samp_report, l_val, 'u59')
    write_p(u59_pec_samp_reports, 11, 0, 1, 1, style_value)
    # > 59 mois
    o59_pec_samp_reports = create_values(report.pec_samp_report, l_val, 'o59')
    write_p(o59_pec_samp_reports, 12, 0, 1, 1, style_value)

    # URENAS 2
    write_p(empty(16), 13, 0, 1, 1)
    # 6-59 mois
    u59_pec_sam_reports = create_values(report.pec_sam_report, l_val, 'u59')
    write_p(u59_pec_sam_reports, 14, 0, 1, 1, style_value)
    # > 59 mois
    o59_pec_sam_reports = create_values(report.pec_sam_report, l_val, 'o59')
    write_p(o59_pec_sam_reports, 15, 0, 1, 1, style_value)
    # SUIVI DE URENI 1
    fu1_pec_sam_reports = create_values(report.pec_sam_report, l_val, 'fu1')
    write_p(fu1_pec_sam_reports, 16, 0, 1, 1, style_value)

    # URENAM 3
    write_p(empty(16), 17, 0, 1, 1)
    # 6-59 mois
    u59_pec_mam_reports = create_values(report.pec_mam_report, l_val, 'u59')
    write_p(u59_pec_mam_reports, 18, 0, 1, 1, style_value)
    # > FE/FA
    pw_pec_mam_reports = create_values(report.pec_mam_report, l_val, 'pw')
    write_p(pw_pec_mam_reports, 19, 0, 1, 1, style_value)
    # SUIVI DE 1 ET 2
    fu12_pec_mam_reports = create_values(report.pec_mam_report, l_val, 'fu12')
    write_p(fu12_pec_mam_reports, 20, 0, 1, 1, style_value)
    # TOTAL
    sum_all_reports = create_values(report, l_val, 'sum_all')
    write_p(sum_all_reports, 21, 0, 1, 1, style_value)

    # Tableau 2
    # header
    header2 = [{u"Groupe \n d'age": [23, 26, 0, 0]},
               {u"Sorties (C)": [23, 23, 1, 11]},
               {u"Total restant à la fin mois (D)": [23, 23, 12, 15]},
               {u"Type de sortie (C1)": [24, 24, 1, 9]},
               {u"Total\n sorties\n (C2)": [24, 26, 10, 10]},
               {u"Sexe (C3)": [24, 24, 11, 12]},
               {u"Total\n (D1)": [24, 26, 13, 13]},
               {u"Sexe (D2)": [24, 24, 14, 15]}]
    write_merge_p(header2, styleheader)
    header2_ = [{u"Gueris": [25, 26, 1, 3]},
                {u"Referes\nvers 3 ou\n2": [25, 26, 4, 4]},
                {u"Deces": [25, 26, 5, 5]},
                {u"Abandons": [25, 26, 6, 6]},
                {u"Non-\nrepondant": [25, 26, 7, 7]},
                {u"Transfert\nmedical": [25, 26, 8, 8]},
                {u"Transfert\nNutritionnel": [25, 26, 9, 9]},
                {u"M": [25, 26, 11, 11]},
                {u"F": [25, 26, 12, 12]},
                {u"M": [25, 26, 14, 14]},
                {u"F": [25, 26, 15, 15]}]
    write_merge_p(header2_, styleheader_)
    l_val1 = ['_healed', '_referred_out', '_deceased',
          '_aborted', '_non_respondant', '_medic_transfered_out',
          '_nut_transfered_out', '_total_out', '_total_out_m',
          '_total_out_f', '_total_end', '_total_end_m',
          '_total_end_f']
    # URENI 1
    write_p(empty(12), 27, 0, 1, 1)
    # < 6 mois
    u6_pec_samp_reports_out = create_values(report.pec_samp_report, l_val1, 'u6')
    write_p(u6_pec_samp_reports_out, 28, 0, 1, 1, style_value)
    # < 6-59  mois
    u59_pec_samp_reports_out = create_values(report.pec_samp_report, l_val1, 'u59')
    write_p(u59_pec_samp_reports_out, 29, 0, 1, 1, style_value)
    # > 59  mois
    o59_pec_samp_reports_out = create_values(report.pec_samp_report, l_val1, 'o59')
    write_p(o59_pec_samp_reports_out, 30, 0, 1, 1, style_value)

    # URENAS 2
    write_p(empty(12), 31, 0, 1, 1)
    # < 6-59  mois
    u59_pec_sam_reports_out = create_values(report.pec_sam_report, l_val1, 'u59')
    write_p(u59_pec_sam_reports_out, 32, 0, 1, 1, style_value)
    # > 59 mois
    o59_pec_sam_reports_out = create_values(report.pec_sam_report, l_val1, 'o59')
    write_p(o59_pec_sam_reports_out, 33, 0, 1, 1, style_value)
    # SUIVI DE URENI 1
    fu1_pec_sam_reports_out = create_values(report.pec_sam_report, l_val1, 'fu1')
    write_p(fu1_pec_sam_reports_out, 34, 0, 1, 1, style_value)

    # URENAM 3
    write_p(empty(12), 35, 0, 1, 1)
    # 6-59 mois
    u59_pec_mam_reports_out = create_values(report.pec_mam_report, l_val1, 'u59')
    write_p(u59_pec_mam_reports_out, 36, 0, 1, 1, style_value)
    # > FE/FA
    pw_pec_mam_reports_out = create_values(report.pec_mam_report, l_val1, 'pw')
    write_p(pw_pec_mam_reports_out, 37, 0, 1, 1, style_value)
    # SUIVI DE 3 ET 2
    fu12_pec_mam_reports_out = create_values(report.pec_mam_report, l_val1, 'fu12')
    write_p(fu12_pec_mam_reports_out, 38, 0, 1, 1, style_value)
    # TOTAL
    sum_all_reports_out = create_values(report, l_val1, 'sum_all')
    write_p(sum_all_reports_out, 39, 0, 1, 1, style_value)

    # Pied de page de la première fille
    footers = [{u"N.B: Ne pas remplir les cases Grisées": [40, 40, 0, 3]},
               {u"Spécifier autres admissions": [41, 41, 0, 2]},
               {u"Nombre de PV VIH": [42, 42, 0, 1]},
               {u"Nombre de Tuberculeux": [42, 42, 4, 6]},
               {u"PPN": [42, 42, 9, 9]},]
    write_merge_p(footers, style_without_border)

    footers_values = [{u"%s" % others_hiv: [42, 42, 2, 2]},
                      {u"%s" % others_tb: [42, 42, 7, 7]},
                      {u"%s" % others_lwb: [42, 42, 10, 10]}]
    write_merge_p(footers_values, style_value)

    #--------------------------------------------------------------------------#
    # INTRANTS
    sheet = book.add_sheet("INTRANTS")
    for i in range(7):
        sheet.col(i).width = 0x0d00 * 1.75

    sheet.row(9).height = 1050
    # Titres
    sheet.write_merge(0, 1, 0, 6,
                      u"RAPPORT MENSUEL SUR LA SITUATION DES INTRANTS PEC MA ",
                       style_title)

    liste_title = [u"REGION", u"District", u"CSCom", u"TYPE DE CENTRE", u"Mois"]
    write_p(liste_title, 2, 1, 0, 0, styleheader_left)
    val_title = [u"Gao", u" ", u"%s" % hc_name, u"%s" % type_center(),
                 u"%s" % report.period]
    write_p(val_title, 2, 1, 1, 0, styleheader_left)
    sheet.write(7,0, u"Les champs ci-dessus sont à remplir dans la feuille PEC.")

    #Tableau des intrants
    h_table_intrant = [u"Désignation", u"Stock Initial",
                       u"Quantités Reçues\npendant la période",
                       u"Quantités Utlisées\npendant la période",
                       u"Quantités Perdues*\npendant la période",
                       u"Quantités Disponibles\nUtilisables en Fin de\npériode",
                       u"Quantités commandées"]
    write_p(h_table_intrant, 9, 0, 0, 1, styleheader)

    # Table values

    data = []
    n = 10

    def geticr(report, code):
        if not report:
            return None
        try:
            return report.icr(code)
        except:
            raise

    for cap in (SEVERE_COMP, SEVERE, MODERATE):
        cap_cons_report = report.get_cons_report(cap)
        cap_order_report = report.get_order_report(cap)
        for iid, icr in [(iid, geticr(cap_cons_report, iid))
                         for iid in CONSUMPTION_TABLE[cap][DEFAULT_VERSION]]:

            if icr is None:
                input_name = u"%(cap)s %(name)s" % {'cap': HC_CAPS[cap],
                                                    'name': iid}
                sheet.write(n, 0, input_name, styleheader_left)
                write_p(empty(5), n, 0, 1, 1)
                n += 1
                continue

            ior = ior_class(order_report=cap_order_report,
                                          nut_input=icr.nut_input).get()

            data = ["%s" % icr.initial, "%s" % icr.received, "%s" % icr.used,
                    "%s" % icr.lost, "%s" % icr.left, "%s" % ior.quantity]
            input_name = u"%(cap)s %(name)s" % {'cap': HC_CAPS[cap],
                                                'name': icr.nut_input
                                                           .name.upper()}
            sheet.write(n, 0, input_name, styleheader_left)
            write_p(data, n, 0, 1, 1)
            n += 1

    sheet.write(23, 0, u"N.B: Le niveau opérationnel (URENI, "
                       u"URENAS et URENAM) et la compilation au "
                       u"niveau des Cercles utilisera l'unité la plus ")
    sheet.write(24, 0, u"élémentaire pour quantifier chacun des "
                       u"intrants (sachet, kg et litre).")
    sheet.write(25, 0, u"L'unité utilisée au niveau des DRS sera "
                       u"le carton, sac, tonnelet (ou bidons),…")

    sheet.write(27, 0, u"Stock début du mois = Solde fin du mois précédent "
                       u"(Ex: Stock début du mois de juin = solde fin de "
                       u"mois de mai)", styleheader_left_g)
    sheet.write(28, 0, u"Solde fin du mois = [Stock debut du mois + Stock recu "
                       u"(facultatif)] - [Stock utilisé + Stock perdu/avarié "
                       u"(facultatif)]", styleheader_left_g)

    sheet.write_merge(30, 30, 0, 6, "OBSERVATIONS", styleheader)
    sheet.write_merge(31, 44, 0, 6, "", style_value)

    stream = StringIO.StringIO()
    book.save(stream)

    return stream


def export_report(report, filepath=None):

    if not filepath:
        filepath = 'report-%s.xls' % str(report.period)
    print('exporting %s to %s' % (report, filepath))
 
    stream = export_report_stream(report)

    f = file(filepath, 'w')
    f.write(stream.getvalue())
    f.close()


def main(argv=[]):
    if len(argv):
        try:
            from nutclient.database import Report
            report = Report.select().get(id=int(argv[1]))
        except:
            report = None

        if not report:
            try:
                from ylmnut.nut.models import NutritionReport
                report = NutritionReport.objects.get(id=int(argv[1]))
            except:
                report = None

    if not report:
        try:
            report = Report.all()[-1]
        except:
            report = list(NutritionReport.objects.all())[-1]
    if not report:
        print("No report to export")
    export_report(report)

if __name__ == '__main__':
    main(sys.argv)
