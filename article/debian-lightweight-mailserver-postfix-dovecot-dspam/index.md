---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20141021051830/https://petermolnar.eu/linux-tech-coding/debian-lightweight-mailserver-postfix-dovecot-dspam/
published: '2014-10-14T09:00:34+00:00'
summary: Configurations for a light memory use, spamfiltering, secure mailserver
    on linux.
tags:
- e-mail
title: Lightweight, secure, database-free, spamfiltering mail server with
    Postfix, Dovecot, openDKIM and dspam on Debian 7

---

<ins datetime="2016-03-08T10:48:16+00:00">
</ins>
## Update 2016-03-08

I wasn't aware Dovecot is case-sensitive by default and this led to
strange situations. Many thanks to the entry Roundcube, Dovecot IMAP and
case sensitive user names[^1] for pointing at the solution.

<ins datetime="2014-11-06T14:36:32+00:00">
</ins>
## Update 2014-11-06

It turned out that the hash segment size was misconfigured earlier and
it resulted in filled up disk space. Fixed now. Also replaced CRYPT with
SHA512-CRYPT.

------------------------------------------------------------------------

## Forewords

I've been using this setup with MySQL as a backend for years; I've moved
away from the database approach for various reasons recently. One of
them was to be able to easily sync the whole server for a secondary
place where the MySQL replication constantly failed due to a somewhat
flaky connection.

If you have a small, rarely chaning system, just stick to the plain text
configs.

## Disclaimer

Although I'm using this setup it does not neccessarily mean it will
works flawlessly for you. This little tutorial is provided without any
warranty or even promise that it will fit your needs.

Even though I've tried to create a copy-paste tutorial here things might
be missing. If you find any goofs, please drop me a mail or similar.

## Prerequisities

Create a user for the virtual mailboxes:

    addgroup --gid 5000 vmail
    adduser --uid 5000 --home /home/vmail --gid vmail --disabled-password vmail

Install the required software:

```bash
apt-get install dspam libdspam7-drv-hash opendkim opendkim-tools memcached postfix postfix-pcre dovecot-antispam dovecot-core dovecot-imapd dovecot-managesieved dovecot-sieve
```

During the process, postfix will ask for it's configuration; it does not
matter what you choose as it will be overwritten.

## Postfix

Generate dhparam files for SPF:

```bash
cd /etc/postfix
openssl dhparam -out dh2048.tmp 2048 && mv dh2048.tmp dh2048.pem
openssl dhparam -out dh1024.tmp 2048 && mv dh1024.tmp dh1024.pem
openssl dhparam -out dh512.tmp 2048 && mv dh512.tmp dh512.pem
```

### `/etc/postfix/main.cf`

```apache
smtpd_banner = your.mailhost.reverse.dns
biff = no
append_dot_mydomain = no
delay_warning_time = 4h
readme_directory = no
mailbox_size_limit = 0
message_size_limit = 52428800
#recipient_delimiter = +
inet_interfaces = all
maximal_queue_lifetime = 1d
queue_run_delay = 300s
minimal_backoff_time = 300s
bounce_queue_lifetime = 1d
myhostname = your.mailhost.reverse.dns
myorigin = your.mailhost.reverse.dns
mydestination = $myhostname localhost localhost.localdomain
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128

virtual_mailbox_domains = hash:/etc/postfix/maps/domain
virtual_mailbox_maps = hash:/etc/postfix/maps/mailbox
virtual_alias_domains = hash:/etc/postfix/maps/aliasdomain
virtual_alias_maps = hash:/etc/postfix/maps/alias

virtual_mailbox_base = /home/vmail
virtual_uid_maps = static:5000
virtual_gid_maps = static:5000

virtual_transport=dovecot

dovecot_destination_recipient_limit = 1
dspam_destination_recipient_limit = 1

## TLS & SSL
smtp_use_tls=yes
smtpd_use_tls=yes
smtpd_tls_security_level = may
smtpd_tls_received_header = yes
tls_random_source = dev:/dev/urandom

smtpd_tls_cert_file = /etc/ssl/your.domain.cert.pem
smtpd_tls_key_file  = /etc/ssl/your.domain.cert.key

smtpd_tls_session_cache_timeout = 3600s
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache

smtpd_sasl_auth_enable = yes
smtpd_sasl_security_options = noanonymous
broken_sasl_auth_clients = yes
smtpd_sasl_authenticated_header = yes
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth

smtpd_tls_ciphers = high
smtpd_tls_exclude_ciphers = aNULL, DES, 3DES, MD5, DES+MD5, RC4
smtpd_tls_protocols = !SSLv3, !SSLv2

# forward secrecy
smtpd_tls_eecdh_grade = strong
tls_eecdh_strong_curve = prime256v1
tls_eecdh_ultra_curve = secp384r1
smtpd_tls_dh1024_param_file = ${config_directory}/dh2048.pem
smtpd_tls_dh512_param_file = ${config_directory}/dh512.pem
tls_preempt_cipherlist = yes

## POSTSCREEN
postscreen_access_list = permit_mynetworks
postscreen_dnsbl_sites = ix.dnsbl.manitu.net*1 zen.spamhaus.org*2 dnsbl-1.uceprotect.net*1 smtp.dnsbl.sorbs.net*1 web.dnsbl.sorbs.net*1

postscreen_dnsbl_action = enforce
postscreen_greet_action = enforce

postscreen_cache_map = memcache:/etc/postfix/postscreen_cache
postscreen_cache_cleanup_interval = 0
postscreen_dnsbl_ttl = 60m

smtpd_helo_required = yes

smtpd_client_restrictions = permit_mynetworks,
    permit_sasl_authenticated

smtpd_helo_restrictions = permit_mynetworks,
    reject_invalid_helo_hostname,
    permit

smtpd_sender_restrictions = reject_unknown_sender_domain,
    check_sender_mx_access pcre:/etc/postfix/regex_blacklist,
    check_sender_access pcre:/etc/postfix/regex_blacklist,
    check_sender_ns_access pcre:/etc/postfix/regex_blacklist,
    permit

smtpd_recipient_restrictions =     permit_mynetworks,
    permit_sasl_authenticated,
    reject_invalid_hostname,
     reject_non_fqdn_recipient,
    reject_unknown_recipient_domain,
    reject_unauth_pipelining,
    reject_unauth_destination,
    check_client_access pcre:/etc/postfix/dspam_filter_access,
    permit

# DKIM
milter_default_action = accept
milter_protocol = 2
smtpd_milters = inet:127.0.0.1:8891
non_smtpd_milters = inet:127.0.0.1:8891
```

