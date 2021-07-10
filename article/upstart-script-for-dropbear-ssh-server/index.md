---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20131129155550/http://petermolnar.eu:80/linux-tech-coding/upstart-script-for-dropbear-ssh-server/
published: '2013-01-10T11:22:07+00:00'
summary: A very sleak upstart job script for dropbear.
tags:
- linux
title: Upstart script for Dropbear SSH server

---

I've replaced the classic OpenSSH server with Dropbear: it's basically
the same speed, lot less on memory and I don't use most of the functions
of OpenSSH.

Since I'm on Ubuntu 12.04, the elengant way would be to use Upstart (
also, the respawn is very useful ), so here is my script in
`/etc/init/dropbear.conf`:

```bash

description "Dropbear SSH server"
author "Peter Molnar <hello @petermolnar.eu>"

start on filesystem or runlevel [2345]
stop on runlevel [!2345]

respawn
respawn limit 10 5
umask 022

env DROPBEAR_PORT=2222
env DROPBEAR_RSAKEY=/etc/dropbear/dropbear_rsa_host_key
env DROPBEAR_DSSKEY=/etc/dropbear/dropbear_dss_host_key
env DROPBEAR_RECEIVE_WINDOW=65535

pre-start script
        test -x /usr/sbin/dropbear || { stop; exit 1; }
end script

expect daemon

exec /usr/sbin/dropbear -d $DROPBEAR_DSSKEY -r $DROPBEAR_RSAKEY -p $DROPBEAR_PORT -W $DROPBEAR_RECEIVE_WINDOW
```