---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125216/https://petermolnar.net/avahi-nfs-zfs/
published: '2017-05-24T08:00:00+00:00'
summary: How to announce ZFS NFS shares on your home network for clients to
    automatically discover them.
tags:
- linux
title: ZFS NFS shares with avahi zeroconf

---

# ZFS and NFS

ZFS[^1] is an exceptional filesystem but some parts are documented with
a certain haze over them. For me, one of these was how to specify the
network you want to share it with, but it turned out to be easy and
straightforward, much like most things with ZFS.

Let's say we want to share a dataset, named `media`, sitting in our
`rpool`.

### Install NFS server

``` {.bash}
apt install nfs-kernel-server
```

### Share the relevant ZFS datasets

``` {.bash}
zfs set sharenfs="rw=@192.168.0.1/24,insecure" rpool/media
```

and restart the service:

``` {.bash}
systemctl restart nfs-kernel-server
```

This will create an insecure, read-write to world share on the media
dataset - consider putting it into read-only if that is needed.

## Avahi

The steps above are enough to share, but not to let clients auto
discovery it; for that, we need `avahi` and a configured avahi service.

### Install avahi

``` {.bash}
apt install avahi-daemon avahi-utils
```

### Create an avahi service for all NFS shares

To do that, here's a simple bash script:

``` {.bash}
#!/bin/bash

for export in $(exportfs | grep -vE "^\s" | awk '{print $1}'); do
# all hail the black magic of bash!
# 'tr' replaces all the / to _, then all the . to _ and in the end
# we replace the first occurance of _ - which had become a prefix
# so instead of /a/shared/nfs/path/, we get a_shared_nfs_path
avahifname=$(tr '/' '_'  <<< ${export} | tr '.' '_');
cat > /etc/avahi/services/${avahifname/_}.service << EOF
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">NFS ${export}</name>
  <service>
    <type>_nfs._tcp</type>
    <port>2049</port>
    <txt-record>path=${export}</txt-record>
  </service>
</service-group>
EOF
done
```

Reload avahi:

``` {.bash}
systemctl restart avahi-daemon
```

And you're good to go; the NFS shares should show up under Network in
your Ubuntu/Mint/etc.

[^1]: <http://zfsonlinux.org/>