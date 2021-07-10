---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120204012301/http://petermolnar.eu:80/linux-tech-coding/vertically-and-horizontally-fluid-css-layout-with-height-100
published: '2011-11-14T09:15:25+00:00'
summary: Totally fluid layout both vertically & horizontally with pure CSS,
    with IE6 (!) compatibility.
tags:
- CSS
title: Vertically and horizontally fluid CSS layout with height 100%

---

I've finally managed to make a working layout with not fixed header and
footer but with vertically 100% layout.

First of all, reset the CSS ( from Eric Meyer[^1] ):

```css
/* http://meyerweb.com/eric/tools/css/reset/
v2.0 | 20110126
License: none (public domain)
*/

html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
margin: 0;
padding: 0;
border: 0;
font-size: 100%;
font: inherit;
vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure,
footer, header, hgroup, menu, nav, section {
display: block;
}
body {
line-height: 1;
}
ol, ul {
list-style: none;
}
blockquote, q {
quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
content: '';
content: none;
}
table {
border-collapse: collapse;
border-spacing: 0;
}
```

The base layout for this:

```html
<div id="container"></div>
```

```css
html {
    height: 100%;
}

body {
    padding: 0;
    margin: 0;
    height: 100%;
}

#container {
    position:relative;
    z-index:1;
    width:100%;
    height:100%;
    margin-left: auto;
    margin-right:auto;
    overflow:hidden;
}

#header,
#footer {
    position:absolute;
    left:0;
    z-index:2;
    width:100%;
    height:1.6em;
    overflow:hidden;
}

#header {
    top:0;
}

#footer {
    bottom:0;
}

#content {
    position:absolute;
    bottom:0;
    top:0;
    right:0;
    left:0;
    z-index:10;
    width: 100%;
    height:auto;
    margin-top:1.6em;
    margin-bottom:1.6em;
    overflow:hidden;
}

#content-text {
    position:relative;
    width:100%;
    height:100%;
    margin-left: auto;
    margin-right:auto;
    overflow:auto;
}
```

And that's all. Notice the same values in the `margin` of `content` the
the height of `footer` and `header`.

[^1]: <http://meyerweb.com/eric/tools/css/reset/>