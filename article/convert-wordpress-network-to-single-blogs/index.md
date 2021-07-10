---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20140719230743/https://petermolnar.eu/linux-tech-coding/convert-wordpress-network-to-single-blogs/
published: '2014-04-29T11:59:33+00:00'
summary: Converting a blog from a WordPress Network to standalone is painful.
tags:
- WordPress
title: moving a site to standalone from a WordPress Network

---

I've been using a WordPress Network[^1] ( Multisite, WordPress MU in
older terminology ) setup for years. I long time ago, when I still
believed I'll run a web business some day, I had a main domain and built
a whole environment around it.

The Network is a brilliant piece of software when it comes to shared
users and centralized management, especially when you're building sites
for less technology aware people and you try to avoid giving them plugin
administration rights.

There are issues with multisite setups, for example, domain mapping can
be tricky to set up initially ( even with the brilliant little WordPress
MU Domain Mapping[^2] ) and a lot of the plugins have paid only version
with multisite support. But the real pain comes when you want to move a
site out of the Network.

My reason is simple: I had issues with my base domain last year. Even if
I could hack my hosts file to point to the right IP all the time, the
plugins and anything using the network access would fail. So I decided
to search for a remote management solution ( I ended up using
InfiniteWP[^3] for now but I do miss the shared users already ) and
started moving the blogs out of the network.

If it was only this simple...

I've tried everything. Database hacks, copying tables, conversions,
backups-imports, but at a certain point, all of them failed. So I went
for the most brutal solution.

-   export the contents and as many settings you can ( WP-SEO has
    export, Custom fields also allow that, and so on )
-   create a folder with a freshly downloaded WordPress core
-   since you need to leave the old setup's files accessible from the
    old URLs, copy the blogs.dir/\[blog id\]/files folder with all it's
    contents to the new setup's wp-content directory ( the Network uses
    domain.com/files access instead of the single site setup, where the
    default is /wp-content/uploads, so this way you'll be able to import
    the files )
-   re-point you webserver to the new location for the domain
-   create a NEW INSTALLATION of WordPress from scratch
-   import the contents ( install the plugin and run the import )
-   WAIT.... and wait....and wait.... apparently WordPress import take a
    loooooooong time...
-   install ( or copy ) the plugins
-   import the plugin settings
-   tweak and tune everything as it used to be, including the theme
    settings

And repeat this for all site, one by one.

WordPress, I do like you, but there has to be a nicer way for this.

At least the database is now clean of leftover options, settings and
years of waste.

[^1]: <http://codex.wordpress.org/Create_A_Network>

[^2]: <http://wordpress.org/plugins/wordpress-mu-domain-mapping/>

[^3]: <http://infinitewp.com/>