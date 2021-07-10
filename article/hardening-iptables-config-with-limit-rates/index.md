---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125517/https://petermolnar.net/hardening-iptables-config-with-limit-rates/
published: '2012-02-10T09:35:57+00:00'
redirect:
- hardening-iptables-config-with-the-goodie-of-limit-rates
summary: How to offload the hard work of blocking brute force to iptables.
tags:
- linux
title: Hardening iptables with limit rates

---

Rate limiting applied at the lowest layer you possibly have access to.
**Note:** these are examples only, not a full configuration.

```apache
*filter
:FORWARD DROP [0:0]
:INPUT DROP [0:0]
:OUTPUT ACCEPT [0:0]

### add your usual safety tricks here ###
### don't forget to allow established and related connections
-A INPUT -m state --state ESTABLISHED -j ACCEPT
-A INPUT -m state --state RELATED -j ACCEPT

### rate limit examples:
# SSH
# be careful with this one, seriously slows SCP down
-A INPUT -m tcp -p tcp --dport 22 -m state --state NEW -m limit --limit 4/s --limit-burst 4 -j ACCEPT

# webserver
-A INPUT -m tcp -p tcp --dport 80 -m state --state NEW -m limit --limit 128/s --limit-burst 128 -j ACCEPT

COMMIT
```