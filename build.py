__author__ = "Peter Molnar"
__copyright__ = "Copyright 2017-2021, Peter Molnar"
__license__ = "apache-2.0"
__maintainer__ = "Peter Molnar"
__email__ = "mail@petermolnar.net"

import glob
import os
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from collections import namedtuple
from time import time
from shutil import copyfileobj
import re
import json
import subprocess
import logging
from shutil import copy2 as cp
from copy import deepcopy
import sqlite3
import urllib.request
import urllib.parse
import hashlib
from htmltruncate import truncate
import lxml.etree as etree
import wand.image
import wand.drawing
import yaml
import frontmatter
import jinja2
import requests

loglevel = 20
LOGGER = logging.getLogger("BUILD")
LOGGER.setLevel(loglevel)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
LOGGER.addHandler(console_handler)
logging.getLogger("asyncio").setLevel(loglevel)

MarkdownImage = namedtuple(
    "MarkdownImage", ["match", "alt", "fname", "title", "css"]
)

BASEPATH = os.path.dirname(os.path.realpath(__file__))
TMPPATH = os.path.join(BASEPATH, ".tmp")
if not os.path.exists(TMPPATH):
    os.makedirs(TMPPATH)

SITEVARS = {
    "domain": "petermolnar.net",
    "name": "petermolnar.net",
    "url": "https://petermolnar.net",
    "hub": "https://petermolnar.superfeedr.com/",
}

WATERMARK = os.path.join(BASEPATH, ".templates", "watermark.png")

IMGSIZES = {
    "src": {"size": 720, "suffix": ""},
    "href": {"size": 1280, "suffix": "_large"},
    "huge": {"size": 1920, "suffix": "_huge"},
    "small": {"size": 480, "suffix": "_small"},
}

RE_FIRSTARCHIVEDMEMEMTO = re.compile(
    r"^\<(?P<url>[^>]+)\>; rel=\"first memento\"; datetime=\"(?P<datetime>[^\"]+).*$"
)

RE_CODE = re.compile(r"^(?:[~`]{3,4}).+$", re.MULTILINE)
RE_PRECODE = re.compile(r'<pre class="([^"]+)"><code>')

RE_MYURL = re.compile(
    r'(^(%s[^"]+)$|"(%s[^"]+)")' % (SITEVARS["url"], SITEVARS["url"])
)

RE_MDIMG = re.compile(
    r"(?P<match>!\[(?P<alt>[^\]]+)?\]\((?P<fname>[^\s\]]+)"
    r"(?:\s[\'\"](?P<title>[^\"\']+)[\'\"])?\)(?:{(?P<css>[^\}]+)\})?)",
    re.IGNORECASE,
)

RE_AUTHOR = re.compile(
    r"(?:P[eé]ter Moln[aá]r)|(?:Moln[aá]r P[eé]ter)|(?:petermolnar\.(?:eu|net))"
)

RE_HTMLTAG = re.compile(r"<[^>]+>")

RE_FLICKR = re.compile(r"(?:www\.)?flickr\.com")

RE_ARCHIVE = re.compile(r"web\.archive\.org")

RE_FIRST_MEMENTO = re.compile(
    r"^\<(?P<url>[^>]+)\>; rel=\"first memento\"; datetime=\"(?P<datetime>[^\"]+).*$"
)

J2 = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(BASEPATH, ".templates")
    ),
    lstrip_blocks=True,
    trim_blocks=True,
)

LENS = {}
with open(os.path.join(BASEPATH, ".templates", "lens.json"), "rt") as f:
    LENS = json.loads(f.read())

MANUALLENS = {}
with open(os.path.join(BASEPATH, ".templates", "manuallens.json"), "rt") as f:
    MANUALLENS = json.loads(f.read())


def unix_timestamp():
    return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())


def relurl(text, baseurl=SITEVARS["url"]):
    for match, standalone, href in RE_MYURL.findall(str(text)):
        needsquotes = False
        url = href
        if len(href):
            needsquotes = True
        else:
            url = standalone

        r = os.path.relpath(url, baseurl)
        if url.endswith("/") and not r.endswith("/"):
            r = f"{r}/index.html"
        if needsquotes:
            r = f'"{r}"'
        text = text.replace(match, r)
    return text


J2.filters["relurl"] = relurl


def printdate(rfc3339):
    dt = datetime.fromisoformat(rfc3339)
    return str(dt.strftime("%Y-%m-%d %H:%M %Z"))


J2.filters["printdate"] = printdate


def extractdomain(url):
    url = urllib.parse.urlparse(url)
    return url.hostname


J2.filters["extractdomain"] = extractdomain


def insertfile(fpath):
    fpath = os.path.join(os.path.join(BASEPATH, ".templates"), fpath)
    if not os.path.exists(fpath):
        return ""
    with open(
        os.path.join(os.path.join(BASEPATH, ".templates"), fpath), "rt"
    ) as f:
        return f.read()


J2.filters["insertfile"] = insertfile


def cachefile(source, target, mtime=None):
    content = None
    if not mtime:
        if os.path.islink(source):
            mtimeof = os.path.realpath(source)
        else:
            mtimeof = source
        mtime = os.path.getmtime(mtimeof)
    if os.path.exists(target):
        if mtime <= os.path.getmtime(target):
            # LOGGER.info(f"cache file {target} age > {source}")
            with open(target, "rt") as f:
                content = f.read()
        else:
            LOGGER.debug(f"cache file {target} is too old")
    else:
        LOGGER.debug(f"no cache found under {target}")
    return content


class cached_property(object):
    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        result = self.method(inst)
        setattr(inst, self.name, result)
        return result


