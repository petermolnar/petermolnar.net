---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20150524123711/https://petermolnar.eu/linux-tech-coding/add-avatar-for-not-comment-type-comments-in-wordpress/
published: '2015-04-09T09:12:03+00:00'
summary: By default only comment type comments get avatars.
tags:
- WordPress
title: Add avatar for not comment type comments in WordPress

---

Sometimes I hate you, WordPress. Finding this took 3 hours of my life.
In case you want avatars for comments with not "comment" comment type
field ( for example, you introduce like, favorite, etc. types ) you need
this to be extended:

```php
$allowed_comment_types = apply_filters(
    'get_avatar_comment_types', array( 'comment' )
);
```

as

```php
add_filter('get_avatar_comment_types', 'add_new_comment_types');

function add_new_comment_types ( $types ) {
    foreach ($this->methods as $method => $type ) {
        if (!in_array( $type, $types ))
            array_push( $types, $type );
    }
    return $types;
}
```