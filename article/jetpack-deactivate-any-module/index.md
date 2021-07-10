---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125651/https://petermolnar.net/jetpack-deactivate-any-module/
published: '2014-04-22T09:15:46+00:00'
redirect:
- wordpress-jetpack-deactivate-module
summary: How to disable any module of JetPack for WordPress.
tags:
- WordPress
title: 'WordPress Jetpack: deactivate any module'

---

After I've installed the JetPack module I saw a lot of plugins I don't
need at all but I did not have a deactivate button for them. To make
them deactivated, you'll need a bit of database hacking:

To show the active modules list:

```sql
SELECT * FROM wp_options WHERE option_name='jetpack_active_modules';
```

The output should be something like this:

```sql
+-----------+------------------------+------------------------+----------+
| option_id | option_name            | option_value           | autoload |
+-----------+------------------------+------------------------+----------+
|    254164 | jetpack_active_modules | a:1:{i:0;s:5:"stats";} | yes      |
+-----------+------------------------+------------------------+----------+
1 row in set (0.00 sec)
```

To deactivate ALL the modules ( you will be able to activate one by one
after this )

```sql
UPDATE wp_options SET option_value='' WHERE option_name='jetpack_active_modules';
```