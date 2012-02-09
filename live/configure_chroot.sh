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

# copy shadow template
cp -v $SRC/shadow.tmpl $DST/root/shadow.tmpl || exit 1

# copy d Window Manager
cp -v $SRC/dwm $DST/usr/bin/dwm.nut || exit 1
chmod +x $DST/usr/bin/dwm.nut || exit 1

# copy xinitrc to startx properly
cp -v $SRC/xinitrc $DST/etc/X11/xinit/xinitrc || exit 1

# copy gtkrc to setup GTK theme
cp -v $SRC/gtkrc $DST/etc/gtk-2.0/gtkrc || exit 1

# copy Trolltech.conf so that QT picks GTK theme
mkdir -p $DST/etc/xdg || exit 1
cp -v $SRC/Trolltech.conf $DST/etc/xdg/Trolltech.conf || exit 1

# copy rc-local which mounts partition
cp -v $SRC/rc.local $DST/etc/rc.local || exit 1
chmod +x $DST/etc/rc.local || exit 1

# copy crontab
cp -v $SRC/crontab $DST/etc/crontab || exit 1

# copy gammu-smsd init
cp -v $SRC/gammu-smsd.lsb $DST/etc/init.d/gammu-smsd || exit 1
chmod +x $DST/etc/init.d/gammu-smsd || exit 1

# copy gammu defaults so it starts as nut
cp -v $SRC/gammu-smsd.default $DST/etc/default/gammu-smsd || exit 1

# copy gammu config
cp -v $SRC/gammurc $DST/etc/gammurc || exit 1
cp -v $SRC/gammu-smsdrc $DST/etc/gammu-smsdrc || exit 1

# copy gammu restart script
cp -v $SRC/restart_gammu $DST/usr/bin/restart_gammu || exit 1
chmod +x $DST/usr/bin/restart_gammu || exit 1

# create mount point for FAT32 partition
mkdir -p $DST/media/export || exit 1
chmod 777 $DST/media/export -R || exit 1
touch $DST/media/export/not_mounted || exit 1

# install gammu
if [ -x "$SRC/gammu-installer.sh" ]; then
    echo "Installing " + `$SRC/gammu-installer.sh --version`
    $SRC/gammu-installer.sh --prefix=$DST/usr --exclude-subdir --skip-license || exit 1
else
    echo "Unable to install Gammu. Archive $SRC/gammu-installer.sh missing."
    exit 1
fi

# install NUT python code
rm -rf $DST/opt/nut/ || exit 1
mkdir -p $DST/opt/nut || exit 1
if [ -e $SRC/nut.tar.gz ]; then
    echo "Copying local nut code"
    cp -v $SRC/nut.tar.gz $DST/opt/nut.tar.gz || exit 1
else
    echo "Downloading nut from github"
    wget -O $DST/opt/nut.tar.gz -c https://github.com/yeleman/nut/tarball/master || exit 1
fi
# extract code to /opt/nut
# ignore tar error as github archive contain garbage
tar xf $DST/opt/nut.tar.gz -C $DST/opt/nut/ --strip-components=1

# install bolibana python code
rm -rf $DST/opt/bolibana/ || exit 1
mkdir -p $DST/opt/bolibana || exit 1
if [ -e $SRC/bolibana.tar.gz ]; then
    echo "Copying local bolibana code"
    cp -v $SRC/bolibana.tar.gz $DST/opt/bolibana.tar.gz || exit 1
else
    echo "Downloading bolibana from github"
    wget -O $DST/opt/bolibana.tar.gz -c https://github.com/yeleman/bolibana/tarball/master || exit 1
fi
# extract code to /opt/nut
# ignore tar error as github archive contain garbage
tar xf $DST/opt/bolibana.tar.gz -C $DST/opt/bolibana/ --strip-components=1

#create virtualenv bundle
if [ -e $SRC/virtualenv.pybundle ]; then
    echo "virtualenv bundle exist."
else
    pip bundle $SRC/virtualenv.pybundle virtualenv || exit 1
fi

# copy virtualenv bundle for later processing (chroot)
cp -v $SRC/virtualenv.pybundle $DST/opt/virtualenv.pybundle || exit 1

# create pip bundle for dependencies
if [ -e $SRC/../client/nutclient/pip-requirements.txt ]; then
    if [ -e $SRC/nutenv.pybundle ]; then
        echo "nutenv bundle exist."
    else
        pip bundle $SRC/nutenv.pybundle -r $SRC/../client/nutclient/pip-requirements.txt || exit 1
    fi
else
    echo "Unable to find pip requirements file $SRC/../client/nutclient/pip-requirements.txt"
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
chmod +x $DST/usr/bin/setup_chroot.sh || exit 1

# copy live hooks
cp -v $SRC/016-sysvinit.hook $DST/lib/live/config/016-sysvinit || exit 1
chmod +x $DST/lib/live/config/016-sysvinit || exit 1
cp -v $SRC/810-adduser.hook $DST/lib/live/config/810-adduser || exit 1
chmod +x $DST/lib/live/config/810-adduser || exit 1