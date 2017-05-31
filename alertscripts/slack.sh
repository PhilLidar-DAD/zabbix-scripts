#!/bin/bash

echo "$@" | slacktee.sh -e "Date and Time" "$(date)" -u "zabbix01"
