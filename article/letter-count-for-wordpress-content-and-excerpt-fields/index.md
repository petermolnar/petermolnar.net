---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125736/https://petermolnar.net/letter-count-for-wordpress-content-and-excerpt-fields/
published: '2014-04-12T10:24:41+00:00'
summary: How to add a simple character counter to excerpt & content fields
    in WordPress.
tags:
- WordPress
title: Character count for WordPress content and excerpt fields

---

<ins datetime="2014-04-24T09:36:27+00:00">
</ins>
UPDATE: I've corrected the JS code by adding a check for the existence
of the excerpt and the word counter entries; without this, JS would fail
to load on pages and custom posts.

I've been looking for a simple letter counter for the WordPress content
& excerpt fields, but the only plugin I've found is not working as of
WordPress 3.8[^1]. I've also come across with a blog post how to do this
for the exceprt[^2], but that was throwing errors, so I corrected it and
added the content counter.

Add this to your theme's functions.php:

```php

/* letter counter */
add_action( 'admin_head-post.php',  'letter_count_js'));
add_action( 'admin_head-post-new.php',  'letter_count_js' ));

public function letter_count_js(){
    echo '<script>jQuery(document).ready(function(){

        if( jQuery("#excerpt").length ) {
            jQuery("#postexcerpt .handlediv").after("<input type='text' value='0' maxlength='3' size='3' id='excerpt_counter' readonly='' style='background:#fff; position:absolute;top:0.2em;right:2em; color:#666;'/>");
            jQuery("#excerpt_counter").val(jQuery("#excerpt").val().length);
            jQuery("#excerpt").keyup( function() {
                jQuery("#excerpt_counter").val(jQuery("#excerpt").val().length);
            });
        }

        if( jQuery("#wp-character-count").length ) {
            jQuery("#wp-word-count").after("<td id='wp-character-count'>Character count: <span class='character-count'>0</span></td>");
            jQuery("#wp-character-count .character-count").html(jQuery("#wp-content-wrap .wp-editor-area").val().length);
            jQuery("#wp-content-wrap .wp-editor-area").keyup( function() {
                jQuery("#wp-character-count .character-count").html(jQuery("#wp-content-wrap .wp-editor-area").val().length);
            });
        }

    });</script>';
}
```

[^1]: <http://wordpress.org/plugins/posts-character-count-admin/>

[^2]: <http://premium.wpmudev.org/blog/daily-tip-how-to-add-a-character-counter-to-the-wordpress-excerpt-box/>