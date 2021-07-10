---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20150524174731/https://petermolnar.eu/linux-tech-coding/howto-android-free-internet-call/
published: '2015-04-07T08:42:18+00:00'
summary: Android has a built-in SIP client in the Phone app which is much
    easier the use than any additional apps - even though it's voice only.
tags:
- android
title: How to use VoIP (SIP) on Android without any app

---

I've tried many apps for VoIP on Android, but it turns out, there is a
pretty hidden feature in the "Phone app" whic allows you to use VoIP in
Android without any additional resource killer.

You'll need a SIP account to use this. SIP[^1] is protocol invented
especially for voice over IP and you can get an account from many
providers. I'd recommend Linphone[^2] for start since it's free. Once
you have a <sip:someone@sip.linphone.org> you can call other
<sip:others@wherever.com> accounts.

Unfortunately not every mobile provider allows SIP protocol on their
network, so this method is mostly to be used over a Wireless Network.

## Adding the account

1.  Open the Phone app ( with the phone icon ) ![android home
    screen](android_native_voip_01.png)

2.  Go to Settings ( the three dots at the bottom ) ![android contacts
    screen](android_native_voip_02.png)

3.  Scroll to the bottom of settings ![android contacts
    menu](android_native_voip_03.png)

4.  Tap on `SIP Accounts`... ![android internet accounts in contacts
    menu](android_native_voip_04.png)

5.  ...and add an account ![android SIP accounts
    menu](android_native_voip_05.png)

6.  Tick the "Recieve incoming calls" if you want to be able to receive
    calls, not just initiate them.

7.  Once you're done, you can add SIP numbers to your contacts by
    selecting the `Internet number` field ![android add SIP to
    contact](android_native_voip_06.png)

8.  It will show up like this: ![android finished SIP of
    contact](android_native_voip_07.png)

And you'll be able to do free VoIP calls, without any memory hog,
resource-eating, privacy intruding app.

[^1]: <http://en.wikipedia.org/wiki/Session_Initiation_Protocol>

[^2]: <http://www.linphone.org/free-sip-service.html>