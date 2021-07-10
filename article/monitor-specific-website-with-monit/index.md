---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20140919053336/https://petermolnar.eu/linux-tech-coding/monitor-specific-website-with-monit/
published: '2014-08-14T08:24:42+00:00'
summary: 'How to: monitor the health of a remote web address with Monit.'
tags:
- linux
title: Monitor specific website with Monit

---

Most of the examples of Monit checking a web address' health is for
localhost and in connection with checking the apache process. However,
in case you want to monitor remote addresses, you'll need this:

```apache
check host domain.com with address domain.com every 6 cycles
    if failed port 80 protocol http for 5 cycles then alert
    alert your.email@provider.com { connection, timeout } with mail-format {
        from: monit@your-server.com
        subject: $EVENT at $DATE on $HOST
        message: domain.com is unreachable from your-server.com server
    }
```