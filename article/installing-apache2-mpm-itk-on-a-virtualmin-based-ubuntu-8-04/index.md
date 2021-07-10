---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111005145532/http://petermolnar.eu:80/sysadmin-blog/installing-apache2-mpm-itk-on-a-virtualmin-based-ubuntu-8-04
published: '2010-03-01T14:43:15+00:00'
redirect:
- installing-apache2-mpm-itk-on-a-virtualmin-based-server
summary: A brief writing on installing apache-mpm-itk on Ubuntu 8.04 server.
tags:
- linux
title: Installing apache2-mpm-itk on a Virtualmin based Ubuntu 8.04

---

For a long time, I've been a fan of Virtualmin[^1]. Stable, quite
secure, and really easy to use - of course, for a sysadmin, but it can
be handy enough for those of willing to learn it.

While I only hosted my friends and well-known customers, I had no
intention increase security over the defaults of virtualmin.

A week ago, I had to install a server for hosting, with old, insecure
sites, and for not too friendly, utterly unknown people, so the need
came for a more secure solution.

One of my college advised suphp[^2]. It was really easy to install under
Virtualmin, no errors. But suphp was getting slow for my taste. The
other problem with it is that opcode cacheing APC[^3], eAccelerator[^4],
Xcache[^5]) cannot be used with it, because it work just like CGI.

So, I started to look for a solution, and luckily, I came across with
Stuart Herbert's Blog[^6], and with the post of apache mpm-itk[^7].

The solution was in my hand, Virtualmin running on Ubuntu, itk is is
package, so:

```bash
apt-get install apache2-mpm-itk
```

And there came the errors:

```bash
The following packages have unmet dependencies:
apache2-mpm-itk: Depends: apache2.2-common (= 2.2.8-1ubuntu0.14) but 2.2.8-10vm is to be installed
E: Broken packages
```

How did that package, out of ubuntu, even get on my server? I started to
search for 2.2.8-10vm package of apache , and I've found it in the
install script of virtualmin. I seems, that because of suexec is default
enabled in Virtualmin, it needs a modified version of suexec module for
apache, to use /home as root for suexec.

That clearly wouldn't need a full apache, but I think, thats a lot more
easy compared to recompiling for the distro's apache.

Ok. Remove apache.

```bash
apt-get remove apache2.2-common
```

```bash
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following packages were automatically installed and are no longer required:
libneon27 irb1.8 libsasl2 clamav webmin-virtualmin-awstats libmail-spf-perl clamav-freshclam awstats dovecot-imapd libdb4.6-dev libdbd-pg-perl libsocket6-perl
libsqlite3-dev rdoc ri liberror-perl libnetaddr-ip-perl clamav-base subversion postgresql-client-8.3 libclamav5 spamassassin libapr1-dev libapache-ruby1.8 libsvn1
spamc clamav-testfiles dovecot-pop3d webmin-virtualmin-mailman webmin-virtualmin-htpasswd libgmp3c2 scponly webmin-security-updates libpg-perl irb clamav-daemon
clamav-docs libnet-ip-perl libnet-dns-perl postgresql rdoc1.8 procmail-wrapper webalizer webmin-virtual-server-theme webmin-virtualmin-dav uuid-dev libgeoip1
libpq-dev postgresql-client-common libhtml-tree-perl usermin-virtual-server-theme libwww-perl libdigest-hmac-perl libversion-perl libaprutil1-dev
libreadline-ruby1.8 postgresql-common dovecot-common postgresql-8.3 webmin-virtualmin-svn libsys-hostname-long-perl ri1.8 libdigest-sha1-perl
Use 'apt-get autoremove' to remove them.
The following packages will be REMOVED:
apache2-mpm-prefork apache2-threaded-dev apache2.2-common libapache2-mod-fcgid libapache2-mod-php5 libapache2-mod-ruby libapache2-svn mailman virtualmin-base
0 upgraded, 0 newly installed, 9 to remove and 11 not upgraded.
After this operation, 51.8MB disk space will be freed.
Do you want to continue [Y/n]?
```

Oh. So if I remove apache, I remove virtualmin, and that's for sure, I
don't want.

At last, I finally found a solution: I have to get the original ubuntu
package, install (technically downgrade the current apache) it, and then
I can install mpm-itk without removing virtualmin.

What we need:

<http://packages.ubuntu.com/hardy/apache2.2-common>
<http://packages.ubuntu.com/hardy/apache2>

These could be needed too:

<http://packages.ubuntu.com/hardy/apache2-threaded-dev>
<http://packages.ubuntu.com/hardy/any/apache2-mpm-prefork>

If you used suphp:
<http://packages.ubuntu.com/hardy/any/apache2-mpm-worker>

Get them, install them with `dpkg -i *.deb` and install apache2-mpm-itk.
Voliá.

Of course, you'll need to add the user directives to all virtualhost,
but at Server Templates, you can insert it already. For example, add
this to Virtualmin Server Templates:

```bash
<ifmodule mpm_itk_module>
AssignUserId ${USER} ${USER}
</ifmodule>
```

[^1]: <http://www.virtualmin.com/>

[^2]: <http://www.suphp.org/Home.html>

[^3]: <http://php.net/manual/en/book.apc.php>

[^4]: <http://eaccelerator.net/>

[^5]: <http://xcache.lighttpd.net/>

[^6]: <http://blog.stuartherbert.com>

[^7]: <http://blog.stuartherbert.com/php/2008/04/19/using-mpm-itk-to-secure-a-shared-server/>