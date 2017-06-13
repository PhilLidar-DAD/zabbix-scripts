#!/bin/bash

echo "$@" | grep -v UNKNOWN | slacktee.sh -e "Date and Time" "$(date)" -u "zabbix01" -a "good" -o "danger" "*PROBLEM*"
