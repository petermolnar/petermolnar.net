---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125427/https://petermolnar.net/ext4-reserved-blocks-size/
published: '2012-06-10T09:00:28+00:00'
redirect:
- free-up-ext4-reserved-blocks
summary: How to get "free" space on EXT filesystem without deleting anything?
tags:
- linux
title: Conquer your EXT partition

---

I've always aware of reserved blocks on an EXT filesystem ( and on NTFS
as well ) - probably this is one reason for newcomers to choose ReiserFS
instead. For them, I'd recommend btrfs[^1], but for those of stability
junkies and EXT lovers: on every non-system disk this is truly safe to
do, and you'll not regret it.

When you format a partition to EXT, the filesystem reserves some space
to store system things inside it. It's also a kind of stability issue,
an inside swap if it pleases - but there's no need for it on non-system
disk. This usually takes 5% of the formatted disk capacity - as for 1 TB
disk it's 50GBs !!

Now, to reduce it:

```bash
sudo tune2fs -m 1 /dev/[your device]
```

This sets the reserved blocks to 1%, therefore on a TB disk to 10GB.
It's still much, I know, and in some cases it's safe to reduce it to 0,
but just to make sure everything is working fine, I left it on 1%.

See what you gained:

```bash
df -h
```

As for Truecrypt devices: When you mount a truecrypt partition ( or full
disk ) there's going to be a `/dev/mapper/truecryptX`, where X is a
number. Use this instead of `/dev/[your device]`

[^1]: <http://en.wikipedia.org/wiki/Btrfs>