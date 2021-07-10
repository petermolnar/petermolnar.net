---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20160810120240/https://petermolnar.eu/why-i-keep-using-email/
published: '2015-12-10T16:52:07+00:00'
summary: How and why I keep using email.
tags:
- e-mail
title: Why I still use email

---

aaronpk's Why I Live in IRC[^1] is one of the best articles I've read in
a long time. For most of the new kids on the block it's probably an
insanely hardcore and nerd way of doing things, especially since IRC is
considered to be old, arcane and thus, something that needs reinventing.
*It's not, and it doesn't need fixing.*

So I started thinking if it would make sense for me to do something
similar, since IRC is easy to deal with - and I came to realize that I
use mostly email, and that I like it that way.

## The main why-s for keeping email

It's lightweight. It has to be, it's roots are dating back to the 70s
(60s?) when computing power wasn't really a thing yet. For the same
reason, it uses a very different communication structure than the ones
we're used to, but hey, I could send an email from an Arduino, using tty
only. In case you want the simplest solution - just want to send things
to yourself and not communicate with others - all you need is an SMTP
server and a local user. If you want remote access, you probably need an
IMAP server, but syncing the plain text files would be just as fine.
*(If you insist on receiving from the world, then spam, SPF, DKIM, DMARC
and all those fancy things, but you'd have to do similar steps to
protect IRC for anything if facing the cruel world lurking behind your
NAT.)*

It's mature, stable, and - if configured properly - extremely reliable.
It's pretty hard to lose an email even in between machines.

It is one of the most pluggable systems. End-to-end encryption? Server
side filters? Different authentication method? TLS or STARTTLS
communication between server and client? All doable; all done.

It's pretty low on bandwidth use - with options to restrict it to
ridiculous level and still keep it working - and it also doesn't require
a constant connection, so regular drops *(hi there, London Tube!)* are
not an issue.

IMAP is probably the one and only protocol for accessing mail nowadays.
It has a feature, called IDLE[^2] which was Push notifications before it
was cool. Also: in case of IMAP lots of things can access a single
source simultaneously.

And one more important aspect: it can easily be backed up. From copying
the Maildir[^3] folder to syncing with offlineimap[^4] there are plenty
of tools to do this.

## The downsides

Email has a pretty unpredictable delay if it involves 2 or more SMTP
servers. It was never intended to be a real-time communication method,
but potential of a severe delay can be an issue in some situations,
especially in alerting. In the past 10 years it's been extremely rare to
see delays over a few minutes though.

Both sending and receiving are centralized, so if you can't access the
server, you can't access your mail. But with most things accessed by
many, this is the usual layout. *(This is also the official reason why
Skype was moved from p2p to a centralized architecture: to be able to
log in from more than one device.)*

## Some of my use cases

### My Reader

When I first came across RSS I used Thunderbird as a reader, and I got
pretty used to having my news in my mail client. *By the way, News in a
mail client is NNTP and is an entirely different thing.*

So when I moved from using a single computer to using X computers,
including webmail, I needed something that gives me RSS as mail. For
years, it was rss2email[^5] v2.70, but it developed some strange issues,
like forgetting about some URLs. So I added a WordPress plugin (think of
WordPress as a horrible storage framework in my case), called
blogroll2email[^6], doing the same for me, but now it can also parse
microformats2 powered sites.

### generic communication

Instead of relying the all-changing sea of various messenger apps, I'm
trying to stick to email. I have it everywhere, the APIs and protocolls
are not changing every second month and it's working. The problem that
it's becoming a little ignored by others, though I'm really not willing
to change this in favour of some random newcomer 'free' app wanting to
store all my things on their servers.

### reporting

Email is perfect for cron outputs, statuses, various summaries and
notifications, that are not urgent and can tolerate a little delay;
mostly because it can give for formatting. ( No, not HTML, there are
formattings in plain text. )

I've been a long time monit[^7] user and by default, monit can
communicate via email only. Normally monit would act - as in restart a
service or trigger a script, etc. - so instead of alerting it's better
to says it's sending reports as well.

