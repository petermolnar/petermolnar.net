---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624130102/https://petermolnar.net/save-files-from-a-dead-screen-android/
published: '2017-05-23T18:40:00+00:00'
summary: How to download your files and safely destroy personal data from
    a Samsung android phone with a dead screen using heimdall, TWRP, and adb.
tags:
- android
title: Save files from Samsung Galaxy S4 with a dead screen with Debian or
    Ubuntu

---

During our incredibly long, 5 days vacation, on the very first day
Nora's Galaxy S4 fell and with this final, rather heavy crack, the
screen went completely dead. For my surprise, the phone itself was
working well, given it woke us up at 4 am, which was slightly
unexpected.

Normally I have my laptop paired with ADB, but due to recent laptop
changes I forgot this step, so I was left without any connection to the
phone, as MTP requires the screen to be unlocked.

Plugging in an external display with an MHL cable didn't work either, so
I decided to flash a custom recovery and try to pull via adb - for my
surprise, it worked.

## Get Heimdall and adb

**All commands are executed as root.**

You'll need the following on Debian:

    apt install heimdall-flash android-tools-adb

*Normally, instead of `heimdall`, it would be `fastboot`, but not for a
Samsung phone.*

## Flash TWRP recovery in Odin mode

-   disconnect USB
-   remove battery
-   insert battery
-   Hold `volume down` + `power` until it vibes for 1 time
-   press `volume up`.
-   connect the USB cable

See if the device is visible:

```bash
heimdall detect
    Device detected
```

If you're good to go, get the TWRP recovery; in my case, the device is
an i9505, codenamed 'jfltexx'.

**Make sure you're getting the right image for your device model.**

```bash
cd /tmp
wget https://eu.dl.twrp.me/jfltexx/twrp-3.1.1-0-jfltexx.img
```

When you have the image, flash it:

```bash
heimdall flash --RECOVERY /tmp/twrp-3.1.1-0-jfltexx.img --no-reboot
```

When you're using `--RECOVERY`, there is no need to download the PIT
file and to look for the recovery partition.

-   remove USB
-   remove the battery

## Boot recovery

-   hold `volume up` + `power` until it vibes
-   release `power` immediately
-   keep holding `volume up` for 1-2s more

Verify you have connection: (it takes a few seconds for recovery to
boot, be patient)

```bash
adb usb
adb devices
    List of devices attached
    d910339a        recovery
```

## Save the data

```bash
adb pull -a /sdcard/ /where/you/want/to/save/
```

This can take a while; also, make sure you have enough space on the
device you're saving to.

## Wipe the personal data

```bash
adb shell
twrp wipe data
twrp wipe cache
twrp wipe dalvik
reboot recovery
```

The last step reboots the device back to recovery; that is to make sure
there is no cached filesystem data.

Once it's back:

```bash
adb shell
ls -la /sdcard
drwxrwx---    3 media_rw media_rw      4096 Jan  1 00:25 .
drwxr-xr-x   24 root     root             0 Jan  1 00:28 ..
drwxrwxrwx    2 root     root          4096 Jan  1 00:25 TWRP

ls -la /data/
drwxrwx--x    4 system   system        4096 Jan  1 00:16 .
drwxr-xr-x   24 root     root             0 Jan  1 00:28 ..
-rw-------    1 root     root             2 Jan  7  1970 .layout_version
drwxrwx---    2 root     root          4096 Jan  7  1970 lost+found
drwxrwx---    5 media_rw media_rw      4096 Jan  7  1970 media
```

If it's all clear, it's safe to put it up for a £0.99 auction on eBay.