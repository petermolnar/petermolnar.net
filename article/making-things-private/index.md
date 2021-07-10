---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20171028220852/https://petermolnar.net/making-things-private/
published: '2017-10-28T15:00:00+00:00'
summary: I spent a lot of time trying centralising my online activities, including
    adding bookmarks and imports from social networks. Lately my site looked
    bloated and unmaintainable. I started questioning what data is my data,
    what data should or could I own - it was time to rethink some ideas.
tags:
- indieweb
title: Content, bloat, privacy, archives

---

**Have you ever reached the point when you started questioning why
you're doing something? ** **I have, but never before with my website.**

![What is my purpose? The unfortunate, sentient robot Rick created for
the sole purpose of passing the butter.](what_is_my_purpose.gif)

The precursor to petermolnar.net started existing for a very simple
reason: I wanted an online home and I wanted to put "interesting" things
on it. It was in 1999, before chronological ordering took over the
internet.[^1] Soon it got a blog-ish stream, then a portfolio for my
photos, later tech howtos and long journal entries, but one thing was
consistent for a very long time: the majority of the content was made by
me.

After encountering the indieweb movement[^2] I started developing the
idea of centralising one's self. I wrote about it not once[^3] but
twice[^4], but going through with importing bookmarks and favourites had
an unexpected outcome: they heavily outweighed my original content.

**Do you know what happens when your own website doesn't have your own
content? It starts feeling distant and unfamiliar. When you get here,
you either leave the whole thing behind or reboot it somehow. I couldn't
imagine not having a website, so I rebooted.**

I kept long journal entries; notes, for replies to other websites and
for short entries; photos; and tech articles - the rest needs to
continue it's life either archived privately or forgotten for good.

## Outsourcing bookmarks

The indieweb wiki entry on `bookmark` says[^5]:

> Why should you post bookmark posts? Good question. People seem to have
> reasons for doing so. (please feel free to replace this rhetorical
> question with actual reasoning)

Since that didn't help, I stepped back one step further: why do I
bookmark?

Usually it's because I found them interesting and/or useful. What I
ended up having was a date of bookmarking, a title, a URL, and some
badly applied tags. In this form, bookmarks on my site were completely
useless: I didn't have the content that made them interesting nor a way
to search them properly.

To solve the first problem, the missing content, my initial idea was to
leave everything in place and pull an extract of the content to have
something to search in. It didn't go well. There's a plethora of
js;dr[^6] sites these days, which don't, any more, offer a working,
plain HTML output without executing JavaScript. For archival purposes,
archive.org introduced an arcane file format, WARC[^7]: it saves
everything about the site, but there is no way to simply open it for
view. Saving pages with crawlers including media files generated a silly
amount of data on my system and soon became unsustainable.

Soon I realised I'm trying to solve a problem others worked on for
years, if not decades, so I decided to look into existing bookmark
managers. I tried two paid services, Pinboard[^8] and Pocket[^9] first.
Pocket would be unbeatable, even though it's not self hosted, if the
article extracts they make were available through their API. They are
not. Unfortunately Pinboard wasn't giving me much over my existing
crawler solutions.

**The winner was Wallabag**[^10]: it's self-hosted, which is great,
painful to install and set up, which is not, but it's completely
self-sustaining, runs on SQLite and good enough for me.

There was only one problem: none of these offered archival copies of
images, and some of the bookmarks I made were solely for the photos on
the sites. I found a format, called MHTML[^11], also known as `.eml`,
which is perfect for single-file archives of HTML pages: it inlines all
images as base64 encoded data.

