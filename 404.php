<?php

function debug( $message ) {
    if (file_exists('./redirect.log')) {
        unlink('./redirect.log');
        return false;
    }

    //if ( empty( $message ) ) {
        //return false;
    //}
    //if ( @is_array( $message ) || @is_object ( $message ) ) {
        //$message = json_encode($message);
    //}
    //file_put_contents('./redirect.log', $message."\n", FILE_APPEND);
}

function redirect($target) {
    header('HTTP/1.0 302 Moved Temporarily');
    #header('HTTP/1.1 301 Moved Permanently');
    #header('HTTP/1.1 307 Temporary Redirect');
    header("Location: ". $target);
    die();
}

function bad_request($uri) {
    header('HTTP/1.0 400 Bad Request');
    die('<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width,initial-scale=1,minimum-scale=1" name="viewport"/>
  <title>Bad Request</title>
 </head>
 <body>
<h1><center>You misspelled that URL.</center></h1>
<p><center><img src="/http-400.jpg" /></center></p>
<hr>
<p><center>'.$uri.'</center></p>
 </body>
</html>');
}

function not_implemented($uri) {
    header('HTTP/1.0 501 Not Implemented');
    die('<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width,initial-scale=1,minimum-scale=1" name="viewport"/>
  <title>Not Implemented</title>
 </head>
 <body>
<h1><center>Why are you even looking for this? Is anything linking here?</center></h1>
<p><center><img src="/http-501.jpg" /></center></p>
<hr>
<p><center>'.$uri.'</center></p>
 </body>
</html>');
}

function gone($uri) {
    header('HTTP/1.1 410 Gone');
    die('<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width,initial-scale=1,minimum-scale=1" name="viewport"/>
  <title>Gone</title>
 </head>
 <body>
<h1><center>This content was deliberately deleted. I probably moved it to a private archive.</center></h1>
<p><center><img src="/http-410.jpg" /></center></p>
<hr>
<p><center>'.$uri.'</center></p>
 </body>
</html>');
}

function notfound($uri) {
    debug("  nothing found for ${uri}");
    header('HTTP/1.0 404 Not Found');
    die('<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width,initial-scale=1,minimum-scale=1" name="viewport"/>
  <title>Not found</title>
 </head>
 <body>

<h1><center>This was not found.</center></h1>
<p><center><img src="/http-404.jpg" /></center></p>
<hr>
<p><center>'.$uri.'</center></p>
 </body>
</html>');
}

/*
 * data structure in the json file
  $data = {
    "bad_request": list of regex patterns for certainly not friendly requests
    "not_implemented": list of regex patterns for not implemented paths
    "path_to_strip_from_uri": list of path that will be dropped from the uri between //
    "filenames_to_strip_from_uri": list of stristr matched filenames to drop from the uri
    "renamed_files": dict of original: replaced with file parts
    "shortslugs": dict of uri: target,
    "redirect": dict of uri: target,
    "gone": dict of uri: 1, so it's a reverse lookup table and is faster
    "rewrites": dict of regex pattern : target for redirect queries, can have $1, $2 group substitutes
    "re_gone": list for regex patterns for gone queries
  }
*/

$data = json_decode(file_get_contents('./404.json'), true);

debug("incoming 404.php request: ${_SERVER['REQUEST_URI']}");
$raw_uri = filter_var($_SERVER['REQUEST_URI'], FILTER_SANITIZE_URL);
/* no traversing directories */
$sanitized_uri = str_replace('../', '', $raw_uri);
/* remove ////// and similar */
$sanitized_uri = preg_replace('#([/]+)\1+#', '$1', $sanitized_uri);
$uri = $sanitized_uri;
if(stristr($uri, "?")) {
    $uri = substr($uri, 0, strpos($uri, "?"));
}
debug("  escaped uri: ${uri}");

/* security-ish features to stop the certainly bad requests */
foreach(array('bad_request', 'not_implemented') as $method) {
    foreach ($data[$method] as $pattern) {
        if (preg_match(sprintf('#%s#', $pattern), $uri)) {
            debug("  method ${method} matched `${uri}` with pattern: `${pattern}`");
            $method($uri);
        }
    }
}

$cleaned_uri = $uri;
foreach($data['regex_replace_in_uri'] as $regex => $substitute) {
    $cleaned_uri = preg_replace("#${regex}#", $substitute, $cleaned_uri);
}

$cleaned_uri = trim(
    str_replace(
        array_map(
            function ($value) { return "/${value}/"; },
            $data['path_to_strip_from_uri']
        ),
        '',
        $cleaned_uri
    ),
    '/'
);

$uri_elements = explode('/', $cleaned_uri);
/* remove filenames that doesn't mean anything, like index.html */
foreach($data['filenames_to_strip_from_uri'] as $filename) {
    if(stristr(end($uri_elements), $filename)) {
        array_pop($uri_elements);
    }
}

/* remove empty elements */
$uri_elements = array_filter($uri_elements);
debug("  cleaned uri: " . json_encode($uri_elements));
$cleaned_uri = trim(implode("/", $uri_elements), '/');

/* try shortslugs */
if(strlen($cleaned_uri) == 6) {
    if(isset($data['shortslugs'][$cleaned_uri])) {
        debug("  redirecting to `". $data['shortslugs'][$cleaned_uri] ."` based on shortslug match");
        redirect($data['shortslugs'][$cleaned_uri]);
    }
}

$urls_to_try = array($uri, $cleaned_uri);

foreach($urls_to_try as $url_to_try) {
    /* try static redirects */
    if(isset($data['redirect'][$url_to_try])) {
        debug("  redirecting to `". $data['redirect'][$url_to_try] ."` based on static match");
        redirect($data['redirect'][$url_to_try]);
    }

    /* try static gone array */
    if(isset($data['gone'][$url_to_try])) {
        debug("  static gone matched: `". $data['gone'][$url_to_try] ."`");
        gone($uri);
    }
}
/* try to locate if the files have moved */
if(sizeof($uri_elements) > 0) {
    debug("  iterating through URI pieces " . json_encode($uri_elements));
    $candidates = array();
    if(preg_match("/.*\.[a-zA-Z0-9]{2,4}/", end($uri_elements))) {
        $e = end($uri_elements);
        foreach($data['renamed_files'] as $original => $current) {
            $e = str_replace($original, $current, $e);
        }
        debug("  we're looking for a file: " . $e);
        $files_could_be = array($e, str_replace('_', '-', $e));
        foreach($files_could_be as $e) {
            $path = getcwd() . '/*/*/' . $e;
            debug("  checking for files under " . $path);
            $candidates = array_merge($candidates, glob($path));
        }
    }
    else {
        $paths = array(
            getcwd() . '/*/' . end($uri_elements),
            getcwd() . '/' . end($uri_elements),
        );
        foreach($paths as $path) {
            $level = glob($path);
            if(sizeof($level) > 0) {
                $candidates = array_merge($level, $candidates);
            }
        }
    }

    if(0==sizeof($candidates)) {
        debug("  no candidate found with uri pieces glob search");
    }
    else {
        if(sizeof($candidates)>1) {
            debug("  multiple candidates found for path pattern: ${path}");
            debug($candidates);
        }
        $candidate = array_pop($candidates);
        $target = str_replace(getcwd(), "", $candidate);
        debug("  redirecting `${cleaned_uri}` to file based candidate `${target}`");
        redirect($target);
    }
}

/* try rewrites */
foreach($data['rewrites'] as $pattern => $target) {
    foreach(array($sanitized_uri, $uri, $cleaned_uri) as $value) {
        if(preg_match(sprintf('#%s#i', $pattern), $value, $matches)) {
            debug("  rewrite matched `${value}`  with pattern: `${pattern}`");
            for($i=1; $i<sizeof($matches); $i++) {
                if (isset($matches[$i])) {
                    $target = str_replace('$' . $i, $matches[$i], $target);
                    debug("  `target` altered to `${target}`");
                }
            }
            redirect($target);
        }
    }
}

/* try gone regex */
foreach($data['re_gone'] as $pattern) {
    foreach(array($uri, $cleaned_uri) as $value) {
        if(preg_match(sprintf('#%s#i', $pattern), $value, $matches)) {
            debug("  regex gone matched `${value}` with pattern: `${pattern}`");
            gone($uri);
        }
    }
}

/* ok, this really wasn't found */
notfound($uri);
