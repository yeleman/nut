#!/bin/bash

SRC=$1 || exit 1
DST=$2 || exit 1

echo "## lb config"
lb config --binary-images usb-hdd --architecture i386 --linux-flavours i686 --apt-secure false --mirror-bootstrap http://affoo:3142/debian --mirror-chroot http://affoo:3142/debian --mirror-chroot-security http://affoo:3142/security --mirror-binary http://affoo:3142/debian --mirror-binary-security http://affoo:3142/security --packages-list minimal --packages "xserver-xorg git-core vim xinit acpi python-qt4 gtk2-engines-murrine usb-modeswitch python-pip sqlite3 libdbd-sqlite3 cron whois" --binary-filesystem fat32 --bootloader syslinux --memtest none --bootappend-live "persistent quickreboot locales=fr_FR keyboard-layouts=fr utc=yes timezone=Africa/Bamako" --debian-installer false --hostname "nut.live" --language fr_FR --syslinux-timeout 3 --syslinux-menu true --templates /usr/share/live/build/templates/ --username nut --win32-loader false --syslinux-splash /home/reg/splash.png --gzip-options "--fast" || exit 1

echo "## lb bootstrap"
lb bootstrap || exit 1

echo "## lb chroot"
lb chroot || exit 1

echo "## configure chroot"
$SRC/configure_chroot.sh $SRC $DST || exit 1

echo "## chroot setup"
chroot ./chroot /usr/bin/setup_chroot.sh || exit 1

echo "## lb binary"
lb binary || exit 1

echo "## lb clean"
#lb clean || exit 1