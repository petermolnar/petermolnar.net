---
author:
    email: mail@petermolnar.net
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20200609132549/https://petermolnar.net/article/less-features-cleaner-site/
published: '2020-06-01T08:30:00+01:00'
summary: Some years ago I decided to walk away from dynamic website in pursuit
    of something that feels a bit more, like the small web, and what's more
    fault tolerant for the future. Unfortunately my solution overgrew its
    promise so it was time for some reaping.
tags:
- internet
title: Refactoring my static generator

---

A few weeks ago I sat down in front of my site and realized: it's doing
too many things, the code is over 3500 lines of Python, and I feel lost
when I look at it. It was an organic growth, and happened somewhat like
this:

*Let's start simple: collect images, extract EXIF using exiftool[^1],
watermark them, if needed, resize them, if needed. Collect markdown
files, convert them to HTML with pandoc[^2] using microformat friendly
templates. Ah, wait I need categories. I also need pages. And feeds.
Multiple feeds, because I'm not going to choose sides, RSS, Atom, JSON,
hfeed. Let's make all of them! I'll even invent YAMLFeed[^3] for the
lulz. I need webmentions. Receive them, create comments before rendering
anything, then render, then sync, then send outgoing webmentions. Oh.
Don't send them every single time, just on change. I need to publish to
flickr, but I need to be able to backfill from brid.gy. Let's handle
gone content properly, also redirects nicely. Let's try JavaScript based
search. Or let's not, it's needs people to download the full index every
time, let's do PHP from Python templates instead. Google zombies are
doing JSON-LD, academics are doing Linked Data, let's do all that. Hell,
let's make an intermediate representation of all my content in JSON-LD
that is made from the Markdown files before it hit's the HTML templates!
In the meanwhile, why not auto-save my posts to archive.org? But what if
I already did it? Let's find the earliest version automagically! OK,
this is a bit slow now, let's start using async stuff. Let's syndicate
to fediverse via fed.brid.gy. I don't like my pagination logic, let's do
some categories flat: all on one page; others paginated by year. I want
to add something funky for IWC this year, I'll add a worldmap for photos
with location data. I see federated things are pinging `.well-known`
locations, let's generate data for them.*

I'm not certain if this is the whole list of features, but it's quite
clear it has overgrown it's original purpose. In my defense, some of
these functionalities were only meant to be learning experiences.

## DRY - don't repeat yourself

I started with the most painful point. The previous iteration had a
`source` directory for the content, with the unprocessed, original
files, a `nasg` for the code, and a `www` for the generated output. What
I should have done from the start it to have 1 and only 1 directory for
everything.

The main reasons for the original layout were to keep my original -
quite large - images safe on my own computer, copy only the resized and
potentially watermarked ones online. The other was to keep the code in
it's own repository, so it can be "Open Sourced". *Why the quotes:
because I've started to question what Open Source means to me and what
it is right now in the world, but this is for another day.*

The more I complicated this the more I realized all these disconnected
pieces are making the originally simple process more and more
convoluted. So I made certain decisions.

**My generator code is not going to live on Github any more. Instead,
it'll be in the root folder of my site content, which will also be the
root folder for the website. I'll generate everything in place.** I'll
move the original images to be hidden files and protect them via
webserver rules, like I did in the WordPress times. I'll place the
Python virtualenv in this directory as well.

With the move to a single directory structure I also moved away from the
weird path system I ended up with: direct uris for entries and
/category/ prefixes for categories. Now everything always is
/folder/subfolder/ etc, as it should have been from the start.

It needed some rewrite magic to have it done properly, but it should all
be fine now.

## Parsing should be stiff and intolerant

When I saved markdown files by hand, I wasn't paying too much attention
to, for example, dates. The Python library I used - arrow - parsed
nearly everything. This also applied to the comments, but the comments
were saved by my own code: missing or `null` authors, bad date formats,
etc.

With the refactoring I decided to ditch as many libraries as possible in
favour of Python's built in ones, and `datetime` suddenly wasn't happy.

I fixed all of them; some with scripts, others by hand. Than swapped to
a very strict parsing: if stuff is malformed, fail hard. Make me have to
fix it.

**No workarounds in the code, no clever hundreds of lines of fallbacks;
the source should be cleaned if there is an issue.**

## Not everything needs templating

In order to have a nice search, I had templated PHP files. Truth is:
it's not essential. Search is happy with a few lines of CSS and a "back
to petermolnar.net" button.

My fallback 404.php can now rely on looking up files itself. Previously
I had `removeduri.del` and `some-old-uri.url` files. The first were
empty files, with the deleted URIs in their names; the second contained
the URL to redirect to. Because of the `content` and `www` directory
setup, I had to parse these, collect them, and then insert in the PHP.
But now I had the files accessible from the PHP itself, meaning it can
look it up itself.

**This way both my `404.php` and my `search.php` became self-sufficient:
no more Python Jinja2 templates for PHP files.** \#\# Semantic HTML5 is
a joke, JSON-LD is a monster, and I have no need for either

