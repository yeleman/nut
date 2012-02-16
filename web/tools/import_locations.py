#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import sys

from bolibana.models import EntityType
from nut.models import NUTEntity


def import_locations(csv_file, use_code=False):
    """ creates Entity object off a CSV filename

    CSV FORMAT:
    NAME, CODE, TYPE SLUG, PARENT ID
    CSV file must NOT include header row. """

    f = open(csv_file)
    for line in f.readlines():
        # explode CSV line
        name, code, type_slug, parent_id, \
        is_mam, is_sam, is_samp = line.strip().split(',')

        # convert name to unicode for django & .title()
        try:
            name = unicode(name, 'utf-8')
        except:
            pass

        # retrieve parent object if address is provided
        try:
            parent = NUTEntity.objects.get(slug=parent_id)
        except:
            parent = None

        # retrieve type from code
        type = EntityType.objects.get(slug=type_slug)

        # create and save object
        entity = NUTEntity(name=name.title(), type=type, \
                           slug=code.lower(), parent=parent,
                           is_mam=bool(is_mam), is_sam=bool(is_sam),
                           is_samp=bool(is_samp))
        entity.save()

        print("%s: %s" % (entity.name, type))
    f.close()

if __name__ == '__main__':
    if sys.argv.__len__() < 2:
        print("No CSV file specified. exiting.")
        exit(1)

    import_locations(sys.argv[1])