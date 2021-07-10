---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20110305054851/http://petermolnar.eu:80/sysadmin-blog/simple-batch-resize-watermark-with-imagemagick
published: '2010-11-21T15:18:41+00:00'
summary: Fast & simple batch image handling with imagemagick, from the command
    line.
tags:
- bash
title: Simple batch resize & watermark with imagemagick

---

Last year I finally decided to end up with Microsoft (Windows 7 is so
far from my attitude), therefore Ubuntu made it into my life.
Fortunately, the most of the software I used was already cross-platform,
the most hard part was with DJ software ( Mixxx with version 1.8 is OK,
but before... ), with graphical editing and something instead of XnView.

Yes, there is XnView MP and nconvert, but both of them is full of bugs.
The only reasonable program to use is ImageMagick, but is has an
extremely awful documentation, which lacks vital examples.

Finally, I figured out the script I needed for resizing and watermaking
images:

```bash
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

And that's all.

Usage:

```bash
bash watermark.sh desired/folder/path/with/images/
```