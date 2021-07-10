---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120415203306/http://petermolnar.eu:80/linux-tech-coding/photoshop-cs5-under-linux
published: '2011-10-21T08:19:48+00:00'
summary: How to get Photoshop CS5 working on wine.
tags:
- linux
title: Photoshop CS5 under linux

---

Adobe still refuses to port Photoshop (and a lot other programs) to
linux, although I do not think it would be that hard from the Mac
version.

Fortunately, there's a very good program for Linux, called wine. Since
wine cames from "Wine Is Not Emulator", it is still an emulator, and it
could be read as "windows emulator". But as anything in linux, if you
want to use it for good, you need some tweaking.

I still use Linux Mint 10 Julia (and I do recommend it above all), it is
based on Ubuntu 10.10 Maverick Meerkat, even Oneiric Ocelot is out now.
To get Photoshop work under linux, you'll need the following.

**The tutorial below comes without any warranty. I do not state it will
work with any config. I am using wine 1.3.29, no other versions are
tested. Photoshop is a commercial software from Adobe. You can try it
for 30 days as trial, but after you have to buy it.**

### Step 01 - install wine and wine addons

Install wine and winetricks.

```bash
sudo apt-get install wine winetricks
```

Install addons for wine. For this, you'll need a license for a Microsoft
Windows. The install process will not ask for it, this is only a
legality requirement. Version (98, XP, 2000, 7, stb) does not really
weight.

```bash
winetricks msxml6 gdiplus gecko vcrun2005sp1 vcrun2008 msxml3 atmlib
```

### Step 02 - add some DLL to wine

Inside this tar file[^1], you'll find 3 DLLs: you need to copy them to
\~/.wine/drive\_c/Windows/system32/.

### Step 03 - tweak wine config

Edit the \~/.wine/user.reg and add the following lines:

**after**

```ini
[AppEventsSchemesAppsExplorerNavigating.Current] some_numbers_here

@=""
```

`ps_cs5_winereg_01.ini`

```ini
[Console] 1314295973
"CursorSize"=dword:00000019
"CursorVisible"=dword:00000001
"EditionMode"=dword:00000000
"ExitOnDie"=dword:00000001
"FaceName"="Digital dream Fat Narrowrrow"
"FontSize"=dword:0011000a
"FontWeight"=dword:00000000
"HistoryBufferSize"=dword:00000032
"HistoryNoDup"=dword:00000000
"MenuMask"=dword:00000000
"QuickEdit"=dword:00000000
"ScreenBufferSize"=dword:00190050
"ScreenColors"=dword:0000000f
"WindowSize"=dword:00190050
```

**after**

```ini
[Control PanelColors] some_numbers_here
```

`ps_cs5_winereg_02.ini`

```ini
"ActiveBorder"="212 208 200"
"ActiveTitle"="94 129 188"
"AppWorkSpace"="128 128 128"
"Background"="16 26 38"
"ButtonAlternateFace"="181 181 181"
"ButtonDkShadow"="133 135 140"
"ButtonFace"="235 233 237"
"ButtonHilight"="255 255 255"
"ButtonLight"="220 223 228"
"ButtonShadow"="167 166 170"
"ButtonText"="0 0 0"
"GradientActiveTitle"="112 177 235"
"GradientInactiveTitle"="131 183 227"
"GrayText"="167 166 170"
"Hilight"="94 129 188"
"HilightText"="255 255 255"
"HotTrackingColor"="0 0 128"
"InactiveBorder"="212 208 200"
"InactiveTitle"="111 161 217"
"InactiveTitleText"="255 255 255"
"InfoText"="0 0 0"
"InfoWindow"="255 255 225"
"Menu"="255 255 255"
"MenuBar"="235 233 237"
"MenuHilight"="94 129 188"
"MenuText"="0 0 0"
"Scrollbar"="212 208 200"
"TitleText"="255 255 255"
"Window"="255 255 255"
"WindowFrame"="0 0 0"
"WindowText"="0 0 0"
```

**after**

```ini
"DragFullWindows"="0"
```

`ps_cs5_winereg_03.ini`

```ini
"FontSmoothing"="2"
"FontSmoothingGamma"=dword:00000578
"FontSmoothingOrientation"=dword:00000001
"FontSmoothingType"=dword:00000002
```

### Step 04 - Buy Photoshop CS5

Stealing is not nice.

### Step 05 - Look for Photoshop CS5 Portable

Search the web for Photoshop CS5 Portable. For legal reasons I cannot
link it directly.

This is a very strange pack of Photoshop CS5: it does not install in the
way programs do in Windows, much more it uses one and only one folder
for itself, like the ones from PortableAppZ[^2]. **This version is not
legal until you bought Photoshop, even if it does not require
registration. Please buy the software.**

### Step 06

Install portable Photoshop CS5 and run it. Da-dam!

[^1]: <https://www.dropbox.com/s/102xd1yyo69hn0o/dll.tar.gz?dl=0>

[^2]: <http://portableappz.blogspot.com>