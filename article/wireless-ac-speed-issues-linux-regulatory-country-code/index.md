---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624130445/https://petermolnar.net/wireless-ac-speed-issues-linux-regulatory-country-code/
published: '2015-07-14T11:10:24+00:00'
summary: 'Less-known depths of wireless: regulations by countries and non-existent
    updates for linux.'
tags:
- linux
title: Why your AC wifi can't reach full speed on 3.13 kernel (Ubuntu 14.04,
    Mint 17, elementaryOS)

---

I've recently bought a new Wifi router, a Linksys WRT1900AC[^1]. Not
only for the speed, but also because it was marketed as a
hacker-friendly router, with no locks and tricks to replace the firmware
with OpenWRT[^2]. ( We had to wait for OpenWRT to support the AC speed,
but it's all fine now. ).

What I was not counting on is the rusty knowledge of mine on wireless.
I've set up everything, test, wow, much speed, such 900Mbit/s. Until
started fine tuning and added the Regulatory Country Code - and got
stuck with 300Mbit/s.

I already knew about the per country limitations ( bureaucracy...
Vogons... ) - what I was unaware of is the fact that this sometimes gets
updated[^3] and that the linux you have never updates it on it's own.

kernel 3.13.0-57-generic ( which is the thing in Ubuntu 14.04 LTS,
Trusty Tahr and also in elementaryOS Freya )

                Ubuntu 14.04             Current online version
  ------------- ------------------------ ------------------------
  Country 00    (2402 - 2472 @ 40)       (2402 - 2472 @ 40)
                (2457 - 2482 @ 40)       (2457 - 2482 @ 40)
                (2474 - 2494 @ 20)       (2474 - 2494 @ 20)
                (5170 - 5250 @ 40)       (5170 - 5250 @ 80)
                (5735 - 5835 @ 40)       (5250 - 5330 @ 80)
                                         (5490 - 5730 @ 160)
                                         (5735 - 5835 @ 80)
                                         (57240 - 63720 @ 2160)
  country GB:   (2402 - 2482 @ 40)       (2402 - 2482 @ 40)
                (5170 - 5250 @ 40)       (5170 - 5250 @ 80)
                (5250 - 5330 @ 40)       (5250 - 5330 @ 80)
                (5490 - 5710 @ 40)       (5490 - 5710 @ 160)
                (57240 - 65880 @ 2160)   (57000 - 66000 @ 2160)

See the difference? no '@ 80' or '@ 160' for GB in the 3.13 kernel. That
is why I was stuck on 300Mbit/s ( 40Mhz width ).

So after a ridiculosly long search I've found Rick Deckardt's entry on
the topic[^4] which finally helped me solve the issue.

Short story:

```bash
#!/bin/bash

cd ~
# this is the current version by the time I'm writing this post;
# go and check the updates before blindly copy-pasting
cur="2015.04.06"
wget "http://kernel.org/pub/software/network/wireless-regdb/wireless-regdb-${cur}.tar.xz"
tar xJf "wireless-regdb-${cur}.tar.xz"
cd "wireless-regdb-${cur}"
make
sudo cp regulatory.bin /lib/crda/regulatory.bin
sudo cp *.pem /lib/crda/pubkeys
sudo reboot
```

Read more:

-   <http://www.cisco.com/c/en/us/products/collateral/wireless/aironet-3600-series/white_paper_c11-713103.html>
-   <https://wireless.wiki.kernel.org/en/developers/Regulatory>
-   <https://forum.openwrt.org/viewtopic.php?id=41392>

[^1]: <http://www.linksys.com/us/p/P-WRT1900AC/>

[^2]: <http://wiki.openwrt.org/toh/linksys/wrt1900ac>

[^3]: <http://drvbp1.linux-foundation.org/~mcgrof/rel-html/wireless-regdb/>

[^4]: <http://deckardt.nl/blog/2011/01/20/regulatory-limitations-in-linux-wireless/>