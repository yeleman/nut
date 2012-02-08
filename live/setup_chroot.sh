#!/bin/bash

# executed from within chroot
## setup python environnement

cd /opt/

echo "Installing virtualenv bundle"
/usr/bin/pip install virtualenv.pybundle || exit 1

echo "Creating environnement"
/usr/local/bin/virtualenv nutenv || exit 1
source /opt/nutenv/bin/activate || exit 1

echo "Installing nutenv bundle"
/opt/nutenv/bin/pip install nutenv.pybundle || exit 1

echo "Creating symlink"
/bin/ln -sf /opt/bolibana /opt/nutenv/lib/python2.6/site-packages/bolibana || exit 1
/bin/ln -sf /opt/nut/client/nutclient /opt/nutenv/lib/python2.6/site-packages/nutclient || exit 1
/bin/ln -sf /opt/nut/nutrsc /opt/nutenv/lib/python2.6/site-packages/nutrsc || exit 1
