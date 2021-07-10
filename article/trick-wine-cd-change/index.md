---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624130356/https://petermolnar.net/trick-wine-cd-change/
published: '2012-06-21T08:29:16+00:00'
redirect:
- neat-trick-change-cd-wine
summary: Need to install something with more than one install CD-s to wine?
    Here's how.
tags:
- linux
title: trick to "change" CD for wine

---

I've had a pretty hard time to install Baldur's Gate 2, even via
PlayOnLinux. The problem lies when you need to change CD-s: PlayOnLinux
do try to solve it for you, but it does not work.

But what works is multiple mounting. Awful and dangerous, but works:

```bash
sudo mount -o loop /path/to/ISO/CD1 /mnt
```

Start PlayOnLinux, select `mnt` as CD source... and step through the
offering to change CDs for you. When the game asks for the next CD, do
the following:

```bash
sudo mount -o loop /path/to/ISO/CD2 /mnt
```

This will not unmount CD1, but at the same point CD2 will be accessible.
Repeat this for CD3 and CD4. When the game asks for CD1:

```bash
sudo umount /dev/loop3
sudo umount /dev/loop2
sudo umount /dev/loop1
```

But don't remove `loop0`! That's CD1.

Done, play Baldur's Gate 2 on Linux.