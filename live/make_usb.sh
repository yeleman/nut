#!/bin/bash

DEVICE=/dev/sdb
SRC="../nut/live"

if [ "$1" != "" ]; then
    DEVICE=$1
fi

if [ "$2" != "" ]; then
    SRC=$2
fi

echo "Unmounting device $DEVICE"
umount ${DEVICE}

sleep 1

echo "Create empty partition table"
parted -s ${DEVICE} mklabel msdos || exit 1

echo "Create FAT32 partition for data"
parted -s ${DEVICE} mkpart primary fat32 1 4096 || exit 1
mkfs.vfat -n DONNEES ${DEVICE}1 || exit 1

echo "Create ext2 partition for system"
parted -s ${DEVICE} mkpart primary ext2 4096 6144 || exit 1
mkfs.ext2 -L DEBIAN_LIVE ${DEVICE}2 || exit 1
tune2fs -c 0 ${DEVICE}2 || exit 1
parted ${DEVICE} set 2 boot on || exit 1

echo "Create ext4 partition for home"
parted -s ${DEVICE} mkpart primary ext2 6144 8192 || exit 1
mkfs.ext4 -L home-rw ${DEVICE}3 || exit 1
tune2fs -c 0 ${DEVICE}3 || exit 1

echo "Mount image file"
umount /mnt/img
mkdir -p /mnt/img || exit 1
mount -t vfat -o loop,offset=512 binary.img /mnt/img || exit 1
sleep 1

echo "Mount USB system partition"
umount /media/DEBIAN_LIVE
mkdir -p /media/DEBIAN_LIVE || exit 1
mount ${DEVICE}2 /media/DEBIAN_LIVE/ || exit 1

echo "Copy image files to USB"
cp -r /mnt/img/* /media/DEBIAN_LIVE/ || exit 1

echo "Edit syslinux configuration"
cp $SRC/splash.png $SRC/syslinux.cfg /media/DEBIAN_LIVE/syslinux/ || exit 1
extlinux --install /media/DEBIAN_LIVE/syslinux || exit 1

echo "Unmount USB"
umount /media/DEBIAN_LIVE

echo "Install MBR to USB"
dd bs=440 conv=notrunc count=1 if=/usr/lib/syslinux/mbr.bin of=${DEVICE} || exit 1

echo "Current partition table"
parted ${DEVICE} print || exit 1