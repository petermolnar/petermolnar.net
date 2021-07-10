---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20200209085138/https://petermolnar.net/freenas-domoticz-zigbee-zwave-rflink/
published: '2020-02-07T19:00:00+00:00'
summary: How to make an Aeotec Z-Wave Z-Stick, a CC2531 Zigbee2MQTT, and an
    RFLink work with a FreeNAS jail running Domoticz
tags:
- FreeNAS
title: Consistent USB device naming in a FreeNAS jail

---

My current home server is a FreeNAS[^1] with a bunch of jails and
plugins; one of these is Domoticz. While I barely do anything above
collecting sensor data with it, I still had to make it work with
RFLink[^2], Zigbee2MQTT[^3], and an Aeotec Z-Stick Gen 5[^4].

I'm not going into the installation of Domoticz on FreeNAS, there are
excellent tutorials on the iX Community forums:

-   \[HOWTO\] Domoticz and open-zwave in a FreeNAS 11 jail![^5]
-   Install script for Domoticz with open-zwave driver in iocage jail
    [^6]

Note: zigbee2mqtt is a node.js daemon; I'm using pm2[^7] to run it.

## iocage hooks

The `iocage` jail controller has some hooks that can run scripts on the
host for the jail. The two hooks needed in this case are the
`exec_poststart` and `exec_prestart` hooks. The prestart runs before the
jails is created; the post start runs once the jail filesystem is up,
but nothing is started yet.

My ZFS dataset for the iocage is called `server`. Modify the paths
according to that, and create the `bin` directory on it.

`/mnt/server/bin/domoticz-prestart.sh`

```bash
#!/bin/bash

# add devfs rules to allow USB devices to be seen from within domoticz
if ! grep -q "devfsrules_jail=5" /etc/devfs.rules; then
    cat <<"EOF" >>  /etc/devfs.rules

[devfsrules_jail=5]
add include $devfsrules_hide_all
add include $devfsrules_unhide_basic
add include $devfsrules_unhide_login
add path zfs unhide
add path 'tty*' unhide
add path 'ugen*' unhide
add path 'cu*' unhide
add path 'usb/*' unhide
EOF
    /usr/sbin/service devfs restart
fi
```

`/mnt/server/bin/domoticz-poststart.sh`

```bash
#!/bin/bash

function get_tty () {
    local vendor="${1}"
    local product="${2}"
    # return the tty{} value, eg; U2
    sysctl dev.umodem | grep "vendor=${vendor} product=${product}" | sed -r 's/.*ttyname=([^\s]+) .*/\1/'
}

function create_symlink () {
    local source="${1}"
    # failsafe
    if [ "${source}" == 'tty' ]; then return; fi
    local target="/mnt/server/iocage/jails/domoticz/root/dev/${2}"
    if [ -e "${target}" ]; then rm -f "${target}"; fi
    ln -s "${source}" "${target}"
}

# rflink is an arduino mega
create_symlink "tty$(get_tty '0x2341' '0x0010')" "ttyUrflink"
# zigbee is a Texas Instrument CC2531
create_symlink "tty$(get_tty '0x0451' '0x16a8')" "ttyUzigbee"
# zwave is a Z-Stick Gen 5
# note: it needs the 'cua' device in domoticz, not the tty device
create_symlink "cua$(get_tty '0x0658' '0x0200')" "cuaUzwave"
```

**Note: these commands are meant to be ran *after* domoticz was
successfully installed in a jail named `domoticz`**

```bash
chmod 0755 /mnt/server/bin/domoticz-poststart.sh
chmod 0755 /mnt/server/bin/domoticz-prestart.sh
iocage stop domoticz
iocage set exec_poststart=/mnt/server/bin/domoticz-poststart.sh domoticz
iocage set exec_prestart=/mnt/server/bin/domoticz-prestart.sh domoticz
iocage set devfs_ruleset=5 domoticz
iocage start domoticz
```

## Hardware configurations inside domoticz

### Z-wave

![Domoticz hardware configuration for aeotec z-wave stick with path of
cuaUzwave](domoticz-freenas-zwave.png)

### RFLink

![Domoticz hardware configuration for rflink with path of
ttyUrflink](domoticz-freenas-rflink.png)

### zigbee

![Domoticz hardware configuration for
zigbee2mqtt](domoticz-freenas-zigbee.png)

`/opt/zigbee2mqtt/data/configuration.yaml`

```yaml
homeassistant: false
permit_join: false
mqtt:
  base_topic: zigbee2mqtt
  server: 'mqtt://localhost'
serial:
  port: /dev/ttyUzigbee
advanced:
  channel: 25
```

## Caveats

There's a weird behaviour of the CC2531 for which I haven't found a
reason or a fix for: after being plugged in, on the very first start the
tty interface shuts down and gets reassigned to another position, eg.
from `ttyU0` it becomes `ttyU4`. I've tried using `devd` rules to
trigger a restart of domoticz or a recreation of the symlink, but so
far, none of them provided good results. I'm not completely happy with
the zigbee2mqtt project anyway, because it requires a separate node.js
daemon to run in the background - one more moving element -, therefore
I'm not too keen to find a fix. Instead l'll probably look into
alternatives, like the dresden elektronik ConBee[^8]

[^1]: <https://www.freenas.org/>

[^2]: <http://rflink.nl/blog2/>

[^3]: <https://www.zigbee2mqtt.io>

[^4]: <https://aeotec.com/z-wave-usb-stick/>

[^5]: <https://www.ixsystems.com/community/threads/howto-domoticz-and-open-zwave-in-a-freenas-11-jail.61030/>

[^6]: <https://www.ixsystems.com/community/threads/install-script-for-domoticz-with-open-zwave-driver-in-iocage-jail.62254/>

[^7]: <https://pm2.keymetrics.io/>

[^8]: <https://www.amazon.co.uk/dp/B07PZ7ZHG5/>