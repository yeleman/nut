#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from nutrsc.data import PECMAMDataHolder, PECSAMDataHolder, PECSAMPDataHolder
from nutrsc.data import CONSMAMDataHolder, CONSSAMDataHolder, CONSSAMPDataHolder, CONSInputDataHolder, ORDERInputDataHolder


def report_sms(report):
    ''' SMS formatted string representing a full report

    nut report login pwhash <this content>-EOM-'''

    def holder_for(cap, section):
        if section == 'P':
            format = 'PEC%sDataHolder'
        elif section == 'C':
            format = 'CONS%sDataHolder'
        elif section == 'O':
            format = 'CONS%sDataHolder'
        return eval(format % cap.upper())
    
    def input_holder_for(section):
        if section == 'C':
            return CONSInputDataHolder
        elif section == 'O':
            return ORDERInputDataHolder

    def report_for(report, section, cap):
        if section == 'P':
            acc = 'pec'
        elif section == 'C':
            acc = 'cons'
        elif section == 'O':
            acc = 'order'
        return getattr(report, 'get_%s_report' % acc)(cap) 

    # report date
    sms = u"%(mo)s%(year)s " % {'mo': str(report.period.month).zfill(2),
                                'year': str(report.period.year)[2:]}

    for section in ('P'):

        # Section ID
        sms += u"#%(section)s" % {'section': section}

        for cap in report.caps():

            section_cap = holder_for(cap, section)()

            # add cap ID
            sms += u"&%(cap)s" % {'cap': cap.upper()}

            # retrive this section cap report
            cap_report = report_for(report, section, cap)

            for age, age_name in cap_report.CATEGORIES:

                # add age ID
                sms += u"|%(age)s " % {'age': age}

                sms += u" ".join([str(getattr(cap_report, field))
                           for field in section_cap.fields_for(age)])

    for section in ('C', 'O'):

        # Section ID
        sms += u"#%(section)s" % {'section': section}

        for cap in report.caps():

            section_cap = holder_for(cap, section)()

            # add cap ID
            sms += u"&%(cap)s" % {'cap': cap.upper()}

            # retrieve this section cap report
            cap_report = report_for(report, section, cap)

            for input_report in cap_report.nutinput_reports:

                # add age ID
                sms += u"|%(code)s " % {'code': input_report.nut_input.slug}

                input_data = input_holder_for(section)()
                input_data.input_code = input_report.nut_input.slug

                sms += u" ".join([str(getattr(input_report, field))
                           for field in input_data.fields()])

    # Other reports
    sms += u"#T %(lwb)d %(tb)d %(hiv)d" % {'lwb': report.others_lwb,
                                           'tb': report.others_tb,
                                           'hiv': report.others_hiv}

    return sms