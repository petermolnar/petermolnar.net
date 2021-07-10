---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125243/https://petermolnar.net/block-lg-smart-tv-on-openwrt/
published: '2014-06-08T08:38:45+00:00'
tags:
- LG
- OpenWRT
- privacy
title: How to block LG smart TVs from phoning home on OpenWRT

---

Edit `/etc/dnsmasq.conf`

and add the following:

    address=/ad.lgappstv.com/127.0.0.1
    address=/yumenetworks.com/127.0.0.1
    address=/smartclip.net/127.0.0.1
    address=/smartclip.com/127.0.0.1
    address=/smartshare.lgtvsdp.com/127.0.0.1
    address=/ibis.lgappstv.com/127.0.0.1