## How it's done

My main server has the following mail stack:

-   `postfix` as SMTP
-   `dovecot` as IMAP and authentication
-   `dspam` as spam filtering hook
-   `openDKIM` as DKIM signing hook on sending
-   `openDMARC` as DMARC verification hook

More details:

-   Lightweight, secure, database-free, spamfiltering mail server with
    Postfix, Dovecot, openDKIM and dspam on Debian 7[^8]
-   Getting DKIM, DMARC and SPF to work with Postfix, OpenDKIM and
    OpenDMARC[^9]

I have a few things at home which are also allowed to send email, but
those are SMTP only, having the main server as relay host. For a long
while I could not get a static IP at home, therefore I had the following
ways for letting those addresses send a mail:

-   setting up an SSH tunnel from the boxes, connecting local port 25 to
    remote port 25 on the main server
-   auto-whitelisting the dynamic IP addresses based on a dynamic DNS
    check

## Footnote: Email isn't broken; email providers are

> Everyone want to "fix" email, and replace it with some proprietary
> bullshit. Email isn't broken. - Spooky23[^10]

What happened is that email had became strong, strong enough that it
became a legal document in some cases. Bookings, flight boarding passes,
various, pretty sensitive information are sent via email, therefore it
needs to get secured deeper and deeper.

Those who keep saying email is broken usually keep repeating the
following: "it's old", "it's complicated", "spam", "not secure" and "no
use uses it anymore".

### old != crap

Just because it was originally invented 30+ years ago does no make email
crap. Age does not make anything crap. Just take a look at what the old
mainframe operating systems were capable on security. Or check out
Fortran and Lisp.

### (hard to do \|\| complitaced) != broken

Runnig a full fledged email stack might be complicated - it's not that
hard - but that doesn't mean it's broken. Yes, it takes a little time
and a bit of knowledge from various sources - such as knowing what DNS
is and being able to make changes to it. It's totally possible do run
you own mail services without running into issues with it, but indeed
you need to understand what you're doing, even if that means you'll
eventually need to learn a few new things which won't work by piping a
bash script from curl.

### secure != anonym

Many are attacking email that it's insecure - it's not. It is not
anonym, but these two sings should not be mixed up. Anonymity is
important nowadays, but it does not equal security, and things that are
not anonym can be pretty tight on security.

### spam != broken

Spam is everywhere. I'm getting pingback and comment spam on my
WordPress even if the comment form is not shown. I admit that it used to
be a serious issue with email, but with the rise of blacklists,
effective and smart spamfilters, it's reduced to a negligible amount.

### no use uses it anymore == bullshit

> Can't believe all the hate I see here. I agree with the Verge writers.
> Email is slowly dying. Slack looks awesome. - vicentedepierola[^11]

Riiiight. External, unencrypted, 3rd party, hosted service for the wins.
I honestly don't want to see a provider sending boarding cards via
Slack.

### The valid problem: too tight security

A few months ago an article emerged: The Hostile Email Landscape[^12].
Though I haven't experience yet what they are talking about, if this
trend continues, email will indeed become an endangered species. Too
tight security does exist, and it's never good.

[^1]: <https://aaronparecki.com/articles/2015/08/29/1/why-i-live-in-irc>

[^2]: <https://tools.ietf.org/html/rfc2177>

[^3]: <https://en.wikipedia.org/wiki/Maildir>

[^4]: <http://offlineimap.org/>

[^5]: <http://www.allthingsrss.com/rss2email/>

[^6]: <https://github.com/petermolnar/blogroll2email>

[^7]: <https://mmonit.com/monit/>

[^8]: <https://petermolnar.net/debian-lightweight-mailserver-postfix-dovecot-dspam/>

[^9]: <https://petermolnar.net/howto-spf-dkim-dmarc-postfix/>

[^10]: <https://news.ycombinator.com/item?id=10691337>

[^11]: <http://www.theverge.com/2014/8/12/5991005/slack-is-killing-email-yes-really#252288840>

[^12]: <http://liminality.xyz/the-hostile-email-landscape/>