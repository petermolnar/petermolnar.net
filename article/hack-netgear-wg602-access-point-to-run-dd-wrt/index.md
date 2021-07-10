---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111116135439/http://petermolnar.eu:80/sysadmin-blog/hack-netgear-wg602-access-point-to-run-dd-wrt/
published: '2010-06-23T11:23:27+00:00'
summary: The basic system of Netgear WG602 is dumb, so get DD-WRT on top of
    it.
tags:
- linux
title: Hack Netgear WG602 access point to run dd-wrt

---

We have two Access Points, both Netgear WG602EE v4. According a review
about the device, it has a limitation of 20 simultaneous sessions, so I
started to look some kind of limit breaking. (Yes, we did have problems
like this.)

Fortunately, these devices are on the list of the ones able to run
dd-wrt. But how to hack?

The steps:

-   download the version for netgear from the dd-wrt page[^1]
-   install tftp ( I use ubuntu, so apt-get install tftp)
-   add an IP address from 192.168.0.1/24 to your existing addresses,
    and one from 192.168.1.1/24 The first is because the access point's
    default is 192.168.0.227, the second is because dd-wrt default is
    192.168.1.1. This is **always** the default.
-   Login with the tftp session and enter the following: (the best is to
    enter these at the location, where you downloaded the dd-wrt binary)

```bash
tftp 192.168.0.227
verbose
trace
put dd-wrt.v24_micro_generic.bin image.idts334
```

Do not press enter at the end of the last line, just put is there!

*The tftp only send/recieve data when put or get is entered, so you can
log in without the other IP even exists.*

-   On the device, press the reset button and hold for at least 10
    seconds, than pull the power cord. Insert the power cord back
    **while** still holding the reset button and hold it for 5 seconds
    more.
-   1 second after press enter at the tftp session. **Attention! At this
    point, there's no return, because no original firmware is available
    from Netgear.**
-   You sould see a lot of send/recieve messages.
-   If the transmission was correct, you should be able to login to
    dd-wrt at the address 192.168.1.1

[^1]: <http://www.dd-wrt.com/site/support/router-database>