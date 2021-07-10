---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624130006/https://petermolnar.net/ramdisk-debian-wheezy-k-tmpfs/
published: '2013-09-27T08:56:51+00:00'
summary: Use tmpfs instead of /dev/ramX in Debian Wheezy for ram based space.
tags:
- linux
title: Ramdisk in Debian Wheezy - a.k.a tmpfs

---

I wanted to play with ram based disks in Debian 7 Wheezy and I ran into
a lot on confusing articles on the topic. I turned out that the classis
/dev/ramX devices are not encouraged anymore instead, there's tmpfs.

If you don't have this, create a mount point for it:

```bash
mkdir -m 1777 /ram
```

and mount it:

```bash
tmpfs   /ram    tmpfs   defaults,size=2g    0   0
```

You have a 2G space in the ram accessible right there.

Also, if you want to keep directories synced:

```bash
vim /root/sync-memdisk.sh
```

```bash

#!/usr/bin/env bash

DIRS=( 'subdir1' )
TARGETS=( '/target/root1' )
ORIGINS=( '/origin/root1' )

for ((i=0; i< ${#TARGETS[@]}; i++)); do
    TARGET=${TARGETS[${i}]}
    ORIGIN=${ORIGINS[${i}]}
    DIR=${DIRS[${i}]}

    if [ ! -d "${TARGET}/${DIR}" ]; then
        echo "Initial sync from ${ORIGIN}/${DIR} to ${TARGET}/"
        rsync -aq ${ORIGIN}/${DIR} ${TARGET}/
    else
        echo "Sync from ${TARGET}/${DIR} to ${ORIGIN}/"
        rsync -au --delete ${TARGET}/${DIR} ${ORIGIN}/
    fi
done
```

Add it to cron:

```bash
*/2     *       *       *       *       /bin/bash /root/sync-memdisk.sh >/dev/null 2>&1
```