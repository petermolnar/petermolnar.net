---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120604220703/http://petermolnar.eu:80/linux-tech-coding/how-to-move-dalvik-cache-to-system-partition-in-android
published: '2012-06-01T05:12:37+00:00'
summary: Move the dalvik-cache from data partition to system on rooted, S-OFF
    android devices.
tags:
- android
title: How to move dalvik-cache to /system partition in Android

---

## Disclaimer: I'm not responsible; it's your device, your hack, your mod.

## This little how-to is for linux.

## There's no guarantee it'll work.

If you ever wondered where is you're free space going on your android
device - or why do every single app takes up twice the space of the
downloaded data - the answer is: dalvik-cache.

Dalvik is a Java Virtual Machine implementation, used in all Android
devices. I've got a HTC Desire ( codenamed Bravo if that's better ). In
this machine, the user have access to 160 MB - this includes the
downloaded apps, the app data and the dalvik cache. No magic here, it's
going to be full in a blink.

One way is moving the apps to the SD card, a lot of scripts exists for
this already, but this had been really unstable for me - meaning a
sudden power loss ment full-reinstall, including the ROM itself.

I searched for an other way: the /system partition is twice the size of
the /data ( the userspace ), 250 MB, and it's more than half empty! Why
is dalvik-cache not located here?

It's simple: security. Nowadays every manufacturer believes that
officially blocking users to take full control of their devices is the
way of a good device. No, it is not.

So... what to do? In a few words: make system writeable permanently,
delete the `/data/dalvik-cache` folder, create `/system/dalvik-cache`
folder and make a symlink from this to `/data/dalvik-cache`.

How? First: root your phone, make it S-OFF, and install your custom ROM.
Then....

1.  unpack your custom ROM's zip.
2.  inside, you'll find a boot.img
3.  download these tools, extract them[^1]
4.  copy boot.img into the extraction folder
5.  run `./extractboot` as root
6.  go into the out/ramdisk folder
7.  modify init.rc (see below)
8.  re-pack the boot.img with `./packboot`
9.  upload with fastboot `fastboot flash boot boot.img`
10. pray

To hack the init.rc file: I'm using "stock" CyanogenMod 7.2.0-rc1, so
the following is especially for this. Search for a line where the
/system is re-mounted as read only something like this:

```bash
mount yaffs2 mtd@system /system ro remount
```

comment this line out OR replace `ro` with `rw`.

Search for the part creating the dalvik-cache, something like this:

```bash
# create dalvik-cache and double-check the perms
mkdir /data/dalvik-cache 0771 system system
chown system system /data/dalvik-cache
chmod 0771 /data/dalvik-cache
```

Modify it:

```bash

# create dalvik-cache and double-check the perms
mkdir /system/dalvik-cache 0771 system system
chown system system /system/dalvik-cache
chmod 0771 /system/dalvik-cache

ln -s /system/dalvik-cache /data/dalvik-cache
chown system system /data/dalvik-cache
chmod 0771 /data/dalvik-cache
```

That' all. Please feel free to ask any questions.

[^1]: <https://www.dropbox.com/s/h004g5vrxae5upt/bootimgtools.tar.gz?dl=0>