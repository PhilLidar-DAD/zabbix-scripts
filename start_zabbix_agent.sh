#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ZABBIX_PATH="${SCRIPT_DIR}/zabbix-agent-3.2.6-freebsd-10.3-amd64"
ZABBIX_CONF="${SCRIPT_DIR}/zabbix_agentd.conf"
ZABBIX_BIN="${ZABBIX_PATH}/sbin/zabbix_agentd"

# FreeNAS 9.3
#ln -sf /usr/local/lib/libiconv.so.3 /usr/local/lib/libiconv.so.2

# FreeNAS 9.10
ln -sf /usr/local/lib/libiconv.so.2.5.1 /usr/local/lib/libiconv.so.2

#make directory if it doesnt exist
mkdir -p /var/run/zabbix/
#create the file if it doesnt exist
touch /var/run/zabbix/zabbix_agentd.pid

/usr/bin/lockf -kns -t 0 $ZABBIX_BIN $ZABBIX_BIN -f -c $ZABBIX_CONF

