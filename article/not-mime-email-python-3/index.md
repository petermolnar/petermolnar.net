---
author:
    email: mail@petermolnar.net
    image: https://petermolnar.net/favicon.jpg
    name: Peter Molnar
    url: https://petermolnar.net
copies:
- http://web.archive.org/web/20170212090023/https://petermolnar.net/not-mime-email-python-3/
published: '2016-09-22T18:00:25+00:00'
redirect:
- how-to-send-utf-8-text-html-email-in-python-3-4
summary: Apparently, sending email in Python is painful. This is what I did
    to ease it.
tags:
- Python3
title: How to send simple UTF-8 email in Python 3.x

---

**Note: some arcane and/or ancient email clients will have trouble
understanding these mails due to the completely ignored encoding rules.
Please take that in account when using these solutions.**

## Summary: dead simple text

Just assemble the text by hand, and force send it via smtplib.

`python_email.py`

```python
import smtplib
import os
import datetime

import conf

"""
config file; place it as conf.py

host = "mail.domain.com"
port =  587
tls =  true
username = ""
password = ""
sender = "XYZ <xyz@domain.com>"
to = "ABC <abc@domain.com>"
"""

def send_email( subject, content ):
    """ Send a simple, stupid, text, UTF-8 mail in Python """

    for ill in [ "\n", "\r" ]:
        subject = subject.replace(ill, ' ')

    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit'
        'From': conf.sender,
        'To': conf.to,
        'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
        'X-Mailer': 'python',
        'Subject': subject
    }

    # create the message
    msg = ''
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    # add contents
    msg += "\n%s\n"  % (content)

    s = smtplib.SMTP(conf.host, conf.port)

    if conf.tls:
        s.ehlo()
        s.starttls()
        s.ehlo()

    if conf.username and conf.password:
        s.login(conf.username, conf.password)

    print ("sending %s to %s" % (subject, headers['To']))
    s.sendmail(headers['From'], headers['To'], msg.encode("utf8"))
    s.quit()
```