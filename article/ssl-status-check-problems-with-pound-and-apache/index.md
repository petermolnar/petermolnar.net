---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111116135521/http://petermolnar.eu:80/sysadmin-blog/ssl-status-check-problems-with-pound-and-apache/
published: '2010-03-16T09:14:18+00:00'
redirect:
- ssl-status-check-problems-with-pound-and-apache-2
summary: Rely on your own HTTP headers, because the built-in ones sometimes
    get lost.
tags:
- linux
title: SSL status check problems with apache behind Pound reverse proxy

---

We have a high-available system, with the following architecture:

-   the main gate: HAProxy on port 80 on the public interface
-   all webservers: nginx on port 80, if the content is not static
    (regex list)
-   proxied to localhost, port 81, to apache2

But this architecture cannot be used for ssl connections, therefore on
port 443, pound is listening on the HA cluster, and forwards every
connection to the HA proxy without SSL.

The problem, is that when a request arrives to one of the apache
servers, I cannot force SSL connection, because it will slip into an
endless loop.

The solution is:

-   add a special HTTP header with pound
-   insted of HTTPS check in apache, check this

`pound.conf:`

```apache
User            "www-data"
Group           "www-data"
LogLevel        0
Alive           2
Control         "/var/run/poundctl.socket"

ListenHTTPS
  Address [IP]
  Port 443
  Cert "/etc/pound/[cert].pem"
  AddHeader "XHTTPS: on"
  Service
    Backend
      Address [IP]
      Port 80
    End
  End
End
```

The check in apache (inside virtualhost):

    RewriteCond %{HTTP:XHTTPS} !on
    RewriteRule ^(.*) https://[domain]/$1 [R,L]