class WebImage(object):
    @property
    def imgsizes(self):
        r = deepcopy(IMGSIZES)
        for name, details in r.items():
            r[name]["fpath"] = os.path.join(
                self.dirname,
                "%s%s%s" % (self.name, details["suffix"], self.fext),
            )
        return r

    def make_map(self):
        if "MAPBOX_TOKEN" not in os.environ or not os.environ["MAPBOX_TOKEN"]:
            return

        token = os.environ["MAPBOX_TOKEN"]
        mapfpath = os.path.join(self.dirname, "map.png")
        if (
            os.path.exists(mapfpath)
            and os.path.exists(self.original)
            and os.path.getmtime(mapfpath) >= os.path.getmtime(self.original)
        ):
            return

        if "GPSLatitude" not in self.exif or "GPSLongitude" not in self.exif:
            LOGGER.debug("gps info missing from exif at: %s", self.fpath)
            return

        lat = round(float(self.exif["GPSLatitude"]), 3)
        lon = round(float(self.exif["GPSLongitude"]), 3)
        url = f"https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/pin-s({lon},{lat})/{lon},{lat},11,20/720x480?access_token={token}"
        LOGGER.info("requesting map for %s with URL %s", self.fpath, url)
        req = urllib.request.Request(url, method="GET")
        response = urllib.request.urlopen(req)
        LOGGER.info("saving map file to %s", mapfpath)
        with open(mapfpath, "wb") as f:
            copyfileobj(response, f)
            t = time()
            os.utime(self.parent.fpath, (int(t), int(t)))

    def linktoreal(self, source):
        realtarget = source.replace(
            self.dirname, os.path.dirname(os.path.realpath(self.fpath))
        )
        if not os.path.exists(realtarget):
            LOGGER.warning(
                f"missing realtarget {realtarget} - can't symlink {source} yet"
            )
            return

        target = os.path.relpath(realtarget, os.path.dirname(source))
        if os.path.exists(source) and os.path.islink(source):
            return
        if os.path.exists(source) and not os.path.islink(source):
            LOGGER.warning(f"replacing file {source} with symlink to {target}")
            os.unlink(source)
        LOGGER.debug(f"creating symlink from {source} to {target}")
        os.symlink(target, source)
        # this is to set the mtime of the symlink itself
        ts = str(
            datetime.fromtimestamp(int(os.path.getmtime(realtarget)))
            .replace(tzinfo=timezone.utc)
            .strftime("%Y%m%d%H%M")
        )
        os.system(f"touch -h -t {ts} {source}")

    def __init__(self, fpath, mdimg, parent):
        self.fpath = fpath
        self.mdimg = mdimg
        self.parent = parent
        self.fname = os.path.basename(self.fpath)
        self.dirname = os.path.dirname(self.fpath)
        self.name, self.fext = os.path.splitext(self.fname)
        self.original = self.fpath.replace(
            self.fname, f".{self.name}.orig{self.fext}"
        )
        self.is_featured = False
        self.is_link = os.path.islink(self.fpath)

        if self.is_link:
            self.linktoreal(self.original)
        elif not os.path.exists(self.original):
            cp(self.fpath, self.original)

        self.size = max(self.exif["ImageHeight"], self.exif["ImageWidth"])

        img = None

        for name, details in self.imgsizes.items():
            # special case of items symlinked to other posts' images
            if self.is_link:
                self.linktoreal(details["fpath"])
                continue

            # image is too small for this size
            if details["size"] >= self.size:
                continue
            # image already exists and is
            if os.path.exists(details["fpath"]) and (
                (
                    os.path.getmtime(details["fpath"])
                    >= os.path.getmtime(self.original)
                    and os.path.getsize(self.original)
                    != os.path.getsize(details["fpath"])
                )
                or (
                    os.path.getmtime(details["fpath"])
                    > os.path.getmtime(self.original)
                    and os.path.getsize(self.original)
                    == os.path.getsize(details["fpath"])
                )
            ):
                LOGGER.debug(
                    "resized image %s for %s already exists", name, self.fpath
                )
                continue

            if not img:
                img = wand.image.Image(filename=self.original)
                img.auto_orient()

                if self.is_my_photo:
                    LOGGER.info(f"{self.fpath} needs watermarking")
                    with wand.image.Image(filename=WATERMARK) as wmark:
                        with wand.drawing.Drawing() as url:
                            w = img.height * 0.2
                            h = wmark.height * (w / wmark.width)
                            if img.width > img.height:
                                x = img.width - w - (img.width * 0.01)
                                y = img.height - h - (img.height * 0.01)

                            else:
                                x = img.width - h - (img.width * 0.01)
                                y = img.height - w - (img.height * 0.01)

                            w = round(w)
                            h = round(h)
                            x = round(x)
                            y = round(y)
                            wmark.resize(w, h)
                            if img.width <= img.height:
                                wmark.rotate(-90)
                            img.composite(image=wmark, left=x, top=y)

                            # url.fill_color = wand.color.Color('#fff')
                            # url.fill_opacity = 0.7
                            # url.font = '.templates/gara_regular.ttf'
                            # url.font_size = round(h * 0.7)
                            # if img.width <= img.height:
                            # url.rotate(-90)
                            # url.text_alignment = 'left'
                            # else:
                            # url.text_alignment = 'right'
                            # url.text(round(img.width - (img.width * 0.015)), round(img.height - (img.height * 0.015)), self.parent.url)
                            # url(img)

            crop = details.get("crop", False)
            ratio = max(img.width, img.height) / min(img.width, img.height)
            horizontal = True if (img.width / img.height) >= 1 else False

            with img.clone() as thumb:
                # panorama: reverse "horizontal" because the limit
                # should be on the shorter side, not the longer, and
                # make it a bit smaller, than the actual limit
                # 2.39 is the wide angle cinematic view: anything
                # wider, than that is panorama land
                # this is to maintain a viewable panorama
                if ratio > 2.39 and not crop:
                    details["size"] = int(details["size"] * 0.6)
                    horizontal = not horizontal

                w = img.width
                h = img.height

                if horizontal != crop:
                    w = details["size"]
                    h = int(float(details["size"] / img.width) * img.height)
                else:
                    h = details["size"]
                    w = int(float(details["size"] / img.height) * img.width)
                thumb.resize(w, h)
                if crop:
                    thumb.liquid_rescale(details["size"], details["size"], 1, 1)

                if self.exif.get("FileType", "").lower() == "jpeg":
                    if "small" == name:
                        thumb.compression_quality = 70
                    else:
                        thumb.compression_quality = 86
                    thumb.unsharp_mask(
                        radius=1, sigma=0.5, amount=0.7, threshold=0.5
                    )
                    thumb.format = "pjpeg"

                # this is to make sure pjpeg happens
                output = details["fpath"]
                with open(output, "wb") as o:
                    wmarkmsg = " "
                    if self.is_my_photo:
                        wmarkmsg = " watermarked "
                    LOGGER.info(f"saving{wmarkmsg}image ({w}x{h}) to {output}")
                    thumb.save(file=o)

                if self.exif.get("FileType", "").lower() == "jpeg":
                    cmd = (
                        "exiftool",
                        f"-XMP:Source={self.parent.url}",
                        "-overwrite_original",
                        output,
                    )
                    p = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    stdout, stderr = p.communicate()
                    if stderr:
                        raise OSError(
                            f"Error writing EXIF to {output}: {stderr}"
                        )

    @cached_property
    def is_my_photo(self):
        for candidate in ["Artist", "Copyright"]:
            if candidate in self.exif:
                if RE_AUTHOR.search(self.exif[candidate]):
                    return True
        return False

    @cached_property
    def src(self):
        return self.fpath.replace(BASEPATH, SITEVARS["url"])

    @cached_property
    def tmplvars(self):
        if len(self.mdimg.alt):
            alt = self.mdimg.alt
        else:
            alt = self.exif.get("Description", "")

        if len(self.mdimg.title):
            title = self.mdimg.title
        else:
            title = self.exif.get("Headline", self.fname)

        width = IMGSIZES["src"]["size"]
        height = IMGSIZES["src"]["size"]
        with wand.image.Image(filename=self.fpath) as img:
            width = img.width
            height = img.height

        tmplvars = {
            "src": self.src,
            "alt": alt,
            "caption": alt,
            "title": title,
            "featured": self.is_featured,
            "width": width,
            "height": height,
            "mime": self.exif.get("MIMEType", "image/jpeg"),
            "bytesize": os.path.getsize(self.fpath),
            "licensor": SITEVARS["url"],
            "name": self.name,
        }
        for s in ["huge", "href", "small"]:
            maybe = os.path.join(
                self.dirname,
                "%s%s%s" % (self.name, IMGSIZES[s]["suffix"], self.fext),
            )
            if os.path.exists(maybe):
                tmplvars[s] = maybe.replace(BASEPATH, SITEVARS["url"])

        if self.is_my_photo:
            tmplvars["license"] = "CC-BY-NC-ND-4.0"
            tmplvars["exif"] = {}
            mapping = {
                "camera": ["Model"],
                "aperture": ["FNumber", "Aperture"],
                "shutter": ["ExposureTime"],
                "focallength": ["FocalLength", "FocalLengthIn35mmFormat"],
                "iso": ["ISO"],
                "lens": ["LensID", "LensSpec", "Lens"],
                "created": ["CreateDate", "DateTimeOriginal"],
                "latitude": ["GPSLatitude"],
                "longitude": ["GPSLongitude"],
            }

            for k, candidates in mapping.items():
                for candidate in candidates:
                    maybe = self.exif.get(candidate, None)
                    if maybe:
                        tmplvars["exif"][k] = maybe
                        break

            # lens info is a bit fragmented, so let's try to identify the
            # real lens, plus add the URL for it
            if "lens" in tmplvars["exif"] and tmplvars["exif"]["lens"] in LENS:
                tmplvars["exif"]["lens"] = LENS[tmplvars["exif"]["lens"]]
            elif (
                "focallength" in tmplvars["exif"]
                and "camera" in tmplvars["exif"]
                and "created" in tmplvars["exif"]
                and tmplvars["exif"]["focallength"] in MANUALLENS
            ):
                epoch = int(
                    datetime.fromisoformat(
                        tmplvars["exif"]["created"].replace('"', "")
                    ).timestamp()
                )
                e = tmplvars["exif"]
                for lens in MANUALLENS[tmplvars["exif"]["focallength"]]:
                    if tmplvars["exif"]["camera"] not in lens["camera"]:
                        continue
                    if "maxepoch" in lens and epoch > int(lens["maxepoch"]):
                        continue
                    if "minepoch" in lens and epoch < int(lens["minepoch"]):
                        continue

                    tmplvars["exif"]["lens"] = lens
                    break

                if (
                    "lens" in tmplvars["exif"]
                    and "name" not in tmplvars["exif"]["lens"]
                ):
                    LOGGER.error(
                        f"failed to identify manual lens at {self.fpath}, exif is {e}"
                    )
                    del tmplvars["exif"]["lens"]

            elif "lens" in tmplvars["exif"]:
                tmplvars["exif"]["lens"] = {
                    "name": tmplvars["exif"]["lens"],
                    "url": "",
                }

            for e in ["latitude", "longitude"]:
                if e in tmplvars["exif"]:
                    tmplvars["exif"][e] = round(float(tmplvars["exif"][e]), 3)

        return tmplvars

    def __str__(self):
        if len(self.mdimg.css):
            return self.mdimg.match

        tmpl = J2.get_template("Figure.j2.html")
        r = tmpl.render(self.tmplvars)
        return r

    @cached_property
    def exif(self):
        if self.is_link:
            cachepath = os.path.join(
                os.path.dirname(os.path.realpath(self.fpath)),
                self.dirname,
                f".{self.fname}.exif.json",
            )
        else:
            cachepath = os.path.join(self.dirname, f".{self.fname}.exif.json")
        content = cachefile(self.original, cachepath)
        if content:
            return json.loads(content)

        cmd = (
            "exiftool",
            "-sort",
            "-json",
            "-dateFormat",
            '"%Y-%m-%dT%H:%M:%S+00:00"',
            "-MIMEType",
            "-FileType",
            "-FileName",
            "-FileSize#",
            "-ModifyDate",
            "-CreateDate",
            "-DateTimeOriginal",
            "-ImageHeight",
            "-ImageWidth",
            "-Aperture",
            "-FOV",
            "-ISO",
            "-FocalLength",
            "-FNumber",
            "-FocalLengthIn35mmFormat",
            "-ExposureTime",
            "-Model",
            "-GPSLongitude#",
            "-GPSLatitude#",
            "-LensID",
            "-LensSpec",
            "-Lens",
            "-ReleaseDate",
            "-Description",
            "-Headline",
            "-HierarchicalSubject",
            "-Copyright",
            "-Artist",
            self.original,
        )

        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = p.communicate()
        if stderr:
            raise OSError(f"Error reading EXIF from {self.original}: {stderr}")

        exif = json.loads(stdout.decode("utf-8").strip()).pop()
        with open(cachepath, "wt") as f:
            LOGGER.info(f"updating EXIF for {self.original} at {cachepath}")
            f.write(json.dumps(exif, indent=4, sort_keys=True))

        return exif


