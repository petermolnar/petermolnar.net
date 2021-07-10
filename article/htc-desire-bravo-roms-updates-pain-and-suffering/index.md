---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120426092832/http://petermolnar.eu:80/linux-tech-coding/htc-desire-bravo-roms-updates-pain-and-suffering/
published: '2012-04-19T07:38:40+00:00'
summary: Replacing the ROM of a HTC Desire; notes for myself if I'd ever want
    to do this again.
tags:
- android
title: 'HTC Desire (Bravo): ROMs, updates, pain and suffering'

---

Prelude: I currently work as an embedded developer, I learnt as one, I
even got my degree on embedded systems - and flashing Android devices
are far more complicated than I've ever thought. **Unless you do really
have a reason, don't do custom ROM upgrades.**

## Only do this if you have TIME , PATIENCE and another phone with you.

Also... this is not a tutorial. This is only a collection of links,
tweaks troubleshoot methods, mostly for myself. I don't say this is
going to work. If you do anything to your phone, you're on your own, no
one to be blamed, so be aware.

## Why?

1 GHz, 576 MB RAM, has more RAM than a usual laptop 5 years ago, but
512MB flash and 150 MB for user is bloat.

Also there are no official, recommended, stable updates for HTC Desire
GSM (Bravo) after Android 2.2. They released a semi-official 2.3
update[^1]: only for experienced users - I've tried it after a custom
ROM, it did not connect to wireless networks, I could not even start a
call.

Another reason is that you want to replace the shipped apps, like I did.
Sometimes there are far better applications out there than the stock
ones - sometimes.

## Why not?

**Because something will definately go wrong, no exception**. ~~For me,
it seems I cannot connect USB Mass Storage anymore, no idea why. ( I've
tried it both in linux and Windows.)~~

### Do not forget to make backups. Always.

*And always verify them; belief is not enough. ClockwordMod backups DO
CAN FAIL.*

## What you need to understand

The system of an Android phone is made up of a lot .img files. These are
byte-by-byte copies of the affs2 filesystems used in embedded devices.
My HTC - and probably your device too - has the following parts:

bootloader :Don't touch this by hand. If you make a bad move, the phone
can only be restored by hardware hacks, and you really don't want to do
this. Use Revolutionary[^2], this will unlock the features of the
bootloader (S-OFF), for example, fastboot via USB.

recovery (recovery.img) :This the "backup" system; an alternative small
system you can boot into <del> to save the day</del> and modify the base
system. This system is usually replaced with Amon\_Ra[^3] or
ClockworkMod[^4]. Revolutionary installs ClockworkMod automatically.

boot (boot.img) :Loads the main kernel and the system itself. Do not
confuse with bootloader: bootloader loads the boot image.

system (system.img) :This is your system, the root partition if it
sounds better. *Clockwordmod says it makes a yaffs2 backup, but that's
not fully true: it dd-s the filesystem, while it should be cat-ed.*

data (data.img) :User data; something between /var and /home.

cache (cache.img) :Cache. Not important.

## Tools & resources

-   Revolutionary[^5] Makes things possible.
-   HTC developer portal[^6] You can access the kernel source, but
    that's only for really hardcore fans.
-   shipped-roms.com[^7] When you reach the point of crying, this is
    really handy: they are collecting the original stock roms and
    installers. Origins from a german forum[^8].

### Custom ROMs

-   cyanogen[^9] One of the most commonly used custom ROMs: fast, easy
    to use, quite stable, but has some serious bugs, like the Sleep of
    Death. Anyway, their wiki is a life-saver[^10].
-   ~~[LeeDroid](http://leedroid.com/)~~ ~~Some say the best ROM in the
    jungle; for me, it only threw errors over errors.~~

I've tried some others, but without success, they were stucked at a
bootloop[^11], and nothing helped at all.

## Lifesavers

-   adb[^12] This is part of all android systems: imagine it as a
    backdoor telnet to Android core. It can be used with USB ( default )
    or via WLAN[^13], this probably needs a rooted phone and a Terminal
    Emulator installed. adb can be installed as part of Android
    SDK[^14]. Also:
    <http://jonwestfall.com/2009/08/backup-restore-android-apps-using-adb/%5B%5E15%5D>
-   fastboot[^15] In short, fastboot is the interface to connect your
    computer to the bootloader via USB. It can re-flash any part of the
    system except the bootloader itself. To see all fastboot oem
    commands type: `fastboot oem ?`

## Hacking

### Step 1: Revolutionary[^16] {#step-1-revolutionary2}

This is the only step without any danger, except you will lose warranty.
Do as the site says; no tricks.

### Step 2: Backup

**Boot into recovery: hold vol down + power, wait, press vol down, wait,
press vol down twice, press power, wait for boot.**

This was the step that went partly wrong in my case, therefore I'm
currently unable to restore the stock system. The thing is that I did do
the backup in Clockworkmod but after reboot, it constantly says md5
mismatch. Later I've found that it says this for all backups but while
most of them is correct ( and can be solved by regenerating md5 hashed,
as described here[^17] ), though my system.img really went wrong: I'm
unable to re-flash it even with fastboot.

### Step 3: Flash your custom ROM

This is really easy. Copy the .zip file to the sdcard, boot into
recovery, wipe data, wipe cache, wipe dalvik cache, and install zip.
That's all.

### Step 4: Wait

First boot takes a long time. The Dalvik ( imagine as JVM for android )
compiles what needs to be compiled. This is stored in
/data/dalvik-cache.

## Troubles and solvings

### Recovery claims: unable to mount sdcard

Get into fastboot and send the following command:

    fastboot oem enableqxdm 0

### No USB Mass storage

Something happens, but the storage doesn't show up.

Get into fastboot and try:

    fastboot oem eraseconfig

Reboot, try mounting usb. If it fails:
<http://forum.xda-developers.com/showthread.php?t=1143252%5B%5E19%5D>

## Tweaks

### Remove system apps

<http://wiki.cyanogenmod.com/wiki/Barebones%5B%5E20%5D>

## Restore stock ROM

Follow the instructions ( Hungarian, so use G translate :) )

<http://pzoley.matraszele.hu/desire.php?p=wiki&i=27%5B%5E21%5D>

*And ... don't forget to sleep. It's important.*

[^1]: <http://shipped-roms.com/download.php?category=android&model=Bravo&file=HTC_Desire_Android_2.3_Upgrade.zip>

[^2]: <http://revolutionary.io/>

[^3]: <http://android-dls.com/wiki/index.php?title=Amon_Ra_recovery_tool>

[^4]: <http://download.clockworkmod.com/recoveries/>

[^5]: <http://revolutionary.io/>

[^6]: <http://htcdev.com/>

[^7]: <http://shipped-roms.com>

[^8]: <http://www.brutzelstube.de/2011/gerootetes-offizieles-htc-stock-rom-2-29-405-5-mit-addons/>

[^9]: <http://www.cyanogenmod.com/>

[^10]: <http://wiki.cyanogenmod.com>

[^11]: <http://wiki.cyanogenmod.com/wiki/Troubleshooting#Bootloop_problem>

[^12]: <http://developer.android.com/guide/developing/tools/adb.html>

[^13]: <http://stackoverflow.com/questions/2604727/how-can-i-connect-to-android-with-adb-over-tcp>

[^14]: <http://developer.android.com/sdk/index.html>

[^15]: <http://en.wikipedia.org/wiki/Fastboot>

[^16]: <http://revolutionary.io/>

[^17]: <http://forum.xda-developers.com/showthread.php?t=976453>