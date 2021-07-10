__author__ = "Peter Molnar"
__copyright__ = "Copyright 2017-2021, Peter Molnar"
__license__ = "apache-2.0"
__maintainer__ = "Peter Molnar"
__email__ = "mail@petermolnar.net"

import os
from datetime import datetime
from datetime import timezone
import json
import subprocess
import urllib.parse
import re
import logging
import glob
import requests
import yaml

BASEPATH = os.path.dirname(os.path.realpath(__file__))

# https://www.peterbe.com/plog/fastest-python-function-to-slugify-a-string
NON_URL_SAFE = [
    '"',
    "#",
    "$",
    "%",
    "&",
    "+",
    ",",
    "/",
    ":",
    ";",
    "=",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "`",
    "{",
    "|",
    "}",
    "~",
    "'",
    ".",
]
TRANSLATE_TABLE = {ord(char): "" for char in NON_URL_SAFE}
RE_NON_URL_SAFE = re.compile(
    r"[{}]".format("".join(re.escape(x) for x in NON_URL_SAFE))
)
RE_REMOVESCHEME = re.compile(r"https?://")
RE_MICROSECONDTIMESTAMP = re.compile(r"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})(?:\.[0-9]+)?([+-0-9:]+)?")

DOMAIN = "petermolnar.net"

loglevel = 20
LOGGER = logging.getLogger("NASG FETCH")
LOGGER.setLevel(loglevel)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
LOGGER.addHandler(console_handler)


def write_mdfile(fpath, meta, txt):
    meta = yaml.dump(
        meta, default_flow_style=False, indent=4, allow_unicode=True, width=72
    )

    r = f"---\n{meta}\n---\n\n{txt}\n"
    with open(fpath, "wt") as f:
        LOGGER.info(f"saving markdown file {fpath}")
        f.write(r)

def slugify(text):
    text = RE_REMOVESCHEME.sub("", text).strip()
    text = RE_NON_URL_SAFE.sub("", text).strip()
    text = text.lower()
    text = "_".join(re.split(r"\s+", text))
    return text


def get_new_webmentions():
    mtime = 0
    for md in sorted(
        glob.glob(os.path.join(BASEPATH, "**", "*.md"), recursive=True)
    ):
        if md.endswith("index.md"):
            continue
        maybe = os.path.basename(md).split("-")[0]
        fmtime = os.path.getmtime(md)
        if maybe.isnumeric():
            fnamemtime = int(maybe)
            fmtime = min(fnamemtime, fmtime)
        mtime = max(mtime, fmtime)

    params = {
        "token": os.environ["WEBMENTIONIO_TOKEN"],
        "since": datetime.fromtimestamp(mtime)
        .replace(tzinfo=timezone.utc)
        .isoformat(),
        "domain": DOMAIN,
    }
    LOGGER.info(params)

    webmentions = requests.get(
        "https://webmention.io/api/mentions", params=params
    )
    if webmentions.status_code != requests.codes.ok:
        raise TypeError(
            f"failed to query webmention.io: {webmentions.status_code} {webmentions.text}"
        )
    mentions = webmentions.json()
    for webmention in mentions.get("links"):
        if "source" not in webmention:
            LOGGER.error(f"empty 'source' for: {webmention}")
            continue

        if "target" not in webmention:
            LOGGER.error(f"empty 'source' for: {webmention}")
            continue

        slug = os.path.split(
            urllib.parse.urlparse(webmention.get("target")).path.lstrip("/")
        )[0]

        # ignore selfpings
        if slug == DOMAIN:
            LOGGER.warn(f"selfping found: {webmention}")
            continue

        if not len(slug):
            LOGGER.error(f"empty target in: {webmention}")
            continue

        fdir = glob.glob(os.path.join(BASEPATH, "**", slug), recursive=True)
        if not len(fdir):
            LOGGER.error(f"no target found for: {webmention}")
            continue
        elif len(fdir) > 1:
            LOGGER.error(f"multiple targets found for: {webmention}")
            continue

        fdir = fdir.pop()
        parsed_url = urllib.parse.urlparse(webmention["source"])

        author = {
            "name": f"{parsed_url.hostname}",
            "url": f"{parsed_url.scheme}://{parsed_url.hostname}",
        }

        if "author" in webmention["data"]:
            for k, v in webmention["data"]["author"].items():
                if v:
                    author[k] = v

        dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        try:
            if "published" in webmention["data"] and webmention["data"]["published"]:
                dt = datetime.fromisoformat(webmention["data"]["published"])
            elif "verified_date" in webmention and webmention["verified_date"]:
                dt = datetime.fromisoformat(webmention["verified_date"])
        except TypeError as e:
            LOGGER.error("failed to parse dt in webmention, using 'now' as timestamp")
            pass

        timestamp = int(dt.timestamp())
        url = re.sub(r"^https?://(?:www)?", "", webmention["source"])
        url = slugify(url)
        slugfname = url[:200]

        fpath = os.path.join(fdir, f"{timestamp}-{slugfname}.md")

        meta = {
            "author": author,
            "date": dt.isoformat(),
            "source": webmention["source"],
            "target": webmention["target"],
            "type": webmention.get("activity", {}).get("type", "webmention"),
        }

        try:
            txt = webmention.get("data").get("content", "").strip()
        except Exception as e:
            txt = ""
            pass

        LOGGER.info(f"saving webmention into {fpath}")
        write_mdfile(fpath, meta, txt)


if __name__ == "__main__":
    get_new_webmentions()