### `/etc/postfix/master.cf`

```apache
smtpd     pass  -       -       n       -       -       smtpd
smtp      inet  n       -       n       -       1       postscreen
smtps     inet  n       -       -       -       -       smtpd
587       inet  n       -       -       -       -       smtpd
tlsproxy  unix  -       -       n       -       0       tlsproxy
dnsblog   unix  -       -       n       -       0       dnsblog

#smtp      inet  n       -       -       -       -       smtpd

pickup    fifo  n       -       -       60      1       pickup
cleanup   unix  n       -       -       -       0       cleanup
qmgr      fifo  n       -       n       300     1       qmgr
tlsmgr    unix  -       -       -       1000?   1       tlsmgr
rewrite   unix  -       -       -       -       -       trivial-rewrite
bounce    unix  -       -       -       -       0       bounce
defer     unix  -       -       -       -       0       bounce
trace     unix  -       -       -       -       0       bounce
verify    unix  -       -       -       -       1       verify
flush     unix  n       -       -       1000?   0       flush
proxymap  unix  -       -       n       -       -       proxymap
proxywrite unix -       -       n       -       1       proxymap
smtp      unix  -       -       -       -       -       smtp
relay     unix  -       -       -       -       -       smtp
showq     unix  n       -       -       -       -       showq
error     unix  -       -       -       -       -       error
retry     unix  -       -       -       -       -       error
discard   unix  -       -       -       -       -       discard
local     unix  -       n       n       -       -       local
virtual   unix  -       n       n       -       -       virtual
lmtp      unix  -       -       -       -       -       lmtp
anvil     unix  -       -       -       -       1       anvil
scache    unix  -       -       -       -       1       scache

dovecot   unix  -       n       n       -       -       pipe
  flags=DRhu user=vmail:vmail argv=/usr/lib/dovecot/deliver -f ${sender} -d ${recipient}

dspam     unix  -       n       n       -       32      pipe
  flags=Ru user=vmail:vmail argv=/usr/bin/dspam --client --deliver=innocent,spam --user ${recipient} --mail-from=${sender}

127.0.0.1:25025 inet n  -       n       -        -      smtpd
  -o content_filter=
  -o receive_override_options=no_unknown_recipient_checks,no_header_body_checks
  -o smtpd_helo_restrictions=
  -o smtpd_client_restrictions=
  -o smtpd_sender_restrictions=
  -o smtpd_recipient_restrictions=permit_mynetworks,reject
  -o mynetworks=127.0.0.0/8,192.168.42.0/24
  -o smtpd_authorized_xforward_hosts=127.0.0.0/8,192.168.42.0/24
```

The alternative 25025 port is for the DSPAM delivery agent that will
send the message back once it's done.

### `/etc/postfix/postscreen_cache`

Postscreen can be rather slow, so a cache does not really matter;
memcached is easy enough to set up and it's built-in already.

```apache
memcache = inet:127.0.0.1:11211
key_format = postscreen:%s
```

