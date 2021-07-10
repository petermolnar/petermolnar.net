---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120802041721/http://petermolnar.eu/linux-tech-coding/conky-with-ical/
published: '2012-02-20T09:45:15+00:00'
summary: Make conky display ical calendars from the web with the help of calcurse.
tags:
- linux desktop
title: conky with ical

---

I encountered a simple problem: how to display ical calendar events with
conky without writing an ical parser. The solution came in the form of a
suprising tool: calcurse. This is a command-line, text-based, slightly
graphical-like interface for ical handling.

So: download the calendar, import it into calcurse, show it in conky.
But how to manage possible remote update? Do this every 30 minutes.

`install calcurse`

```bash
sudo apt-get install calcurse
```

`load_calendars.sh`

```bash
#!/bin/bash

# clear calcurse data
rm ~/.calcurse/apts

# array for remote calendars
calendars=( 'http://link-to-first-cal.ics' 'http://link-to-second-cal.ics' 'and so on' );

# temp file to save a calendar
TMPCAL=/tmp/temp.ics

# run through the calendars
for ical in "${calendars[@]}"
do
    # download ical file
    wget -q "$ical" -O $TMPCAL
    # import into calcurse, error & output silenced
    calcurse -i $TMPCAL >/dev/null 2>&1
    # clear the temp calendar file
    rm $TMPCAL
done

# display current & next 6 days (7 altogether)
calcurse -r7
```

`conky-cal.conf`

```apache
use_xft yes
xftfont DejaVu Sans:size=8
xftalpha 0.8
text_buffer_size 2048
total_run_times 0
no_buffers yes
uppercase no
cpu_avg_samples 1
net_avg_samples 1
override_utf8_locale yes
double_buffer yes
use_spacer none

own_window yes
own_window_transparent yes
own_window_type normal
own_window_hints undecorated,below,sticky,skip_taskbar,skip_pager
minimum_size 420 0
maximum_width 420
draw_shades no
draw_outline no
draw_borders no
stippled_borders 0
border_width 0
default_color grey
own_window_colour grey
alignment top_left

update_interval 3600
gap_x 20
gap_y 20

TEXT
${font DejaVu Sans:style=Bold:size=10}EVENTS${font}
${font DejaVu Sans:size=9}${exec /path/to/load_calendars.sh}${font}
```