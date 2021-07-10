---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120602200216/http://petermolnar.eu:80/linux-tech-coding/how-to-make-ubuntu-12-04-lts-precise-pangolin-usable
published: '2012-05-04T14:30:42+00:00'
summary: Tweaks after install in order to achieve the usability of Linux Mint
    10. But the new mascot is pretty cute.
tags:
- linux desktop
title: How to make Ubuntu 12.04 LTS (Precise Pangolin) usable

---

I've started using Ubuntu on servers from version 6.06[^1] and I still
say, for server, it's one of the best and most easily maintainable
distributions out there - not mention the commercial support behind the
system. On the desktop side however... from 9.04 to 10.04 Ubuntu was a
good choice. Afterwards I've migrated to Linux Mint[^2], especially to
Mint 10, Julia[^3] - I have to say that version was probably the best
I've encountered with.

But time has passed and unfortunately, Mint 10 was not a long term
support version and it's official lifespan has ended. Also, it's quite
impossible to install the freshly released Gimp 2.8[^4] on a 1,5 old
system - *which is actually ridiculous and sad, but true* - so I needed
to change. Ubuntu 11.04 and 11.10 was a total mess, mostly with the
premature Unity and the forced kernel updates. *Between 2.6.36 and 3.2
there shouldn't have been any update in my opinion*.

Mint 12[^5] - based on Ubuntu 11.10 - was near to usable with
Cinnamon[^6]: lots of version problems, PPA not recognizing the version,
etc., so right after the release of the next long-term-support Ubuntu, I
decided to move back AND have the Mint desktop Cinnamon on it.

12.04 LTS[^7] comes with Unity[^8]. Unity is progressive and has a lot
of ideas in it, unfortunately most of them just renders things unusable
for everyday work. It's fun, yes, it's nice and pretty and everything,
but for someone using a linux desktop professionally, it's simply
ineffective. **Eventually I forced myself to use Unity for a week; for
my surprise, it did change my opinion on the topic, see later in this
article.**

## Fail at install: encrypt home without swap partition

I have 4 GB memory in my notebook; it has been enough for years without
swap. Even if I'm in the need of swap, I would not add it as partition
just a simple file using `swapon` command. But... 12.04 requires a swap
partition if you want your home folder encrypted - otherwise the whole
install process will fail. Isn't that nice from a version that's planned
for 5 years?! I've installed the system without encrypted home, and
followed Danny Stieben's[^9] guide how to encrypt it on an installed
system[^10].

Yes, it's already been reported[^11].

## Conquer your desktop once again

Two possibilities to get a desktop like the good'ol Gnome2:
`gnome-panel` (a rearranged Gnome3 fallback mode) or Cinnamon. Both
provides conventional desktops, meaning you do have a window list,
screen is not jumping on the move of your mouse, you can actually find
the close button for a software.

### gnome-panel

Gnome2 layout based on GTK3. Most of the functions are
backward-compatible, meaning you can have applets again. For more
information, see the OMG! Ubuntu! article on gnome-panel[^12]. It's
simple to install:

```bash
apt-get install gnome-panel
```

### Cinnamon desktop

Cinnamon[^13] is the Linux Mint way to enlightenment: a GTK3, especiall
Gnome Shell based desktop environment with traditional layout. It's at
version 1.4, lacks a lot of features, but it's nice, fast, responsive
and suprisingly low on CPU & memory usage. It's not the part of Ubuntu,
so you're going to need to add an additional repository.

```bash
add-apt-repository ppa:gwendal-lebihan-dev/cinnamon-stable
apt-get update
apt-get install cinnamon
```

I needed a dock in order to get this fully functional ( the lack of CPU
applet for example ), my choose was Avant Window Navigator[^14].

```bash
apt-get install avant-window-navigator
```

## The for people who use their machine both day and night

I hate high contrast themes. Really. They are for vanilla people, using
their pretty little machine only by day. For Gnome2 the choice was Shiki
Colors[^15], especially Shiki Brave - a more-or-less replacement for
GTK3 is Zukitwo[^16].

## ThinkPad users: tp-smapi-dkms

