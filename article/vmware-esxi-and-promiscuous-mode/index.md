---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120414091531/http://petermolnar.eu:80/linux-tech-coding/vmware-esxi-and-promiscuous-mode/
published: '2010-06-02T05:52:16+00:00'
redirect:
- vmware-esxi-and-promiscuous-mode-2
summary: VMWare ESXi 4.1 vs promiscuous mode
tags:
- linux
title: VMWare ESXi and promiscuous mode

---

The problem: I had a XenServer guest, serving as our gateway, and I
needed to convert it to VmWare. The only error was, that no bridged
network work: the gateway saw both, but the networks could not
communicate.

After searching for a while, I'd found the keyword: **promiscuous
mode**. But where can I enable it in VMWare ESXi 4.1? The solution:
select the server (the host server) from the list on the left, goto
"configuration" tab, search for Virtual Switch: (), and click on
Properties of the Virtual Switch. The you'll see the networks configured
with the virtual switch. Selecting on network, click on Edit down, and
select security tab. You'll find promiscuous mode there.