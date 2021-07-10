---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20170630120947/https://petermolnar.net/replacing-baikal-with-radicale-for-carrdav-and-caldav/
published: '2017-01-26T17:30:00+00:00'
summary: 'I was becoming unhappy with Baïkal, my contact and calendar sync
    server: a growing number of clients was unable to use it, so I started
    to look for alternatives. This time I wanted something plain text based.'
tags:
- linux
title: Replacing Baïkal with Radicale
updated: '2019-07-16T18:00:00+01:00'

---

**Note: this entry has been updated at 2019-07-16 with for Radicale 2.
Apart from the radicale config itself, nothing changed. The original
configuration for radicale v1 is at the bottom of this page.**

Probably one of the most attacked - as in argument - pages on the
indieweb wiki[^1] is the database-antipattern entry[^2]; it's one of
those with which nearly all of us disagrees when they first come in
contact with it.

Let me quote it:

> The **database antipattern** is the use of a database for **primary
> long-term storage** of posts and other personal content (like on an
> indieweb site), and is an anti-pattern due to the additional
> maintenance costs, uninspectability, platform-dependence, and
> long-term fragility of databases and their storage files, as
> documented with specific examples below.

The important part is in bold: database as primary, long term storage.
For syncing my contacts I've been using:

-   Baïkal[^3] as server
-   DAVDroid[^4] on my phone
-   Evolution[^5] and Thunderbird[^6] on desktop
-   Rainloop[^7] as webmail

All of these can sync contacts, some calendars as well, all through the
abomination called DAV, but all of them are storing these in some kind
of database, mostly SQLite. SQLite is an ideal storage - for cache and
for fast in-app lookups, but not for long term. If you've ever tried to
import dumps from MySQL to SQLite or the other way around it quickly
becomes visible why that antipattern entry was written.

So I decided to look for an alternative which would store my contacts in
actual vcf and ics files. For the record, Baïkal has the actual VCF text
in the database, so it's not much more than a regular file storage.

A quick search revealed a Python implementation, called Radicale[^8].
Although it mentions that it has a backend, called *multifilesystem*,
which uses per contact files, unfortunately I could not get that one
running. So I'm running it with *filesystem* backend, which uses a
single, merged file per resource.

It wasn't hard to get it running, and the documentation works fine as
well, so if you want something that stores your contacts and calendars
in plain text (well, ICS and VCF, not the most readable format, but it's
text), radicale is out there, use it.

`/etc/radicale/config`

```ini
[server]
hosts = 127.0.0.1:5232
daemon = True

[encoding]
request = utf-8
stock = utf-8

[auth]
type = htpasswd
htpasswd_filename = /etc/radicale/users

[rights]
type = owner_only
file = /etc/radicale/rights

[storage]
type = multifilesystem
filesystem_folder = /var/lib/radicale/collections

[web]

[logging]
config = /etc/radicale/logging

[headers]
```

`/etc/radicale/logging`

```ini
[loggers]
keys = root

[handlers]
keys = console,file

[formatters]
keys = simple,full

[logger_root]
level = WARNING
handlers = console,file

[handler_console]
class = StreamHandler
level = INFO
args = (sys.stdout,)
formatter = simple

[handler_file]
class = FileHandler
args = ('/home/radicale/log',)
formatter = full

[formatter_simple]
format = %(message)s

[formatter_full]
format = %(asctime)s - %(levelname)s: %(message)s
```

`radicale_nginx.conf`

```apache
location /radicale {
    try_files $uri @radicale;
}

location /.well-known/carddav {
    try_files $uri @radicale;
}

location /.well-known/caldav {
    try_files $uri @radicale;
}

location @radicale {
    proxy_set_header Proxy "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Proxy-Connection "";
    proxy_ignore_client_abort on;
    proxy_pass http://127.0.0.1:5232;
}
```

## Optional: authenticate via Dovecot

In my tiny server setup the source for authentication is Dovecot. It
might be a bin unusual, but works very well, and is an extremely simple
solution.

Radicale 1 had a built-in IMAP authentication module, but this is gone
with version 2. To overcome this, I added:

```bash
sudo apt install python3-pip
sudo pip3 install radicale-dovecot-auth
```

and replaced the `auth` section in the radicale config as:

```ini
[auth]

type = radicale_dovecot_auth
auth_socket = /var/run/radicale/auth
auth_host = 127.0.0.1
auth_port = 9993
```

This needs support from dovecot as well, so in the dovecot
configuration, inside the `service auth` block, as shown:

    service auth {
        user = root

        # Radicale
        unix_listener /var/run/radicale/auth {
            mode = 0660
            user = radicale
            group = radicale
        }
    }

And things happen magically.

## DNS entries for CalDAV and CardDAV

If you want certain services, such as Gnome Evolution, to be able to
detect features for an email account, adding these DNS entries help:

    _caldavs._tcp.petermolnar.net. 1800 IN SRV 0 0 443 dav.petermolnar.net.
    _carddavs._tcp.petermolnar.net. 1800 IN SRV 0 0 443 dav.petermolnar.net.
    dav.petermolnar.net. 1800 IN A 176.9.91.49

## Historical: Radicale 1 config

`radicale.conf`

```ini
[server]
hosts = 127.0.0.1:5232
daemon = True
pid = /tmp/radicale.pid
ssl = False
base_prefix = /radicale/
realm = Radicale - Password Required

[encoding]
request = utf-8
stock = utf-8

[well-known]
caldav = '/home/radicale/%(user)s/caldav/'
carddav = '/home/radicale/%(user)s/carddav/'

[auth]
type = IMAP

imap_hostname = my.imap.server
imap_port = 993
imap_ssl = True

[git]
committer = Peter Molnar <hello@petermolnar.eu>

[rights]
type = owner_only

[storage]
type = filesystem

filesystem_folder = /home/radicale/db

[logging]
config = /home/radicale/radicale_logging.conf


[headers]
#Access-Control-Allow-Origin = *
```

[^1]: <http://indieweb.org/>

[^2]: <http://indieweb.org/database-antipattern>

[^3]: <http://sabre.io/baikal/>

[^4]: <https://davdroid.bitfire.at/>

[^5]: <https://wiki.gnome.org/Apps/Evolution/>

[^6]: <https://www.mozilla.org/en-GB/thunderbird/>

[^7]: <http://www.rainloop.net/>

[^8]: <http://radicale.org/>