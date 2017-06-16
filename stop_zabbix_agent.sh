#!/bin/bash

ps auxww | grep zabbix | awk '{print $2}' | xargs kill

