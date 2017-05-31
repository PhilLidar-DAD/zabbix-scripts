Overview
========

Place slack.sh in /usr/lib/zabbix/alertscripts
dont forget to make it executable
It simply echoes the parameters to [slacktee.sh](https://github.com/course-hero/slacktee)

Installation
============
```
git clone https://github.com/course-hero/slacktee
bash slacktee/install.sh
cp slack.sh /usr/lib/zabbix/alertscripts/
chmod +x /usr/lib/zabbix/alertscripts/slack.sh
```

slacktee is included in this repository just in case the git repository in github gets taken down.
Slactee tends to read ~/.slacktee first, slacktee.conf is supposed to be placed in /etc/slacktee.conf

Requirements
------------
slacktee uses curl command to communicate with Slack.

Configure slacktee before using!
