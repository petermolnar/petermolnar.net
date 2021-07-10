---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111116135015/http://petermolnar.eu:80/sysadmin-blog/2-6-38-kernel-on-ubuntu-maverick-meerkat-10-10-broadcom-sta-linux-driver/
published: '2011-04-28T21:22:19+00:00'
summary: Feel free to install pre-released version of ubuntu kernel into the
    current!
tags:
- linux
title: Ubuntu 10.10 Maverick Meerkat 2.6.38 kernel vs Broadcom STA linux driver

---

Today, my Ubuntu popped up if I'd like to upgrade to 11.04 Natty
Narwhal, and no, for a bit of time, I'm truly sure, I don't. But what I
do want is the 200 lines magic patched kernel of Natty, so I gave a
shoot.

Download it from Ubuntu Kernel PPA[^1]:

After downloading, install them with `dpkg -i *.deb`.

But, after adding I also wanted to compile Broadcom STA driver, since
the Ubuntu version is only 5.60, and the latest is 5.100, and there's a
really large difference.

During the compilation, a received the following error:

    src/wl/sys/wl_linux.c:485: error: implicit declaration of function ‘init_MUTEX'

After a bit of searching around, I've found a simple solution on Linux
Mint forums[^2]:

    "I solved the problem by changing line 487 from
    init_MUTEX(&wl->sem);
    into
    sema_init(&wl->sem, 1);"

And hey, it does solve the problem!

I do feel one more step closer to Linux Mint Debian Edition, Unity just
tastes like Windows 7 tasted, and Windows 7 made me change into linux
only machine. Maybe Unity will blow me to a Debian rolling edition.

[^1]: <http://kernel.ubuntu.com/~kernel-ppa/mainline/v2.6.38.4-natty/>

[^2]: <http://forums.linuxmint.com/viewtopic.php?f=141&t=57056&p=378103>