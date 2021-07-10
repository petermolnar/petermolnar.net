---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20141202094633/https://petermolnar.eu/linux-tech-coding/rss-is-still-alive/
published: '2014-11-12T10:27:47+00:00'
summary: Examples for RSS feed options of some social sites.
tags:
- internet
title: Hidden and less hidden RSS feeds on some major social networks

---

RSS[^1] used to be THE thing to follow people all around. It has a
gargantuan advantage compared to any "Follow" button on any website: it
used to be platform and service independent but centralized in your
chosen RSS reader. The reader crawled all the RSS feeds you were
"following" from all around the internet - and that's it. Like e-mail.
*And it's also the easiest way to anonymously stalk around.* Since
Google phased out it's Reader, RSS slowly started to fade out but some
other services still have it - and it's good for you.

## The Good

Below the services who play nice and do show the RSS feed URLs in the
gallery/page/portfolio site source code - only none of the "modern"
browsers care anymore to show the RSS icon in the toolbar.

### deviantArt

`http://backend.deviantart.com/rss.xml?q=gallery%3AUSERNAME`.

`gallery:` becomes `gallery%3A` due to the URL encoding; only replace
the `USERNAME` with the deviantArt username.

### Tumblr

`http://USERNAME.tumblr.com/rss`

Tumblr is one of the exceptions: most of the themes still have the RSS
logo with the RSS link underneath it.

### WordPress

WordPress ( both .com and hosted sites ) nearly always have RSS feeds
for the site, for the categories, the tags; even for comments, sitewise
and per entry.

Examples:

full site feed
:   `http://USERNAME.wordpress.com/comments/feed`

full comments feed
:   `http://USERNAME.wordpress.com/comments/feed`

category feed
:   `http://USERNAME.wordpress.com/category/CATEGORYNAME/feed`

post specific comments feed
:   `http://USERNAME.wordpress.com/URL/TO/THE/POST/feed`

### Blogspot.com

`http://USERNAME.blogspot.com/feeds/posts/default`

## The Ugly

The following sites are not really announcing - or not the way they
should, within the actual page - the following RSS feed options.

### Flickr

To get the feed of a single person use:
`https://api.flickr.com/services/feeds/photos_public.gne?lang=en-us&format=rss_200&id=USERID`.

Unfortunately, the USERID is not the username, and to get the actual ID
you either need to need to use the Flickr API or visit a 3rd party
service, like <http://idgettr.com/>. At least you can specify set IDs as
well to follow, the details are at
<https://www.flickr.com/services/feeds/>.

There is also a way to get the feed of everyone you follow:
`https://api.flickr.com/services/feeds/photos_friends.gne?lang=en-us&format=rss_200&id=USERID`
but in this case, USERID should be your own ID.

### Behance

`https://www.behance.net/USERNAME.xml`

Replace USERNAME with the Behance portfolio owner's username.

## Pinterest

`http://www.pinterest.com/USERNAME/BOARDNAME.rss`

to get the feed of a specific board. I could not find the way to get a
feed of all boards of a user.

## Instagram

`http://widget.websta.me/rss/n/USERNAME`

will get a user's feed.

## And the Bad

### Facebook

Nope. No RSS. Nothing to see here.

### Twitter

[Not
anymore](https://www.seroundtable.com/twitter-rss-depreciated-16973.html).

### Google+

There never was one.

## Footnotes

There is a small software, rss2email[^2] that can parse RSS feeds and
convert the entries to e-mails; I'm still using it, and it's great. No
missed posts, no looking around for updates, just new messages in my
Inbox. *Also, 2.70 works better for me than 2.71.*

[^1]: <https://en.wikipedia.org/wiki/Rss>

[^2]: <http://www.allthingsrss.com/rss2email/download/>