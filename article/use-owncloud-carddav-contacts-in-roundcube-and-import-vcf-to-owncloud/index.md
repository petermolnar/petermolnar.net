---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120526150533/http://petermolnar.eu:80/linux-tech-coding/use-owncloud-carddav-contacts-in-roundcube-and-import-vcf-to-owncloud
published: '2012-02-08T14:05:16+00:00'
summary: How to use OwnCloud CardDAV  service as address book in RoundCube
    and how to import vcf into OwnCloud.
tags:
- linux
title: Use OwnCloud CardDAV contacts in RoundCube ( and import .vcf to OwnCloud)

---

OwnCloud is getting better and better, and by some tweakings in nginx,
it is now useable on my server as well. But to really become an
alternative for Google Apps, I needed to connect it into RoundCube
WebMail[^1]. *I've given up on Thunderbird, it's choose to take walk the
same way as Firefox, for example, by ruining plugin compatibility, lack
of sync features, and so on.*

So how to connect RoundCube address book with OwnCloud CardDAV server?

-   I suppose you have a working RoundCube installation. If not, here's
    the official howto[^2].
-   Download the CardDAV plugin from Benjamin Schieder[^3] (as buy
    something for him from his whishlist[^4] )
-   uncompress the downloaded tar.bz2 file
-   move the extracted `carddav` folder into the `plugins` folder of
    your RoundCube
-   move the `config.inc.php.dist` file to `config.inc.php` in the
    carddav folder. This config file contains two pre-defined address
    books, comment out them, if you have no need. Be careful to leave
    the `$prefs['db_version'] = 2` in, that is not to be commented!
-   add `carddav` into `roundcube/config/main.inc.php` to the
    `$rcmail_config['plugins']` array -login to roundcube and go to
    `Personal settings`, `CardDAV`
-   add a new address book with the URL to your contact list provided by
    OwnCloud. You can find this by:
    -   nagivate to Contacts in owncloud
    -   click on `Addressbooks` at the top right corner
    -   click on the little Earth icon in the line of the address book
        you're about to use
    -   copy the URL
-   optional: if you'd like to use as default address book, go to
    `Personal settings`, `Address Book`, `Main Options` and change the
    default address book there.

After you're ready, you can go the the new address book in RoundCube and
import any vcf file with the help of it - and because the address book
is really located at OwnCloud it's going to be imported into OwnCloud.

[^1]: <http://roundcube.net/>

[^2]: <http://trac.roundcube.net/wiki/Howto_Install>

[^3]: <http://www.crash-override.net/carddavdownload.html>

[^4]: <http://www.crash-override.net/say-thanks.html>