### `/etc/postfix/dspam_filter_access`

The ddspam filter access file is to tell which master.cf route to use as
name:filter\_route format.

```apache
# Everything beginning with either ham or spam avoids the filter
/^(spam|ham)@.*$/ OK

# The rest is redirected to be filtered
/./ FILTER dspam:dspam
```

### `/etc/postfix/regex_blacklist`

The regex blacklist file contains domain names you explicitly want to
send to hell. It's useful when you receive spams from directions easy to
define by sender domain.

```apache
/gigaplaza\.sk$/    REJECT Byez
```

### Mappings

#### `/etc/postfix/maps/alias`

If you need virtual aliases.

```apache
abuse@your.other.domain        abuse@your.domain
hostmaster@your.other.domain    hostmaster@your.domain
postmaster@your.other.domain    postmaster@your.domain
webmaster@your.other.domain    webmaster@your.domain
```

#### `/etc/postfix/maps/aliasdomain`

If you want to use virtual alias domains.

```apache
your.other2.domain your.domain
```

#### `/etc/postfix/maps/domain`

Domains you want to accept mail for.

```apache
your.domain
your.other.domain
```

#### `/etc/postfix/maps/mailbox`

Virtual mailboxes. The `the_directory_name_for_the_address` will be
created under the `virtual_mailbox_base` specified in main.cf.

```apache
you@your.domain the_directory_name_for_the_address/
```

#### `/etc/postfix/maps/user`

This well be the password file for dovecot. Since we're not using local
users, we need a virtual users table.

```apache
you@your.domain:SHA512_hashed_password_for_the_mailbox
```

For a hashed password:

```bash
mkpasswd --method=sha-512
```

## memcached

Just install memcached with the defaults; no need for any changes in the
configuration.

## dspam

Dspam needs a lot of training, but once trained enough, it's dead
accurate, small and fast.

### `/etc/dspam/default.prefs`

```apache

trainingMode=TEFT
spamAction=deliver
spamSubject=
enableBNR=on
enableWhitelist=on
statisticalSedation=5
signatureLocation=headers
whitelistThreshold=10
showFactors=off
optIn=off
optOut=off
```

