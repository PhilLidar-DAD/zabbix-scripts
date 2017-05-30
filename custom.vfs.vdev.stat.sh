#!/bin/bash
DISK_STATS=`cat /proc/diskstats | grep -v sr | grep -v ram | grep -v loop`
DEV=$1
STAT=$2

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
esac
