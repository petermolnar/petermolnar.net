---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120416170357/http://petermolnar.eu:80/linux-tech-coding/dell-latitude-e6400-and-linux-mint-11-fine-tuning
published: '2011-06-10T19:59:48+00:00'
summary: Tweaking and modifying some "minor" things in Linux Mint 11 for better
    performance and usability on Dell Latitude E6400.
tags:
- linux
title: Dell Latitude E6400 and Linux Mint 11 fine tuning

---

Currently I have a Latitude E6400, and I needed lots of tweaks to get it
work as I like it under Linux (currently Mint 11, Katya, prevoiusly
Ubuntu 10.10, Maverick Meerkat).

## Tweak the touchpad

For an unknown reason, Dell keeps using ALPS touchpads, with all their
errors and bugs. My usual error: keeping my finger on the scrolling area
kills the touchpad: it becomes uresponsive or very-very slow, and only
gets well if the trackpoint is moved.

After searching a lot, I've found, that the synaptics driver can be used
instead of the default mouse driver, and maxtap parameters can be set
with this driver.

```bash
apt-get install xserver-xorg-input-synaptics
```

After successfull install, replace the default mouse part in
`/etc/X11/xorg.conf`:

```apache
Section "InputDevice"
Identifier     "Mouse0"
Driver         "synaptics"
Option         "Device" "/dev/input/event2"
Option         "Protocol" "event"
Option         "SendCoreEvents" "true"
Option         "Emulate3Buttons" "no"
Option         "ZAxisMapping" "4 5"
Option         "MaxTapTime" "180"
Option         "MaxTapMove" "110"
EndSection
```

For me, this is still under testing, I really hope, it solves my
problems.

## Update WiFi driver for BCM4322

Please visit my previous post about this topic[^1].

## Tweak nVidia config to achieve powersave mode

Change the default part of "Device0" in `/etc/X11/xorg.conf` to the
following:

```apache
Section "Device"
Identifier          "Device0"
Driver              "nvidia"
VendorName              "NVIDIA Corporation"
BoardName               "Quadro NVS 160M"
Option              "NoLogo"    "True"
Option              "Coolbits" "1"
Option              "RegistryDwords" "PowerMizerEnable=0x1; PerfLevelSrc=0x2222; PowerMizerLevel=0x3; PowerMizerDefault=0x3; PowerMizerDefaultAC=0x3; PowerMizerLevelAC=0x3; EnableMClkSlowdown=0x1; EnableCoreSlowdown=0x1; EnableNVClkSlowdown=0x1"
EndSectionn
```

This enables the strongest powersafe mode both running from battery and
AC power. Some say, this won't work, although it does reduced my
notebook need for energy.

## Control the fan yourself

**WARNING! THIS MAY RUIN YOUR COMPUTER PERMANENTLY! I DO NOT TAKE ANY
RESPONSIBILITY FOR THIS STEP, AND ONLY DO IT IF YOU REALLY KNOW, WHAT
YOU'RE DOING!**

My previously owned machine (Lenovo T500) was merely heard, the fan
didn't really make a squeak. (Although it constatly made a very high
piched noise, some say, it's because a powersave mode of the CPU itself,
and just to make it clear, it was annoying). However, the Dell E6400 has
constant fan problems in every possible way: a lot of people complained
about overheating in the Intel GPU models, and there's already been 28
(!) BIOS updates, yet the thermal table is still awful.

The main problem, that the machine's termal control listen to the CPU,
GPU, motherboard and disk temperatures, and the fan will be on, if the
disk is over 38 °C. My disk is a 250GB, 7200 RPM Hitachi and it's
operating temperature is about 41 °C... it doesn't really ever gets a
lot warmer, but it keeps the fan running.

To control the fan, first you need to prevent the BIOS from taking the
control back in every 3 seconds: (it is really annoying, the BIOS tries
to spin the fan to at least 3K in every 3 seconds...). You can do the
following in any operating system, but wait until the system booted up
(if I tried this during Linux boot, sometimes it prevented the system to
load) `press and hold SHIFT + FN, and press in order: 1 5 3 2 4n`.

After this, if you've done it right, the three keyboard indicator LED
will flash, and the most right one will stay flashing.

You can now press `FN + Rn` to access the thermal control system.With
the arrows, go to the "Disable thermal control" part, press right, than
enter two times, thus the thermal control is disabled.

Now you can run i8ktools[^2] or dellfand\^3[^3]. A minor drawback is
that both program can only change the speed in 3 steps: no fan, low and
high. Low is about 2500 turn/min, high is about 4400.

I tried to hack dellfand as setting the control values (originally 256
and 512 decimal for low and high), but nothing between the two original
values made any changes, so it seems, we need to be satisfied with this.

[^1]: <https://petermolnar.net/better-driver-for-bcm4322-802-11abgn-in-ubuntu-10-10/>

[^2]: <http://www.diefer.de/i8kfan/>

[^3]: <http://dellfand.dinglisch.net/>