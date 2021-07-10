---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20150203041116/https://petermolnar.eu/linux-tech-coding/solution-for-gtk-warning-error-loading-theme-icon/
published: '2012-11-24T20:31:14+00:00'
summary: How to fix Gtk fatal error of PNG images.
tags:
- linux desktop
title: 'Solution for: Gtk-WARNING **: Error loading theme icon'

---

I'm still running RawTherapee 2.4.1[^1] instead of version 3 or 4. This
is simply because I find it a lot more easy to use and I still like the
the more aggressive noise reduction in it.

After upgrading to Mint 14, I've received errors when trying to start
it, errors like:
`Gtk-WARNING **: Error loading theme icon 'text-x-generic' for stock: Fatal error reading PNG image file: Invalid IHDR data`

The solution is quite simple, though not really trivial: update icon
cache for fallback icon sets. This will do ( run it as root ):

```bash
for i in /usr/share/icons/*; do sudo gtk-update-icon-cache $i; done
```

[^1]: <http://archive.getdeb.net/ubuntu/pool/apps/r/rawtherapee/rawtherapee_2.4.1-1~getdeb1_amd64.deb>