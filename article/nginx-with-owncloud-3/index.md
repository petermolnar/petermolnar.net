---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120405231439/http://petermolnar.eu:80/linux-tech-coding/nginx-with-owncloud-3
published: '2012-02-02T09:56:14+00:00'
summary: nginx is one of the best webservers out there, owncloud make cloud
    computing secure using your very own service, but putting them together
    really gave me a headache.
tags:
- linux
title: nginx with ownCloud 3

---

Yesterday I've spent hours and hours trying to make the freshly released
owncloud 3[^1] play nice with nginx.

The web interface was running correctly, but any kind of DAV access
failed. I've tried everything but the closest I've got was an xml error
from the Sabre DAV server of the project.

Until I've found a mail archieve from a KDE list from last year
October[^2] saying I need on more fast CGI parameter than ususally.

So to solve the problem add:

```nginx
fastcgi_split_path_info ^(.+.php)(/.*)$;
```

into your server config's fastcgi params, and suddenly the sky becomes
bluer the bird starts singing and you can start playing with your own
cloud.

Thank you very much, Weng Xuetian!

[^1]: <http://owncloud.org/>

[^2]: <http://mail.kde.org/pipermail/owncloud/2011-October/001111.html>