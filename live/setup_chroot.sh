#!/bin/bash

# executed from within chroot
## setup python environnement

cd /opt/

# create environnement
/usr/bin/virtualenv nutenv || exit 1
source /opt/nutenv/bin/activate || exit 1
/usr/bin/pip install nutenv.pybundle || exit 1

/bin/ln -sf /opt/bolibana /opt/nutenv/lib/python2.6/site-packages/bolibana || exit 1
/bin/ln -sf /opt/nut/client/nutclient /opt/nutenv/lib/python2.6/site-packages/nutclient || exit 1
/bin/ln -sf /opt/nut/nutrsc /opt/nutenv/lib/python2.6/site-packages/nutrsc || exit 1
