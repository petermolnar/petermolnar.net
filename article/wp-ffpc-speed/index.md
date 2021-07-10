---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20160709135524/https://petermolnar.eu/wp-ffpc-speed/
published: '2014-04-28T11:03:33+00:00'
summary: WP-FFPC - speeding up your WordPress site at leas 9 times.
tags:
- WordPress
title: 'WP-FFPC: speed test'

---

I've made a little speed comparison to check how much difference my
cache plugin, WP-FFPC[^1] makes. I've run the test only a few times,
therefore the measurement is not as precise as it should be, it's just a
brief note.

I tested four setups:

1.  logged in request - in this case, WP-FFPC does not kick in
2.  APC  is set to be used as backend
3.  Memcached is set as backend, served directly from nginx
4.  Memcached is set as backend, served from PHP

One typical outcome: (not median, these are exact copies from a run
after running a few each and selecting typical a one )

                      No cache (ms)   APC (ms)   Memcached via nginx(ms)   Memcached via PHP (ms)
  ------------------- --------------- ---------- ------------------------- ------------------------
  Blocking            1.836           1.328      1.432                     0.570
  Proxy               0.298           0.904      0.905                     0.333
  Sending             3.674           0.277      0.855                     0.271
  Waiting             561.818         51.878     35.388                    33.005
  Receiving           0.649           0.550      26.487                    1.513
  Sum send+wait+rec   566.141         52.705     62.73                     34.789

A little explanation:

-   the "proxy" element is because I'm behind a proxy; it's irrelevant
    to this test
-   the sending has a very high difference with no cache, this is
    because of the cookie size

But the simple conclusion: **WP-FFPC speeds up your site AT LEAST 9
times no matter which backend engine you're using.**

The ranking:

-   memcached through PHP
-   APC
-   memcached through nginx

nginx is not expected to be slower that PHP. It's probably an issue with
my nginx setup or an error in the memcached plugin version I'm using
with nginx. I will look into this.

Any tests either confirming or questioning my outputs are welcome!

[^1]: <http://wordpress.org/plugins/wp-ffpc/>