### `/etc/dspam/dspam.conf`

    Home /var/spool/dspam

    StorageDriver /usr/lib/x86_64-linux-gnu/dspam/libhash_drv.so
    HashRecMax 49157
    HashAutoExtend on
    HashMaxExtents 1024
    HashExtentSize 49157
    HashPctIncrease        10
    HashMaxSeek        10
    HashConnectionCache    20

    TrustedDeliveryAgent "/usr/sbin/sendmail"
    UntrustedDeliveryAgent "/usr/lib/dovecot/deliver -d %u"

    DeliveryHost        127.0.0.1
    DeliveryPort        25025
    DeliveryIdent        dspam.your.mailhost.reverse.dns
    DeliveryProto        SMTP

    OnFail error

    Trust root
    Trust dspam
    Trust postfix
    Trust vmail
    Trust dspam-user

    # Debug *

    TrainingMode teft
    TestConditionalTraining on
    Feature tb=3

    Algorithm graham burton
    Tokenizer osb
    PValue bcr

    WebStats on

    ImprobabilityDrive on

    Preference "signatureLocation=headers"
    Preference "showFactors=off"
    Preference "spamAction=deliver"
    Preference "spamSubject="
    Preference "optIn=off"
    Preference "optOut=off"

    Notifications    off

    PurgeSignatures 14    # Stale signatures
    PurgeNeutral    90    # Tokens with neutralish probabilities
    PurgeUnused    90    # Unused tokens
    PurgeHapaxes    30    # Tokens with less than 5 hits (hapaxes)
    PurgeHits1S    15    # Tokens with only 1 spam hit
    PurgeHits1I    15    # Tokens with only 1 innocent hit

    LocalMX 192.168.1.0/24 127.0.0.1

    SystemLog    on
    UserLog        on

    TrainPristine off

    Opt out

    TackSources spam virus

    ParseToHeaders on
    ChangeModeOnParse on
    ChangeUserOnParse full

    MaxMessageSize 4194304

    ServerHost        127.0.0.1
    ServerPort        2424
    ServerQueueSize    32
    ServerPID        /var/run/dspam/dspam.pid
    ServerMode auto

    ServerPass.client "a_random_client_id"

    ServerParameters "--deliver=innocent,spam -d %u"
    ServerIdent    "your.hostname"

    ClientHost    127.0.0.1
    ClientPort    2424
    ClientIdent    "a_random_client_id@client"

    ProcessorURLContext on
    ProcessorBias on
    StripRcptDomain off

    IgnoreHeader Accept-Language
    IgnoreHeader Approved
    IgnoreHeader Archive
    IgnoreHeader Authentication-Results
    IgnoreHeader Cache-Post-Path
    IgnoreHeader Cancel-Key
    IgnoreHeader Cancel-Lock
    IgnoreHeader Complaints-To
    IgnoreHeader Content-Description
    IgnoreHeader Content-Disposition
    IgnoreHeader Content-ID
    IgnoreHeader Content-Language
    IgnoreHeader Content-Return
    IgnoreHeader Content-Transfer-Encoding
    IgnoreHeader Content-Type
    IgnoreHeader DKIM-Signature
    IgnoreHeader Date
    IgnoreHeader Disposition-Notification-To
    IgnoreHeader DomainKey-Signature
    IgnoreHeader Importance
    IgnoreHeader In-Reply-To
    IgnoreHeader Injection-Info
    IgnoreHeader Lines
    IgnoreHeader Message-Id
    IgnoreHeader Message-ID
    IgnoreHeader NNTP-Posting-Date
    IgnoreHeader NNTP-Posting-Host
    IgnoreHeader Newsgroups
    IgnoreHeader OpenPGP
    IgnoreHeader Organization
    IgnoreHeader Originator
    IgnoreHeader PGP-ID
    IgnoreHeader Path
    IgnoreHeader Received
    IgnoreHeader Received-SPF
    IgnoreHeader References
    IgnoreHeader Reply-To
    IgnoreHeader Resent-Date
    IgnoreHeader Resent-From
    IgnoreHeader Resent-Message-ID
    IgnoreHeader Thread-Index
    IgnoreHeader Thread-Topic
    IgnoreHeader User-Agent
    IgnoreHeader X--MailScanner-SpamCheck
    IgnoreHeader X-AV-Scanned
    IgnoreHeader X-AVAS-Spam-Level
    IgnoreHeader X-AVAS-Spam-Score
    IgnoreHeader X-AVAS-Spam-Status
    IgnoreHeader X-AVAS-Spam-Symbols
    IgnoreHeader X-AVAS-Virus-Status
    IgnoreHeader X-AVK-Virus-Check
    IgnoreHeader X-Abuse
    IgnoreHeader X-Abuse-Contact
    IgnoreHeader X-Abuse-Info
    IgnoreHeader X-Abuse-Management
    IgnoreHeader X-Abuse-To
    IgnoreHeader X-Abuse-and-DMCA-Info
    IgnoreHeader X-Accept-Language
    IgnoreHeader X-Admission-MailScanner-SpamCheck
    IgnoreHeader X-Admission-MailScanner-SpamScore
    IgnoreHeader X-Amavis-Alert
    IgnoreHeader X-Amavis-Hold
    IgnoreHeader X-Amavis-Modified
    IgnoreHeader X-Amavis-OS-Fingerprint
    IgnoreHeader X-Amavis-PenPals
    IgnoreHeader X-Amavis-PolicyBank
    IgnoreHeader X-AntiVirus
    IgnoreHeader X-Antispam
    IgnoreHeader X-Antivirus
    IgnoreHeader X-Antivirus-Scanner
    IgnoreHeader X-Antivirus-Status
    IgnoreHeader X-Archive
    IgnoreHeader X-Assp-Spam-Prob
    IgnoreHeader X-Attention
    IgnoreHeader X-BTI-AntiSpam
    IgnoreHeader X-Barracuda
    IgnoreHeader X-Barracuda-Bayes
    IgnoreHeader X-Barracuda-Spam-Flag
    IgnoreHeader X-Barracuda-Spam-Report
    IgnoreHeader X-Barracuda-Spam-Score
    IgnoreHeader X-Barracuda-Spam-Status
    IgnoreHeader X-Barracuda-Virus-Scanned
    IgnoreHeader X-Bogosity
    IgnoreHeader X-Brightmail-Tracker
    IgnoreHeader X-CRM114-CacheID
    IgnoreHeader X-CRM114-Status
    IgnoreHeader X-CRM114-Version
    IgnoreHeader X-CTASD-IP
    IgnoreHeader X-CTASD-RefID
    IgnoreHeader X-CTASD-Sender
    IgnoreHeader X-Cache
    IgnoreHeader X-ClamAntiVirus-Scanner
    IgnoreHeader X-Comment-To
    IgnoreHeader X-Comments
    IgnoreHeader X-Complaints
    IgnoreHeader X-Complaints-Info
    IgnoreHeader X-Complaints-To
    IgnoreHeader X-DKIM
    IgnoreHeader X-DMCA-Complaints-To
    IgnoreHeader X-DMCA-Notifications
    IgnoreHeader X-Despammed-Tracer
    IgnoreHeader X-ELTE-SpamCheck
    IgnoreHeader X-ELTE-SpamCheck-Details
    IgnoreHeader X-ELTE-SpamScore
    IgnoreHeader X-ELTE-SpamVersion
    IgnoreHeader X-ELTE-VirusStatus
    IgnoreHeader X-Enigmail-Supports
    IgnoreHeader X-Enigmail-Version
    IgnoreHeader X-Extra-Info
    IgnoreHeader X-Face
    IgnoreHeader X-Forwarded
    IgnoreHeader X-GMX-Antispam
    IgnoreHeader X-GMX-Antivirus
    IgnoreHeader X-GPG-Fingerprint
    IgnoreHeader X-GPG-Key-ID
    IgnoreHeader X-GPS-DegDec
    IgnoreHeader X-GPS-MGRS
    IgnoreHeader X-GWSPAM
    IgnoreHeader X-Gateway
    IgnoreHeader X-Greylist
    IgnoreHeader X-HTMLM
    IgnoreHeader X-HTMLM-Info
    IgnoreHeader X-HTMLM-Score
    IgnoreHeader X-HTTP-Posting-Host
    IgnoreHeader X-HTTP-UserAgent
    IgnoreHeader X-HTTP-Via
    IgnoreHeader X-ID
    IgnoreHeader X-IMAIL-SPAM-STATISTICS
    IgnoreHeader X-IMAIL-SPAM-URL-DBL
    IgnoreHeader X-IMAIL-SPAM-VALFROM
    IgnoreHeader X-IMAIL-SPAM-VALHELO
    IgnoreHeader X-IMAIL-SPAM-VALREVDNS
    IgnoreHeader X-Info
    IgnoreHeader X-IronPort-Anti-Spam-Filtered
    IgnoreHeader X-IronPort-Anti-Spam-Result
    IgnoreHeader X-KSV-Antispam
    IgnoreHeader X-Kaspersky-Antivirus
    IgnoreHeader X-MDAV-Processed
    IgnoreHeader X-MDRemoteIP
    IgnoreHeader X-MDaemon-Deliver-To
    IgnoreHeader X-MIE-MailScanner-SpamCheck
    IgnoreHeader X-MIMEOLE
    IgnoreHeader X-MIMETrack
    IgnoreHeader X-MMS-Spam-Filter-ID
    IgnoreHeader X-MS-Has-Attach
    IgnoreHeader X-MS-TNEF-Correlator
    IgnoreHeader X-MSMail-Priority
    IgnoreHeader X-MailScanner
    IgnoreHeader X-MailScanner-Information
    IgnoreHeader X-MailScanner-SpamCheck
    IgnoreHeader X-Mailer
    IgnoreHeader X-Mlf-Spam-Status
    IgnoreHeader X-NAI-Spam-Checker-Version
    IgnoreHeader X-NAI-Spam-Flag
    IgnoreHeader X-NAI-Spam-Level
    IgnoreHeader X-NAI-Spam-Report
    IgnoreHeader X-NAI-Spam-Route
    IgnoreHeader X-NAI-Spam-Rules
    IgnoreHeader X-NAI-Spam-Score
    IgnoreHeader X-NAI-Spam-Threshold
    IgnoreHeader X-NEWT-spamscore
    IgnoreHeader X-NNTP-Posting-Date
    IgnoreHeader X-NNTP-Posting-Host
    IgnoreHeader X-NetcoreISpam1-ECMScanner
    IgnoreHeader X-NetcoreISpam1-ECMScanner-From
    IgnoreHeader X-NetcoreISpam1-ECMScanner-Information
    IgnoreHeader X-NetcoreISpam1-ECMScanner-SpamCheck
    IgnoreHeader X-NetcoreISpam1-ECMScanner-SpamScore
    IgnoreHeader X-Newsreader
    IgnoreHeader X-Newsserver
    IgnoreHeader X-No-Archive
    IgnoreHeader X-No-Spam
    IgnoreHeader X-OSBF-Lua-Score
    IgnoreHeader X-OWM-SpamCheck
    IgnoreHeader X-OWM-VirusCheck
    IgnoreHeader X-Olypen-Virus
    IgnoreHeader X-Orig-Path
    IgnoreHeader X-OriginalArrivalTime
    IgnoreHeader X-Originating-IP
    IgnoreHeader X-PAA-AntiVirus
    IgnoreHeader X-PAA-AntiVirus-Message
    IgnoreHeader X-PGP-Fingerprint
    IgnoreHeader X-PGP-Hash
    IgnoreHeader X-PGP-ID
    IgnoreHeader X-PGP-Key
    IgnoreHeader X-PGP-Key-Fingerprint
    IgnoreHeader X-PGP-KeyID
    IgnoreHeader X-PGP-Sig
    IgnoreHeader X-PIRONET-NDH-MailScanner-SpamCheck
    IgnoreHeader X-PIRONET-NDH-MailScanner-SpamScore
    IgnoreHeader X-PMX
    IgnoreHeader X-PMX-Version
    IgnoreHeader X-PN-SPAMFiltered
    IgnoreHeader X-Posting-Agent
    IgnoreHeader X-Posting-ID
    IgnoreHeader X-Posting-IP
    IgnoreHeader X-Priority
    IgnoreHeader X-Proofpoint-Spam-Details
    IgnoreHeader X-Qmail-Scanner-1.25st
    IgnoreHeader X-Quarantine-ID
    IgnoreHeader X-RAV-AntiVirus
    IgnoreHeader X-RITmySpam
    IgnoreHeader X-RITmySpam-IP
    IgnoreHeader X-RITmySpam-Spam
    IgnoreHeader X-Rc-Spam
    IgnoreHeader X-Rc-Virus
    IgnoreHeader X-Received-Date
    IgnoreHeader X-RedHat-Spam-Score
    IgnoreHeader X-RedHat-Spam-Warning
    IgnoreHeader X-RegEx
    IgnoreHeader X-RegEx-Score
    IgnoreHeader X-Rocket-Spam
    IgnoreHeader X-SA-GROUP
    IgnoreHeader X-SA-RECEIPTSTATUS
    IgnoreHeader X-STA-NotSpam
    IgnoreHeader X-STA-Spam
    IgnoreHeader X-Scam-grey
    IgnoreHeader X-Scanned-By
    IgnoreHeader X-SenderID
    IgnoreHeader X-Sohu-Antivirus
    IgnoreHeader X-Spam
    IgnoreHeader X-Spam-ASN
    IgnoreHeader X-Spam-Check
    IgnoreHeader X-Spam-Checked-By
    IgnoreHeader X-Spam-Checker
    IgnoreHeader X-Spam-Checker-Version
    IgnoreHeader X-Spam-Clean
    IgnoreHeader X-Spam-DCC
    IgnoreHeader X-Spam-Details
    IgnoreHeader X-Spam-Filter
    IgnoreHeader X-Spam-Filtered
    IgnoreHeader X-Spam-Flag
    IgnoreHeader X-Spam-Level
    IgnoreHeader X-Spam-OrigSender
    IgnoreHeader X-Spam-Pct
    IgnoreHeader X-Spam-Prev-Subject
    IgnoreHeader X-Spam-Processed
    IgnoreHeader X-Spam-Pyzor
    IgnoreHeader X-Spam-Rating
    IgnoreHeader X-Spam-Report
    IgnoreHeader X-Spam-Scanned
    IgnoreHeader X-Spam-Score
    IgnoreHeader X-Spam-Status
    IgnoreHeader X-Spam-Tagged
    IgnoreHeader X-Spam-Tests
    IgnoreHeader X-Spam-Tests-Failed
    IgnoreHeader X-Spam-Virus
    IgnoreHeader X-Spam-Warning
    IgnoreHeader X-Spam-detection-level
    IgnoreHeader X-SpamAssassin-Clean
    IgnoreHeader X-SpamAssassin-Warning
    IgnoreHeader X-SpamBouncer
    IgnoreHeader X-SpamCatcher-Score
    IgnoreHeader X-SpamCop-Checked
    IgnoreHeader X-SpamCop-Disposition
    IgnoreHeader X-SpamCop-Whitelisted
    IgnoreHeader X-SpamDetected
    IgnoreHeader X-SpamInfo
    IgnoreHeader X-SpamPal
    IgnoreHeader X-SpamPal-Timeout
    IgnoreHeader X-SpamReason
    IgnoreHeader X-SpamScore
    IgnoreHeader X-SpamTest-Categories
    IgnoreHeader X-SpamTest-Info
    IgnoreHeader X-SpamTest-Method
    IgnoreHeader X-SpamTest-Status
    IgnoreHeader X-SpamTest-Version
    IgnoreHeader X-Spamadvice
    IgnoreHeader X-Spamarrest-noauth
    IgnoreHeader X-Spamarrest-speedcode
    IgnoreHeader X-Spambayes-Classification
    IgnoreHeader X-Spamcount
    IgnoreHeader X-Spamsensitivity
    IgnoreHeader X-TERRACE-SPAMMARK
    IgnoreHeader X-TERRACE-SPAMRATE
    IgnoreHeader X-TM-AS-Category-Info
    IgnoreHeader X-TM-AS-MatchedID
    IgnoreHeader X-TM-AS-Product-Ver
    IgnoreHeader X-TM-AS-Result
    IgnoreHeader X-TMWD-Spam-Summary
    IgnoreHeader X-TNEFEvaluated
    IgnoreHeader X-Text-Classification
    IgnoreHeader X-Text-Classification-Data
    IgnoreHeader X-Trace
    IgnoreHeader X-UCD-Spam-Score
    IgnoreHeader X-User-Agent
    IgnoreHeader X-User-ID
    IgnoreHeader X-User-System
    IgnoreHeader X-Virus-Check
    IgnoreHeader X-Virus-Checked
    IgnoreHeader X-Virus-Checker-Version
    IgnoreHeader X-Virus-Scan
    IgnoreHeader X-Virus-Scanned
    IgnoreHeader X-Virus-Scanner
    IgnoreHeader X-Virus-Scanner-Result
    IgnoreHeader X-Virus-Status
    IgnoreHeader X-VirusChecked
    IgnoreHeader X-Virusscan
    IgnoreHeader X-WSS-ID
    IgnoreHeader X-WinProxy-AntiVirus
    IgnoreHeader X-WinProxy-AntiVirus-Message
    IgnoreHeader X-cid
    IgnoreHeader X-iHateSpam-Checked
    IgnoreHeader X-iHateSpam-Quarantined
    IgnoreHeader X-policyd-weight
    IgnoreHeader X-purgate
    IgnoreHeader X-purgate-Ad
    IgnoreHeader X-purgate-ID
    IgnoreHeader X-sgxh1
    IgnoreHeader X-to-viruscore
    IgnoreHeader Xref
    IgnoreHeader acceptlanguage
    IgnoreHeader thread-index
    IgnoreHeader x-uscspam
    IgnoreHeader X-Paranoid-Spam
    IgnoreHeader X-Paranoid-Prob
    IgnoreHeader X-Paranoid-Report
    IgnoreHeader X-ArGoMail-Read

