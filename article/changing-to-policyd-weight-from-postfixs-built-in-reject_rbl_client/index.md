---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120414091518/http://petermolnar.eu:80/linux-tech-coding/changing-to-policyd-weight-from-postfixs-built-in-reject_rbl_client/
published: '2010-03-07T22:41:54+00:00'
summary: Install a weighted RBL daemon for Postfix.
tags:
- e-mail
title: Changing to policyd-weight from postfix's built-in reject_rbl_client

---

Last week my own server - hosting some sites from old and relatively
close client - had been hijacked, and got listed on some RBL lists.

Using apache2-mpm-itk[^1] it was quite easy to trace it back, *because
the spamsender process was running with a user's id, not with simple
www-data.* Someone managed to log in with an FTP account, placed some
scripts in the www directory, and started it from a web request. The
real beauty was that the script removed itself after loading. It also
sent the mails from the domain's default name, so, unfortunately it
wasn't forged, and a lot of lists added my IP.

Using the help of mxtoolbox.com, a site for monitoring mailservers[^2],
a lot of hours and at least 10 apologizing mails I managed to remove
myself. This reminded me, that I use the same method: RBL blockings
right inside postfix's main.conf.

So if anyone got listed on one the lists I use, I reject their mail just
like it happened to me. I clearly feel now, that this is not the good
approach. So I looked for some kind of weighted possibility, like
spamassassin for spam, and I met policyd-weight. It is the perfect tool
I was looking for, and the best, Ubuntu has it as package.

```bash
apt-get install policyd-weight
```

The only thing: it does not provide a default conf file, you need to
create it with a build-in feature:

```bash
policyd-weight defaults > /etc/policyd-weight.conf
```

You also need to add it to postfix's main.conf, right into
`smtp_recipient_restrictions`

```bash
check_policy_service inet:127.0.0.1:12525,
```

You can also remove every RBL entry from here after this is enabled.

Reload postfix

```bash
/etc/init.d/postfix reload
```

and your system is ready to use policyd-weight, a lot more sophisticated
solution for RBL listings, than built-in version of postfix.

To see more, visit Ubuntu manpage of policyd-weight[^3], or the poject's
website[^4].

[^1]: <http://tech.webportfolio.hu/4/installing-apache2-mpm-itk-on-a-virtualmin-based-ubuntu-8-04/>

[^2]: <http://mxtoolbox.com>

[^3]: <http://manpages.ubuntu.com/manpages/hardy/man8/policyd-weight.8.html>

[^4]: <http://www.policyd-weight.org/>