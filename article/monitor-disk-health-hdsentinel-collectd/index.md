---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20131129155535/http://petermolnar.eu:80/linux-tech-coding/monitor-disk-health-hdsentinel-collectd/
published: '2013-10-08T12:22:08+00:00'
summary: A little shell script to connect HDSentinel to collectd.
tags:
- linux
title: Monitor disk health with HDSentinel and collectd

---

HDSentinel[^1] is a brilliant little freeware capable of showing
S.M.A.R.T. data from the disks in various ways. Since these values are
important in monitoring and I'm using collecd as monitoring system, I
needed a way to integrate the two. I ended up using the Exec plugin of
collectd.

The steps:

```bash
wget http://www.hdsentinel.com/hdslin/hdsentinel_008_x64.zip
unzip hdsentinel_008_x64.zip
chmod 0755 HDSentinel
mv HDSentinel /usr/bin/hdsentinel
```

Add the monitor scripts:

```bash
vim /etc/collect/scripts/hdsentinel.sh
```

```bash
#!/usr/bin/env bash

HOSTNAME=`uname -n`
INTERVAL="${COLLECTD_INTERVAL:-1}"

disks=`ls /dev/sd[a-z]`

while sleep "${INTERVAL}"; do
    hdsentinel=`/usr/bin/sudo /usr/bin/hdsentinel`
    for disk in ${disks}; do
        data=`echo "${hdsentinel}" | grep -A11 ${disk}`
        name=`echo "${data}" | grep "HDD Device" | awk '{print $4}'`
        disk=${disk##/dev/}

        temp=`echo "${data}" | grep "Temperature" | awk '{print $3}'`
        echo "PUTVAL "${HOSTNAME}/hdsentinel-${disk}/temperature" interval=$INTERVAL N:${temp}"

        tempmax=`echo "${data}" | grep "Highest Temp" | awk '{print $3}'`
        echo "PUTVAL "${HOSTNAME}/hdsentinel-${disk}/temperature-max" interval=$INTERVAL N:${tempmax}"

        health=`echo "${data}" | grep "Health" | awk '{print $3}'`
        echo "PUTVAL "${HOSTNAME}/hdsentinel-${disk}/percent-health" interval=$INTERVAL N:${health}"

        performance=`echo "${data}" | grep "Performance" | awk '{print $3}'`
        echo "PUTVAL "${HOSTNAME}/hdsentinel-${disk}/percent-performance" interval=$INTERVAL N:${performance}"

    done
done
```

Note: "percent" and "temperature" are types of collectd. Thx
deadite66[^2]!

Add the collectd plugin:

```bash
vim /etc/collectd/collectd.conf
```

```bash
LoadPlugin exec
<plugin exec>
  Exec "nobody" "/etc/collectd/scripts/hdsentinel.sh"
</plugin>
```

Add "nobody" to sudoers, but only for hdsentinel ( install sudo if you
need to, hdsentinel needs root access to run, but collectd will not exec
with root user ):

```bash
vim /etc/sudoers
```

```bash
# add to the end
nobody    ALL=(ALL) NOPASSWD: /usr/bin/hdsentinel
```

[^1]: <http://www.hdsentinel.com/hard_disk_sentinel_linux.php>

[^2]: <http://ubuntuforums.org/showthread.php?t=1479963>