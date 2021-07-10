---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20180114124716/https://petermolnar.net/linkedin-public-settings-ignored/
published: '2018-01-14T12:00:00+00:00'
summary: Logged out users are prevented from reaching LinkedIn profiles set
    to complete public visibility
tags:
- internet
title: LinkedIn is ignoring user settings

---

A few days ago, on the \#indieweb Freenode channel[^1] one of the users
asked if we knew an indieweb-friendly way of getting data out of
LinkedIn. I wasn't paying attention to any recent news related to
LinkedIn, though I've heard a few things, such as they are struggling to
prevent data scraping: the note mentioned that they believe it's a
problem that employers keep an eye on changes in LinkedIn profiles via
3rd party. This, indeed, can be an issue, but there are ways to manage
this within LinkedIn: your public profile settings[^2].

In my case, this was set to visible to everyone for years, and by the
time I had to set it up (again: years), it was working as intended. But
a few days ago, for my surprise, visiting my profile while logged out
resulted in this:

![LinkedIn showing a paywall-like 'authwall' for profiles set explicitly
to public for everyone](linkedin-public-profile-issues-authwall.png)

and this:

```bash
$ wget -O- https://www.linkedin.com/in/petermolnareu
--2018-01-14 10:26:12--  https://www.linkedin.com/in/petermolnareu
Resolving www.linkedin.com (www.linkedin.com)... 91.225.248.129, 2620:109:c00c:104::b93f:9001
Connecting to www.linkedin.com (www.linkedin.com)|91.225.248.129|:443... connected.
HTTP request sent, awaiting response... 999 Request denied
2018-01-14 10:26:12 ERROR 999: Request denied.
```

or this:

```bash
$ curl https://www.linkedin.com/in/petermolnareu
<html><head>
<script type="text/javascript">
window.onload = function() {
  // Parse the tracking code from cookies.
  var trk = "bf";
  var trkInfo = "bf";
  var cookies = document.cookie.split("; ");
  for (var i = 0; i < cookies.length; ++i) {
    if ((cookies[i].indexOf("trkCode=") == 0) && (cookies[i].length > 8)) {
      trk = cookies[i].substring(8);
    }
    else if ((cookies[i].indexOf("trkInfo=") == 0) && (cookies[i].length > 8)) {
      trkInfo = cookies[i].substring(8);
    }
  }

  if (window.location.protocol == "http:") {
    // If "sl" cookie is set, redirect to https.
    for (var i = 0; i < cookies.length; ++i) {
      if ((cookies[i].indexOf("sl=") == 0) && (cookies[i].length > 3)) {
        window.location.href = "https:" + window.location.href.substring(window.location.protocol.length);
        return;
      }
    }
  }

  // Get the new domain. For international domains such as
  // fr.linkedin.com, we convert it to www.linkedin.com
  var domain = "www.linkedin.com";
  if (domain != location.host) {
    var subdomainIndex = location.host.indexOf(".linkedin");
    if (subdomainIndex != -1) {
      domain = "www" + location.host.substring(subdomainIndex);
    }
  }

  window.location.href = "https://" + domain + "/authwall?trk=" + trk + "&trkInfo=" + trkInfo +
      "&originalReferer=" + document.referrer.substr(0, 200) +
      "&sessionRedirect=" + encodeURIComponent(window.location.href);
}
</script>
</head></html>
```

So I started digging. According to the LinkedIn FAQ[^3] there is a page
where you can set your profile's public visibility. Those settings, for
me, were still set to: ![LinkedIn public profile
settings](linkedin-public-profile-issues-settings.png)

Despite the settings, there is no public profile for logged out users.

I'd like to understand what it going on, because so far, this looks like
a fat lie from LinkedIn. Hopefully just a bug.

## UPDATE

~~I tried setting referrers and user agents, used different IP
addresses, still nothing.~~ I can't type today and managed to mistype
`https://google.com` - the referrer ended up as `https:/google.com`. So,
following the notes on HN, setting a referrer to Google sometimes works.
After a few failures it will lock you out again, referrer or not. This
is even uglier if it was a proper authwall for everyone.

```bash
curl 'https://www.linkedin.com/in/petermolnareu' \
-e 'https://google.com/' \
-H 'accept-encoding: text' -H \
'accept-language: en-US,en;q=0.9,' \
-H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
```

```html
<!DOCTYPE html>...
```

[^1]: <https://chat.indieweb.org>

[^2]: <https://www.linkedin.com/public-profile/settings>

[^3]: <https://www.linkedin.com/help/linkedin/answer/83?query=public>