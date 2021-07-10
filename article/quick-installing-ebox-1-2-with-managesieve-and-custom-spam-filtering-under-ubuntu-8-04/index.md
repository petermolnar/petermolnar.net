---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20111116135104/http://petermolnar.eu:80/sysadmin-blog/quick-installing-ebox-1-2-with-managesieve-and-custom-spam-filtering-under-ubuntu-8-04/
published: '2010-03-01T22:15:44+00:00'
redirect:
- quick-installing-ebox-1-2-with-managesieve-and-custom-spam-filtering-under-ubuntu-8-04-2
summary: Although eBox has it's own distribution, I wanted to get it work
    on Ubuntu 8.04 - but the version in the repo is only 1.0, and I really
    needed 1.2.
tags:
- e-mail
title: Quick installing eBox 1.2 with managesieve and custom spam filtering
    under Ubuntu 8.04

---

[eBox platform](http://www.ebox-platform.com/) is a Perl-based web
administration console for a linux small business server. When you own
one or not too many servers, and not only redneck linux sysadmins for
the tasks, eBox is a free choice over Microsoft solution. You can read a
lot more about it in forum, on it's site or Wikipedia.

Although eBox has it's own distribution, I wanted to get it work on
Ubuntu 8.04 - but the version in the repo is only 1.0, and I really
needed 1.2. Fortunatelly, eBox has a PPA site[^1], so it can be inserted
into Hardy. Open `/etc/apt/sources.list` with your favourite editor
(vim, vim, emacs, etc.) and add the following lines:

```bash
deb http://ppa.launchpad.net/ebox/1.2/ubuntu hardy main
deb-src http://ppa.launchpad.net/ebox/1.2/ubuntu hardy main
```

You'll also need an apt-key for this to get it work:

```bash
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 342D17AC
```

There's another PPA, published by Molnár Károly, a fellow Hungarian.
It's **very** important to put it in the **begining** of the file,
before the ubuntu standards! That is because the installed version by
apt is the first possibility on the list.

```bash
deb http://ppa.launchpad.net/karoly-molnar/dovecot-managesieve/ubuntu hardy main
deb-src http://ppa.launchpad.net/karoly-molnar/dovecot-managesieve/ubuntu hardy main
```

and the key:

```bash
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B498A2C
```

We're going to need this for Dovecot with Sieve, read on.

Updates repos,

```bash
apt-get update
```

and eBox is ready for install. I didn't need everything, so I just gave
the following command:

```bash
apt-get install ebox-antivirus ebox-firewall ebox-mail ebox-network ebox-objects ebox-services ebox-usersandgroups
```

This is going to install a **lot of** software, so be patient, and
prepare with enough bandwidth. After all, you can access your eBox
platform on <https://%5Byour> ip\]. I didn't install `ebox-mailfilter`
for reason. First of all, I don't really like amavisd, and second, it is
going to fail, and the whole mail system will going to stop because of
an error in the eBox stub naming related to amavisd: amavisd does not
read /etc/amavisd/amavisd.conf as it's conf file. If you rename it,
it'll work, but eBox keeps naming it back. So I looked for something
else as a solution. I needed to:

1.  install spamassassin
2.  add clamav plugin to it
3.  get a version of dovecot with sieve patch for local delivery
4.  change ebox settings about to use all of this.

We already added Károly Molnár's dovecot with sieve and a security
patch, so Dovecot with Managsieve is installed. The next thing is
spamassassin and it's clamav plugin.[^2]

```bash
apt-get install spamassassin spamc
```

```bash
cpan
```

CPAN will ask some questions at first run, just hit Enter, usually
that's enough. When the promt is ready, install

```perl
cpan> install File::Scan::ClamAV
cpan> exit
```

When it is complete, save the two files (clamav.cf, clamav.pm) from
<http://wiki.apache.org/spamassassin/ClamAVPlugin%5B%5E3%5D> into
`/etc/mail/spamassassin`

Now, nearly everything is complete, the last step is to modify the stubs
of eBox. This is not the best solution; an update could overwrite all
changes, the perfect solution would be to place regex patterned scripts
into `/etc/ebox/`, but that was too much for my taste. So I opened the
configuration templates from `/usr/share/ebox/stubs/mail/`and modified
what I needed.

```bash
vim /usr/share/ebox/stubs/mail/dovecot.conf.mas
```

Find the line started with `protocols =` and add `managesieve` after
`%&gt;` Managesieve listens on port 2000, you'll have to open this in
eBox firewall.

After `protocol POP3`, add the following:

```apache
##
## MANAGESIEVE specific settings
##

protocol managesieve {
# Login executable location.
login_executable = /usr/lib/dovecot/managesieve-login

# MANAGESIEVE executable location. See IMAP's mail_executable above for
# examples how this could be changed.
mail_executable = /usr/lib/dovecot/managesieve

# Maximum MANAGESIEVE command line length in bytes. This setting is
# directly borrowed from IMAP. But, since long command lines are very
# unlikely with MANAGESIEVE, changing this will not be very useful.
#managesieve_max_line_length = 65536

# Specifies the location of the symlink pointing to the active script in
# the sieve storage directory. This must match the SIEVE setting used by
# deliver (refer to http://wiki.dovecot.org/LDA/Sieve#location for more
# info). Variable substitution with % is recognized.
sieve=~/.dovecot.sieve

# This specifies the path to the directory where the uploaded scripts must
# be stored. In terms of '%' variable substitution it is identical to
# dovecot's mail_location setting used by the mail protocol daemons.
sieve_storage=~/sieve

# If, for some inobvious reason, the sieve_storage remains unset, the
# managesieve daemon uses the specification of the mail_location to find out
# where to store the sieve files (see explaination in README.managesieve).
# The example below, when uncommented, overrides any global mail_location
# specification and stores all the scripts in '~/mail/sieve' if sieve_storage
# is unset. However, you should always use the sieve_storage setting.
# mail_location = mbox:~/mail

# To fool managesieve clients that are focused on timesieved you can
# specify the IMPLEMENTATION capability that the dovecot reports to clients
# (default: dovecot).
#managesieve_implementation_string = Cyrus timsieved v2.2.13
}

##
## LDA specific settings
##

protocol lda {
# Address to use when sending rejection mails.
# postmaster_address = mail@domain

log_path = /var/log/dovecot.log
info_log_path = /var/log/dovecot.log

# Hostname to use in various parts of sent mails, eg. in Message-Id.
# Default is the system's real hostname.
#hostname =

# Support for dynamically loadable plugins. mail_plugins is a space separated
# list of plugins to load.
#mail_plugins =
#mail_plugin_dir = /usr/lib/dovecot/modules/lda

# Binary to use for sending mails.
#sendmail_path = /usr/lib/sendmail

# UNIX socket path to master authentication server to find users.
#auth_socket_path = /var/run/dovecot/auth-master

# Enabling Sieve plugin for server-side mail filtering
mail_plugins = cmusieve
}
```

And in `plugin {}` part insert

```bash
sieve

sieve_global_path = [your path]
```

The given path should be writeable by dovecot.

Save the file, and open the next one:

```bash
vim /usr/share/ebox/stubs/mail/main.cf.mas
```

Find the lines

```apache
virtual_transport = virtual
mailbox_transport = virtual
```

and replace `virtual` with `dovecot` so it would look like this:

```apache
mailbox_transport = dovecot
virtual_transport = dovecot
```

Save the file, and open the next:

```bash
vim /usr/share/ebox/stubs/mail/master.cf.mas
```

Search for the line:

```apache
dovecot   unix  -       n       n        -      -       pipe
```

and add this after:

```bash
 flags=DRhu user=ebox:ebox argv=/usr/bin/spamc -e /usr/lib/dovecot/deliver -d ${recipient} -f {sendder}
```

If there's something similar, replace it with this.

The system is now ready to use. What we've done now: the mail is
recieved by Postfix, than given to spamassassin (and clamav, with the
plugin), which adds the X-Spam and X-Spam-Virus headers, and then
Dovecot's Local Delivery Agent delivers it to the users maildir.

The only thing left is to create a default sieve filter, so create a
file named `sieve.default`, save it to the \[path\] you've given in the
dovecot.conf.mas as global sieve path, and add the following content to
it:

    require "fileinto";

        if header :contains "X-Spam-Virus" "Yes" {
            fileinto "Virus";
            stop;
        }
        if header :contains "X-Spam-Flag" "YES" {
            fileinto "Junk";
            stop;
        }

Enjoy. Roundcube[^3] has a perfect plugin to configure sieve filters per
user.

**UPDATE:** According to Dovecot Prebuild binaries page[^4], all Ubuntu
releases are built with managesieve, so the additional apt source can be
skipped. I tested it; I seems to be true.

[^1]: <https://launchpad.net/~ebox/+archive/1.2>

[^2]: <http://wiki.apache.org/spamassassin/ClamAVPlugin>

[^3]: <http://roundcube.net/>

[^4]: <http://wiki.dovecot.org/PrebuiltBinaries>