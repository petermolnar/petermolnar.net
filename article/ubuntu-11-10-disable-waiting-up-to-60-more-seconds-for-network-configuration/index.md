---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120604214914/http://petermolnar.eu:80/linux-tech-coding/ubuntu-11-10-disable-waiting-up-to-60-more-seconds-for-network-configuration
published: '2012-02-29T19:34:18+00:00'
summary: After upgrading from Ubuntu 11.04 to 11.10 boot hangs for more than
    one minute, waiting for network. Here's how to solve it the correct way.
tags:
- linux
title: How to disable "Waiting up to 60 more seconds for network configuration"

---

------------------------------------------------------------------------

**This post is made of copy-pasted parts from a blog post on
CodeWhirl[^1], from author Wrostek[^2]. I only placed it here to make
Google show better results for the correct solution instead of the
symlink one.**

The original post can be visited here:
<http://www.codewhirl.com/2011/10/ubuntu-11-10-waiting-up-to-60-more-seconds-for-network-configuration/>

------------------------------------------------------------------------

So, the only other solution must be to edit ‘Waiting for network
configuration…' script. This script is actually located here:
`/etc/init/failsafe.conf`

Approximately 25 lines down in the file you will see a section:

```bash
# Plymouth errors should not stop the script because we *must* reach
# the end of this script to avoid letting the system spin forever
# waiting on it to start.
$PLYMOUTH message --text="Waiting for network configuration..." || :
sleep 40

$PLYMOUTH message --text="Waiting up to 60 more seconds for network configuration..." || :
sleep 59
$PLYMOUTH message --text="Booting system without full network configuration..." || :
```

To solve the problem, you can just remove the calls to sleep, by
commenting the out ( or at least reduce the wait time if your network
really does need to wait )

```bash
# Plymouth errors should not stop the script because we *must* reach
# the end of this script to avoid letting the system spin forever
# waiting on it to start.
$PLYMOUTH message --text="Waiting for network configuration..." || :
#sleep 40

$PLYMOUTH message --text="Waiting up to 60 more seconds for network configuration..." || :
#sleep 59
$PLYMOUTH message --text="Booting system without full network configuration..." || :
```

[^1]: <http://www.codewhirl.com/>

[^2]: <http://www.codewhirl.com/author/wrostek/>