class MarkdownDoc(object):
    def __init__(self, fpath):
        self.fpath = fpath
        self.fname = os.path.basename(self.fpath)
        self.dirname = os.path.dirname(fpath)
        self.name, self.fext = os.path.splitext(self.fname)

    @property
    def mtime(self):
        return int(os.path.getmtime(self.fpath))

    @cached_property
    def parsed(self):
        with open(self.fpath, mode="rt") as f:
            meta, txt = frontmatter.parse(f.read())

        if "author" not in meta:
            raise LookupError(f"Missing author on {self.fpath}")
        return (meta, txt)

    @property
    def meta(self):
        return self.parsed[0]

    @property
    def txt(self):
        if not self.parsed[1] or not len(self.parsed[1]):
            return str("")
        else:
            return self.parsed[1]

    @property
    def author(self):
        return self.meta["author"]

    def save(self):
        LOGGER.info(f"=> WRITING MARKDOWN FILE <= {self.fpath}")
        with open(self.fpath, "wt") as f:
            f.write(
                "---\n%s\n---\n\n%s"
                % (
                    yaml.dump(
                        self.meta,
                        default_flow_style=False,
                        indent=4,
                        allow_unicode=True,
                    ),
                    pandoc_formattedmarkdown(self.txt),
                )
            )


