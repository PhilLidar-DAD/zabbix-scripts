#!/bin/bash
version="0.2.1"
DEVS=$( cat /proc/diskstats | awk '{print $3}' | grep -v sr | grep -v ram | grep -v loop | egrep -v [0-9] )
POSITION=1
echo "{"
echo " \"data\":["
for DEV in $DEVS; do
    if [ $POSITION -gt 1 ]; then
        echo ","
    fi
    echo -n "  { \"{#DISK_ID}\": \"$DEV\" }"
    POSITION=$[POSITION+1]
done
echo ""
echo " ]"
echo "}"
