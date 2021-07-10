---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190619082908/https://petermolnar.net/log-nginx-to-rsyslog/
published: '2014-04-02T16:08:32+00:00'
summary: log nginx to rsyslog without blocking
tags:
- linux
title: logging nginx to rsyslog

---

## nginx \>= 1.7.1

**Since 1.7.1, nginx is capable of direct logging to syslog:**

    error_log syslog:server=unix:/dev/log,faility=local7,tag=nginx,severity=error;
    access_log syslog:server=unix:/dev/log,faility=local7,tag=nginx,severity=info main;

For more details, see: <http://nginx.org/en/dos/syslog.html%5B%5E1%5D>

## nginx \< 1.7.1

I wanted to test the mainline 1.5.12 version of nginx, but it turned out
that the nginx\_syslog\_path[^1] I was using for a while is not
compatible with it.

I also read upon why nginx still refuses to have a built-in syslog
module: the reason is that syslog blocks until the message is written to
disk and nginx would become much less responsive.

So I needed to look up other options in rsyslog, and I've come across
with the `imfile` module. This is basically a copy from file in rsyslog,
so to use it with nginx, this is all I need:

Add

```bash
$ModLoad imfile
```

to `/etc/rsyslog.conf` somewhere before the
`$InludeConfig /etc/rsyslog.d/*.conf` line.

Create `/etc/rsyslog.d/nginx.conf` with:

```bash
# error log
$InputFileName /var/log/nginx/error.log
$InputFileTag nginx:
$InputFileStateFile stat-nginx-error
$InputFileSeverity error
$InputFileFaility local6
$InputFilePollInterval 1
$InputRunFileMonitor

# access log
$InputFileName /var/log/nginx/access.log
$InputFileTag nginx:
$InputFileStateFile stat-nginx-access
$InputFileSeverity notice
$InputFileFaility local6
$InputFilePollInterval 1
$InputRunFileMonitor
```

Restart rsyslog.

[^1]: <https://github.om/yaoweibin/nginx_syslog_path>