class Comment(MarkdownDoc):
    @cached_property
    def parsed(self):
        meta, txt = super().parsed
        if "source" not in meta:
            raise LookupError(f"Missing 'source' on {self.fpath}")
        if "target" not in meta:
            raise LookupError(f"Missing 'target' on {self.fpath}")
        if "type" not in meta:
            raise LookupError(f"Missing 'type' on {self.fpath}")
        return (meta, txt)

    @property
    def dt(self):
        try:
            dt = datetime.fromisoformat(self.meta["date"])
        except TypeError as err:
            raise TypeError(f"failed 'date' parsing on {self.fpath}: {err}")
        if self.mtime != int(dt.timestamp()):
            os.utime(self.fpath, (int(dt.timestamp()), int(dt.timestamp())))
        return dt

    @property
    def tmplvars(self):
        return self.meta


class Entry(MarkdownDoc):
    def __init__(self, fpath):
        super().__init__(fpath)
        self.subentries = {}

    @cached_property
    def parsed(self):
        meta, txt = super().parsed
        if "published" not in meta:
            raise LookupError(f"Missing 'published' on {self.fpath}")
        return (meta, txt)

    @property
    def dt(self):
        try:
            dt = datetime.fromisoformat(self.meta["published"])
        except TypeError as err:
            raise ValueError(
                f"failed 'published' parsing on {self.fpath}: {err}"
            )
        return dt

    @property
    def is_future(self):
        my_ts = datetime.fromisoformat(self.meta["published"]).timestamp()
        unix_ts = unix_timestamp()
        if my_ts > unix_ts:
            return True
        else:
            return False

    @property
    def title(self):
        if "title" in self.meta and len(self.meta["title"]) > 0:
            return self.meta["title"]
        else:
            return printdate(self.dt.isoformat())

    @property
    def updated(self):
        return (
            datetime.fromtimestamp(self.mtime)
            .replace(tzinfo=timezone.utc)
            .isoformat()
        )

    @property
    def mtime(self):
        mtime = int(os.path.getmtime(self.fpath))
        if not self.is_future:
            mtime = max(mtime, int(self.dt.timestamp()))
        if len(self.subentries):
            mtime = max(mtime, max([v.mtime for v in self.subentries.values()]))
        if len(self.comments):
            mtime = max(mtime, max([v.mtime for v in self.comments.values()]))

        return mtime

    # everything second level, eg article/entry/index.md has a category
    @cached_property
    def category(self):
        pathdiff = os.path.relpath(self.fpath, BASEPATH)
        if 2 == pathdiff.count("/"):
            return pathdiff.split("/")[0]
        else:
            return None

    # everything second level, eg article/entry/index.md has a category
    @cached_property
    def entry(self):
        if "index.md" == self.fname:
            return os.path.basename(self.dirname)
        else:
            return self.dirname

    @cached_property
    def type(self):
        pathdiff = os.path.relpath(self.fpath, BASEPATH)
        if pathdiff.count("/") >= 2:
            return "post"
        elif pathdiff.count("/") == 1:
            subentries = glob.glob(
                os.path.join(self.dirname, "**", "index.md"), recursive=True
            )
            if len(subentries) > 1:
                return "category"
            else:
                return "page"
        else:
            return "home"

    @cached_property
    def comments(self):
        comments = {}
        for candidate in glob.glob(os.path.join(self.dirname, "*.md")):
            if candidate.endswith("index.md") or candidate.endswith("README.md"):
                continue
            comment = Comment(candidate)
            comments[int(comment.dt.timestamp())] = comment
        return comments

    @cached_property
    def images(self):
        images = {}
        for match, alt, fname, title, css in RE_MDIMG.findall(self.txt):
            mdimg = MarkdownImage(match, alt, fname, title, css)
            imgpath = os.path.join(self.dirname, fname)
            if not os.path.exists(imgpath):
                raise OSError(f"{imgpath} is missing from {self.fpath}")
            else:
                webimg = WebImage(imgpath, mdimg, self)
                if webimg.name == self.entry:
                    webimg.is_featured = True
                    webimg.make_map()
                images.update({match: webimg})
        return images

    @cached_property
    def featured_image(self):
        if len(self.images):
            for match, webimg in self.images.items():
                if webimg.is_featured:
                    return (match, webimg)
        return (None, None)

    @cached_property
    def html(self):
        if not len(self.txt):
            return ""

        txt = self.txt
        if len(self.images):
            # remove the featured image from the content, that will
            # be added separetely
            # replace all the others with their HTML version
            for match, webimg in self.images.items():
                if webimg.is_featured:
                    txt = txt.replace(match, "")
                else:
                    txt = txt.replace(match, str(webimg))
        c = pandoc(txt)
        c = RE_PRECODE.sub('<pre><code lang="\g<1>" class="language-\g<1>">', c)
        return c

    @cached_property
    def description(self):
        if "summary" in self.meta and len(self.meta["summary"]):
            return self.meta["summary"]
        return truncate(self.html, 255, "…")

    @property
    def url(self):
        return "%s/" % (self.dirname.replace(BASEPATH, SITEVARS["url"]))

    @cached_property
    def tmplvars(self):
        post = deepcopy(self.meta)
        post.update(
            {
                "title": self.title,
                "html": self.html,
                # "gmi": md2gemini(self.txt),
                "description": self.description,
                "entry": self.entry,
                "category": self.category,
                "url": self.url,
                "updated": self.updated,
                "year": self.dt.strftime("%Y"),
                "type": self.type,
                "has_code": RE_CODE.search(self.txt),
                "has_map": os.path.exists(
                    os.path.join(self.dirname, "map.png")
                ),
            }
        )

        if "license" not in post:
            post.update({"license": "CC-BY-4.0"})

        webimg = self.featured_image[1]
        if webimg:
            post["image"] = webimg.tmplvars
            post["image"]["html"] = str(webimg)

        if len(self.comments):
            post["comments"] = [
                self.comments[k].tmplvars
                for k in sorted(self.comments.keys(), reverse=True)
            ]

        return post

    def backfill_archiveorg(self):
        if "ARCHIVE" not in os.environ or not os.environ["ARCHIVE"]:
            return

        if self.is_future:
            return

        # self.category means the category of the post; it's None for
        # actual categories
        if not self.category:
            return

        if "copies" in self.meta.keys() and len(self.meta["copies"]):
            for copy in self.meta["copies"]:
                if copy and RE_ARCHIVE.search(copy):
                    return

        target = f"http://web.archive.org/web/timemap/link/{self.url}"
        LOGGER.info(f"requesting mementos from archive.org at: {target}")
        response = requests.get(target)
        for memento in response.text.split("\n"):
            m = RE_FIRST_MEMENTO.match(memento)
            if m:
                if "copies" not in self.meta:
                    self.meta["copies"] = []
                self.meta["copies"].append(m.group("url"))
                self.save()
                return

    def backfill_flickr(self):
        if (
            "FLICKR_API_KEY" not in os.environ
            or "FLICKR_USER_ID" not in os.environ
            or not os.environ["FLICKR_API_KEY"]
            or not os.environ["FLICKR_USER_ID"]
        ):
            return

        if self.is_future:
            return

        if not self.featured_image[1]:
            return

        if "copies" in self.meta.keys() and len(self.meta["copies"]):
            for copy in self.meta["copies"]:
                if copy and RE_FLICKR.search(copy):
                    return

        dt = datetime.fromisoformat(self.meta["published"])
        now = datetime.now(dt.tzinfo)
        if dt < (now - timedelta(days=90)):
            LOGGER.debug(
                f"missing flickr info from {self.fpath} but it's older, than 3 months"
            )
            return

        LOGGER.warning(f"entry needs flickr info: {self.fpath}")
        params = {
            "method": "flickr.photos.search",
            "api_key": os.environ["FLICKR_API_KEY"],
            "user_id": os.environ["FLICKR_USER_ID"],
            "min_upload_date": int(dt.timestamp() - 86400),
            "format": "json",
            "nojsoncallback": 1,
            "text": os.path.basename(self.dirname),
            "per_page": 1,
        }
        r = requests.get("https://api.flickr.com/services/rest/", params=params)
        results = r.json()

        try:
            photo = results["photos"]["photo"][0]
            photo_url = "https://www.flickr.com/photos/%s/%s" % (
                photo["owner"],
                photo["id"],
            )
            if "copies" not in self.meta:
                self.meta["copies"] = []
            self.meta["copies"].append(photo_url)
            self.save()

        except IndexError as e:
            LOGGER.error("no flickr entry found (empty array)")
        except Exception as e:
            LOGGER.error("there was an error with flickr results:", e)

    def __str__(self):
        gopherpath = os.path.join(self.dirname, "gophermap")
        gopher = cachefile(self.fpath, gopherpath, self.mtime)

        if "category" == self.type and not gopher:
            LOGGER.info(f"saving gophermap {gopherpath}")
            with open(gopherpath, "wt") as f:
                lines = [
                    "%s - %s" % (self.title, SITEVARS["name"]),
                    "",
                    "",
                ]
                for subentry in [
                    self.subentries[k]
                    for k in sorted(self.subentries.keys(), reverse=True)
                ]:
                    line = "0%s\t/%s\t%s\t70" % (
                        subentry.title,
                        os.path.relpath(subentry.fpath, BASEPATH),
                        SITEVARS["domain"],
                    )
                    lines.append(line)
                    if "summary" in subentry.meta and len(
                        subentry.meta["summary"]
                    ):
                        lines.extend(
                            pandoc_formattedtext(
                                subentry.meta["summary"]
                            ).split("\n")
                        )
                    for img in subentry.images.values():
                        line = "I%s\t/%s\t%s\t70" % (
                            img.fname,
                            os.path.relpath(img.fpath, BASEPATH),
                            SITEVARS["domain"],
                        )
                        lines.append(line)
                    lines.append("")
                f.write("\r\n".join(lines))

        htmlpath = os.path.join(self.dirname, f"{self.name}.html")
        html = cachefile(self.fpath, htmlpath, self.mtime)
        if not html:
            LOGGER.info(f"saving {htmlpath}")
            with open(htmlpath, "wt") as f:
                if "category" == self.type:
                    tmpl = J2.get_template("Category.j2.html")
                else:
                    tmpl = J2.get_template("Singular.j2.html")
                tmplvars = {
                    "baseurl": self.url,
                    "site": SITEVARS,
                    "post": self.tmplvars,
                }
                if len(self.subentries):
                    tmplvars["subentries"] = [
                        self.subentries[k].tmplvars
                        for k in sorted(self.subentries.keys(), reverse=True)
                    ]
                html = tmpl.render(tmplvars)
                f.write(html)
                del tmpl
                del tmplvars
        return html


