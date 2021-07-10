---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120801221957/http://petermolnar.eu/linux-tech-coding/owncloud-finally-a-working-webdav-server-in-php/
published: '2011-12-20T09:14:47+00:00'
redirect:
- webdav-server-in-php
summary: 'At last: turn your own server into your private cloud, interfacing
    any webDAV or web-browser capable client - and you only need a webserver
    with PHP!'
tags:
- linux
title: 'owncloud: finally a working webDAV server in PHP'

---

Finally a good implementation of webDAV has arrived: ownCloud 2[^1].
This little marvell turns your own server into a common interface for
any kind of computer capable of connecting to webDAV - and because
webDAV uses http ports, it may go through nearly from every location ;)

An unfortunate bug is the only thing that could be an issue: during the
install, if the `open_basedir` is in effect and you whished not to uses
the system-wide tmp dir, owncloud uses `sys_get_tmp_dir`, and the
install will fail with the following:

```php
MDB2_Schema Error: schema parse error: Parser error:
```

In order to get rid of it either place `:/tmp` at the end of the
`open_basedir` directory, or replace the `sys_get_tmp_dir()` function
call at line \#247 in lib/db.php on the owncloud directory.

You can find a brief ( or more likely quick-and-dirty ) install guide
for owncloud 2 at webupd8.org blog[^2].

I'd like to add, that it works like a charm even with nginx and php-fpm.

No words can describe how happy I am that it does not need anything more
than a webserver with PHP support. And it is not just for file sync,
it's capable of calendar, contants and music sharing as well!

[^1]: <http://owncloud.org/>

[^2]: <http://www.webupd8.org/2011/10/owncloud-2-your-personal-cloud-server.html>