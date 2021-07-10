---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125410/https://petermolnar.net/elementaryos-plank-position/
published: '2012-12-21T11:31:13+00:00'
summary: How to move elementaryOS Luna Plank to different position.
tags:
- linux desktop
title: Reposition elementaryOS dock (Plank)

---

I've tried elementaryOS Luna for the first time, and I'm really deeply
impressed by the speed, the responsibility and the user experience.

What I don't like:

-   the Mac design ( MediterraneanNight[^1], Shiki-Brave[^2], please, we
    have enough Mac-clone skins already, and high contrast is just an
    eye-killer, seriously. )
-   the position of the dock ( Plank ): before using Unity for a while,
    positioning the dock to the left seemed the worst idea ever - but
    suprisingly it is better with the wide screens and a lot faster to
    access.

The first problem may be handled in a while, the second is easier:

```bash
gedit ~/.config/plank/dock1/settings
```

Search for the line

```bash
Position=3
```

and change the number the way you want:

```bash
0 => left
1 => right
2 => top
3 => bottom
```

To position it top-left, right below the panel: Search for the line

```bash
Offset=0
```

and replace `0` with `-90`

Save the file, log out, log in back again.

[^1]: <http://gnome-look.org/content/show.php?content=148398>

[^2]: <http://gnome-look.org/content/show.php/Shiki-Colors?content=86717>