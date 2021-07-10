---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111116135225/http://petermolnar.eu:80/sysadmin-blog/changing-postfixs-incoming-smtp-port/
published: '2010-03-08T09:27:00+00:00'
summary: Which line to change to have Postfix listen on specific ports are
    well?
tags:
- e-mail
title: Changing postfix's incoming smtp port

---

This is one of the most simple tasks, yet I had to Google around for
hours: change the incoming port of postfix's SMTP, without iptables
prerouting.

Open `/etc/postfix/master.cf`, and search for the following line
(usually the first uncommented line):

```apache
smtp    inet    n   -   -   -   -   smtpd
```

To change the port, simply write the number instead of smtp in the
begining.

For example:

```apache
2525    inet    n   -   -   -   -   smtpd
```

Restart postfix

```bash
/etc/init.d/postfix restart
```

and the system can not accept messages on the port you added. Don't
forget to enable the port on your firewall, if you have one!