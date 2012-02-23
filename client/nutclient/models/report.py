#!/usr/bin/env python
# encoding=utf-8

from datetime import datetime

import peewee

from . import BaseModel, User, Period


class Report(BaseModel):

    """ Workflow:
        1. CREATED (internal)
        2. DRAFT (anytime before it reachs end of forms)
        3. COMPLETE (end of form if data is valid) | can send
        4. SENT | can send (resend) 
        5. RECEIVED (server ack reception) | can NOT send
        6. REMOTE_MODIFIED (received edits from server) | can NOT send
        7. LOCAL_MODIFIED (updated after received) | can send
        8. MODIFIED_SENT | can send
        9. MODIFIED_RECEIVED | can NOT send
        10. VALIDATED | can NOT send """
    STATUS_CREATED = 0 # blank created
    STATUS_DRAFT = 1 # started edition
    STATUS_COMPLETE = 2 # ready for transmission
    STATUS_SENT = 3 # SMS sent
    STATUS_RECEIVED = 4 # SMS sent and received by server
    STATUS_REMOTE_MODIFIED = 5 # modified by server users
    STATUS_LOCAL_MODIFIED = 6 # modified locally after remote.
    STATUS_MODIFIED_SENT = 7 # update sent
    STATUS_MODIFIED_RECEIVED = 8 # SMS update sent and received by server
    STATUS_VALIDATED = 9 # has been validated online.
    STATUSES = ((STATUS_CREATED, u"Commencé"),
                (STATUS_DRAFT, u"Commencé"),
                (STATUS_COMPLETE, u"Terminé (non envoyé)"),
                (STATUS_SENT, u"Envoyé"),
                (STATUS_RECEIVED, u"envoyé (reçu)"),
                (STATUS_REMOTE_MODIFIED, u"Attente corrections"),
                (STATUS_LOCAL_MODIFIED, u"Corrigé (non envoyé)"),
                (STATUS_MODIFIED_SENT, u"Envoyé (corrigé)"),
                (STATUS_MODIFIED_RECEIVED, u"envoyé (corrigé reçu)"),
                (STATUS_VALIDATED, u"Validé"))
    
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
    
    def __repr__(self):
        return '%d/%d' % (self.period.month, self.period.year)

    def caps(self):
        caps = []
        for cap in ['samp', 'sam', 'mam']:
            if getattr(self, 'hc_is%s' % cap):
                caps.append(cap)
        return caps

    def verbose_caps(self):
        return "+".join([cap.upper() for cap in self.caps()])

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
            
            ConsumptionReport.create_safe(report=r, 
                                          nut_type=ConsumptionReport.MAM)

            OrderReport.create_safe(report=r, 
                                    nut_type=OrderReport.MAM)

        if r.is_sam:
            sam = PECSAMReport(report=r)
            sam.save()

            ConsumptionReport.create_safe(report=r, 
                                          nut_type=ConsumptionReport.SAM)

            OrderReport.create_safe(report=r, 
                                    nut_type=OrderReport.SAM)

        if r.is_samp:
            samp = PECSAMPReport(report=r)
            samp.save()

            ConsumptionReport.create_safe(report=r, 
                                          nut_type=ConsumptionReport.SAMP)

            OrderReport.create_safe(report=r, 
                                    nut_type=OrderReport.SAMP)

        return r

    def create_revision_safe(self):

        for report in self.tied_reports():
            report.create_revision_safe()

        self.create_revision()

    def delete_safe(self):

        for report in self.tied_reports():
            report.delete_safe()

        self.delete_instance()

    def can_edit(self):
        """ Only if report has not been sent or has been modified remotely """

        return self.status in (self.STATUS_CREATED,
                               self.STATUS_DRAFT,
                               self.STATUS_COMPLETE,
                               self.STATUS_REMOTE_MODIFIED,
                               self.STATUS_LOCAL_MODIFIED)


    def can_send(self):
        return self.status in (self.STATUS_COMPLETE,
                               self.STATUS_SENT,
                               self.STATUS_LOCAL_MODIFIED,
                               self.STATUS_MODIFIED_SENT)

    def touch(self):
        """ mark report as changed (change status according to previous one) """

        # can't touch such a report
        if self.status in (self.STATUS_SENT,
                           self.STATUS_RECEIVED,
                           self.STATUS_MODIFIED_SENT,
                           self.STATUS_MODIFIED_RECEIVED,
                           self.STATUS_VALIDATED):
            return False
        
        if self.status <= self.STATUS_COMPLETE:
            self.status = self.STATUS_DRAFT
        else:
            self.status = self.STATUS_LOCAL_MODIFIED
        self.save()
        return True

    def verbose_status(self):
        for status, name in self.STATUSES:
            if status == self.status:
                return name
        return self.status

    def tied_reports(self):

        for type_ in ('pec', 'cons', 'order'):
            for report in self.get_reports(type_):
                yield report

    def is_valid(self):
        # launch checks on all sub-reports then change status.
        for report in self.tied_reports():
            print('checking %s' % report)
            if not report.is_valid():
                return False
        
        # check the Other values
        pec_reports_others = sum([report.all_other for report in self.pec_reports()])
        if self.all_others != pec_reports_others:
            return False
        
        return True

    @property
    def is_mam(self):
        return self.hc_ismam

    @property
    def is_sam(self):
        return self.hc_issam

    @property
    def is_samp(self):
        return self.hc_issamp

    def get_reports(self, type_):
        reports = []
        for cap in self.caps():
            report = getattr(self, 'get_%s_report' % type_)(cap)
            if report:
                reports.append(report)
        return reports

    def pec_reports(self):
        return self.get_reports('pec')

    def cons_reports(self):
        return self.get_reports('cons')

    def order_reports(self):
        return self.get_reports('order')

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

    @property
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
    
    @property
    def all_others(self):
        return sum([self.others_lwb, self.others_hiv, self.others_tb])
    
    @property
    def sum_all_others(self):
        ''' sum of all others field from linked reports '''
        return sum([report.all_other for report in self.pec_reports()])

    def has_previous_validated(self):
        return Report.filter(period=self.period.previous(),
                             status=self.STATUS_VALIDATED).count()

    def previous(self):
        if self.has_previous_validated():
            return Report.filter(period=self.period.previous(),
                                 status=self.STATUS_VALIDATED).get()
        return None

    def mark_as_complete(self):
        if self.status < self.STATUS_COMPLETE:
            self.status = self.STATUS_COMPLETE
            self.save()

    def sum_pec_fields(self, field):
        return sum([getattr(r, field, 0) for r in self.pec_reports()])

    @property
    def sum_all_other(self):
        return self.sum_pec_fields('all_other')

    @property
    def sum_all_total_out(self):
        return self.sum_pec_fields('all_total_out')

    @property
    def sum_all_healed(self):
        return self.sum_pec_fields('all_healed')

    @property
    def sum_all_aborted(self):
        return self.sum_pec_fields('all_aborted')

    @property
    def sum_all_deceased(self):
        return self.sum_pec_fields('all_deceased')

    @property
    def sum_all_non_respondant(self):
        return self.sum_pec_fields('all_non_respondant')

    @property
    def sum_all_total_beginning(self):
        return self.sum_pec_fields('all_total_beginning')

    @property
    def sum_all_total_beginning_m(self):
        return self.sum_pec_fields('all_total_beginning_m')

    @property
    def sum_all_total_beginning_f(self):
        return self.sum_pec_fields('all_total_beginning_f')

    @property
    def sum_all_total_admitted(self):
        return self.sum_pec_fields('all_total_admitted')

    @property
    def sum_all_hw_b7080_bmi_u18(self):
        return self.sum_pec_fields('all_hw_b7080_bmi_u18')

    @property
    def sum_all_muac_u120(self):
        return self.sum_pec_fields('all_muac_u120')

    @property
    def sum_all_hw_u70_bmi_u16(self):
        return self.sum_pec_fields('all_hw_u70_bmi_u16')

    @property
    def sum_all_muac_u11_muac_u18(self):
        return self.sum_pec_fields('all_muac_u11_muac_u18')

    @property
    def sum_all_oedema(self):
        return self.sum_pec_fields('all_oedema')

    @property
    def sum_all_new_case(self):
        return self.sum_pec_fields('all_new_case')

    @property
    def sum_all_relapse(self):
        return self.sum_pec_fields('all_relapse')

    @property
    def sum_all_returned(self):
        return self.sum_pec_fields('all_returned')

    @property
    def sum_all_nut_transfered_in(self):
        return self.sum_pec_fields('all_nut_transfered_in')

    @property
    def sum_all_nut_referred_in(self):
        return self.sum_pec_fields('all_nut_referred_in')

    @property
    def sum_all_total_admitted(self):
        return self.sum_pec_fields('all_admitted')

    @property
    def sum_all_total_admitted_m(self):
        return self.sum_pec_fields('all_admitted_m')

    @property
    def sum_all_total_admitted_f(self):
        return self.sum_pec_fields('all_admitted_f')

    @property
    def sum_all_admitted(self):
        return self.sum_pec_fields('all_admitted')

    @property
    def sum_all_admitted_m(self):
        return self.sum_pec_fields('all_admitted_m')

    @property
    def sum_all_admitted_f(self):
        return self.sum_pec_fields('all_admitted_f')

    @property
    def sum_all_refered_out(self):
        return self.sum_pec_fields('all_refered_out')

    @property
    def sum_all_referred_out(self):
        return self.sum_pec_fields('all_refered_out')

    @property
    def sum_all_medic_transfered_out(self):
        return self.sum_pec_fields('all_total_medic_transfered_out')

    @property
    def sum_all_nut_transfered_out(self):
        return self.sum_pec_fields('all_total_nut_transfered_out')

    @property
    def sum_all_total_out_m(self):
        return self.sum_pec_fields('all_total_out_m')

    @property
    def sum_all_total_out_f(self):
        return self.sum_pec_fields('all_total_out_f')

    @property
    def sum_all_total_end(self):
        return self.sum_pec_fields('all_total_end')

    @property
    def sum_all_total_end_m(self):
        return self.sum_pec_fields('all_total_end_m')

    @property
    def sum_all_total_end_f(self):
        return self.sum_pec_fields('all_total_end_f')


class ReportHistory(BaseModel):

    report = peewee.ForeignKeyField(Report, related_name='exchanges')

    previous_status = peewee.CharField()
    # store a Pickle serialized version of changed fields
    # with previous values
    modified_fields = peewee.CharField()