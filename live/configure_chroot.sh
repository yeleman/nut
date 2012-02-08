#!/bin/bash

# copy files to chroot

function usage {
    echo "Usage: $0 [SOURCE DESTINATION]"
}

# if only one parameter
if [ $# -eq 1 ]; then
    usage
    exit
fi

SRC="~/nut/live"

if [ "$1" != "" ]; then
    SRC=$1
fi

DST="./chroot"

if [ "$2" != "" ]; then
    DST=$2
fi

echo "SOURCE: $SRC"
echo "DESTINATION: $DST"

# copy hooks
mkdir -p $DST/../config/includes.chroot/lib/live/config/
cp -v $SRC/800-inittab.hook $DST/../config/includes.chroot/lib/live/config/800-inittab || exit 1

# copy shadow template
cp -v $SRC/shadow.tmpl $DST/root/shadow.tmpl || exit 1

# copy d Window Manager
cp -v $SRC/dwm $DST/usr/bin/dwm || exit 1

# copy xinitrc to startx properly
cp -v $SRC/xinitrc $DST/etc/X11/xinit/xinitrc || exit 1

# copy gtkrc to setup GTK theme
cp -v $SRC/gtkrc $DST/etc/gtk-2.0/gtkrc || exit 1

# copy Trolltech.conf so that QT picks GTK theme
cp -v $SRC/Trolltech.conf $DST/etc/xdg/Trolltech.conf || exit 1

# copy rc-local which mounts partition
cp -v $SRC/rc.local $DST/etc/rc.local || exit 1

# copy crontab
cp -v $SRC/crontab $DST/etc/crontab || exit 1

# copy gammu-smsd init
cp -v $SRC/gammu-smsd.lsb $DST/etc/init.d/gammu-smsd || exit 1

# copy gammu defaults so it starts as nut
cp -v $SRC/gammu-smsd.default $DST/etc/default/gammu-smsd || exit 1

# copy gammu config
cp -v $SRC/gammurc $DST/etc/gammurc || exit 1
cp -v $SRC/gammu-smsdrc $DST/etc/gammu-smsdrc || exit 1

# copy gammu restart script
cp -v $SRC/restart_gammu $DST/usr/bin/restart_gammu

# create mount point for FAT32 partition
mkdir -p $DST/media/export || exit 1
chmod 777 $DST/media/export -R || exit 1
touch $DST/media/export/not_mounted || exit 1

# install gammu
if [ -x "$DST/gammu-installer.sh" ]; then
    echo "Installing " + `$DST/gammu-installer.sh --version`
    $DST/gammu-installer.sh --prefix=$DST/usr --exclude-subdir --skip-license
else
    echo "Unable to install Gammu. Archive $DST/gammu-installer.sh missing."
    exit 1
fi

# install NUT python code
mkdir -p $DST/opt/nut || exit 1
if [ -e $SRC/nut.tar.gz ]; then
    echo "Copying local nut code"
    cp -v $SRC/nut.tar.gz $DST/opt/nut.tar.gz
else
    echo "Downloading nut from github"
    wget -O $DST/opt/nut.tar.gz -c https://github.com/yeleman/nut/tarball/master
fi
# extract code to /opt/nut
tar xf $DST/opt/nut.tar.gz -C $DST/opt/nut/ --strip-components=1 || exit 1

# install bolibana python code
mkdir -p $DST/opt/bolibana
if [ -e $SRC/bolibana.tar.gz ]; then
    echo "Copying local bolibana code"
    cp -v $SRC/bolibana.tar.gz $DST/opt/bolibana.tar.gz
else
    echo "Downloading bolibana from github"
    wget -O $DST/opt/bolibana.tar.gz -c https://github.com/yeleman/bolibana/tarball/master
fi
# extract code to /opt/nut
tar xf $DST/opt/bolibana.tar.gz -C $DST/opt/bolibana/ --strip-components=1 || exit 1

# create pip bundle for dependencies
if [ -e $DST/../client/nutclient/pip-requirements.txt ]; then
    pip bundle $SRC/nutenv.pybundle -r $DST/../client/nutclient/pip-requirements.txt
else
    echo "Unable to find pip requirements file $DST/../client/nutclient/pip-requirements.txt"
    exit 1
fi

# copy pip bundle for later processing (chroot)
cp -v $SRC/nutenv.pybundle $DST/opt/nutenv.pybundle || exit 1

# copy nosmsd configuration
cp -v $SRC/nosmsd.conf.py $DST/etc/nosmsd.conf.py || exit 1

# copy client local configuration (for DB)
cp -v $SRC/local_config.py $DST/opt/nut/client/nutclient/local_config.py || exit 1

# copy in-chroot setup script
cp -v $SRC/setup_chroot.sh $DST/usr/bin/setup_chroot.sh || exit 1