Even in 11.04, tp-smapi install was plain simple, working right after
the apt-get install command. Not from 11.10; tp-smapi-dkms moved from
version 0.40 to version 0.41 and thus not working
anymore.<del datetime="2012-11-16T10:15:14+00:00"> Get the package from
Natty[^17], and install it by hand. Extract it to `/usr/src/` ( as
`/usr/src/tp-smapi-0.40` ), and use the following:</del> Natty is out of
support, so I uploaded the patched version to GitHub[^18], use it from
there please.

```bash
dkms add -m tp-smapi -v 0.40
dkms build -m tp-smapi -v 0.40
dkms install -m tp-smapi -v 0.40
```

## Regain aircrack-ng

These are my favourite ones: a slight but, it's not maintaned, so it
gets dropped. And oh, no alternatives. Anyway, Riyaz Ahemed Walikar[^19]
has written a post on gettin aircrack work in Precise Pangolin[^20].

```bash
apt-get install build-essential libssl-dev
wget http://download.aircrack-ng.org/aircrack-ng-1.1.tar.gz
tar -zxvf aircrack-ng-1.1.tar.gz
cd aircrack-ng-1.1
```

Replace the line

```c
CFLAGS ?= -g -W -Wall -Werror -O3
```

to:

```c
CFLAGS ?= -g -W -Wall -O3
```

in `common.mak`. Then

```bash
make &amp;&amp; make install
```

## From now on...

I'm going to extend this post whenever I encounter something strange.

<ins datetime="2012-05-07-T11:00:00GMT">
</ins>
## "Loggin in..." freeze in lightdm

Caused by disabling the login sound[^21] with Ubuntu Tweak[^22]. Either
replace lightdm with gdm or don't disable the logon sound.

<ins datetime="2012-05-08-T18:51:00GMT">
</ins>
## Wireless semi-disconnecting

The connection itself stays but no data flows in any direction. Solution
by Sam Armstrong[^23]:

```bash
sudo iwconfig wlan0 power off
```

<ins datetime="2012-07-19-T16:00:00GMT">
</ins>
### another solution, from a ThinkPad forum:

```bash
create /etc/modprobe.d/iwl.conf with the following:

#!/bin/sh
options iwlwifi bt_coex_active=0
```

<ins datetime="2012-06-16-T22:34:00GMT">
</ins>
## Show all startup applications

Some startup applications are hidden by default. Just the way Apple and
MS is walking on... grats.

```bash
sudo sed -i 's/NoDisplay=true/NoDisplay=false/g' /etc/xdg/autostart/*.desktop
```

<ins datetime="2012-06-17-T08:42:00GMT">
</ins>
## Freakingly annoying right-clik popup when F10 is pressed in terminal

Press F10 in terminal, for Midnight Commander to exit ... you'll have
right-click menu popped up. Isn't this wonderful?! To disable, put this
into `~/.config/gtk-3.0`:

```bash
@binding-set NoKeyboardNavigation {
     unbind "<shift>F10"
}

* {
     gtk-key-bindings: NoKeyboardNavigation
}
```

and this into `~/.gtkrc-2.0`:

```bash
binding "NoKeyboardNavigation" {
    unbind "</shift><shift>F10"
}

class "*" binding "NoKeyboardNavigation"
```

<ins datetime="2012-08-16-T16:00:00GMT">
</ins>
## Unity - maybe it's not the Devil itself?

I tried Cinnamon and MATE - both of them is unstable enough to cause
problems for, so I forced myself to give a chance to Unity and use it
for a week. The result? This really was made for keyboard freaks,
sysadmins and not that bad as I first feeled.

First off: the global menu is not that bad. For me, I'm using Terminator
as terminal emulator, and it can split itself in one window. Second: the
"flying" scrollbar is still annoying a bit sometimes, but reasonable,
and you don't need to move the mouse to the top or the bottom. And most
importantly: even multi-windows applications are not really a problem,
Xsane works perfectly. To be sure, you can always open it on another
virtual desktop, separated from the others.

The thing is, it's far-far away from the classics, nearly as far as
Fluxbox. But it is useable. It lacks tweaking, yes, but to be honest,
you only tweaked when you needed something it was not capable of... and
it seems, Unity is capable of doing a lot of things.

