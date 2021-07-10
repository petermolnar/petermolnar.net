---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120414091357/http://petermolnar.eu:80/linux-tech-coding/installing-php-5-3-on-ubuntu-9-10-karmic-koala/
published: '2010-03-15T10:00:20+00:00'
summary: How to get PHP 5.3 on Karmic Koala from dotdeb.
tags:
- linux
title: Installing PHP 5.3 on Ubuntu 9.10 Karmic Koala

---

In production, we use Ubuntu 9.10, because of the need of the newer
kernel. Now we also need 5.3 PHP, because of Symfony, so I started
searching. I've found a post on JMOZ blog[^1], about installing 5.3 PHP
from dotdeb packages, but when I tried, I recieved some more errors over
the one libicu38 mentioned in the post, so I decided to write them down.

The needed additional apt sources:

```apache
# for PHP 5.3
deb http://php53.dotdeb.org stable all
deb-src http://php53.dotdeb.org stable all

# for libicu38
deb http://security.ubuntu.com/ubuntu jaunty-security main
deb-src http://security.ubuntu.com/ubuntu jaunty-security main

# for libltdl3
deb http://archive.ubuntu.com/ubuntu hardy main
deb-src http://archive.ubuntu.com/ubuntu hardy main
deb http://archive.ubuntu.com/ubuntu hardy-updates main
deb-src http://archive.ubuntu.com/ubuntu hardy-updates main
```

[^1]: <http://blog.jmoz.co.uk/post/435401471/install-php-5-3-on-ubuntu-karmic-koala-from-dotdeb>