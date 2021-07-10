---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20170708205715/https://petermolnar.net/trackpoint-drifting-stop/
published: '2017-05-31T18:00:00+00:00'
summary: How to stop Trackpoint from constantly, slowly moving on it's own
    under linux
tags:
- linux
title: A dirty fix for non-stop drifting Trackpoint

---

## The problem

> \[...\] **PROBLEM**: The cursor always slowly moves to the lower left.
> One pixel every few seconds[^1].\[...\]

I had the exact same issue[^2]: painfully slowly drifting Trackpoint on
my X250, never stopping. I'm aware of the Trackpoint self-calibration, I
had that on the X200, on the T400, and on the T500, but this was
different. **If you have the pointer moving fast or just rarely on it's
own, that is normal.** In my case, it never stopped.

The really surprising thing was that this only happened under Debian
Stretch (RC2) and not under Ubuntu 16.04, so I started looking around
`/sys`:

*Note: it's probably serio2, but could be 3, 4, etc., depending on
module load order and number of input devices.*

```bash
# ls /sys/devices/platform/i8042/serio1/serio3
bind_mode    driver       id       mindrag          protocol    resolution   speed      upthresh
description  drvctl       inertia  modalias         rate        resync_time  subsystem  ztime
draghys      ext_dev      input    power            reach       sensitivity  thresh
drift_time   firmware_id  jenks    press_to_select  resetafter  skipback     uevent
```

Most of these are pretty much undocumented and so far none of the GUI
configuration managers supported them. The 3 interesting ones are
`drift_time`, `sensitivity`, and `speed` in this case.

**Despite this fix, this is most probably a hardware problem, so
consider replacing the keyboard, especially if it's still under
warranty, though if it doesn't happen under Windows, this will be near
impossible to get through the service.**

## Temporary fix

Most will recommend to lower the sensitivity, but that doesn't always
work or help.

```bash
echo 2 > /sys/devices/platform/i8042/serio1/serio2/drift_time
echo 180 > /sys/devices/platform/i8042/serio1/serio2/sensitivity
echo 50 > /sys/devices/platform/i8042/serio1/serio2/speed
```

## Keep it after reboot

```bash
systemd-tmpfiles --prefix=/sys --create
sensible-editor /etc/tmpfiles.d/trackpoint.conf
```

    w /sys/devices/platform/i8042/serio1/serio2/speed - - - - 50
    w /sys/devices/platform/i8042/serio1/serio2/sensitivity - - - - 180
    w /sys/devices/platform/i8042/serio1/serio2/drift_time - - - - 2

<ins>
UPDATE<time datetime="2019-02-14T20:12:06+0000">2019-02-14</time></ins>

The path has changed:

    w /sys/devices/rmi4-00/rmi4-00.fn03/serio3/speed - - - - 180
    w /sys/devices/rmi4-00/rmi4-00.fn03/serio3/sensitivity - - - - 120
    w /sys/devices/rmi4-00/rmi4-00.fn03/serio3/drift_time - - - - 2

[^1]: <https://superuser.com/questions/1200352/thinkpad-trackpoint-moves-on-its-own-on-linux>

[^2]: <https://www.reddit.com/r/thinkpad/comments/68sxua/x250_trackpoint_acting_up_on_debian_up_to_date/>