---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120625002446/http://petermolnar.eu:80/linux-tech-coding/apache2-mpm-itk-on-ubuntu-10-04-with-virtualmin-running-php-5-3-and-php-5-2-side-by-side
published: '2010-12-14T13:43:34+00:00'
summary: Run PHP 5.2 and 5.3 on the same apache, on a production hosting server,
    with security? Possible, but ugly.
tags:
- linux
title: apache2-mpm-itk on Ubuntu 10.04 with Virtualmin running PHP 5.3 and
    PHP 5.2 side-by-side

---

The case:

-   an Ubuntu 8.04 server, with Virtualmin, needed to be upgraded to
    10.04
-   10.04 runs PHP 5.3 as mod\_php with apache2, and most of my sites
    will die with fatal errors
-   Virtualmin would allow to run PHP with SuExec and FCGID, but I'd
    like to stay with mpm-itk, because it will run everything under the
    user permissions, even mod\_passenger

I need to be able to run PHP 5.2 and PHP 5.3 side-by-side on the same
server, under Ubuntu 10.04, with Virtualmin and under Apache2 MPM ITK.
Nice.

Of course, my first intention was to run mod\_php and FastCGI (or
FCGID). After trying to achieve a single phpinfo for hours, I gave up,
and searched for running PHP as CGI. For my surprise, I some forums
mention, that because mpm itk is a preforked version of apache - instead
of worker, that is usually for fastcgi-setups -, the plain old CGI will
run lot faster than FastCGI with it.

Setting up PHP to run as CGI is nearly the same as setting it up for
FastCGI:

1.  compile PHP

-   download the needed code from php.net[^1]
-   untar the code into a directory, for example /usr/local/php-5.2/
-   cd to the directory /usr/local/php-5.2/
-   compile the code ( I used the following options ):

```bash
./configure --prefix=/opt/php-5.2.15 --with-config-file-path=/usr/local/php-5.2 --with-mcrypt --with-pgsql --with-mysqli --with-mysql --with-curl --with-gd --with-jpeg --with-jpeg-dir --enable-cli --enable-fastcgi --enable-discard-path --enable-force-cgi-redirect --with-zlib

make

make test
sudo make install
```

-   it is possible, that it will fail, needing some libs; install them
    with apt-get.
-   you'll have your PHP compled at /usr/local/php-5.2/bin/ directory.

2.  enable CGI handler in the Apache2 VirtualHost

Add the following into the virtualhost conf:

```apache
# PHP 5.3 disable
<ifmodule mod_php5.c>
php_admin_value engine off
</ifmodule>

# PHP 5.2, as CGI
<ifmodule mod_cgid.c>
<filesmatch ".ph(p3?|tml)$">
SetHandler application/x-httpd-php52
</filesmatch>
Action application/x-httpd-php52 "/cgi-bin/php-5.2.12.cgi"
</ifmodule>
```

-   this needs a script, with x (run) permissions on it, placed inside
    the VirtualHost's home/cgi-bin
-   it also need the user to be the owner, because of mpm-itk
-   the content of the script:

```bash
#!/bin/bash

PHPRC=/etc/php/apache2
export PHPRC
exec /usr/local/php-5.2/bin/php-cgi
```

And that's all.

[^1]: <http://php.net/downloads.php>