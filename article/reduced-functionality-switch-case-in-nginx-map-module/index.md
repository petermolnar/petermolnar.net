---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120323000158/http://petermolnar.eu:80/linux-tech-coding/reduced-functionality-switch-case-in-nginx-map-module
published: '2012-02-11T06:55:33+00:00'
summary: There's no switch-case in nginx, though map is available for similar
    but reduced functionality cases.
tags:
- linux
title: 'reduced functionality switch - case in nginx: map module'

---

<ins datetime="2012-12-20T13:17:48+00:00">
</ins>
**Update**

There's a WordPress Plugin, called Nginx ( nginx-helper )[^1] which can
create the required map for WordPress multisite.

I was searching for a switch-case possibility in nginx without success.
Although a module named "map" can do something similar but only for
setting a variable.

Like the following:

```apache
map $host $dirnum {
    default        0;
    domain1.com    1;
    domain2.com    2;
}
```

This has to be placed *outside* the `server` part but inside `http`.

Afterwards the variable becomes useable, in, for example rewrite rules:

```apache
# if domain is mapped
if ($dirnum != 0 ) {
    rewrite ^/files/(.*)$ /wp-content/blogs.dir/$dirnum/files/$1 last;
}
# otherwise fall back to "normal" rule
if ($dirnum = 0 ) {
    rewrite ^(.*)/files/(.*)$ /wp-includes/ms-files.php?file=$2 last;
}
```

[^1]: <http://wordpress.org/extend/plugins/nginx-helper/>