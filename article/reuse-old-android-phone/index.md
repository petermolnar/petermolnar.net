---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20140919105218/https://petermolnar.eu/linux-tech-coding/reuse-old-android-phone/
published: '2014-08-06T13:32:32+00:00'
summary: Old(ish) Android device? Upgrade it, use it as webcam, SMS gw, backup
    server… there's no need to throw it away.
tags:
- android
title: What is an old(ish) Android phone / tablet good for?

---

No matter what the ads say, there are plenty of options an old ( or
slightly less old ) Android device could be reused as.

## 1. Enhance it and keep using it: install a new operating system ( it will definitely feel like having a new phone )

Buying a new phone will not necessarily be a new experience. In case
you're staying with the same brand, the feel will be the same, the
system will be very, very similar. And it will probably be bigger, which
is not always that good. ( My pockets were about the same in the past 20
years and there is a certain problem fitting an 5" screen in there )

If you like your current phone, but it feels a bit slow, it lacks space
or even it sounds dull, there is a way make it better.

I had an HTC Desire before my Nexus 4 and I was quite disappointed when
it turned out that out of the 512MB internal memory there was \~152MB
available for user apps. *( Sounds like the distant past, yet it was
only 4 years ago )*

It turned out that there are "hacked" Androids that let you use parts of
the SD card as memory, or ones that swaps the original user parition
with the system partition ( which was \~200MB ) and voilá, the phone
suddenly had 4+GB app storage and plenty of space. I had my issues with
the install process[^1], but at the end, it definitely worth it.

Some devices, like HTC and Samsung are unfortunately very protective and
does not let you easily change the system; others, like the Nexus
devices were planned to be used as development devices as well; those
are easy to hack.

If you want to go along with this ( and realize how much faster & better
your device could be ), start at "the original" alternative firmware,
Cyanogenmod[^2] - you'll be able to install it through an app, just to
make your life easier. Their wiki[^3] have lots of information as well.

There are other, very exotic, Android based systems as well, like
MIUI[^4]. Version 4 was much like a merge of IOS and Android (closed
source, but also blazing fast), version 5 was a truly exotic one,
version 6 looks really promising. (This is also the official system of
Xiaomi phones.)

*Disclaimer: since I'm talking about old devices I believe there is no
warranty available for them anymore. Reinstalling the operating system
on the device may invalidate the warranty in case it still has one.*

## 2. Put it into use in your household: make it a home server!

### 2.1 Using Android apps to provide server-like features

There are some apps that provide server like functionalities for an
Android device, especially if you're about to use the phone
functionalities.

Examples:

-   use it as a wifi webcam / security cam with
    -   Wifi Camera[^5]
    -   MobileWebCam[^6]
    -   Spydroid[^7]
-   use it as SMS gateway server
    -   Turn your Android Phone into a SMS Gateway[^8]
-   turn it into a 3G hotspot
    -   use FoxFi[^9] to avoid some carrier limitations
    -   Use Your Android Phone as a Wi-Fi Hotspot for Free[^10]
-   use it as file or Media server
    -   Servers Ultimate Turns Your Old Android Phone Into a Tiny,
        Multipurpose Server[^11]
    -   How to turn you android phone or tablet into a web, file or
        media server[^12]
-   use it as media / gaming console ( HDMI out capable devices only )
    -   How to Turn Your Android into a Killer Portable Media and Gaming
        Center[^13]
    -   Droid Meets HDMI: How To Connect Your Android Phone To Your
        TV[^14]

### 2.2 Take it one step further: install a full-fledged linux on top of Android

There are applications[^15] and guides[^16] to install a full-fletched
Debian on top of you Android.

About a year ago I managed to get nginx, PHP-FPM, Percona MySQL server
on an HTC Desire which was capable of running a WordPress site. It was
slow and I'd rather recommend running something less resource intense
but hey, I used my phone as a webserver!

Examples that a phone-server would be good for:

-   (rsync) backup server for a small VPS ( 16+GB SDcard is recommended
    )
-   (S)FTP server with dynamic DNS
-   webserver
-   mail server
-   proxy
-   and anything you can think of…

## 3. Let someone reuse it

In case you do not want any of those above, but the phone is still
functioning or would function with a bit of repair, please don't throw
it away; someone else would happily use it and you can help reduce the
amount of e-waste we generate.

### 3.1 Give it away

If you have family members, friends, neighbours who would use your old
one happily, give it to them.

### 3.2 Donate it

Electronic donations can be very useful. Think about it before throwing
you working, but worn device away.

Examples:

-   5 Charities for Donating Your Old Electronics[^17]
-   Give Electricals AU[^18]
-   UK IT recycling Ltd[^19]

### 3.3 Sell it

You can sell anything on eBay[^20], even broken devices, as spare parts.
Someone might just be looking for a part in your dead device. Start it
as a £1 auction and be surprised how long it can go! (Be honest with the
description.)

### 3.4 If it's utterly broken

…there might still be someone to fix it for you or teach you how to fix
it. Get in touch with a local Restart Party[^21], a local
Hackerspace[^22], take cookies with you and talk to them.

## 4. Why the hassle?

Because even recycling is good, but it's not the best option[^23].

[^1]: <https://petermolnar.net/htc-desire-bravo-roms-updates-pain-and-suffering/>

[^2]: <http://beta.download.cyanogenmod.org/install>

[^3]: <http://wiki.cyanogenmod.org/w/Main_Page>

[^4]: <http://en.miui.com/>

[^5]: <https://f-droid.org/repository/browse/?fdfilter=webcam&fdid=teaonly.droideye>

[^6]: <https://f-droid.org/repository/browse/?fdfilter=webcam&fdid=com.dngames.mobilewebcam>

[^7]: <https://f-droid.org/repository/browse/?fdfilter=camera&fdid=net.majorkernelpanic.spydroid>

[^8]: <http://www.etctips.com/turn-your-android-phone-into-a-sms-gateway/>

[^9]: <http://foxfi.com/>

[^10]: <http://lifehacker.com/5930111/use-your-android-phone-as-a-wi-fi-hotspot-for-free>

[^11]: <http://lifehacker.com/5936339/servers-ultimate-turns-your-old-android-phone-into-a-tiny-multipurpose-server>

[^12]: <http://www.digitaltrends.com/mobile/how-to-make-an-android-server/#!bwd347>

[^13]: <http://lifehacker.com/5915083/how-to-turn-your-android-into-an-awesome-portable-media-and-gaming-center>

[^14]: <http://www.makeuseof.com/tag/droid-meets-hdmi-how-and-why-to-connect-your-android-phone-to-your-tv/>

[^15]: <https://guardianproject.info/code/lildebi/>

[^16]: <http://forum.xda-developers.com/showthread.php?t=1872752>

[^17]: <http://mashable.com/2010/04/29/donating-electronics/>

[^18]: <http://www.givenow.com.au/otherways/electricals>

[^19]: <http://www.ukitrecycling.com/charity>

[^20]: <http://www.ebay.co.uk>

[^21]: <http://therestartproject.org/events/>

[^22]: <http://hackerspaces.org/wiki/List_of_Hacker_Spaces>

[^23]: <http://ifixit.org/recycling>