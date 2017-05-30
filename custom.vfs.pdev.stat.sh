#!/bin/bash
version="0.3.3"
DISK_IDS=$( ls -hl /dev/disk/by-id/ | egrep '[ata|scsi]' | grep -v part )
DISK_ID=$1
STAT=$2
DISK_STATS=$( cat /proc/diskstats | grep sd )

DEV=`echo "$DISK_IDS" | grep $DISK_ID | head -1 | awk '{print $11}' | awk -F'/' '{print $3}'`
#echo $DEV

case $STAT in
    read.ops)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $4}'
        ;;
    read.sectors)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $6}'
        ;;
    read.ms)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $7}'
        ;;
    write.ops)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $8}'
        ;;
    write.sectors)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $10}'
        ;;
    write.ms)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $11}'
        ;;
    io.active)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $12}'
        ;;
    io.ms)
        echo "$DISK_STATS" | grep $DEV | head -1 | awk '{print $13}'
        ;;
    temp)
        temp=$( sudo /usr/sbin/smartctl -A /dev/$DEV | grep -m1 Temperature_Cel | awk '{print $10}' )
        if [ -z $temp ]; then
            temp=$( sudo /usr/sbin/smartctl -A /dev/$DEV | grep -m1 Temperature | awk '{print $(NF-1)}' )
        fi
        echo $temp
        ;;
esac
