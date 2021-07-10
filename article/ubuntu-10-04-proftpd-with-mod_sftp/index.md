---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20120314220818/http://petermolnar.eu:80/linux-tech-coding/ubuntu-10-04-proftpd-with-mod_sftp
published: '2010-12-15T18:46:07+00:00'
summary: 'SFTP enabled FTP: secure, chrooted FTP server.'
tags:
- linux
title: Ubuntu 10.04 ProFTPd with mod_sftp

---

The last releases of ProFTP contan a module, called mod\_sftp. Yes. This
is just the thing I was searching for years, trying to achive chrooted
ssh with OpenSSH (see internal SFTP option), but now with a lot better
solution.

But the thing is... Ubuntu's last LTS, 10.04 only has a version lower of
ProFTPd. Compile? Yes, one solution, the hardcore way. The lazy way:
Debian Sid, the current unstable version, and it's packages:

First, the two dependency package:

-   libncurses5[^1]
-   libssl0.9.8[^2]

And the ProFTPd itself:

-   proftpd-basic[^3]

Install them:

```bash
dpkg -i *
```

Edit `/etc/proftpd/modules.conf`:

comment out the line, we don't need it for now.

```apache
LoadModule                mod_tls.c
```

add a line

```apache
LoadModule                mod_sftp.c
```

Also, edit `/etc/proftpd/proftpd.conf`, and add the following:

```apache
<ifmodule mod_sftp.c>

SFTPEngine on
SFTPLog /var/log/proftpd/sftp.log
TransferLog /var/log/proftpd/xferlog-sftp.log

# Configure the server to listen on the normal SSH2 port, port 22
Port 22

# Configure both the RSA and DSA host keys, using the same host key
# files that OpenSSH uses.
SFTPHostKey /etc/ssh/ssh_host_rsa_key
SFTPHostKey /etc/ssh/ssh_host_dsa_key

# Configure the file used for comparing authorized public keys of users.
SFTPAuthorizedUserKeys file:~/.sftp/authorized_keys

# Enable compression
SFTPCompression delayed

# Allow the same number of authentication attempts as OpenSSH.
#
# It is recommended that you explicitly configure MaxLoginAttempts
# for your SSH2/SFTP instance to be higher than the normal
# MaxLoginAttempts value for FTP, as there are more ways to authenticate
# using SSH2.
MaxLoginAttempts 3

</ifmodule>
```

You'll also need the change the port of the OpenSSH server, but that's
recommended anyway.

[^1]: <http://packages.debian.org/sid/amd64/libncurses5/download>

[^2]: <http://packages.debian.org/sid/amd64/libssl0.9.8/download>

[^3]: <http://packages.debian.org/en/sid/amd64/proftpd-basic/download>