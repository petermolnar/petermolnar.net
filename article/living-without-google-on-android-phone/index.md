---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20160709135044/https://petermolnar.eu/living-without-google-on-android-phone/
published: '2014-07-15T12:48:29+00:00'
redirect:
- android-without-google
- living-without-google
summary: Android without any Google App? What to use instead of Hangouts,
    Map, Gmail?  Is that even possible? And why would anyone want to live
    without Google?
tags:
- android
title: Alternative for Google Apps on Android - living without Google on Android

---

I've been using a lot of different custom ROMs on my devices, so far the
two best: plain Cyanogenmod 11 snapshot on the Nexus 4[^1], and MIUI
2.3.2 on the HTC Desire G7[^2]. All the others ( MUIU 5, MIUI 6
unofficial, AOKP, Kaos, Slim, etc ) were either ugly, unusable, too
strange or exceptionally problematic on battery life.

For a long time, the first step for me was to install the Google Apps,
gapps packages for Plays Store, Maps, and so on, but lately they require
so much rights on the phone that I started to have a bad taste about
them. Then I started to look for alternatives.

## So, what to replace with what?

Play Store
:   I've been using F-Droid[^3] as my primary app store for a while now,
    but since it's strictly Free Software[^4] store only, sometimes
    there's just no app present for your needs; aptoide[^5] comes very
    handy in that cases.

Hangouts
:   I never liked Hangouts since the move from Gtalk although for a
    little while it was exceptional for video - I guess it ended when
    the mass started to use it in replacement of Skype and its recent
    suckyness. For chat only, check out: ChatSecure[^6],
    Conversations[^7] or Xabber[^8]. All of them is good for Gtalk-like,
    oldschool client and though Facebook can be configured as XMPP as
    well, I'd recommend Xabber for that, the other two is a bit flaky
    with Facebook. And you can also use VoIP on any Android[^9] - there
    is a built-in option for that, you don't even need any additional
    apps.

Map
:   This is the most problematic replacement: Maps is exceptional, an
    incredible tool, fast, accurate - but it still collects a crazy
    amount of data about you. Osmand[^10] is a good map, but it's a bit
    geeky and slow; RMaps[^11] on the other hand seem to be doing a very
    good job.

Gmail
:   First of all: don't use Gmail. They read your mails.[^12] And for
    mail on Android, use K9[^13], because it's a really, really good
    mail client. I'd like to have it on my desktop as well.

Chrome
:   There are tons of browsers out there, I'd recommend 3: Firefox[^14],
    because it's full-fledged, Open Source and under active development;
    Lightning[^15], because it's a Free Software and very small; Tint
    Browser[^16], because it's Open Source and has the fastest rendering
    speed I've seen so far (and has adblock addon[^17]).

Google+
:   I have no idea why would you want Google+ as an app. Use the browser
    to access it.

Google Keyboard
:   I was not aware of this until I checked the gapps packages; just use
    Hacker's Keyboard[^18].

Google Play Books, Google Play Games, Google Play Newsstand, Google Play Music, Google Play Movies
:   Books, music, movies: my recommendations on this is the oldschool
    way: by the CDs, the ebooks, the movies, rip them to your computer
    and copy the files. Use VLC[^19] for media, Cool Reader[^20] or
    FBReader[^21] for ebooks, MuPDF[^22] for magazines, VuDroid[^23] for
    djvu. For plain old music playing, also see Just Player[^24] This
    way, no one can remotely delete your books, music, or video[^25].

YouTube
:   If you're using Youtube to listen to music, check out
    NetMBuddy[^26]. For videos, see PTVStar[^27]/jp.co.asbit.pvstar).

Google Drive
:   For plain file synchronisation check out Syncthing[^28]; ironically
    there's not alternative way to download it officially, so I've
    uploaded it to dropbox[^29]. MD5 sum the two if you feel unsafe. For
    web as well, try Owncloud[^30]. Yes, it needs a server and setup and
    all the fuss, but you will not be judged by your data.[^31]

Wallet
:   There's no alternative for this yet, but I guess if you're willing
    to pay by your phone as credit card, you're not concerned about
    privacy or security.

Sync services
:   Use Baikal[^32] with DAVDroid[^33] or Owncloud[^34] with Owncloud
    Client[^35] for contact & calendar sync, Syncthing[^36] or Owncloud
    for data & files sync.

## Will it worth it?

**From the privacy point of view, it will.** From the user experience
point: no, it will probably not. Some apps are just as good as the
corporate surveillance[^37] ones, like K9, Tint Browser, but some will
give you an edgy feeling, like Xabber: even though it's fast, works
really stable, it does not look good and the whole UI is pretty rough.

