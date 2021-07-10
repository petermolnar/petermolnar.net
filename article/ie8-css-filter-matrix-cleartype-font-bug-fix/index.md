---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120311023159/http://petermolnar.eu:80/linux-tech-coding/ie8-css-filter-matrix-cleartype-font-bug-fix
published: '2012-01-10T10:05:50+00:00'
summary: Really cross-browser CSS opacity or rotation with anti-aliasing even
    on IE? You can do it.
tags:
- CSS
title: Cross-browser CSS opacity and rotation with ClearType IE font render
    bug fixed

---

A long long time ago Microsoft[^1] was an innovative company. They
created Internet Explorer 5.5 and 6, two browsers that brought lots of
functions and solutions with immense capabilities. For example, the
much-hyped @font-face[^2] was already introduced in IE6 in 2001! *The
only problem was that just like all global companies, Microsoft used
it's own solution for font files, named eot[^3], one of the most ugly
file formats I've ever seen.*

Years passed and new functions emerged in the world of CSS: opacity,
transforms, text-shadow, etc. Microsoft refused to make these into IE8,
saying the whole CSS3 standard is not complete yet and they will not
implement fractions.

To be honest, this is nonsense, when the even mammoth companies have
started to develop in scrum[^4]), or at least in some agile[^5] way:
small, but more often changes.

Poor web designers therefore had to stick with old technologies like
tables and images or do some really nasty solutions in JavaScript, and
so on. Although... all IEs from version 6 had an interesting option: the
filters[^6] and the CSS expressions[^7]. I'm only going to talk about
the first one, the second is basically JS expressions inside CSS, a bit
similar to today's - also hyped - media queries[^8].

Nearly all modern effects, like opacity, transform, gradient background
could be done in IE as well - but it comes with a price: you'll loose
anti-aliasing on the fonts, namely the ClearType function. Or... ... you
can make some "hacks".

## Cross-browser CSS opacity with ClearType font even in IE6

```css

    /* W3C CSS3 standard */
    opacity: 0.6;
    /* Firefox */
    -moz-opacity: 0.6;
    /* webkit (Chrome, Safari, mobile browsers, etc) */
    -webkit-opacity: 0.6;
    /* IE6 & 7 */
    filter:alpha(opacity=60);
    /* IE8 */
    -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=60)";
    position:relative;

    /* Konqueror: so small market share, you could even left it out  */
    -khtml-opacity: 0.6;
```

The vital point: add `position:relative;`.

IE8 - without position:relative ![IE CSS opacity ugly
font](ie8-css-screenshot-8.png)

IE8 - with position:relative ![IE CSS opacity nice
font](ie8-css-screenshot-10.png)

## Cross-browser CSS rotation transform with correctly rendered ClearType font

```css
{

transform: translateX(-100%) rotate(-90deg);
transform-origin: right top;
/* Firefox */
-moz-transform: translateX(-100%) rotate(-90deg);
-moz-transform-origin: right top;
/* webkit (Chrome, Safari, mobile browsers, etc) */
 -webkit-transform: translateX(-100%) rotate(-90deg);
 -webkit-transform-origin: right top;
/* Opera */
-o-transform: translateX(-100%) rotate(-90deg);
-o-transform-origin: right top;
/* IE>=9 */
-ms-transform: translateX(-100%) rotate(-90deg);
-ms-transform-origin: right top;
/* IE8 */
-ms-filter: "progid:DXImageTransform.Microsoft.BasicImage(rotation=3)";
/* IE&lt;8 */
filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);

background-image:url('some_image.jpg');
background-repeat:repeat;
}
```

The vital point: add a background image.

IE8 - without background image ![IE8 font render without background
image](ie8-css-screenshot-4.png)

IE8 - with background image ![IE8 font render with background
image](ie8-css-screenshot-2.png)

[^1]: <http://www.microsoft.com>

[^2]: <http://www.css3.info/preview/web-fonts-with-font-face/>

[^3]: <http://www.w3.org/Submission/EOT/>

[^4]: <http://en.wikipedia.org/wiki/Scrum_(development>

[^5]: <http://en.wikipedia.org/wiki/Agile_software_development>

[^6]: <http://reference.sitepoint.com/css/filter>

[^7]: <http://gadgetopia.com/post/2774>

[^8]: <http://www.w3.org/TR/css3-mediaqueries/>