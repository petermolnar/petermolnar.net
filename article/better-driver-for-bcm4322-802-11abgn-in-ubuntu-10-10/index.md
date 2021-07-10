---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120304032158/http://petermolnar.eu:80/linux-tech-coding/better-driver-for-bcm4322-802-11abgn-in-ubuntu-10-10
published: '2011-04-16T18:43:10+00:00'
summary: In Ubuntu 10.10, Broadcom driver is old, therefore it's full of bugs,
    and totally unusable for current cards, like BCM4322. Upgrade it.
tags:
- linux
title: Better driver for BCM4322 802.11a/b/g/n in Ubuntu 10.10

---

After several connection problems in Ubuntu 10.10 with the recommended
STA driver (in restricted drivers), I decided to somehow solve it. The
result: a working BCM4322, with "n" speed.

<del datetime="2011-04-29T16:26:06+00:00">
</del>
~~How: Remove dell\_laptop and wl modules, if there present.~~

~~rmmod wl~~ ~~rmmod dell\_laptop~~

Get the latest driver from
<http://www.broadcom.com/support/802.11/linux_sta.php%5B%5E1%5D> - as
I'm writing these lines, it's hybrid-portsrc\_x86\_64-v5\_100\_82\_38.

To download and install, use the following lines:

```bash
#!/bin/bash
VERSION="hybrid-portsrc_x86_64-v5_100_82_38"

mkdir broadcom_sta_$VERSION
cd broadcom_sta_$VERSION
wget http://www.broadcom.com/docs/linux_sta/$VERSION.tar.gz
tar xf $VERSION.tar.gz
make
```

Install standard Ubuntu Broadcom driver first. This is a DKMS driver,
meaning, it will automatically upgrade with every kernel update as well.

To replace the default driver follow the steps above. You'll find the
default driver at

```bash
/lib/modules/`uname -r`/updates/dkms/wl.ko
```

To update, first remove the current driver:

```bash
rmmod wl
```

Then overwrite the /lib... file with the compiled, and run:

```bash
depmod -a
modprobe wl
```