### `/etc/default/dspam`

```apache
START=yes
USER=dspam
OPTIONS=""
RUN_NOTIFY="no"
```

## Dovecot

### `/etc/dovecot/dovecot.conf`

Main dovecot config file; not too many things to see here.

```apache
## Dovecot configuration file

# Enable installed protocols
!include_try /usr/share/dovecot/protocols.d/*.protocol
listen = *, ::
instance_name = dovecot
login_greeting = mail
shutdown_clients = yes
default_vsz_limit = 64M
default_internal_user = vmail
!include conf.d/*.conf
```

### `/etc/dovecot/conf.d/10-auth.conf`

Dovecot authentication setup; this will provide the auth socket for
Postfix as well.

```apache
##
## Authentication processes
##

#   plain login digest-md5 cram-md5 ntlm rpa apop anonymous gssapi otp skey
#   gss-spnego
auth_cache_size = 1024
auth_cache_ttl = 1 hour
auth_cache_negative_ttl = 1 hour
auth_worker_max_count = 128
auth_mechanisms = plain login
auth_username_format = %Lu


##
## Password and user databases
##

passdb {
    driver = passwd-file
    args = scheme=SHA512-CRYPT /etc/postfix/maps/user
}

userdb {
    driver = static
    args = uid=5000 gid=5000 home=/home/vmail/%Lu
}

service auth {
    user = root

    unix_listener auth-userdb {
        mode = 0666
        user = $default_internal_user
        group = $default_internal_user
    }

    # Postfix smtp-auth
    unix_listener /var/spool/postfix/private/auth {
        mode = 0666
        user = postfix
        group = postfix
    }
}

service auth-worker {
    user = $default_internal_user
}
```

