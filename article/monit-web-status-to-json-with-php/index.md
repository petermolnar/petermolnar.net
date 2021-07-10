---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20130616182821/http://petermolnar.eu:80/linux-tech-coding/monit-web-status-to-json-with-php
published: '2013-06-13T13:29:29+00:00'
summary: Show monit status in JSON for other software to understand.
tags:
- linux
title: Monit web status to JSON with PHP

---

Monit[^1]'s web interface is pretty easy to read for a human, but
incredibly ugly to parse. In order to show a machine-readable output, it
needs to be parsed to JSON.

You'll need PHP Simple HTML DOM Parser[^2] for it, and this script to
show the JSON output: `monit2json.php`

```php
<?php

include ('simple_html_dom.php');
$html = file_get_html('http://127.0.0.1:2812/');

$contents = array();

$cntr_table = 0;
foreach ( $html->find('table[id=header-row]') as $table ) {

    $cntr_tr = 0;
    foreach ( $table->find('tr') as $tr ) {

        $cntr_td = 0;
        foreach ( $tr->find('th') as $th ) {
            $columns [ $cntr_td ] = strip_tags ( $th->innertext );
            $cntr_td++;
        }

        $cntr_td = 0;
        foreach ( $tr->find('td') as $td ) {
            $contents[ $cntr_table ][ $cntr_tr ][ $columns[ $cntr_td ] ] =  str_replace( '&nbsp;', ' ', strip_tags( $td->innertext ) );
            $cntr_td++;
        }

        $cntr_tr++;
    }

    $cntr_table++;
}

foreach ( $contents as $table  ) {
    foreach  ( $table as $process ) {
        if ( isset ( $process['Process'] ) ) {
            $proc = $process['Process'];
            unset ( $process['Process'] );

            $out[ $proc ] = $process;
        }
    }
}

$out = json_encode ( $out, JSON_PRETTY_PRINT );
echo $out;
```

Result:

```json
{
    "sshd": {
        "Status": "Running",
        "Uptime": "2d 20h 1m ",
        "CPU Total": "0.0%",
        "Memory Total": "5.6% [28904 kB]"
    },
    "rsyslogd": {
        "Status": "Running",
        "Uptime": "49d 4h 50m ",
        "CPU Total": "0.0%",
        "Memory Total": "1.8% [9344 kB]"
    },
    "postfix": {
        "Status": "Running",
        "Uptime": "21d 21h 45m ",
        "CPU Total": "0.0%",
        "Memory Total": "4.3% [22236 kB]"
    },
    "php5-fpm": {
        "Status": "Running",
        "Uptime": "1h 0m ",
        "CPU Total": "0.0%",
        "Memory Total": "29.1% [147824 kB]"
    },
    "nginx": {
        "Status": "Running",
        "Uptime": "51m ",
        "CPU Total": "0.0%",
        "Memory Total": "2.7% [13816 kB]"
    },
    "mysqld": {
        "Status": "Running",
        "Uptime": "7d 21h 59m ",
        "CPU Total": "0.0%",
        "Memory Total": "16.9% [86180 kB]"
    },
    "memcached": {
        "Status": "Running",
        "Uptime": "1d 3h 40m ",
        "CPU Total": "0.0%",
        "Memory Total": "5.7% [29080 kB]"
    },
    "fail2ban": {
        "Status": "Running",
        "Uptime": "21d 21h 37m ",
        "CPU Total": "0.0%",
        "Memory Total": "0.8% [4536 kB]"
    },
    "dspam": {
        "Status": "Running",
        "Uptime": "56d 21h 28m ",
        "CPU Total": "0.0%",
        "Memory Total": "4.5% [22936 kB]"
    },
    "dropbear": {
        "Status": "Running",
        "Uptime": "79d 4h 8m ",
        "CPU Total": "0.0%",
        "Memory Total": "0.0% [180 kB]"
    },
    "dovecot": {
        "Status": "Running",
        "Uptime": "21d 21h 45m ",
        "CPU Total": "0.0%",
        "Memory Total": "9.3% [47364 kB]"
    },
    "crond": {
        "Status": "Running",
        "Uptime": "47d 23h 59m ",
        "CPU Total": "0.0%",
        "Memory Total": "0.0% [224 kB]"
    },
    "collectd": {
        "Status": "Running",
        "Uptime": "3d 1h 20m ",
        "CPU Total": "0.2%",
        "Memory Total": "1.1% [5596 kB]"
    }
}
```

[^1]: <http://mmonit.com/monit/>

[^2]: <http://simplehtmldom.sourceforge.net/>