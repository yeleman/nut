#!/bin/bash

DEVICE=/dev/sdb

if ["$1" -neq ""] then
    DEVICE=$1
fi

echo "Unmounting device $DEVICE"
umount $DEVICE

sleep 1

echo "Create empty partition table"
parted -s /dev/sdb mklabel msdos

parted -s /dev/sdb mkpart primary fat32 1 4096
mkfs.vfat -n DONNEES /dev/sdb1

parted -s /dev/sdb mkpart primary ext2 4096 6144
mkfs.ext2 -L DEBIAN_LIVE /dev/sdb2
tune2fs -c 0 /dev/sdb2
parted /dev/sdb set 2 boot on

parted -s /dev/sdb mkpart primary ext2 6144 8192
mkfs.ext4 -L home-rw /dev/sdb3
tune2fs -c 0 /dev/sdb3

echo "Mounting image file"
#dd if=binary.img of=$DEVICE bs=5M
umount /mnt/img
mkdir -p /mnt/img
mount -t vfat -o loop,offset=512 binary.img /mnt/img
sleep 1
umount /media/DEBIAN_LIVE
mkdir -p /media/DEBIAN_LIVE
mount /dev/sdb2 /media/DEBIAN_LIVE/
cp -r /mnt/img/* /media/DEBIAN_LIVE/

cp ../splash.png ../syslinux.cfg /media/DEBIAN_LIVE/syslinux/
extlinux --install /media/DEBIAN_LIVE/syslinux
umount /media/DEBIAN_LIVE
dd bs=440 conv=notrunc count=1 if=/usr/lib/syslinux/mbr.bin of=/dev/sdb

echo "Current partition table"
parted $DEVICE print