### `/etc/dovecot/conf.d/10-logging.conf`

Set logging to syslog so you'll have it all in one place.

```apache
##
## Log destination.
##

log_path = syslog
syslog_facility = mail

##
## Logging verbosity and debugging.
##

auth_verbose = no
auth_verbose_passwords = no
auth_debug = no
auth_debug_passwords = no

mail_debug = no
verbose_ssl = no

##
## Log formatting.
##

log_timestamp = "%Y-%m-%d %H:%M:%S "

# Format to use for logging mail deliveries. You can use variables:
#  %$ - Delivery status message (e.g. "saved to INBOX")
#  %m - Message-ID
#  %s - Subject
#  %f - From address
#  %p - Physical size
#  %w - Virtual size
deliver_log_format = msgid=%m: %$
```

### `/etc/dovecot/conf.d/10-mail.conf`

Mailbox setup.

```apache
##
## Mailbox locations and namespaces
##

mail_location = maildir:~/Maildir

namespace inbox {
    inbox = yes

    mailbox Drafts {
        special_use = \Drafts
    }

    mailbox Spam {
        special_use = \Junk
    }

    mailbox Trash {
        special_use = \Trash
    }

    mailbox Sent {
        special_use = \Sent
    }
}

mail_privileged_group = mail
```

### `/etc/dovecot/conf.d/10-ssl.conf`

