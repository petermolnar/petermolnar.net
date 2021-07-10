---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20130307033423/http://petermolnar.eu:80/linux-tech-coding/add-ram-to-ubuntu-12-04-for-free-zram
published: '2013-01-11T10:17:05+00:00'
summary: More RAM for free? By installing a software?! Enter zRAM.
tags:
- linux
title: 'Add RAM to Ubuntu 12.04+ for free: zRAM'

---

In the mainline generic kernel of Ubuntu, there's a module called zram.
This is a pretty good trick to add additional "free" RAM to your machine
without any change: it creates in-memory compressed block for swap,
meaning it eats a bit of your CPU but gives you literally more RAM.

If you're on a VPS for example, having 512 MB RAM, this would actually
give you access to 750 MB RAM and would eat just a little CPU from you -
I don't even notice it on the Munin graphs.

To install:

```bash
apt-get install zram-config
```

Make sure it's started and running:

```bash
cat /proc/swaps
```

If you see something like this

```bash
# cat /proc/swaps
Filename     Type       Size    Used    Priority
/dev/zram0   partition  62712   6804    5
/dev/zram1   partition  62712   6768    5
/dev/zram2   partition  62712   6744    5
/dev/zram3   partition  62712   6768    5
```

then it's already running.

Reboot your machine, and voilá.

More to read:

-   Increased performance in linux with zRAM[^1]
-   Ubuntu Linux Considers Greater Usage Of zRAM[^2]

[^1]: <http://www.webupd8.org/2011/10/increased-performance-in-linux-with.html>

[^2]: <http://www.phoronix.com/scan.php?page=news_item&px=MTI0NjQ>