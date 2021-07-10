---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20171202025751/https://petermolnar.net/hard-drive-spindown-clicking-noise/
published: '2017-05-24T06:35:00+00:00'
summary: How to spin down hard drive and get rid of the clicking noise in
    Debian 9 (Strecth) and Ubuntu 16.04 on a Thinkpad X250
tags:
- linux
title: Fix the hard drive killer APM

---

## Killing your drive by trying to save milliwatts

There is a well-known problem, especially in the linux word, of "drive
clicking". It's root cause can vary (thinkwiki has an extensive list of
them[^1]), but it's mostly because badly configured power management.

**This misconfiguration can easily mean the end of your hard drive
within months.**

I have both and SSD and a HDD in my X250; I also I have a HGST 1TB
drive[^2] in my home server. This has 29230 hours of power-on time
(that's roughly 3 years) and 945437 Load Cycle Count - and this latter
is not funny.

The drive, in theory, rated to tolerate 600000 of these, not a million,
so I'm a little worried if the drive will fail on me.

To save my other drives from this fate I started looking into the issue
deeper, just to learn that I couldn't find any page where someone would
describe:

-   how to get rid of the clicking
-   still spin down the disk automatically when unused
-   why this wasn't an issue a few years and linux distributions ago

So, here are my answers.

## What didn't work

### `/etc/hdparm.conf`

`hdparm`[^3] is a low-level hard drive utility, and in this case, it has
two important parameters:

-   -B - Get/set Advanced Power Management feature
-   -S - set the standby (spindown) timeout for the drive

The answer for my third question - why this wasn't an issue - lies here:
the APM was not a thing on many old machines, and, by default, it was
set to 255, disabled.

The spindown timeout was also respected, when it was put into
`/etc/hdparm.conf`, which is not the case any more.

### Advanced Power Management

> **-B** Get/set Advanced Power Management feature, if the drive
> supports it. A low value means aggressive power management and a high
> value means better performance. Possible settings range from values 1
> through 127 (which permit spin-down), and values 128 through 254
> (which do not permit spin-down). The highest degree of power
> management is attained with a setting of 1, and the highest I/O
> performance with a setting of 254. A value of 255 tells hdparm to
> disable Advanced Power Management altogether on the drive (not all
> drives support disabling it, but most do).

According to SilverbackNet[^4], -B accepts the following values:

    Maximum performance FEh
    Intermediate power management levels without Standby 81h-FDh
    Minimum power consumption without Standby 80h
    Intermediate power management levels with Standby 02h-7Fh
    Minimum power consumption with Standby 01h
    Reserved FFh
    Reserved 00h

In the case of HGST, FF (255) disables Advanced Power Management and
completely stops trying to spin the disk down every second.
Unfortunately this also means you'll need to configure spinning the disk
down manually, since the power management is not going to do it for you
any more.

A downside is that it will also stop unloading the head, and so the disk
will consume more - and more consistent amount - of watts.

### Standby timeout

> **-S** Put the drive into idle (low-power) mode, and also set the
> standby (spindown) timeout for the drive. This timeout value is used
> by the drive to determine how long to wait (with no disk activity)
> before turning off the spindle motor to save power. Under such
> circumstances, the drive may take as long as 30 seconds to respond to
> a subsequent disk access, though most drives are much quicker. The
> encoding of the timeout value is somewhat peculiar. A value of zero
> means "timeouts are disabled": the device will not automatically enter
> standby mode. Values from 1 to 240 specify multiples of 5 seconds,
> yielding timeouts from 5 seconds to 20 minutes. Values from 241 to 251
> specify from 1 to 11 units of 30 minutes, yielding timeouts from 30
> minutes to 5.5 hours. A value of 252 signifies a timeout of 21
> minutes. A value of 253 sets a vendor-defined timeout period between 8
> and 12 hours, and the value 254 is reserved. 255 is interpreted as 21
> minutes plus 15 seconds. Note that some older drives may have very
> different interpretations of these values.

## What did work

There's just one problem: no matter what I tried, this parameters was
ignored in Debian 9+, until I found a thread, mentioning that from now
on, you need to configure `udisks2`.

Forget `/etc/default/tlp` and `/etc/hdparm.conf`, because for -S, they
will be ignored.

To actually allow it, you'll need the following magic:

```bash
info=$(smartctl -i /dev/sda)
device=$(echo -i "$info" | grep 'Device Model' | cut -d":" -f2 | xargs | sed 's/ /-/m')
serial=$(echo "$info" | grep -i 'Serial Number' | cut -d":" -f2 | xargs | sed 's/ /-/m')

echo -e "[ATA]\nStandbyTimeout=180" > "/etc/udisks2/$device-$serial.conf"
```

This script creates a file under `/etc/udisks2/device-serialnumber.conf`
with the contents needed to configure the StandbyTimeout ATA parameter.

There. Clicking stopped, spindown re-enabled.

[^1]: <http://www.thinkwiki.org/wiki/Problem_with_hard_drive_clicking>

[^2]: <http://amzn.to/2lKj2OG>

[^3]: <https://linux.die.net/man/8/hdparm>

[^4]: <https://superuser.com/a/558622/74821>