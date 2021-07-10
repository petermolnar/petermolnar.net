<?php

function _syslog($msg) {
    $trace = debug_backtrace();
    $caller = $trace[1];
    $parent = $caller['function'];
    if (isset($caller['class'])) {
        $parent = $caller['class'] . '::' . $parent;
    }

    if ( @is_array( $msg ) || @is_object ( $msg ) ) {
        $msg = json_encode($msg);
    }
    file_put_contents('./micropub.log', $msg."\n", FILE_APPEND);
    return error_log( "{$parent}: {$msg}" );
}

function notimplemented() {
    header('HTTP/1.1 501 Not Implemented');
    die("This functionality is yet to be implemented");
}

function unauthorized($text) {
    header('HTTP/1.1 401 Unauthorized');
    _syslog("unauth:" . $text);
    die($text);
}

function badrequest($text) {
    header('HTTP/1.1 400 Bad Request');
    _syslog("badreq:" . $text);
    die($text);
}

function remoteerror($text) {
    header('HTTP/1.1 421 Misdirected Request');
    _syslog("remote_err:" . $text);
    die($text);
}

function httpok($text) {
    header('HTTP/1.1 200 OK');
    _syslog("ok:" . $text);
    echo($text);
    exit(0);
}

function jsonok($text) {
    header('Content-type:application/json;charset=utf-8');
    httpok($text);
}

function accepted() {
    header('HTTP/1.1 202 Accepted');
    header('Location: https://petermolnar.net/');
    _syslog("accepted");
    exit(0);
}

function created($target) {
    header('HTTP/1.0 HTTP/1.1 201 Created');
    header("Location: ". $target);
    exit(0);
}

function verify_token($token) {
    $request = curl_init();
    curl_setopt($request, CURLOPT_URL, 'https://tokens.indieauth.com/token');
    curl_setopt($request, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/x-www-form-urlencoded',
        "Authorization: Bearer {$token}"
    ));
    curl_setopt($request, CURLOPT_RETURNTRANSFER, 1);
    $response = curl_exec($request);
    curl_close($request);
    parse_str(urldecode($response), $verification);

    if (! isset($verification['scope']) ) {
        unauthorized('missing "scope"');
    }
    if (! isset($verification['me']) ) {
        unauthorized('missing "me"');
    }
    if ( ! stristr($verification['me'], 'petermolnar.net') ) {
        unauthorized('wrong domain');
    }
}

function categories() {
    $categories = array();
    foreach(scandir(getcwd()) as $path) {
        if(!is_dir("$path")) {
            continue;
        }
        elseif (strpos($path,".") === 0) {
            continue;
        }
        elseif (strpos($path, "_") === 0) {
            continue;
        }
        else {
            array_push($categories, $path);
        }
    }
    return $categories;
}

function save_to_wallabag($url) {
    $secrets = parse_ini_file(".secrets");
    $wallabag_url = $secrets["WALLABAG_URL"];
    $data = array(
        "client_id" => $secrets["WALLABAG_ID"],
        "client_secret" => $secrets["WALLABAG_SECRET"],
        "username" => $secrets["WALLABAG_USER"],
        "password" => $secrets["WALLABAG_PASS"],
        "grant_type" => "password"
    );

    $request = curl_init();
    curl_setopt($request, CURLOPT_URL, "{$wallabag_url}/oauth/v2/token");
    curl_setopt($request, CURLOPT_POST, 1);
    curl_setopt($request, CURLOPT_POSTFIELDS,http_build_query($data));
    curl_setopt($request, CURLOPT_RETURNTRANSFER, 1);
    $response = curl_exec($request);
    curl_close($request);

    try {
        $wallabag_token = json_decode($response, true);
    } catch (Exception $e) {
        remoteerror("failed to parse response from wallabag: " . $response);
    }

    if (! isset($wallabag_token['access_token']) ) {
        remoteerror("failed to obtain access token from wallabag: " . $response);
    }

    $data = array(
        "url" => $url,
        "archive" => 1
    );
    $headers = array(
        'Content-Type: application/x-www-form-urlencoded',
        "Authorization: Bearer ". $wallabag_token["access_token"]
    );
    $request = curl_init();
    curl_setopt($request, CURLOPT_URL, "{$wallabag_url}/api/entries");
    curl_setopt($request, CURLOPT_POST, 1);
    curl_setopt($request, CURLOPT_POSTFIELDS,http_build_query($data));
    curl_setopt($request, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($request, CURLOPT_RETURNTRANSFER, 1);
    $response = curl_exec($request);
    curl_close($request);
    try {
        $is_saved = json_decode($response, true);
        if (isset($is_saved["id"])) {
            $target = $wallabag_url . '/view/' . $is_saved["id"];
            return($target);
        }
    } catch (Exception $e) {
        remoteerror("failed to parse response to save from wallabag: " . $response);
    }
    return null;
}

function maybe_array_pop($x) {
    if(is_array($x)) {
        return array_pop($x);
    }
    else {
        return $x;
    }
}

if (!empty($_GET)) {
    if ((isset($_GET['q']) && "config" == $_GET['q']) || isset($_GET['q']['config'])) {
        jsonok(json_encode(categories()));
    }
    elseif((isset($_GET['q']) && "syndicate-to" == $_GET['q']) || isset($_GET['q']['syndicate-to'])) {
        jsonok(json_encode(array('syndicate-to' => array())));
    }
}

$raw = file_get_contents("php://input");
$decoded = 'null';
try {
    $decoded = json_decode($raw, true);
} catch (Exception $e) {
    _syslog('failed to decode JSON, trying decoding form data');
}
if($decoded == 'null' or empty($decoded)) {
    try {
        parse_str($raw, $decoded);
    }
    catch (Exception $e) {
        _syslog('failed to decoding form data as well');
        badrequest('invalid POST contents');
    }
}

$token = '';
if (isset($decoded['access_token'])) {
    $token = $decoded['access_token'];
    unset($decoded['access_token']);
}
elseif (isset($_SERVER['HTTP_AUTHORIZATION'])) {
    $token = trim(str_replace('Bearer', '', $_SERVER['HTTP_AUTHORIZATION']));
}

if (empty($token)) {
    unauthorized('missing token');
}
else {
    verify_token($token);
}

/* likes and bookmarks*/
$to_bookmark = '';
if(isset($decoded["properties"]) && isset($decoded["properties"]["bookmark-of"])) {
    $to_bookmark = maybe_array_pop($decoded["properties"]["bookmark-of"]);
}
elseif(isset($decoded["bookmark-of"])) {
    $to_bookmark = maybe_array_pop($decoded["bookmark-of"]);
}

if(!empty($to_bookmark)) {
    $saved = save_to_wallabag($to_bookmark);
    if ($saved) {
        created($saved);
    }
    else {
        remoteerror();
    }
}

$t = microtime(true);
$fname = "/drafts/{$t}.json";
$fpath = realpath(".") . $fname;
if(!is_dir(dirname($fpath))) {
    mkdir(dirname($fpath), 0755, true);
}

$c = json_encode($decoded, JSON_PRETTY_PRINT);
if (file_put_contents($fpath, $c)) {
    created("https://petermolnar.net" . $fname);
}

/* fallback to not implemented */
notimplemented();
