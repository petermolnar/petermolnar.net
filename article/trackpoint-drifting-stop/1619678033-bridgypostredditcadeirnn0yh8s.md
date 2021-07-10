---
author:
    name: Benaxle
    photo: https://webmention.io/avatar/www.redditstatic.com/4bd9870349aedef6da73965dbc7781f3db43e42d93a695d3a0b588d7297fb95d.png
    url: https://reddit.com/user/Benaxle/
date: '2021-04-29T06:33:53+00:00'
source: https://brid.gy/post/reddit/cadeirn/n0yh8s
target: https://petermolnar.net/article/trackpoint-drifting-stop/
type: link

---

Pretty cool title, but the behavior is the most annoying thing ever and requires me to restart.
Two issues I want to fix on my X240, running voidlinux and Swaywm.

* at random the pointer will jump to corners of the screen for no reason and randomly click, that can last up to 20seconds

* at random the pointer will head to a random direction at a certain speed and this lasts forever (it nevers resets the drift)

I had scripts to reset the drift manually on X :

    echo -n none &gt; /sys/devices/platform/i8042/serio1/drvctl
    echo -n reconnect &gt; /sys/devices/platform/i8042/serio1/drvctl
    
    #https://petermolnar.net/trackpoint-drifting-stop/

But If I use them now, my pointer stops and never work again.

How do I setup the trackpoint correctly, how do I fix the drift issue?

Thank you!
<a class="u-mention" href="https://petermolnar.net/article/trackpoint-drifting-stop/"></a>
<a href="https://petermolnar.net/trackpoint-drifting-stop/">https://petermolnar.net/trackpoint-drifting-stop/</a>
