#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _, ugettext_lazy
from django.conf import settings

from bolibana.web.decorators import provider_required
from bolibana.tools.utils import send_email


def contact_choices(contacts):
    """ returns (a[0], a[1] for a in a list """
    # SUPPORT_CONTACTS contains slug, name, email
    # we need only slug, name for contact form.
    return [(slug, name) for slug, name, email in settings.SUPPORT_CONTACTS]


class ContactForm(forms.Form):
    """ Simple contact form with recipient choice """

    name = forms.CharField(max_length=50, required=True, \
                                 label=ugettext_lazy(u"Your Name"))
    email = forms.EmailField(required=False, \
                             label=ugettext_lazy(u"Your e-mail address"))
    phone_number = forms.CharField(max_length=12, required=False, \
                                   label=ugettext_lazy(u"Your phone number"))
    subject = forms.CharField(max_length=50, required=False, \
                                label=ugettext_lazy(u"Subject"))

    recipient = forms.ChoiceField(required=False, \
                                  label=ugettext_lazy(u"Recipient"), \
                          choices=contact_choices(settings.SUPPORT_CONTACTS), \
                                  help_text=_(u"Choose DNS for operational " \
                                              u"requests and ANTIM for " \
                                              u"technical ones."))

    message = forms.CharField(required=True, \
                              label=ugettext_lazy(u"Your request"), \
                              widget=forms.Textarea)


def contact(request):
    category = 'contact'
    context = {'category': category}

    try:
        web_provider = request.user.get_profile()
    except:
        web_provider = None

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            try:
                dest_mail = [email for s, n, email \
                                   in settings.SUPPORT_CONTACTS \
                                   if s == 'pnlp'][0]
            except:
                dest_mail = []

            mail_cont = {'provider': web_provider, \
                         'name': form.cleaned_data.get('name'),
                         'email': form.cleaned_data.get('email'),
                         'phone_number': form.cleaned_data.get('phone_number'),
                         'subject': form.cleaned_data.get('subject'),
                         'message': form.cleaned_data.get('message')}

            sent, sent_message = send_email(recipients=dest_mail, \
                                        context=mail_cont,
                                       template='emails/support_request.txt', \
                             title_template='emails/title.support_request.txt')
            if sent:
                messages.success(request, _(u"Support request sent."))
                return redirect('support')
            else:
                messages.error(request, _(u"Unable to send request. Please " \
                                          "try again later."))

    if request.method == 'GET':
        if web_provider:
            initial_data = {'name': web_provider.name_access, \
                          'email': web_provider.email, \
                          'phone_number': web_provider.phone_number}
        else:
            initial_data = {}

        form = ContactForm(initial=initial_data)

    context.update({'form': form})

    return render(request, 'contact.html', context)


@provider_required
def dashboard(request):
    category = 'dashboard'
    context = {'category': category}

    from bolibana.models import Entity
    from nut.models import NutritionReport
    from nut.data import (current_period, \
                          current_reporting_period, current_stage, \
                          time_cscom_over, time_district_over, \
                          time_region_over, contact_for)

    def sms_received_sent_by_period(period):
        from nosmsd.models import Inbox, SentItems
        received = Inbox.objects\
                        .filter(receivingdatetime__gte=period.start_on,
                                receivingdatetime__lte=period.end_on).count()
        sent = SentItems.objects\
                        .filter(sendingdatetime__gte=period.start_on,
                                sendingdatetime__lte=period.end_on).count()
        return (received, sent)

    current_period = current_period()
    period = current_reporting_period()

    context.update({'current_period': current_period,
                    'current_reporting_period': period,
                    'current_stage': current_stage(),
                    'current_sms': sms_received_sent_by_period(current_period),
                    'current_reporting_sms': \
                         sms_received_sent_by_period(period),
                    'total_cscom': Entity.objects\
                                         .filter(type__slug='cscom').count(),
                    'time_cscom_over': time_cscom_over(period),
                    'time_district_over': time_district_over(period),
                    'time_region_over': time_region_over(period)})

    received_cscom_reports = \
        NutritionReport.objects.filter(period=period, entity__type__slug='cscom')
    cscom_reports_validated = \
        NutritionReport.validated.filter(period=period, \
                                       entity__type__slug='cscom')
    district_reports_validated = \
        NutritionReport.validated.filter(period=period, \
                                       entity__type__slug='district')
    reporting_rate = \
        float(NutritionReport.validated.filter(period=period).count()) \
        / Entity.objects.count()

    cscom_missed_report = \
        Entity.objects.filter(type__slug='cscom')\
                      .exclude(id__in=[r.entity.id \
                                       for r \
                                       in received_cscom_reports])\
                      .order_by('name')

    def entities_autoreports(level):
        districts_missed_report = {}
        auto_validated_cscom_reports = \
            NutritionReport.validated\
                         .filter(entity__type__slug=level, \
                                 modified_by__user__username='autobot')
        for report in auto_validated_cscom_reports:
            if not report.entity.parent.slug in districts_missed_report:
                districts_missed_report[report.entity.parent.slug] = \
                    {'entity': report.entity.parent, \
                     'nbauto': 0, \
                     'contact': contact_for(report.entity.parent, False)}
            districts_missed_report[report.entity.parent.slug]['nbauto'] += 1
        return districts_missed_report

    districts_missed_report = entities_autoreports('cscom')
    regions_missed_report = entities_autoreports('district')

    context.update({'received_cscom_reports': received_cscom_reports.count(),
                'cscom_reports_validated': cscom_reports_validated.count(),
              'district_reports_validated': district_reports_validated.count(),
                'reporting_rate': reporting_rate,
                'cscom_missed_report_count': cscom_missed_report.count(),
                'cscom_missed_report': [(e, contact_for(e, True)) \
                                        for e in cscom_missed_report[:20]],
                'districts_missed_report': districts_missed_report,
                'regions_missed_report': regions_missed_report})

    return render(request, 'dashboard.html', context)


class DateForm(forms.Form):
    import datetime
    date = forms.DateField(initial=datetime.date.today)


def change_date(request):

    context = {}

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            import subprocess
            subprocess.call(['sudo', 'date',
                             form.cleaned_data.get('date') \
                                              .strftime('%m%d1200%Y')])
            context.update({'success': True})
        else:
            pass
        print form
    else:
        form = DateForm()

    context.update({'form': form})

    return render(request, 'date.html', context)