Unfortunately, at this point in time, you need to choose: "free"
services, in exchange for knowledge on everything you do ( yes,
including that copied ebook, because your friend would have lent it to
you, but with ebooks, there's no such thing as lending anymore, hell, I
think publishers would try to stop lending real books if the could ), or
slightly unpolished, Free and Open alternatives.

Choose your future, like you did with web 2.0[^38].

[^1]: <http://download.cyanogenmod.org/?device=mako>

[^2]: <http://pzoley.matraszele.hu/desire.php?p=176>

[^3]: <https://f-droid.org/>

[^4]: <https://en.wikipedia.org/wiki/Free_software>

[^5]: <http://m.aptoide.com/>

[^6]: <https://f-droid.org/repository/browse/?fdfilter=xmpp&fdid=info.guardianproject.otr.app.im>

[^7]: <https://f-droid.org/repository/browse/?fdfilter=xmpp&fdid=eu.siacs.conversations>

[^8]: <https://f-droid.org/repository/browse/?fdfilter=xmpp&fdid=com.xabber.androiddev>

[^9]: <https://petermolnar.net/linux-tech-coding/howto-android-free-internet-call/>

[^10]: <https://f-droid.org/repository/browse/?fdfilter=osmand&fdid=net.osmand.plus>

[^11]: <http://eroe.store.aptoide.com/app/market/com.robert.maps/8140/3414820/RMaps:%20Offline%20maps>

[^12]: <http://www.huffingtonpost.com/2014/04/15/gmail-ads_n_5149032.html>

[^13]: <https://f-droid.org/repository/browse/?fdfilter=k9&fdid=com.fsck.k9>

[^14]: <https://f-droid.org/repository/browse/?fdfilter=firefox&fdid=org.mozilla.firefox>

[^15]: <https://f-droid.org/repository/browse/?fdfilter=lightning&fdid=acr.browser.lightning>

[^16]: <http://m.collusion.store.aptoide.com/app/market/org.tint/10/4696767/Tint%20Browser>

[^17]: <http://m.arcanatoria.store.aptoide.com/app/market/org.tint.adblock/3/1112870/Tint%20Browser%20Adblock%20addon>

[^18]: <https://f-droid.org/repository/browse/?fdfilter=hacker&fdid=org.pocketworkstation.pckeyboard>

[^19]: <https://f-droid.org/repository/browse/?fdfilter=vlc&fdid=org.videolan.vlc>

[^20]: <https://f-droid.org/repository/browse/?fdfilter=reader&fdid=org.coolreader>

[^21]: <https://f-droid.org/repository/browse/?fdfilter=reader&fdid=org.geometerplus.zlibrary.ui.android>

[^22]: <https://f-droid.org/repository/browse/?fdfilter=mupdf&fdid=com.artifex.mupdfdemo>

[^23]: <https://f-droid.org/repository/browse/?fdfilter=reader&fdid=org.vudroid>

[^24]: <https://f-droid.org/repository/browse/?fdfilter=just%20player&fdid=jp.co.kayo.android.localplayer>

[^25]: <http://www.nytimes.com/2009/07/18/technology/companies/18amazon.html?_r=0>

[^26]: <https://f-droid.org/repository/browse/?fdcategory=Multimedia&fdid=free.yhc.netmbuddy&fdpage=3>

[^27]: <http://www.appbrain.com/app/pvstar-youtube-music-player>

[^28]: <https://play.google.com/store/apps/details?id=com.nutomic.syncthingandroid>

[^29]: <https://f-droid.org/repository/browse/?fdid=com.nutomic.syncthingandroid>

[^30]: <https://owncloud.com/>

[^31]: <http://www.extremetech.com/computing/179495-how-dropbox-knows-youre-a-dirty-pirate-and-why-you-shouldnt-use-cloud-storage-to-share-copyrighted-files>

[^32]: <http://baikal-server.com/>

[^33]: <https://f-droid.org/repository/browse/?fdfilter=davdroid&fdid=at.bitfire.davdroid>

[^34]: <https://owncloud.org/>

[^35]: <https://f-droid.org/repository/browse/?fdfilter=owncloud&fdid=com.owncloud.android>

[^36]: <https://f-droid.org/repository/browse/?fdfilter=syncthing&fdid=com.nutomic.syncthingandroid>

[^37]: <https://ind.ie/manifesto/>

[^38]: <https://web.archive.org/web/20111109014223/http://interface-7.net/20060919/>