Just turn Zeitgeist off[^24]; now that's something making the system
slow and you really don't need it. Honestly.

<ins datetime="2012-11-12T14:36:31+00:00">
</ins>
## Solve the "blank screen after resume from suspend"

Once in a while my machine seemed to freeze after resume from suspend:
blank screen, command line cursor at the upper left corner, no response
except changing to tty\[1-6\], but the login fails with no error message
- just nothing happens. It turned out I'm not the only one and it's not
dependent of any of my hacks - phc, SSD, etc. - but occurs independently
from machine type. The solution was found on Ubuntu Forums[^25], this is
the lot shorter one recommended in the thread:

```bash
sudo touch /etc/pm/sleep.d/20_custom-ehci_hcd
sudo chmod 755 /etc/pm/sleep.d/20_custom-ehci_hcd

sudo cat >> /etc/pm/sleep.d/20_custom-ehci_hcd < < EOF
#!/bin/sh
# File: "/etc/pm/sleep.d/20_custom-ehci_hcd".
TMPLIST=/tmp/ehci-dev-list

case "${1}" in
        hibernate|suspend)

        ;;
        resume|thaw)

     chvt 1
     chvt 7
        ;;
esac
EOF
```

<ins datetime="2012-11-22T11:39:27+00:00">
</ins>
## Faenza icon theme missing icon for indicator-cpufreq

Fix submitted in this thread[^26].

<ins datetime="2013-12-03T09:38:00+00:00">
</ins>
## 16 steps of brightness for ThinkPads instead of 8

Due to some bug, on some ThinkPad instead of the 16 brightness steps,
only 8 is available. This is because two systems are handling the
request: the BIOS and linux itself. To solve it there are two ways,
according to this thread, this worked and was easy:

    echo -n 0 > /sys/module/video/parameters/brightness_switch_enabled

[^1]: <http://old-releases.ubuntu.com/releases/6.06/>

[^2]: <http://linuxmint.com>

[^3]: <http://old-releases.ubuntu.com/releases/6.06/>

[^4]: <http://www.webupd8.org/2012/05/gimp-28-stable-finally-available-for.html>

[^5]: <http://www.linuxmint.com/release.php?id=17>

[^6]: <http://cinnamon.linuxmint.com>

[^7]: <http://releases.ubuntu.com/releases/12.04/>

[^8]: <http://unity.ubuntu.com/>

[^9]: <http://www.makeuseof.com/tag/author/danny/>

[^10]: <http://www.makeuseof.com/tag/encrypt-home-folder-ubuntu-installation-linux/>

[^11]: <https://bugs.launchpad.net/ubuntu/+source/ubiquity/+bug/991139>

[^12]: <http://www.omgubuntu.co.uk/2012/03/gnome-classic-in-ubuntu-12-04-its-like-nothing-ever-changed/>

[^13]: <http://cinnamon.linuxmint.com>

[^14]: <https://launchpad.net/awn/>

[^15]: <http://gnome-look.org/content/show.php/Shiki-Colors?content=86717>

[^16]: <http://lassekongo83.deviantart.com/art/Zukitwo-203936861>

[^17]: <http://packages.ubuntu.com/natty/all/tp-smapi-dkms/download>

[^18]: <https://github.com/petermolnar/tp-smapi-0.40-patched/downloads>

[^19]: <http://www.blogger.com/profile/10553011445419057597>

[^20]: <http://www.riyazwalikar.com/2010/12/installing-aircrack-ng-on-ubuntu-1204.html>

[^21]: <https://bugs.launchpad.net/unity-greeter/+bug/986967>

[^22]: <http://ubuntu-tweak.com>

[^23]: <https://plus.google.com/106676640127767267723/about>

[^24]: <http://linuxaria.com/howto/how-to-remove-zeitgeist-in-ubuntu-and-why?lang=en>

[^25]: <http://ubuntuforums.org/showthread.php?t=1978290>

[^26]: <https://bugs.launchpad.net/indicator-cpufreq/+bug/772084>