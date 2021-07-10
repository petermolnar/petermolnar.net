---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20150523170706/https://petermolnar.eu/linux-tech-coding/how-block-access-to-original-jpg-files-on-wordpress-with-nginx/
published: '2015-03-23T14:28:26+00:00'
summary: Block access to non-resized JPG files. Use it with caution.
tags:
- WordPress
title: How block access to original JPG files on WordPress with nginx

---

**WARNING**: this will block access to **all** original JPGs, not only
the large, resized ones. Use this with caution.

```nginx
location ~ "^/files/(?:(?!.*-[0-9]{2,4}x[0-9]{2,4}).)*\.jpe?g$" {
    rewrite ^/files(.*) /wp-content/files$1 break;
allow 127.0.0.1;
    deny all;
}

location ~ "^/(?:(?!cache).*?)/(?:(?!.*-[0-9]{2,4}x[0-9]{2,4}).)*\.jpe?g$" {
allow 127.0.0.1;
allow 192.168.42.11;
deny all;
}
```