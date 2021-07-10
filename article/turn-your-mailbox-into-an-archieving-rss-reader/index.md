---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624130401/https://petermolnar.net/turn-your-mailbox-into-an-archieving-rss-reader/
published: '2012-02-02T12:48:21+00:00'
redirect:
- turn-your-webmail-into-a-you-archievable-online-rss-reader
summary: 'Most RSS readers lack something: maybe offline version, online version,
    or just managed by someone 3rd party. A simple solution: back to the basics
    with rss2email, turniing the news into email.'
tags:
- e-mail
title: Turn your mailbox into an archieving RSS reader

---

A long time ago before RSS became a standard, Twitter was not on the
horizon yet all sites that wanted to inform their regular users used
newsletters. Some sites even still uses them, piecing together regular
RSS with special news. *(Although even before the www era existed
Network News Transfer Protocol[^1] to deliver news to people. You did
not even need to subscribe, it was easy to search and had a built-in
archieving structure, I really wonder when will be the renessaince of
NNTP.)*

RSS is a good thing. It is well structured, documented, easy to parse
and use in programs - but the available readers a suprisingly bad.

What's my problem? I'd like to access my RSS just from as many devices I
use for email

-   from work, online
-   from phone, online but with cached data
-   from laptop, offline

Here' a little list why I was searching for *something else*.

Google Reader[^2]
:   One of the most commonly used reader is Google Reader. Pretty
    simple, available anywhere - but not anytime. You need to be online,
    and also, Google has one more thing about you to chew on and serve
    even more commercials made especially for you.

Mozilla Thunderbird[^3]
:   I used to love Thunderbird. About 5 years ago I knew everything I
    wanted in a mailer and it could even read RSS. But today? It lacks
    sync abilities for caldav, for carddav, for SyncML, it's slow and
    becoming more and more incompatible with most if it's plugins,
    thanks for the update intervals. It's digging it's own grave, just
    like Firefox, and I really hope someone turn Tunderbird back into
    the yearly releases as before. Regarding the bugs and the problems,
    it still does one thing pretty good: it can copy RSS to an imap
    folder, therefore it's able to archiving them quite easily.

Tiny tiny RSS[^4]
:   This small project creates deployable online RSS reader, just
    prefect to replace Google Reader - my thoughts until I realized it
    does not work with PHP open\_basedir restriction. Let it pass!

This is the point where the obvious come in: let's parse RSS on my
server, and send them as emails!

## The solution: rss2email

Living in 2012 I was sure someone had already done a tool for this.
After a few commercial applications I've found a python based open
source solution to send RSS as email[^5], named rss2email.

It has a pretty good description in installation and configuration[^6],
I could not write a better one. Just one thing: first I tried installing
it from Ubuntu repository, but I was unable to locate the `config.py`
file needed to configure the program, so I downloaded the latest and
everything worked nicely.

[^1]: <http://en.wikipedia.org/wiki/Network_News_Transfer_Protocol>

[^2]: <http://www.google.com/reader>

[^3]: <http://www.mozilla.org/projects/thunderbird/>

[^4]: <http://tt-rss.org>

[^5]: <http://www.allthingsrss.com/rss2email/>

[^6]: <http://www.allthingsrss.com/rss2email/getting-started-with-rss2email/>