However, **no browser offers a save-as-mhtml in headless mode, so to get
your archives, you'll need to revisit your bookmarks. All of them.** I
enabled[^12] save as MHTML in Chrome (Firefox doesn't know this format),
installed the Wayback Machine[^13] extension and saved GBs of websites.
I also added them into Wallabag. It's an interesting, though very long
journey, but you'll rediscover a lot of things for sure.

When this was done, I dropped thousands of bookmark entries from my
site.

**If I do want to share a site, I'll write a note about it, but
bookmarks, without context, belong to my archives.**

## (Some) microblog imports should never have happened

I had iterations of imports, so after bookmarks it seemed reasonable to
check what else may simply be noise on my site.

*Back in the days* people mostly wrote much lengthier entries:
journal-like diary pages, thoughts, and it was, nearly always,
anonymous. It all happened under pseudonyms.

Parallel to this there were the oldschool instant messengers, like ICQ
and MSN Messenger. In many cases, though you all had handles, or
numbers, or usernames, you knew exactly who you were talking to. Most of
these programs had a feature called status message - looking back at it
they may have been precursors to microblogging, but there was a huge
difference: they were ephemeral.

With the rise of Twitter and Facebook status message also came (forced?)
real identities, and tools letting us post from anywhere, within
seconds. The content that earlier landed in status messages - *XY is
listening to....*, *Feels like...*, etc - suddenly became readable at
any time, sometimes to anyone.

I had content like this and I am, as well, guilty of posting short,
meaningless, out-of-context entries. Imported burps of private life;
useless shares of music pointing to long dead links; one-liner jokes,
linking to bash.org; tiny replies and notes that should have been sent
privately, either via email or some other mechanism.

**Some things are meant to be ephemeral**, no matter how loud the
librarian is screaming deep inside me. **Others belong in logs, and
probably not on the public internet**.

I deleted most of them and placed a `HTTP 410 Gone` message for their
URLs.

## Reposts are messy

For a few months I've been silently populating a category that I didn't
promote openly: `favorite`s. At that page, I basically had a lot of
`repost`s: images and galleries, with complete content, but with big fat
URLs over them, linking to the original content.

By using a silo you usually give permission to the silo to use your work
wherever they want it. Due to the effects of `vote`s and `like`s (see
later) you do, in fact, boost the visibility of the artist. *Note that
usually these permissions are much broader, than you imagine: a lawyer
reworded the policy of Instagram to let everyone understand, that by
using the service, you allow them to do more or less anything the want
to with your work[^14]*.

But what if you take content out of a silo? **The majority of images and
works are not licensed in any special way, meaning you need to assume
full copyright protection**. Copyright prohibits publishing works
without the author's explicit consensus, **so when you repost**
something that doesn't indicate it's OK with it - Creative Commons,
Public Domain, etc -, **what you do is illegal**.

Also: for me, it feels like reposts, without notifying the creator, even
though the licence allows it, are somewhat unfair - which is exactly
what I was doing with these. Webmentions[^15] would like to address this
by having an option to send notifications and delete requests, but silos
are not there yet to send or to receive any of these.

**There is a very simple solution: avoid reposting anything without
being sure it's licence allows you.** Save it in a private, offline
copy, if you really want to. Cweiske had a nice idea about adding source
URLs into JPG XMP metadata [^16], so you know where it's from.

## Silo reactions only make sense within the silo

When I started writing this entry, I differentiated 3, not-comment
reaction types in silos:

A `reaction` **is a social interaction, essentially a templated
comment**. "Well done", "I disagree", "buu", "acknowledged", ❤, 👍, ★,
and so on. *I asked my wife what she thinks about likes, why she uses
them, and I got an unexpected answer: because, unlike with regular, text
comments, others will not be able react to it - so no trolling or abuse
is possible.*

A `vote` **has direct effect on ranking**: think reddit up- and
downvotes. Ideally it's anonymous: list of voters should not be
displayed, not even for the owner of the entry.

A `bookmark` **is solely for one's self: save this entry because I value
it and I want to be able to find it again**. They should have no social
implications or boosting effect at all.

In many of the silos these are mixed - a Twitter fav used to range from
an appreciation to a sarcastic meh[^17]. With a range of reactions
available this may get simpler to differentiate, but a `like` in
Facebook still counts as both a `vote` and a `reaction`.

I thought a lot about reactions and I came to the conclusion that I
should not have them on my site. The first problem is they will be
linking into a walled garden, without context, maybe pointing at a
private(ish) post, available to a limited audience. **If the content is
that good, bookmark it as well. If it's a reaction for the sake of being
social, it's ephemeral.**

## Conclusions

Don't let your ideas take over the things you enjoy. Some ideas can be
beneficial, others are passing experiments.

There's a lot of data worth collecting: scrobbles, location data, etc.,
but these are logs, and most of them, in my opinion, should be private.
If I'm getting paranoid about how much services know about me, I
shouldn't publish the same information publicly either.

And finally: keep things simple. I'm finding myself throwing out my
filter coffee machine and replacing it with a pot that has a paper
filter slot - it makes an even better coffee and I have to care about
one less electrical thing. The same should apply for my web presence:
the simpler is usually better.

[^1]: <https://stackingthebricks.com/how-blogs-broke-the-web/>

[^2]: <https://indieweb.org/>

[^3]: <https://petermolnar.net/indieweb-decentralize-web-centralizing-ourselves/>

[^4]: <https://petermolnar.net/personal-website-as-archiving-vault/>

[^5]: <https://indieweb.org/bookmark>

[^6]: <http://tantek.com/2015/069/t1/js-dr-javascript-required-dead>

[^7]: <http://www.archiveteam.org/index.php?title=Wget_with_WARC_output>

[^8]: <http://pinboard.in/>

[^9]: <http://getpocket.com/>

[^10]: <https://wallabag.org/en>

[^11]: <https://en.wikipedia.org/wiki/MHTML>

[^12]: <https://superuser.com/a/445988>

[^13]: <https://chrome.google.com/webstore/detail/waybackmachine/gofnhkhaadkoabedkchceagnjjicaihi>

[^14]: <https://qz.com/878790/a-lawyer-rewrote-instagrams-terms-of-service-for-kids-now-you-can-understand-all-of-the-private-data-you-and-your-teen-are-giving-up-to-social-media/>

[^15]: <https://webmention.net/draft/#sending-webmentions-for-deleted-posts>

[^16]: <http://cweiske.de/tagebuch/exif-url.htm>

[^17]: <http://time.com/4336/a-simple-guide-to-twitter-favs/>