---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120223230828/http://petermolnar.eu:80/linux-tech-coding/nginx-config-for-wordpress-network/
published: '2012-02-10T08:52:59+00:00'
redirect:
- nginx-config-for-wordpress-network-multisite-with-secure-and-non-secure-ports
summary: Easy and clean nginx config for a secure WordPress Network.
tags:
- WordPress
title: nginx config for a WordPress Network

---

The real bottleneck of a WordPress Network is that the static files of the sub-blogs will be served by PHP - unless you write some tricky rewrite rules. The drawback? This is not automatic; each sub-blog will require a new entry, but it falls back safely to the original, PHP based serving if blog is not mapped yet.

**Note**: PHP-FPM is required, otherwise this config will _not_ work. That's going to be in an other entry, it's not here.

nginx is still marvellous and it's config is getting incredibly easy and nice. For example, this config is enough to run a WordPress site on port 80 and 443 with SSL enabled only on 443.

```apache

# if nginx map module is available, this can be used to serve the
# static files from sub-blogs of a network directly with nginx
# instead of PHP
# this reduces page load time and server load as well
#
# left: sub-blog domain
# right: the number of the sub-blog in WordPress Network
map $host $wordpress_network_blog_dir {
    default                         0;
    subblog1.your-domain.com        1;
    subblog2.your-domain.com        2;
}


server {
    ## Ports
    listen          80;
    listen          443  ssl;

    ## SSL certs
    ssl_certificate         /etc/ssl/yourcert.crt;
    ssl_certificate_key     /etc/ssl/yourcert.key;

    ## server name
    # . acts as wildcard
    server_name     .your-domain.com;

    ## root
    root            /path/to/your/root/;

    ## global rewrites
    # WordPress Network sites files (map is above)
    if ( $wordpress_network_blog_dir!= 0 )
    {
        rewrite ^/files/(.*)$ /wp-content/blogs.dir/$wordpress_network_blog_dir/files/$1 last;
    }
    # fallback if site is not mapped
    if ( $wordpress_network_blog_dir= 0 )
    {
        rewrite ^(.*)/files/(.*)$ /wp-includes/ms-files.php?file=$2 last;

    }

    ## locations
    location / {

        # enable browser cache for images
        # not location, because this applies for PHP served images as well in WP Network
        if ( $uri ~ .(ico|gif|jpg|jpeg|png)$  ) {
            expires 30d;
            add_header Pragma public;
            add_header Cache-Control "public, must-revalidate, proxy-revalidate";
        }

        # enable browser cache for css / js
        # not location, because this applies for PHP served files as well in WP Network
        if ( $uri ~ .(css|js)$  ) {
            expires 7d;
            add_header Pragma public;
            add_header Cache-Control "public, must-revalidate, proxy-revalidate";
        }

        # default uri
        try_files $uri $uri/ @rewrites;
    }

    # rewrite rules
    location @rewrites {
        rewrite ^(.*)$ /index.php?q=$1 last;
    }

    ## hide files starting with .
    location ~ /. {
        deny all;
        log_not_found off;
    }

    ## enable nginx status screen, optional
    location /nginx_status {
        stub_status on;
    }

    ## pass to PHP5-FPM server in the background
    location ~ .php {
        fastcgi_param   QUERY_STRING            $query_string;
        fastcgi_param   REQUEST_METHOD          $request_method;
        fastcgi_param   CONTENT_TYPE            $content_type;
        fastcgi_param   CONTENT_LENGTH          $content_length;
        fastcgi_param   SCRIPT_FILENAME         $document_root$fastcgi_script_name;
        fastcgi_param   SCRIPT_NAME             $fastcgi_script_name;
        fastcgi_param   REQUEST_URI             $request_uri;
        fastcgi_param   DOCUMENT_URI            $document_uri;
        fastcgi_param   DOCUMENT_ROOT           $document_root;
        fastcgi_param   SERVER_PROTOCOL         $server_protocol;
        fastcgi_param   GATEWAY_INTERFACE       CGI/1.1;
        fastcgi_param   SERVER_SOFTWARE         nginx;
        fastcgi_param   REMOTE_ADDR             $remote_addr;
        fastcgi_param   REMOTE_PORT             $remote_port;
        fastcgi_param   SERVER_ADDR             $server_addr;
        fastcgi_param   SERVER_PORT             $server_port;
        fastcgi_param   SERVER_NAME             $server_name;
        # PHP only, required if PHP was built with --enable-force-cgi-redirect
        fastcgi_param   REDIRECT_STATUS         200;

        fastcgi_index                           index.php;
        fastcgi_connect_timeout                 60;
        fastcgi_send_timeout                    180;
        fastcgi_read_timeout                    180;
        fastcgi_buffer_size                     128k;
        fastcgi_buffers                         4       256k;
        fastcgi_busy_buffers_size               256k;
        fastcgi_temp_file_write_size            256k;
        fastcgi_intercept_errors                on;
        fastcgi_split_path_info ^(.+.php)(/.*)$;
        fastcgi_pass    127.0.0.1:9000;
    }
}
```

When a new site is added into WordPress, a directory is created for it inside wp-content/blogs.dir/, with the same number the site was added to the system. This is the number I've called $wordpress_network_blog_dir in the config above.

Feel free to ask question if there are.