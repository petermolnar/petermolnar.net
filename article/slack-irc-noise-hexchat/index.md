---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20160709135342/https://petermolnar.eu/slack-irc-noise-hexchat/
published: '2016-02-02T14:00:09+00:00'
summary: I've been pushed to use Slack besides our current jabber, but it's
    too noisy.
tags:
- linux desktop
title: Suppress Slack IRC 'voice' noise in Hexchat

---

I honestly appreciate Slack has an IRC option, but it's noisy: due to
the intolerable amount of 'voice' notes, it's impossible to see actual
messages. I'm using a ZNC bouncer, and the best would be to filter it
there, but so far I could not figure out, how, so after a little
digging, I've found this on Linux Mint forums[^1]:

( migrated from xchat to hexchat )

```python
#!/bin/sh

# change directory to the desired one
cd $1

# create resized dir
# warning! if exists, the pictures will be overwritten!
mkdir resized

# look up files with extensions
for fname in *.*; do

  # this is the resize and slightly sharpen part
  echo "resizing $fname"
  mogrify -sharpen 1 -quality 96% -write "./resized/$fname" -resize 540x540 "$fname"

  # this is the watermarking part
  echo "watermarking $fname"
  composite -compose atop -gravity SouthEast "/path/to/watermark/image" "./resized/$fname" "./resized/$fname"

done
```

[^1]: <http://forums.linuxmint.com/viewtopic.php?f=42&t=50381&start=0>