---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624130451/https://petermolnar.net/wordpress-insert-image-as-markdown-extra/
published: '2014-07-17T16:46:19+00:00'
summary: WordPress + Markdown are not there yet, hacks needed.
tags:
- WordPress
title: WordPress - insert image as Markdown Extra

---

I'm getting a bit angry on the Markdown plugins of WordPress[^1]: all of
them will store the text as HTML, while the original goal for me would
be to **store** in Markdown, for future readability. With Parsedown[^2]
+ a persistent WordPress Object cache[^3] parsing on the fly is really
not an issue.

So as always, I need to come up with a solution - *a hack if that sounds
better* - to store posts in Markdown Extra[^4]. The nasty part is the
editor, especially with media, so I decided chop it into pieces.

This is for images only, since video or audio is not supported by any of
the Markdown flavours I know.

```php
<?php

add_filter( 'post_thumbnail_html', 'rebuild_media_string', 10 );
add_filter( 'image_send_to_editor', 'rebuild_media_string', 10 );

function preg_value ( $string, $pattern, $index = 1 ) {
    preg_match( $pattern, $string, $results );
    if ( isset ( $results[ $index ] ) && !empty ( $results [ $index ] ) )
        return $results [ $index ];
    else
        return false;
}

function rebuild_media_string( $str ) {
    if ( strstr ( $str, '<img' ) )
        $src = preg_value ( $str, '/src="([^"]+)"/' );
        $title = preg_value ( $str, '/title="([^"]+)"/' );
        $alt = preg_value ( $str, '/alt="([^"]+)"/' );
        if ( empty ( $alt ) && !empty ( $title ) ) $alt = $title;
        $wpid = preg_value ( $str, '/wp-image-(\d*)/' );
        $src = preg_value ( $str, '/src="([^"]+)"/' );
        $cl = preg_value ( $str, '/class="([^"]+)?(align(left|right|center))([^"]+)?"/', 2 );

        $img = '!['.$alt.']('. $src .' '. $title .'){#img-'. $wpid .' .'.$cl.'}';
        return $img;
    }
    else {
        return $str;
    }
}
```

[^1]: <http://premium.wpmudev.org/blog/can-wordpress-do-markdown-like-ghost>

[^2]: <http://parsedown.org/demo?extra=1>

[^3]: <http://wordpress.org/plugins/apcu/>

[^4]: <https://michelf.ca/projects/php-markdown/extra/>