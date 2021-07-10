---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20110926213043/http://petermolnar.eu:80/sysadmin-blog/cheapvps-co-uk-kvm-vps-v1-review
published: '2011-09-19T07:27:29+00:00'
summary: Review a small, UK based KVM VPS. Without expectations but with surprisingly
    good results.
tags:
- hardware
title: CheapVPS.co.uk KVM VPS V1 review

---

For nearly two years, I've ran a hosted server as the base of my (very)
small business hosting solutions. It is a HP DL360 G4, not a too
up-to-date hardware: 2 of 72 GB HP U320 SCSI disk in RAID 1, 4 GB memory
and a 64-bit Xeon 3 GHz processor. Also, I'm hosting it now for about
60€/month.

Unfortunately, after updating it from Ubuntu 8.04 to 10.04, it somehow
lost some of it's performance. I've had to be quick not to generate too
much downtime, and this is my reward.

Before this, I rented a VPS server from a Hungarian company. It was a
Virtuozzo-based system (pretty much the same as OpenVZ), and I don't
really have good experiences with both OpenVZ both the company. OpenVZ
uses the very same kernel on every container, so they had tons of
restrictions (no sshfs for example...) and lots of maintance time.

Nowadays I'm giving up hosting on my own hardware, basically it doesn't
worth it, so I looked around a bit what changed at VPS hosting in the
past years. I was searching for a small server with the following: at
least 512MB RAM, XEN or KVM based, not more than 25 € / month at max, no
small, starter or upcomer company and no paperwork. In Hungary, you have
to sign papers for *everything*, and I do mean everything.

Also, I planned to search in Europe. I'm not intending to leave Europe
so far, and I'd like my system to serve at a reasonable speed.

This was the way I've found CheapVPS.co.uk[^1]. A quick payment via
Paypal, a few hours of waiting (I payed at around 10pm so it is
reasonable), and I had a VPS, with self-install possibility. The provide
a web-interface and a Java based VNC console, so it was just like a
normal install. There was a small suprise, since I selected Ubuntu 11.04
from a list as my future system, but they only provided mountable ISO
images for 10.10. No problem, it was solved after install with
do-release-upgrade.

## Comparison

### System comparison

                     wintermute                    akasha
  ------------------ ----------------------------- ----------------------------
  computer type      hosted physical machine       KVM VPS
  CPU                Intel© Xeon™ CPU 3.00GHz      unknown
  RAM                4 GB                          512 MB
  swap               4 GB                          1 GB
  operating system   Ubuntu 10.04 LTS Lucyd Lynx   Ubuntu 11.04 Natty Narwhal
  kernel             2.6.35-020635rc1-generic      2.6.38-11-server

### Network speed

Network speed was tested with iperf, where the target was runing with
`iperf -s -p xxxx` and the source started with
`iperf -c <hostname> -p xxxx`

  source / target   wintermute       akasha
  ----------------- ---------------- ----------------
  wintermute        \-               25.6 Mbits/sec
  akasha            48.4 Mbits/sec   \-
  my machine        1.54 Mbits/sec   1.53 Mbits/sec

### Disk speed

Test mechanish: `dd if=/dev/zero of=/testfile bs=1M count=1024` four
times, average calculated.

  wintermute   akasha
  ------------ ------------
  \~82 MB/s    \~148 MB/s

## Conclusions

I have to say, I was pretty surprised by the performance of the VPS. The
last time I tried installing a KVM based system it bleed on disk speed:
Xen overdone it by about 300%. Also, there's no perceptible difference
in connection speed, nor in web page serving, nor in SSH based file
transfer. The CPU is significantly more powerful on the VPS than on the
6 year old architecture. Until now, I did not experienced any glitches,
errors or mistakes in the VPS, but I keep an eye on the Munin graphs of
the new machine. The only thing I can tell is that cheapvps.co.uk[^2]
does worth it in every way.

[^1]: <http://cheapvps.co.uk>

[^2]: <http://cheapvps.co.uk/>