Security for dovecot.

```apache
##
## SSL settings
##

ssl = yes

ssl_cert = </etc/ssl/your.domain.cert.pem
ssl_key  = </etc/ssl/your.domain.cert.key

# SSL protocols to use
ssl_protocols = !SSLv2 !SSLv3

# SSL ciphers to use
ssl_cipher_list = ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA:AES128-GCM-SHA256:AES128-SHA:HIGH:!ADH:!EXP:!LOW:!RC2:!3DES:!SEED:!MD5:!aNULL:!EDH:!CAMELLIA:!MEDIUM:!RC4:!eNULL;

# SSL crypto device to use, for valid values run "openssl engine"
ssl_crypto_device = rsax
```

### `/etc/dovecot/conf.d/15-lda.conf`

Local delivery agent setup

```apache
##
## LDA specific settings (also used by LMTP)
##

postmaster_address = postmaster@your.domain
hostname = your.hostname

rejection_subject = Rejected: %s
rejection_reason = Message <%t> was rejected:%n%r

lda_mailbox_autocreate = yes
lda_mailbox_autosubscribe = yes

protocol lda {
    log_path = syslog
    mail_plugins = $mail_plugins sieve
    mail_fsync = optimized
}
```

### `/etc/dovecot/conf.d/20-imap.conf`

