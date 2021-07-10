---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20160810120256/https://petermolnar.eu/reducing_js/
published: '2015-12-08T10:36:38+00:00'
summary: Requiring JS to open a menu or to resize images to the viewport is
    not cool.
tags:
- WordPress
title: Reducing Javascript on petermolnar.eu

---

## Why? JS is cool, ya' know. It's what the cool kids do.

A long time ago a phrase emerged in some web development circles: the
semantic and accessible web. This included a theory that in every single
case you should first do a working page in HTML only. No CSS, no
Javascript, to make sure that everyone - including screen readers - can
access the site correctly. *Including everything, so comments, forms,
everything. Yes, it was, and still is, possible, but it won't be fancy.*

As the years passed, everything got 'smarter'; and while Google can now
index most of the JavaScript content[^1], JS got a little overused, even
for things like in-browser templating[^2]. This, in my opinion, should
not happen, as I share the opinion of @tantek: js;dr[^3].

## Replaced: the menu

Update then I got rid of the animated menu completely; it's pure HTML
and responsive CSS now. I'm only leaving the reference to the advanced
checkbox hack from Tim Pietrusky[^4] now, because it's still brilliant.

## Replaced: limiting image width & height

Since I have photos on the site, I prefer relatively nice quality for
them. The problem is that these are usually larger than the viewport, so
there has to be a limitation to fit the window.

### Original: JavaScript

```javascript
window.addEventListener('load', function() {
    var vh = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)

    var adaptimg = document.getElementsByClassName('adaptimg');
    [].forEach.call(adaptimg, function (el) {
        //var w = el.offsetWidth;
        var h = el.offsetHeight;

        if ( h > vh ) {
            el.style.height = vh + 'px';
            el.style.width = 'auto';
        }
    });
});
```

### Replacement: native CSS

There are some interesting CSS units which can now be considered
supported: vw, vh, vmin, vmax[^5].

```css
.adaptimg {
  position: relative;
  display: block;
  max-height: 100vh;
  max-width: 98%;
  width: auto;
  height: auto;
  margin: 0.6em auto 0.6em auto;
  padding: 0;
}
```

## The special cases are here to stay

~~Sadly, srcset[^6] is not supported by many, so Picturefill[^7] is here
to stay for now.~~ I've added a larger default image and got rid of
Picturefill. The older machines, which would not run new enough browsers
to support srcset simple won't have large enough resolution for this to
be an issue - with the exception of the holy grail of the ThinkPads, the
ThinkPad R50p[^8]

~~Syntax highlighting is a tricky thing, and so far, for my greatest
surprise, the best, most lightweight and fastest one I've found is a JS
implementation, called prism JS[^9].~~

I've switched to Pandoc[^10] to generate HTML from Markdown from the
previous Parsedown[^11]. While Parsedown is 1-2 magnitude faster, Pandoc
can generate **anything** from Markdown, and it has built-in syntax
highlighting.

The third thing to stay is the JS for WP-Slimstat[^12], because I'm
curious on who visits my site, and the server logs don't give me enough
information.

Thankfully, these are all loaded from my own domain. I'm avoiding
including JS from 3rd party, even if it's coming from Google, for two
main reasons:

-   they are a security risk[^13]
-   some parts of the world my have the origin block - like China vs
    Google -, thus you're crippling your own site for a few billion
    potential visitors

Also, stick to vanilla JS[^14]. You don't need jQuery anymore[^15] - or
at least you might not need jQuery anymore[^16].

## More to read

-   CSS3 Instagram filters[^17]
-   CSS3 animations and transitions[^18]

[^1]: <http://www.centrical.com/test/google-json-ld-and-javascript-crawling-and-indexing-test.html>

[^2]: <http://underscorejs.org/>

[^3]: <http://tantek.com/2015/069/t1/js-dr-javascript-required-dead>

[^4]: <http://timpietrusky.com/advanced-checkbox-hack>

[^5]: <http://caniuse.com/#search=vh>

[^6]: <http://www.w3.org/html/wg/drafts/html/master/embedded-content.html#attr-img-srcset>

[^7]: <https://scottjehl.github.io/picturefill/>

[^8]: <http://www.thinkwiki.org/wiki/Category:R50p>

[^9]: <http://prismjs.com/>

[^10]: <http://pandoc.org/>

[^11]: <http://parsedown.org/>

[^12]: <https://wordpress.org/plugins/wp-slimstat/>

[^13]: <http://www.darkreading.com/application-security/third-party-code-fertile-ground-for-malware/a/d-id/1316656>

[^14]: <http://vanilla-js.com/>

[^15]: <http://blog.garstasio.com/you-dont-need-jquery/why-not/>

[^16]: <http://youmightnotneedjquery.com/>

[^17]: <http://designpieces.com/2014/09/instagram-filters-css3-effects/>

[^18]: <http://css3.bradshawenterprises.com/transitions/>