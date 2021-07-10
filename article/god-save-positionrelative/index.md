---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111116135020/http://petermolnar.eu:80/sysadmin-blog/god-save-positionrelative/
published: '2011-09-13T07:36:13+00:00'
summary: How to fix Internet Explorer 8 rotation opacity bug
tags:
- CSS
title: God save position:relative

---

I've been searching for a very nasty bug that hits all versions of IE up
to 8 in CSS.

Basically the bug is the following: there's a div (\#inner) placed
inside an other (\#container). If I give opacity to the inner element in
IE8, the font color of the inner div (\#inner) will become the same as
the background-color of the outer (\#container) element.

The solution was the same for the infamous anti-aliasing bug related to
transparency: add `position:relative` to all elements, and thus: all
bugs are fixed.

If you use

```css
filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);
-ms-filter: "progid:DXImageTransform.Microsoft.BasicImage(rotation=3)";
```

you need to add a background image to make IE render the font correctly.