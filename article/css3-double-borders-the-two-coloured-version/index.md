---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120413193502/http://petermolnar.eu:80/linux-tech-coding/css3-double-borders-the-two-coloured-version/
published: '2012-01-25T13:45:10+00:00'
summary: One element, two borders in different colours - (nearly) pure CSS3.
tags:
- CSS
title: CSS3 double borders - the two-coloured version

---

For a long-long while nasty hacks existed to achieve double bordered,
rounded corner elements, including pixel sized layouts with background
images, hardcore JavaScript playing with dynamic image-replacements, and
so on. CSS3 does so much for the poor designers it cannot be said in
word, so I'm going to show it.

You'd like to have the same double border that is surrounding this very
text? (Yes, you have to use a browser, not IE. That's still a crap.)

## CSS

```css
background-color:#444;
border:1px solid #666;
-moz-box-shadow: 0 0 2px #111;
-webkit-box-shadow: 0 0 2px #111;
box-shadow: 0 0 2px #111;
```

## Demo

<div style="text-align:center; margin-top: 1em;">
[this box has double
border!]{style="border:1px solid #666; -moz-box-shadow: 0 0 2px #111; -webkit-box-shadow: 0 0 2px #111; box-shadow: 0 0 2px #111; padding: 1em; display:inline-block;"}</div>