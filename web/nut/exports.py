#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin
# maintainer: Fad

import xlwt
import StringIO


def report_as_excel(report):
    """ Export les données d'un rapport en xls """

    book = xlwt.Workbook(encoding='utf-8')

    sheet = book.add_sheet(u"Report")

    sheet.write(0, 0, u"Reçu")
    sheet.write(0, 1, report.receipt)

    stream = StringIO.StringIO()
    book.save(stream)

    return stream
