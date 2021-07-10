---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20190624125847/https://petermolnar.net/nginx-no-primary-script-unknown/
published: '2017-01-05T21:01:00+00:00'
summary: Add `try_files $uri $script_name =404;` to your PHP handling block.
    Click more for details
tags:
- linux
title: 'How to get rid of ''FastCGI sent in stderr: Primary script unknown''
    in nginx logs'

---

I've tried countless methods to get rid of annoying messages in my nginx
log, like `[error] 358#0: *44 open()` and
`[error] 10643#0: *2262 FastCGI sent in stderr: "Primary script unknown" while reading response header from upstream`.

These are errors, sent to STDERR by the FastCGI upstream, in this case,
PHP-FPM, and they happen when either index.php is not present in the
folder or when a nonexistent file gets redirected to index.php and in
can't handle it.

Apparently, I was missing a single line:

```nginx
location ~ ^(?<script_name>.+?\.php)(?<path_info>.*)$ {
    try_files $uri $script_name =404;
    ...
}
```

That `try_files $uri $script_name =404;` needs to go into the PHP
handling block of nginx, and the error vanishes from the logs.