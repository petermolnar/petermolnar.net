__author__ = "Peter Molnar"
__copyright__ = "Copyright 2017-2020, Peter Molnar"
__license__ = "apache-2.0"
__maintainer__ = "Peter Molnar"
__email__ = "mail@petermolnar.net"

import os
from datetime import datetime
from datetime import timezone
import re
import yaml
from fetch import slugify

BASEPATH = os.path.dirname(os.path.realpath(__file__))

def run():
    url = input('replying to URL:' )

    meta = {
        "author": {
            "email": "mail@petermolnar.net",
            "image": "https://petermolnar.net/favicon.jpg",
            "name": "Peter Molnar",
            "url": "https://petermolnar.net"
        },
        "in-reply-to": url,
        "published": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    }

    r = "---\n%s\n---\n\n%s" % (
        yaml.dump(
            meta,
            default_flow_style=False,
            indent=4,
            allow_unicode=True,
            width=72
        ),
        ''
    )
    slug = slugify(url)
    dirname = os.path.join(BASEPATH, 'note', f"re-{slug}")
    if not os.path.isdir(dirname):
        print(f"creating {dirname}")
        os.makedirs(dirname)
    fpath = os.path.join(dirname, "index.md")
    with open(fpath, "wt") as f:
        print(f"starting document at {fpath}")
        f.write(r)

if __name__ == "__main__":
    run()
