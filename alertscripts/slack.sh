#!/bin/bash

echo "$@" | grep -v UNKNOWN | sed 's/server-admins@dream.upd.edu.ph //g' | slacktee.sh -e "Date and Time" "$(date)" -u "zabbix01" -a "good" -o "danger" "^PROBLEM"
