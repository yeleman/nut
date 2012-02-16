#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import sys

import xlwt

from database import Report

def export_report(report, filepath=None):
    if not filepath:
        filepath = 'report-%s.xls' % str(report.period)
    print('exporting %s to %s' % (report, filepath))


def main(argv):
    report = Report.all()[-1]
    export_report(report)

if __name__ == '__main__':
    main(sys.argv)