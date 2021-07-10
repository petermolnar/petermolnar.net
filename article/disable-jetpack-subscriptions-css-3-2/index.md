---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20141129064553/https://petermolnar.eu/linux-tech-coding/disable-jetpack-subscriptions-css-3-2/
published: '2014-11-06T10:31:31+00:00'
summary: Quickfix for annoying additional CSS from Jetpack.
tags:
- WordPress
title: Disable Jetpack subscriptions CSS (3.2+)

---

I've searched for a solution for this issue, the thread I came
across[^1] and it's first comment together solved it, so the whole
solution together:

```php
<?php

add_action( 'wp_footer', 'deregister_css_js' );
add_filter( 'jetpack_implode_frontend_css', '__return_false' );

function deregister_css_js () {
    wp_deregister_style( 'jetpack-subscriptions' );
    wp_deregister_style( 'jetpack_css' );
}
```

This should do it.

[^1]: <https://www.twirlingumbrellas.com/wordpress/remove-deregister-jetpack-contact-form-styles/>