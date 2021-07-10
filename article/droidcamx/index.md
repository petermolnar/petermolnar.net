---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20210127222833/https://petermolnar.net/article/droidcamx/
published: '2021-01-27T18:50:00+00:00'
summary: I found a program, called Droidcam, that can turn any Android phone
    into a surprisingly nice webcam over USB, and it works remarkably well
    even on linux.
title: 'Budget-friendly webcam upgrade: smartphone with DroidcamX over USB'

---

*Note: nobody paid me for this article, I merely want to share my
experiences, but some links at the bottom are amazon affiliate links.*

## DroidCamX

Today is March 333, 2020: I'm still in a full-on lockdown in the UK, and
all my life is happening through online video, just like for the past
nearly one year. I've put many of my activities on hold, including
progressing with my martial studies[^1], but considering there doesn't
seem to be an end to any of it soon, it's time to make it work through
the dreaded video. *(I'm not against videochat, but doing martial arts,
even tai chi, alone, on video conferencing is anything but ideal, if one
wants to learn, correct their mistakes, and progress.)*

I found that my laptop's webcam quality was simply not up to the game:
slow frame rate, low resolution, terrible low light performance. It's ok
for daily meetings, but not for capturing movement. At first I was
looking into building a Raspberry Pi Zero webcam[^2] with a high quality
lens, but I was reluctant to spend a considerate amount of money on it
(it would have been over £100), and to add yet another device to my
home.

I had countless rounds trying to turn some of my former smartphones into
a security camera, so I had some experience with IP camera apps, and I
was never completely happy with the outcome. Recently, however, I
started to see reviews around apps that turn iPhones into exceptionally
good webcams - Camo[^3] and EpocCam[^4] to be specific -, using USB. The
only problem is: I have android(s).

In the end I somehow found Droidcam[^5], and it's paid version,
DroidCamX[^6]: an app/software combo, that allows Windows and Linux
(sic) users to use their devices as webcam. The paid upgrade is to allow
HD and fullHD resolution; for a one-off £4.99, it's a good deal.

Their website has perfect description on how to set it up at:
<https://www.dev47apps.com/>

The step-up from the laptop's webcam is formidable:

![This camera quality of a Lenovo ThinkPad X250's built-in webcam -
"SunplusIT" according to lshw -, in natural light. This is the full,
native, 848x480 resolution, captured with
VLC](lenovo-thinkpad-x250-built-in-webcam.jpg)

![A Moto E5 phone, using Droidcamx, connected via USB, set to 1920x1080
resolution; same time, same day, same spot, though the camera was \~5cm
closer to me.](droidcamx-full-hd-with-a-moto-e5.jpg)

I've tried using it on an old android, namely a Samsung Galaxy Nexus. I
had to install an old CyanogenMod version[^7] on it to have Android 5.1,
but it worked just fine afterwards.

~~The last official Android version for this phone was 4.3[^8] and the
camera API was altered considerably in 5.0 - which is the minimum
requirement for DroidCam. I've tried a have a custom ROM based on
android 7 on the device, Droidcam only resulted in a blank, black
screen, so it's safe to conclude that one will need a device that was
released with Android 5.0 or higher.~~

## Wide angle

Normally my camera angle is enough, but I'm planning to move my workouts
to a much smaller space where I can hang a punching bag. I've had a
round with a wide angle lens at the start of the pandemic, which I ended
up sending back, given it cut off about 1/4 of the view due to being too
small.

This time I spent a lot time on reading review, focusing on the
wide-angle and not the macro experience - that is because nearly every
clip-on lens out there is at least a 2-in-1: a macro and a wide angle.

In the end I've found a 140º Wide Angle Camera Lens on amazon[^9],
costing £16.79 in a sale, and I was pleasantly surprised:

![LUXSURE Professional wide angle lens - it's bigger, and heavier, than
it looks](wide-angle-clip-on-lens.jpg)

![A Moto E5 phone, using Droidcamx, connected via USB, set to 1920x1080
resolution; same time, same day, same spot at the other Moto E5 photo
from before, but with a wide-angle clip on
lens](droidcamx-full-hd-with-a-moto-e5-with-wide-angle-clip-on-lens.jpg)

Obviously, with similar any addon lens, it will make the image quality
is a bit worse, but there's no vignetting, no dark corners. The barrel
distortion is quite heavy, but I wasn't expecting miracles for that
price - in comparison, a real wide-angle lens for a Pentax camera is
well into the £600 range at minimum.

It's important to note that if it's not positioned correctly, the
picture will get very blurry; if this happens, make sure that the center
of the lens is directly above the center of camera - not the camera
bump/area, but the hole, which is the camera itself.

## Stand/mount

I didn't have any kind of stand/mount/holder for my phone, that could
hold the position required, or be mounted on a tripod. When I started
looking most results where for cheap, basically single use, plastic
mounts.

I'm very tired of buying equipment that fails me way too soon: in
comparison, my trusty Slik Sprint tripod is from 2006, and still going
strong, despite having experienced seawater, mud, rain, and a lot of
abuse.

So I decided to go for something that looks like it might last, and
payed £24.99 for a metal phone holder[^10], instead of \~£9 plastic one.
So far so good - even the tightening knob is metal!

![Woohoto is not yet a well respected photo gear brand, but if they keep
producing this kind of quality, they could
be](metal-smartphone-mount.jpg)

## Notes

There were quite a few articles recently around the topic that webcam
quality is terrible, even for the expensive ones[^11] compared to
basically any current day phone. This lead me to avoid the search for a
webcam and explore what could be done with some upgrade to my existing
equipment. DroidCamX works very nice.

The only downside is that encoding a 480x360 video stream is not the
same as encoding 1920x1080 - your machine will certainly work harder
during the video conferences. If it can't cope with it, consider
lowering the resolution, because even if the resolution is the same, the
image quality is still significantly better, than of a built-in laptop
webcam.

[^1]: <https://pakua.com>

[^2]: <http://www.davidhunt.ie/raspberry-pi-zero-with-pi-camera-as-usb-webcam/>

[^3]: <https://reincubate.com/camo/>

[^4]: <https://www.elgato.com/en/epoccam>

[^5]: <https://www.dev47apps.com/>

[^6]: <https://play.google.com/store/apps/details?id=com.dev47apps.droidcamx>

[^7]: <https://cloud.petermolnar.net/index.php/s/9Xdbjopr9GjDz6Z>

[^8]: <https://developers.google.com/android/images#yakju>

[^9]: <https://amzn.to/3qW8FEx>

[^10]: <https://amzn.to/2MnBZot>

[^11]: <https://reincubate.com/support/how-to/why-are-webcams-bad/>
