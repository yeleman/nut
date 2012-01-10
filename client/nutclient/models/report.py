#!/usr/bin/env python
# encoding=utf-8

from datetime import datetime

import peewee

from . import BaseModel, User, Period


class Report(BaseModel):

    STATUS_CREATED = 0 # blank created
    STATUS_DRAFT = 1 # started edition
    STATUS_COMPLETE = 2 # ready for transmission
    STATUS_SENT = 3 # SMS sent
    STATUS_REMOTE_MODIFIED = 4 # modified by server users
    STATUS_LOCAL_MODIFIED = 5 # modified locally after remote. next is SENT
    STATUS_VALIDATED = 6 # has been validated online.
    STATUSES = ((STATUS_CREATED, u"Vide"),
                (STATUS_DRAFT, u"Commencé"),
                (STATUS_COMPLETE, u"Terminé (non envoyé)"),
                (STATUS_SENT, u"Envoyé"),
                (STATUS_REMOTE_MODIFIED, u"Attente corrections"),
                (STATUS_LOCAL_MODIFIED, u"Corrigé (non envoyé)"),
                (STATUS_VALIDATED, u"Validé"))
    
    #report_id = peewee.PrimaryKeyField()
    created_by = peewee.ForeignKeyField(User, related_name='reports')
    created_on = peewee.DateTimeField()
    modified_on = peewee.DateTimeField(null=True)
    period = peewee.ForeignKeyField(Period, unique=True)
    status = peewee.IntegerField(default=STATUS_DRAFT)

    # Health Center informations
    # Subject to change over time
    hc_code = peewee.CharField(max_length=20)
    hc_name = peewee.CharField(max_length=50)
    hc_ismam = peewee.BooleanField(default=False)
    hc_issam = peewee.BooleanField(default=False)
    hc_issamp = peewee.BooleanField(default=False)

    # non-capability dependent fields: Others break down
    others_lwb = peewee.IntegerField(default=0)
    others_hiv = peewee.IntegerField(default=0)
    others_tb = peewee.IntegerField(default=0)

    def __unicode__(self):
        return self.period.__unicode__()

    def caps(self):
        caps = []
        for cap in ['mam', 'sam', 'samp']:
            if getattr(self, 'hc_is%s' % cap):
                caps.append(cap)
        return caps

    def verbose_caps(self):
        return "+".join([_(cap.upper()) for cap in self.caps()])

    @classmethod
    def opened(cls):
        return cls.filter(status__ne=cls.STATUS_SENT)

    @classmethod
    def create_safe(cls, period, user):
        # re-cast User
        user = User.filter(username=user.username).get()
        r = cls()
        r.created_by = user
        r.created_on = datetime.now()
        r.modified_on = datetime.now()
        r.period = period
        r.status = cls.STATUS_CREATED
        r.hc_code = user.hc_code
        r.hc_name = user.hc_name
        r.hc_ismam = user.hc_ismam
        r.hc_issam = user.hc_issam
        r.hc_issamp = user.hc_issamp
        r.save()

        # sorry: avoiding circular dependency
        from pec import PECMAMReport, PECSAMReport, PECSAMPReport
        from consumption import ConsumptionReport
        from order import OrderReport

        # creating all related reports with default values
        if r.is_mam:
            pec_mam = PECMAMReport(report=r)
            pec_mam.save()
            
            cons_mam = ConsumptionReport.create_safe(report=r, 
                                                 nut_type=ConsumptionReport.MAM)

            order_mam = OrderReport.create_safe(report=r, 
                                                nut_type=OrderReport.MAM)

        if r.is_sam:
            sam = PECSAMReport(report=r)
            sam.save()

            cons_sam = ConsumptionReport.create_safe(report=r, 
                                                 nut_type=ConsumptionReport.SAM)

            order_sam = OrderReport.create_safe(report=r, 
                                                nut_type=OrderReport.SAM)

        if r.is_samp:
            samp = PECSAMPReport(report=r)
            samp.save()

            cons_samp = ConsumptionReport.create_safe(report=r, 
                                                nut_type=ConsumptionReport.SAMP)

            order_samp = OrderReport.create_safe(report=r, 
                                                 nut_type=OrderReport.SAMP)

        return r

    def can_edit(self):
        """ Only if report has not been sent or has been modified remotely """
        return self.status in (self.STATUS_DRAFT,
                               self.STATUS_REMOTE_MODIFIED,
                               self.STATUS_LOCAL_MODIFIED)

    def verbose_status(self):
        for status, name in self.STATUSES:
            if status == self.status:
                return name
        return self.status

    @property
    def is_mam(self):
        return self.hc_ismam

    @property
    def is_sam(self):
        return self.hc_issam

    @property
    def is_samp(self):
        return self.hc_issamp

    def get_pec_report(self, cap):
        try:
            return getattr(self, 'pec_%s_reports' % cap.lower()).get()
        except:
            return None

    def get_cons_report(self, cap):
        from consumption import ConsumptionReport
        caps = {
                'mam': ConsumptionReport.MAM,
                'sam': ConsumptionReport.SAM,
                'samp': ConsumptionReport.SAMP}
        try:
            return self.cons_reports \
                       .filter(nut_type=caps[cap]).get()
        except:
            return None

    def get_order_report(self, cap):
        from order import OrderReport
        caps = {
                'mam': OrderReport.MAM,
                'sam': OrderReport.SAM,
                'samp': OrderReport.SAMP}
        try:
            return self.order_reports \
                       .filter(nut_type=caps[cap]).get()
        except:
            return None

    @property
    def pec_mam_report(self):
        return self.get_pec_report('mam')

    @property
    def pec_sam_report(self):
        return self.get_pec_report('sam')

    def pec_samp_report(self):
        return self.get_pec_report('samp')

    @property
    def cons_mam_report(self):
        return self.get_cons_report('mam')

    @property
    def cons_sam_report(self):
        return self.get_cons_report('sam')

    @property
    def cons_samp_report(self):
        return self.get_cons_report('samp')

    @property
    def order_mam_report(self):
        return self.get_order_report('mam')

    @property
    def order_sam_report(self):
        return self.get_order_report('sam')

    @property
    def order_samp_report(self):
        return self.get_order_report('samp')

    def reset_others(self):
        self.others_tb = 0
        self.others_hiv = 0
        self.others_lwb = 0

    def sum_for_field(self, field):
        total = 0
        for cap in ('mam', 'sam', 'samp'):
            rep = getattr(self, 'pec_%s_report' % cap)
            if hasattr(rep, field):
                total += getattr(rep, field)
        return total


class ReportHistory(BaseModel):

    report = peewee.ForeignKeyField(Report, related_name='exchanges')

    previous_status = peewee.CharField()
    # store a Pickle serialized version of changed fields
    # with previous values
    modified_fields = peewee.CharField()