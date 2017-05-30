#!/bin/bash
version="0.2.2"
DEVS=$( cat /proc/diskstats | awk '{print $3}' | grep sd | egrep -v [0-9] )
POSITION=1
DISK_IDS=$( ls -hl /dev/disk/by-id/ | egrep '[ata|scsi]' | grep -v part )
# echo "$DISK_IDS"
# exit 1
echo "{"
echo " \"data\":["
for DEV in $DEVS; do
    # echo
    # echo $DEV
    DISK_ID=$( echo "$DISK_IDS" | grep "${DEV}$" | head -1 | awk '{print $9}' )
    if [ $? -eq 0 ]; then
        if [ $POSITION -gt 1 ]; then
            echo ","
        fi
        echo -n "  { \"{#DISK_ID}\": \"$DISK_ID\" }"
        POSITION=$[POSITION+1]
    fi
done
echo ""
echo " ]"
echo "}"
