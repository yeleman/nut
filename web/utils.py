#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

"""
    Generic tools that should be in nutsrc or anywhere else but that while
    have to put here untill the python path and import issues are sorted
    out.
"""


def extract(data, *keys, **kwargs):
    """
        Extract a data from nested mapping and sequences using a list of keys
        and indices to apply successively. If a key error or an index error
        is raised, returns the default value.

        res = extract(data, 'test', 0, 'bla')

        is the equivalent of

        try:
            res = data['test'][0]['bla']
        except (KeyError, IndexError):
            res = None

    """
    try:
      value = data[keys[0]]

      for key in keys[1:]:
          value = value[key]
    except (KeyError, IndexError, TypeError):
      return kwargs.get('default', None)

    return value