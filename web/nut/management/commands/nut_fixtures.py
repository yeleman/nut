#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu


from django.core.management.base import BaseCommand
from django.contrib.auth.models import ContentType

from bolibana.models import Access
from nut.models import NUTEntity


class Command(BaseCommand):

    def handle(self, *args, **options):

        print(u"Fix Access fixtures")

        nut_id = None
        # find the ID of the NUTEntity CT
        for ct in ContentType.objects.all():
            if ct.model_class() == NUTEntity:
                nut_id = ct
                break
        
        if not nut_id:
            print(u"Unable to find %s in ContentType" % NUTEntity)
            exit(1)

        access = Access.objects.all()

        for acc in access:
            acc.content_type = nut_id
            acc.save()
            print(u"\tfixed %s" % acc)
        
        print(u"All done.")