class SearchDB(object):
    def __init__(self):
        self.fpath = os.path.join(BASEPATH, "search.sqlite")

    @property
    def mtime(self):
        if os.path.exists(self.fpath):
            mtime = int(os.path.getmtime(self.fpath))
        else:
            mtime = 0
        return mtime

    def open(self):
        self.db = sqlite3.connect(self.fpath)
        self.db.execute("PRAGMA auto_vacuum = INCREMENTAL;")
        self.db.execute("PRAGMA journal_mode = MEMORY;")
        self.db.execute("PRAGMA temp_store = MEMORY;")
        self.db.execute("PRAGMA locking_mode = NORMAL;")
        self.db.execute("PRAGMA synchronous = FULL;")
        self.db.execute('PRAGMA encoding = "UTF-8";')
        self.db.execute(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS data USING fts4(
                url,
                mtime,
                name,
                title,
                category,
                content,
                summary,
                featuredimg,
                notindexed=category,
                notindexed=url,
                notindexed=mtime,
                notindexed=featuredimg,
                tokenize=porter
            )"""
        )

    def __exit__(self):
        self.db.commit()
        self.db.execute("PRAGMA auto_vacuum;")
        self.db.close()

    # def append(self, posturl, mtime, name, title, category, content):
    def append(self, post):
        existing_mtime = 0
        exists = False
        maybe = self.db.execute(
            "SELECT mtime FROM data WHERE name = ?", (post.entry,)
        ).fetchone()
        if maybe and int(maybe[0]) < post.mtime:
            self.db.execute("DELETE FROM data WHERE name=?", (post.entry,))
        elif maybe and int(maybe[0]) >= post.mtime:
            exists = True

        if post.featured_image[1]:
            featuredimg = post.featured_image[1].src
        else:
            featuredimg = ""

        if not exists:
            self.db.execute(
                """
                INSERT INTO data (url, mtime, name, title, category, content, summary, featuredimg)
                VALUES (?,?,?,?,?,?,?,?);
            """,
                (
                    post.url,
                    post.mtime,
                    post.entry,
                    post.meta.get("title", ""),
                    post.category,
                    post.txt,
                    post.description,
                    featuredimg,
                ),
            )
            self.is_changed = True


def maybe_hash_cache(prefix, txt):
    _h = hashlib.md5(txt.encode())
    _md5 = _h.hexdigest()
    _hf = os.path.join(TMPPATH, f"{prefix}_{_md5}")
    if not os.path.exists(_hf):
        return None
    with open(_hf, "rt") as f:
        return f.read()


def write_hash_cache(prefix, txt, content):
    _h = hashlib.md5(txt.encode())
    _md5 = _h.hexdigest()
    _hf = os.path.join(TMPPATH, f"{prefix}_{_md5}")
    with open(_hf, "wt") as f:
        f.write(content)


def pandoc_formattedmarkdown(txt):
    _h = maybe_hash_cache("fmarkdown", txt)
    if _h:
        return _h

    mdoptions = [
        "+footnotes",
        "+pipe_tables",
        "+strikeout",
        "+superscript",
        "+subscript",
        "-markdown_in_html_blocks",
        "+raw_html",
        "+definition_lists",
        "+backtick_code_blocks",
        "+fenced_code_attributes",
        "+shortcut_reference_links",
        "+lists_without_preceding_blankline",
        "+autolink_bare_uris",
        "-smart",
    ]
    mdoptions = "".join(mdoptions)
    f = f"--from=markdown{mdoptions}"
    t = f"--to=markdown{mdoptions}"
    cmd = (
        "pandoc",
        "-o-",
        f,
        t,
        "--quiet",
        "--wrap=auto",
        "--columns=72",
    )

    PANDOCPROCESS = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = PANDOCPROCESS.communicate(input=txt.encode())
    if stderr:
        raise OSError(f"Error during pandoc call of `{cmd}`: {stderr}")
    r = stdout.decode("utf-8").strip()
    write_hash_cache("fmarkdown", txt, str(r))
    return str(r)


def pandoc_formattedtext(txt):
    _h = maybe_hash_cache("ftext", txt)
    if _h:
        return _h

    f = f"--from=markdown"
    t = f"--to=plain"
    cmd = (
        "pandoc",
        "-o-",
        f,
        t,
        "--quiet",
        "--wrap=auto",
        "--columns=72",
    )

    PANDOCPROCESS = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = PANDOCPROCESS.communicate(input=txt.encode())
    if stderr:
        raise OSError(f"Error during pandoc call of `{cmd}`: {stderr}")
    r = stdout.decode("utf-8").strip()
    write_hash_cache("ftext", txt, str(r))
    return str(r)


def pandoc(txt):
    _h = maybe_hash_cache("html", txt)
    if _h:
        return _h

    mdoptions = [
        "+footnotes",
        "+pipe_tables",
        "+strikeout",
        "+superscript",
        "+subscript",
        # "-markdown_in_html_blocks",
        "+raw_html",
        "+definition_lists",
        "+backtick_code_blocks",
        "+fenced_code_attributes",
        "+shortcut_reference_links",
        "+lists_without_preceding_blankline",
        "+autolink_bare_uris",
        "+auto_identifiers",
        "+space_in_atx_header" "-smart",
    ]
    mdoptions = "".join(mdoptions)
    f = f"--from=markdown{mdoptions}"
    t = "--to=html5"
    cmd = (
        "pandoc",
        "-o-",
        f,
        t,
        "--no-highlight",
        "--quiet",
        "--wrap=auto",
        "--columns=72",
        "--toc",
        "--toc-depth=4",
    )

    PANDOCPROCESS = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = PANDOCPROCESS.communicate(input=txt.encode())
    if stderr:
        raise OSError(f"Error during pandoc call of `{cmd}`: {stderr}")
    r = stdout.decode("utf-8").strip()
    write_hash_cache("html", txt, str(r))
    return str(r)


def mkfeed(entries):
    xmlfeedfile = os.path.join(BASEPATH, "feed", "index.xml")
    htmlfeedfile = os.path.join(BASEPATH, "feed", "hfeed.html")
    sitemapfile = os.path.join(BASEPATH, "sitemap.txt")
    if not os.path.isdir(os.path.dirname(xmlfeedfile)):
        os.makedirs(os.path.dirname(xmlfeedfile))

    firstentry = entries[0]
    for e in entries:
        if not e.is_future:
            firstentry = e
            break

    up_to_date = True
    for f in [xmlfeedfile, htmlfeedfile, sitemapfile]:
        if not os.path.exists(f) or os.path.getmtime(f) < firstentry.mtime:
            up_to_date = False

    if up_to_date:
        return

    LOGGER.info("making feeds")
    feed = etree.Element(
        "{http://www.w3.org/2005/Atom}feed",
        nsmap={
            "atom": "http://www.w3.org/2005/Atom",
            "xlink": "https://www.w3.org/1999/xlink",
        },
    )
    xmldoc = etree.ElementTree(feed)
    feed.addprevious(
        etree.ProcessingInstruction(
            "xml-stylesheet",
            'type="text/xsl" href="//petermolnar.net/feed/atom.xsl"',
        )
    )

    feedid = etree.SubElement(feed, "{http://www.w3.org/2005/Atom}id")
    feedid.text = "%s/" % (SITEVARS["url"].strip("/"))

    feedtitle = etree.SubElement(feed, "{http://www.w3.org/2005/Atom}title")
    feedtitle.text = "Latest entries from %s" % (SITEVARS["name"])

    feedupdated = etree.SubElement(feed, "{http://www.w3.org/2005/Atom}updated")
    feedupdated.text = firstentry.dt.isoformat()

    selflink = etree.SubElement(
        feed,
        "{http://www.w3.org/2005/Atom}link",
        attrib={
            "href": "%s/feed/" % (SITEVARS["url"]),
            "rel": "self",
            "type": "application/rss+xml",
        },
    )
    hublink = etree.SubElement(
        feed,
        "{http://www.w3.org/2005/Atom}link",
        attrib={
            "href": SITEVARS["hub"],
            "rel": "hub",
        },
    )
    sitelink = etree.SubElement(
        feed,
        "{http://www.w3.org/2005/Atom}link",
        attrib={
            "href": SITEVARS["url"],
            "rel": "alternate",
            "type": "text/html",
        },
    )

    icon = etree.SubElement(feed, "{http://www.w3.org/2005/Atom}icon")
    icon.text = "%s/favicon.png" % (SITEVARS["url"])

    htmlentries = []
    sitemapentries = []
    rss_cntr = 0
    for entry in entries:
        if entry.is_future:
            continue
        if "post" != entry.type:
            continue

        sitemapentries.append(entry.url)

        if 14 == rss_cntr:
            continue

        htmlentries.append(entry.tmplvars)

        xmlentry = etree.SubElement(feed, "{http://www.w3.org/2005/Atom}entry")
        eid = etree.SubElement(xmlentry, "{http://www.w3.org/2005/Atom}id")
        eid.text = entry.url

        etitle = etree.SubElement(
            xmlentry, "{http://www.w3.org/2005/Atom}title"
        )
        etitle.text = entry.title
        eupdated = etree.SubElement(
            xmlentry, "{http://www.w3.org/2005/Atom}updated"
        )
        eupdated.text = entry.updated

        epublished = etree.SubElement(
            xmlentry, "{http://www.w3.org/2005/Atom}published"
        )
        epublished.text = entry.dt.isoformat()

        atomauthor = etree.SubElement(
            xmlentry, "{http://www.w3.org/2005/Atom}author"
        )
        atomauthor_name = etree.SubElement(
            atomauthor, "{http://www.w3.org/2005/Atom}name"
        )
        atomauthor_name.text = entry.meta["author"]["name"]

        elink = etree.SubElement(
            xmlentry,
            "{http://www.w3.org/2005/Atom}link",
            attrib={
                "href": entry.tmplvars["url"],
                "rel": "alternate",
                "type": "text/html",
            },
        )

        ecategory = etree.SubElement(
            xmlentry,
            "{http://www.w3.org/2005/Atom}category",
        )
        ecategory.text = entry.category

        atomsummary = etree.SubElement(
            xmlentry,
            "{http://www.w3.org/2005/Atom}summary",
            attrib={"type": "html"},
        )
        atomsummary.text = entry.description

        if "image" in entry.tmplvars:
            img = etree.SubElement(
                xmlentry,
                "{http://www.w3.org/2005/Atom}link",
                attrib={
                    "rel": "enclosure",
                    "href": entry.tmplvars["image"]["href"],
                    "type": entry.tmplvars["image"]["mime"],
                    "length": str(entry.tmplvars["image"]["bytesize"]),
                },
            )

        cdata = "%s\n\n%s" % (entry.description, entry.html)
        if "in-reply-to" in entry.meta:
            cdata = '<p>This post is a reply to: <a href="%s">%s</a></p>%s' % (
                entry.meta["in-reply-to"],
                entry.meta["in-reply-to"],
                cdata,
            )

        atomcontent = etree.SubElement(
            xmlentry,
            "{http://www.w3.org/2005/Atom}content",
            attrib={"type": "html"},
        )
        atomcontent.text = cdata

        rss_cntr = rss_cntr + 1

    LOGGER.info("saving XML")
    with open(xmlfeedfile, "wb") as f:
        f.write(
            etree.tostring(
                xmldoc,
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )
        )

    LOGGER.info("saving HTML")
    with open(htmlfeedfile, "wt") as f:
        tmpl = J2.get_template("hfeed.j2.html")
        tmplvars = {"feed": SITEVARS, "entries": htmlentries}
        content = tmpl.render(tmplvars)
        f.write(content)

    LOGGER.info("saving sitemap")
    with open(sitemapfile, "wt") as f:
        f.write("\n".join(sitemapentries))

    return


def run():
    freshest_mtime = 0

    everything = {
        # unix timestamp: Entry object
    }
    categories = {
        # category name string: Entry object
    }
    feed = {
        # unix timestamp: Entry object
    }
    # collect data first
    for e in sorted(
        glob.glob(os.path.join(BASEPATH, "**", "index.md"), recursive=True)
    ):
        doc = Entry(e)
        LOGGER.info(f"parsing {doc.type} :: {doc.category} :: {doc.entry}")

        # these potentially change the mtime of the doc, so it should be as
        # soon as possible
        doc.backfill_flickr()
        doc.backfill_archiveorg()

        ts = int(doc.dt.timestamp())
        everything[ts] = doc
        freshest_mtime = max(doc.mtime, freshest_mtime)
        if "category" == doc.type and doc.entry not in categories:
            categories[doc.entry] = doc

    # sort out categories and their posts
    # select which posts can go into the feed(s)
    # populate search, if needed
    search = SearchDB()
    search_on = False
    if freshest_mtime > search.mtime:
        search_on = True
        search.open()

    for mtime, post in everything.items():
        if "post" != post.type:
            continue

        if post.category not in categories:
            continue

        if post.is_future:
            LOGGER.warning(
                f"skipping future entry {post.category} :: {post.entry} (sheduled for {post.dt})"
            )
            continue

        post_ts = int(post.dt.timestamp())

        if post_ts in categories[post.category].subentries:
            maybe_problem = categories[post.category].subentries[post_ts]
            LOGGER.warning(
                f"TIMESTAMP COLLISION IN CATEGORY {post.category}: {post.fpath} vs {maybe_problem.fpath}"
            )
        else:
            categories[post.category].subentries[post_ts] = post

        if post_ts in feed:
            maybe_problem = feed[post_ts]
            LOGGER.warning(
                f"TIMESTAMP COLLISION IN FEED: {post.fpath} vs {maybe_problem.fpath}"
            )
        else:
            feed[post_ts] = post

        if search_on:
            search.append(post)

    if search_on:
        search.__exit__()

    # render
    for post in everything.values():
        try:
            post.images
            str(post)
        except NotImplementedError as err:
            LOGGER.error(f"{post.fpath} needs to wait")

    # create feeds
    mkfeed([feed[k] for k in sorted(feed.keys(), reverse=True)])


if __name__ == "__main__":
    run()