The IMAP server setup itself.

```apache
##
## IMAP specific settings
##

protocol imap {
    mail_max_userip_connections = 512
    imap_idle_notify_interval = 24 mins
    mail_plugins = $mail_plugins antispam
}

service imap-login {
    # enabled if you want non-ssl imap
    #inet_listener imap {
    #    port = 143
    #}

    inet_listener imaps {
        port = 993
        ssl = yes
    }

}

service imap {
#    process_limit = 64
}
```

### `/etc/dovecot/conf.d/20-lmtp.conf`

```apache
##
## LMTP specific settings
##

protocol lmtp {
    #auth_socket_path = director-userdb
    mail_fsync = optimized
    mail_plugins = $mail_plugins sieve
}

service lmtp {
    user = vmail

    unix_listener lmtp {
        mode = 0666
    }

    inet_listener lmtp {
        address = 127.0.0.1
        port = 24
    }

}
```

### `/etc/dovecot/conf.d/20-managesieve.conf`

Sieve setup. Create the folder and the file before running dovecot with
this setup:

```bash
mkdir /etc/dovecot/sieve
touch /etc/dovecot/sieve/sieve.before
touch /etc/dovecot/sieve/sieve.default
chown -R vmail:vmail /etc/dovecot/sieve
```

```apache
##
## ManageSieve specific settings
##

# Service configuration

protocol sieve {
    #managesieve_max_line_length = 65536
}

# Service definitions
service managesieve-login {
    inet_listener sieve {
        port = 4190
    }

    inet_listener sieve_deprecated {
        port = 2000
    }
}

service managesieve {
    # process_count = 32
}

plugin {
    # The path to the user's main active script. If ManageSieve is used, this the
    # location of the symbolic link controlled by ManageSieve.
    sieve = ~/.dovecot.sieve
    sieve_default = /etc/dovecot/sieve/sieve.default
    sieve_dir = ~/sieve
    sieve_global_dir = /etc/dovecot/sieve
    sieve_before = /etc/dovecot/sieve/sieve.before

    sieve_max_actions = 1024
}
```

### `/etc/dovecot/conf.d/80-antispam.conf`

Dspam can hook in to dovecot so there's no need for any manual train;
when a mail is moved in our out the Spam folder, dspam will
automatically be trained on it.

```apache
##
## antispam plugin config
##
plugin {
    antispam_backend = dspam
    antispam_dspam_binary = /usr/bin/dspam
    antispam_signature = X-DSPAM-Signature
    antispam_signature_missing = move
    antispam_dspam_result_header = X-DSPAM-Result
    antispam_dspam_result_blacklist = Virus;Blocklisted;Blacklisted

    antispam_trash = trash;Trash;Deleted Items;Deleted Messages
    antispam_trash_pattern_ignorecase = TRASH
    antispam_spam = Spam;Junk
    antispam_spam_pattern_ignorecase = SPAM;JUNK

    antispam_dspam_args = --client;--user;%Lu;--source=error
    antispam_dspam_spam = --class=spam
    antispam_dspam_notspam = --class=innocent
}
```

## DKIM

### `/etc/opendkim.conf`

```apache

Syslog            yes
UMask            002
# postfix user
UserID            104

Domain            your.domain
KeyFile            /etc/ssl/your.domain.dkim.private
Selector        mail

Mode sv
SubDomains yes
AutoRestart yes
Background yes
Canonicalization relaxed/relaxed
DNSTimeout 5
SignatureAlgorithm rsa-sha256
#UseASPDiscard no
##Version rfc4871
X-Header yes

InternalHosts /etc/internalhosts

OversignHeaders        From
```

[^1]: <http://fuerstnet.de/en/roundcube-dovecot-imap-and-case-sensitive-user-names>