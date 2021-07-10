---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111112123826/http://petermolnar.eu:80/sysadmin-blog/automatically-version-controlled-directory-with-bazaar-on-linux/
published: '2011-10-29T17:34:54+00:00'
summary: Dropbox-like file versioning functionality with bazaar VCS and inotifywait.
tags:
- linux
title: Automatically version controlled directory with bazaar on linux

---

I have some folders I edit from various places and modes: ssh, remote
connection, etc. This is an important folder, so I decided to make it
versioned somehow following all the modifications made to all files.

After spending hours of reading about version control, autosync, push,
pull, etc, it became clear, that there are no software solutions for
this right know but the filesystems themselves like btrfs or zsf, but I
did not want to convert my ext4.

Since I'm quite stubborn, I still wanted to achieve this somehow. The
solution: I have a folder, which contains a bazaar repository. This
repository is checked out locally - this is the one to be reached with
ssh, ftp, DAV, etc. I fire inotifywait monitors for various events with
various actions to commit the changes - and that's all.

I'm still testing the effectiveness, but it looks good. And of course:
this tutorial comes without any responsibility or expectation.

On Ubuntu, you need to install bazaar and inotifytools.

```bash
sudo apt-get install inotify-tools bzr bzrtools
```

Now create a new repository.

```bash
# change directory
cd path/to/repository/directory/root
# create repository main dir
mkdir www-repository;
# init repository
bzr init-repo www-repository;
# change into repository directory
cd www-repository;
# create main branch directory
mkdir trunk;
# init main branch
bzr init trunk;
# change into main branch directory
cd trunk;
# copy file you want at checkout
cp -a /path/to/the/files/you/want/at/first/checkout ./;
# add copied file
bzr add *;
# commit changes
bzr commit -m "repository initialisation";
# change to www parent directory
cd path/to/www/parent;
# create www dir & checkout repository trunk in it
# lightweight means it's not a full repo, just the files, it requires the trunk to be
# always accessible, but since its on the same server, it's OK
bzr checkout --lightweight path/to/repository/directory/root/www-repository/trunk/ ./www;
```

Start monitoring for changes recursively on the checkout repository.

```bash
#!/bin/bash

# go to checkout repository folder you want to watch
cd path/to/www/parent/www
# start watching the directory for changes recusively, ignoring .bzr dir
# comment is made out of dir/filename
# no output is shown from this, but wrinting a filename instead of /dev/null would
# allow logging
inotifywait --exclude .bzr -r -q -m -e CLOSE_WRITE --format="bzr commit -m 'autocommit for %w/%f'" ./ | sh  2>/dev/null 1>&2 &
# disown the pid, so the inotify thread will get free from parent process
# and will not be terminated with it
PID=`ps aux | grep inotify | grep CLOSE_WRITE | grep -v grep | awk '{print $2}'`
disown $PID

# this is for new files, not modifications, optional
inotifywait --exclude .bzr -r -q -m -e CREATE --format="bzr add *; bzr commit -m 'new file added %w/%f'" ./ | sh  2>/dev/null 1>&2 &
PID=`ps aux | grep inotify | grep CREATE | grep -v grep | awk '{print $2}'`
disown $PID

exit 0;
```

And if you want to create a public resource, these lines will start a
bazaar server for the repository:

```bash
#!/bin/bash

# start bzr server
bzr serve --port=localhost:8888 --directory=/path/to/repository/directory/root 1>/dev/null 2>&1 &
PID=`ps aux | grep bzr | grep serve | grep -v grep | awk '{print $2}'`
disown $PID

exit 0;
```