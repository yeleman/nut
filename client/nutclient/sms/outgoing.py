#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu}

from nutrsc.data import PECMAMDataHolder, PECSAMDataHolder, PECSAMPDataHolder
from nutrsc.data import CONSMAMDataHolder, CONSSAMDataHolder, CONSSAMPDataHolder, CONSInputDataHolder, ORDERInputDataHolder
from nutrsc.mali import compress_pec_field, compress_cons_field

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


def report_sms(report):
    ''' SMS formatted string representing a full report

    nut report login pwhash <this content>-EOM-'''

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

def report_update_sms(report):

    def dirty_fields(report):
        d = {}
        exclude = ('id',
                   'created_by',
                   'created_on',
                   'modified_on',
                   'period',
                   'status',
                   'hc_code',
                   'hc_name',
                   'hc_ismam',
                   'hc_issam',
                   'hc_issamp',
                   'cons_report',
                   'order_report',
                   'nut_input',
                   'report',
                   'nut_type',
                   'version')
        for k, v in report.dirty_fields.items():
            if not k in exclude:
                d[k] = v
        return d

    # report date
    sms = []
    sms.append(u"%(mo)s%(year)s " % {'mo': str(report.period.month).zfill(2),
                                     'year': str(report.period.year)[2:]})

    for section in ('P'):

        sec_sms = []

        for cap in report.caps():

            section_cap = holder_for(cap, section)()

            # retrive this section cap report
            cap_report = report_for(report, section, cap)

            print(cap_report)

            df = dirty_fields(cap_report)
            print(df)
            if len(df):
                sec_sms.append(u"&%(cap)s" % {'cap': cap.upper()})

                for field, value in df.items():
                    sec_sms.append((u"%(code)s:%(val)d"
                            % {'code': compress_pec_field(field),
                               'val': value}))
        if len(sec_sms):
            # Section ID
            sms.append(u"#%(section)s" % {'section': section})
            sms += sec_sms

    for section in ('C', 'O'):

        sec_sms = []

        for cap in report.caps():

            section_cap = holder_for(cap, section)()

            cap_sms = []

            # retrieve this section cap report
            cap_report = report_for(report, section, cap)
            print(cap_report)
            for input_report in cap_report.nutinput_reports:
                print(input_report.nut_input.slug)

                input_data = input_holder_for(section)()
                input_data.input_code = input_report.nut_input.slug

                df = dirty_fields(input_report)

                # only add if there's something
                if len(df):
                    #cap_sms.append(u"|%(code)s "
                    #           % {'code': input_report.nut_input.slug})

                    for field, value in df.items():
                        cap_sms.append((u"%(code)s:%(val)d"
                                    % {'code': compress_cons_field(input_report.nut_input.slug,
                                                                   field),
                                       'val': value}))
            if len(cap_sms):
                sec_sms.append(u"&%(cap)s" % {'cap': cap.upper()})
                sec_sms += cap_sms

        if len(sec_sms):
            # Section ID
            sms.append(u"#%(section)s" % {'section': section})
            sms += sec_sms

    # Other reports
    df = dirty_fields(report)
    if len(df):
        sms.append(u"#T")
        for field, value in df.items():
            print(field)
            sms.append((u"%(code)s:%(val)d"
                % {'code': compress_pec_field(field),
                   'val': value}))

    return ' '.join(sms)