Some elements in HTML5 are good, and were much needed. Personally I'm
very happy with `figure` and `figcaption`, `details` and `summary`, and
`time`.

I find`header`, `footer` , and `nav` a bit useless, but nothing tops the
`main`, `section`, `article` (and probably some other) mess. There's no
definitive way of using one or the other, so everyone is doing which
make sense to them[^4] - which is the opposite of a standard. Try to
figure out which definition goes for which (official definitions from
the "living" HTML standard):

> The X element represents a generic section of a document or
> application. The X , in this context, is a thematic grouping of
> content, typically with a heading.

> The Y element represents a complete, or self-contained, composition in
> a document, page, application, or site and that is, in principle,
> independently distributable or reusable, e.g. in syndication.

> The Z element represents the dominant contents of the document.

So I dropped most of it; especially because I have microformats[^5] v1
and v2 markup already, and that is an actual standard with obvious
guidelines.

Next ripe for reaping was JSON-LD. I got into the semantic web
possibilities because I was curios. I learnt a lot, including the fact
that I have no need for it.

The enforced vocabulary for JSON-LD, schema.org, is terrible to use.
Whenever you have a need for something that's not present already,
you're done for, and it'll probably pollute the structured data results,
because all the search engines, especially Google, are picky: they limit
the options plus they require properties. Examples everything MUST have
a photo! And and address! And a publisher! If you don't believe me, try
to make a resume with schema.org then check the opinion of the Google
Structured Data Testing Tool about it.

No, Google. Not everything has an image - see <http://textfiles.com>
Like it or not, a website doesn't need and address. The list goes on
forever.

**I'm going to stop feeding it, stop feeding all of them, stop playing
by their weird rules. HTML has `link` and `meta` elements, plus `rel=`
property, so it can already represent the minimum, which is enough.
Plus, again, there's microformats, and Google is still OK with
them[^6].**

Note: with structured data, in theory, one could pull in other
vocabularies to overcome problems like nonexistent properties in one,
but search engines are not real RDF parsers. Unless you're writing for
academic publishing tools that will do so, don't bother.

Update: 2020-07-08: it very much seems like Google is sunsetting their
microformats supports with their incredibly shitty new Rich Results
Test, that doesn't even tell you what's wrong[^7], so I'm putting RDFa
back.

## Pick your format, and pick just one

Between 2003 and 2007 some tragic mud-throwing (*mirror translated
Hungarian phrase, just because it's pretty visual*) was going on on the
web, over something ridiculously small: my XML is better, than your XML!
[^8].

When I first encountered with the whole "feed" idea itself, there was
only RSS, and for a very long time, I was happy with it. Then I read
opinions of people I listen to on how Atom is better.
<https://fed.brid.gy> is Atom only. Much later someone on the internet
popped the JSONFeed thought.

*When I first saw JSONFeed, I thought it's a joke. Turned out it's not,
because there are simpletons who honestly believe the world will be
better if things are JSON and not XML. It won't, it'll only result in
things like JSON-LD*

*In the heat of the moment, I coined the thought of YAMLFeed[^9],
strictly as a satire, but for a brief time I actually maintained a
YAMLFeed file as well Do not follow my example.*

And then I found myself serving them all. I had a `Category` class in
Python, that had `JSONFeed` and `XMLFeed`subclasses, which latter had
`AtomFeed` and `RSSFeed` subclasses, it used `FeedParser` to deal with
it, and so on... in short, I made a monster.

~~**I went back an RSS 2.0 feed and a h-feed.**~~ Update from
2021-05-22: I settled on Atom after learning a bit more about the
possibilities in it. It can still be made with the `lxml` library
directly. I still prefer the "RSS" acronym though.

## Closure

If you have a website in 2020, it's probably a hobby for you as well;
don't let anything change that.

It should never become a burden, any part of it. It did for me, and I
seriously considered firing up something like Microsoft FrontPage 98 to
start from the proverbial scratch, but managed to salvage it before
resulting to drastic measures.

Don't follow trends. Once a solution grows deep enough roots -
microformats, RSS, etc - it'll be around for a very long time.

Screw SEO. If you're like me, and you write for yourself, and, maybe,
for the small web[^10], don't bother trying to please an ever-changing
power play.

If you want to learn something new, be careful not to embed it too deep
as it may be a fast fading idea.

[^1]: <https://exiftool.org/>

[^2]: <https://pandoc.org/>

[^3]: <https://indieweb.org/YAMLFeed>

[^4]: <https://www.w3schools.com/html/html5_semantic_elements.asp>

[^5]: <http://microformats.org/>

[^6]: <https://aaronparecki.com/2016/12/17/8/owning-my-reviews#historical-recommendations>

[^7]: <https://webmasters.googleblog.com/2020/07/rich-results-test-out-of-beta.html>

[^8]: <https://indieweb.org/RSS_Atom_wars>

[^9]: <https://indieweb.org/YAMLFeed>

[^10]: <https://neustadt.fr/essays/the-small-web/>