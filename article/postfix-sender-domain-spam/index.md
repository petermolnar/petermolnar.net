---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20141130152004/https://petermolnar.eu/linux-tech-coding/postfix-sender-domain-spam/
published: '2014-11-10T15:53:13+00:00'
summary: Some bash lines to generate sender checks for postfix.
tags:
- e-mail
title: Reject mails in postfix based on sender domain

---

**NOTE: it turned out that this can get dangerous; for example, if you
mark a mail coming from `gmail.com` spam, you'll reject gmail.com, which
is obviously not a bright idea. I'll leave the article here, but be
warned.**

Recently I noticed that I get many spams from the same sender domains.
In this case, I could safely apply a manually updated list to postfix to
reject these domains in the first place.

Go to the spam Maildir's `cur` folder:

```bash
#!/bin/bash

cd /path/to/spam/Maildir/cur

touch /etc/postfix/sender_checks
grep -ri ^From * | awk '{ print $3}' | grep @ | sed 's/[<>]//g' | cut -d"@" -f2 | sort | uniq >/tmp/spammer
sed -i "s/^/\//g" /tmp/spammer
sed -i "s/$/\$\/ REJECT\ Byez\ spammer/g" /tmp/spammer
cat /etc/postfix/sender_checks >> /tmp/spammer
cat /tmp/spammer | sort | uniq > /etc/postfix/sender_checks
```

Add to `/etc/postfix/main.cf`:

```apache
smtpd_sender_restrictions = reject_unknown_sender_domain,
    check_sender_mx_access pcre:/etc/postfix/sender_checks,
    check_sender_access pcre:/etc/postfix/sender_checks,
    check_sender_ns_access pcre:/etc/postfix/sender_checks,
```

It will not catch too many spams only a few per day, but even that can
be useful.