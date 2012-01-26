#!/usr/bin/env python
# encoding: utf-8
# maintainer: rgaudin

from django.utils.translation import ugettext as _

from bolibana.models import Provider, Entity
from nut.models import NUTEntity
from nutrsc.errors import LOGIN_ERRORS


def nut_login(message, args, sub_cmd, **kwargs):
    """ Client login handshake

    At first use or on request, user identifies itself into the system.
    He sends his login/pwhash to the server.
    The server then sends back either an error code + message or a credential
    with an indication of the HC capabilities: MAM, SAM, SAM+.

    > nut login rgaudin 4663950500290933446
    < nut logged-in 4663950500290933446 mam+sam ntil|N'Tillit
                hash capabilities HC-code | HC Name
    < nut logged-out 0|Cet identifiant n'existe pas.
                 Error-code | Error Message """

    def resp_error(code, msg):
        message.respond(u"nut logged out %(code)s|%(msg)s" \
                        % {'code': code, 'msg': msg})
        return True

    def nut_capabilities(entity):
        if isinstance(entity, Entity):
            entity = NUTEntity.objects.get(id=entity.id)
        caps = []
        for cap in ('mam', 'sam', 'samp'):
            if getattr(entity, 'is_%s' % cap):
                caps.append(cap)
        return '+'.join(caps)

    # extract username & pwhash
    try:
        username, pwhash = args.split()
        username = username.strip()
        pwhash = pwhash.strip()
    except:
        return resp_error('OTHER', _(u"Malformed login request."))

    # get Provider based on username
    try:
        provider = Provider.objects.get(user__username=username)
    except Provider.DoesNotExist:
        return resp_error('NO_ACC', LOGIN_ERRORS['NO_ACC'])

    # check that provider pwhash is good
    if not provider.check_hash(pwhash):
        return resp_error('BAD_PASS', LOGIN_ERRORS['BAD_PASS'])

    # check that user is not disabled
    if not provider.is_active:
        return resp_error('ACC_DIS', LOGIN_ERRORS['ACC_DIS'])
    
    # retrieve entity
    try:
        entity = provider.first_target()
    except:
        return resp_error('OTHER', _(u"Username is not tied to an Entity."))

    try:
        nutcap = nut_capabilities(entity)
    except:
        nutcap = None

    if not nutcap:
        return resp_error('OTHER', _(u"Username's Entity is not NUT."))

    # all good, let's send that SMS back
    msg = u"nut logged-in %(user)s %(hash)s %(nutcap)s %(hcslug)s|%(hcname)s" \
          % {'hash': pwhash, 'nutcap': nutcap, 'hcslug': entity.slug,
             'hcname': entity.name.title(), 'user': username}

    message.respond(msg)
    return True
