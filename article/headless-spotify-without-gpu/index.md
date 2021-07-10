---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20180901185436/https://petermolnar.net/headless-spotify-without-gpu/
published: '2017-09-19T18:00:00+01:00'
summary: Fine tunes and extras for Vivek Panyam's guide "How to build a headless
    Spotify Streaming box"
tags:
- Spotify
title: Headless Spotify Debian linux server fine tunes

---

I have a minor local collection of music files - these days I'm trying
to buy only from BandCamp[^1], given nobody else is offering FLAC - so I
found myself listening to Spotify more and more.

My home server used to have mpd[^2] running on it, which was later
replaced by mopidy[^3], because that has a Spotify plugin[^4]. While the
plugin is decent the Spotify API is very restricted and doesn't allow,
for example, radios. *I still want the last.fm radio algorythm back.
Their radio was completely different and was recalculated after each
track played, unlike Spotify, where the playlist of a track, album, or
artist gets boring very soon.*

So I started looking around what other ways are there to run Spotify on
a headless server and I came across Vivek Panyam's guide: "How to build
a headless Spotify Streaming box"[^5].

It's almost perfect, only a few things were missing.

## First run and config

In order to run Spotify on the server, but display it on your own host
do the following:

    ssh -C -X [my-username]@[my-server] /usr/bin/spotify --disable-gpu

This needs the option `X10Forwarding yes` enabled in
`/etc/ssh/sshd_config` on the server.

Explanation:

`-C`
:   compress all data

`-X`
:   forward X (the program will run remotely but will be displayed on
    your ssh client)

Log in, make your configurations and exit.

## Systemd unit file

I wanted to be able to run spotify for more, than one user, so I needed
a multi-user unit file on the server.

`/lib/systemd/system/spotify@.service`

    [Unit]
    Description=Spotify
    Documentation=
    After=network.target

    [Service]
    User=%i
    ExecStart=/usr/bin/xvfb-run -f /home/%i/.Xauthority --auto-servernum /usr/bin/spotify --disable-gpu
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target

The `-f` is in order for us to be able to match all the processes, one
by one by monit. `--disable-gpu` is a Chromium flag[^6] - since Spotify
sadly is an electron app, by default it tries to do all the things
Chromium does, including accessing the GPU for hardware acceleration.
This is not available in the virtual X environment `xvfb` is providing,
so we need to turn it off.

Enable it for a user as:

    sudo systemctl enable spotify@[my-username]
    sudo systemctl start spotify@[my-username]

## Optional: Monit

monit[^7] is a small system supervisor which, in our case, is needed to
check if Spotify is behaving, as in not eating our CPU and memory.

`/etc/monit/monitrc.d/spotify.conf`

    CHECK PROCESS "spotify-[my-username]" matching "xvfb-run.*[my-username].*spotify"
        if total cpu > 50% for 5 cycles then restart
        if total memory usage > 15% for 10 cycles then restart

Careful with the memory usage: Spotify easily consumes at minumim 3-400
MB so change the setting according to your server capacity.

[^1]: <https://bandcamp.com/>

[^2]: <https://www.musicpd.org/>

[^3]: <https://www.mopidy.com/>

[^4]: <https://github.com/mopidy/mopidy-spotify>

[^5]: <https://blog.vivekpanyam.com/build-a-spotify-media-server/>

[^6]: <https://peter.sh/experiments/chromium-command-line-switches/>

[^7]: <https://mmonit.com/monit/>