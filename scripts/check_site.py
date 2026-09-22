"""Check the production output for missing pages, broken local links and lost maths."""
from html.parser import HTMLParser
from hashlib import sha256
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path("output")
ORIGIN = "https://cobalt-lensing.github.io"


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.headings = 0
        self.missing_alt = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        if tag == "img" and "alt" not in attrs:
            self.missing_alt = True
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


def check():
    errors = []
    required = [
        "index.html", "about/index.html", "science/index.html",
        "CitizenScience/index.html", "Alerts/index.html", "Members/index.html",
        "news/index.html", "404.html", "feed.xml",
        "2021/08/11/a-post-with-a-picture.html",
        "2021/08/11/the-cobalt-project-has-a-new-website.html",
    ]
    members = "Adam Charlie Daniela Greg Hugh Maddie Marika Matt Nora Poshak Simon".split()
    required += [f"{name}.html" for name in members]
    required += [f"{name}.md" for name in members]
    for name in required:
        if not (ROOT / name).is_file():
            errors.append(f"Missing expected output: {name}")

    documents = {}
    for path in ROOT.rglob("*.html"):
        text = path.read_text()
        document = documents[path] = Document(text)
        if "{%" in text or "{{" in text:
            errors.append(f"Unrendered template syntax: {path}")
        if document.headings != 1:
            errors.append(f"Expected one primary heading: {path}")
        if document.missing_alt:
            errors.append(f"Image without alt text: {path}")

    for path, document in documents.items():
        base = ORIGIN + "/" + path.relative_to(ROOT).as_posix()
        for link in document.links:
            url = urlsplit(urljoin(base, link))
            if url.scheme not in ("http", "https") or url.netloc != urlsplit(ORIGIN).netloc:
                continue
            target = ROOT / unquote(url.path).lstrip("/")
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"Broken link in {path}: {link}")
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                errors.append(f"Missing anchor in {path}: {link}")
            if target.is_file() and url.path.startswith(("/theme/", "/assets/")):
                expected = sha256(target.read_bytes()).hexdigest()[:16]
                if parse_qs(url.query).get("v") != [expected]:
                    errors.append(f"Missing or stale asset version in {path}: {link}")

    science = ROOT / "science/index.html"
    if science.exists():
        text = science.read_text()
        if text.count('<div class="arithmatex">') != 3 or "R_{E}" not in text or "mathjax@3.2.2" not in text:
            errors.append("Science page lost display equations or MathJax support")
    feed = ROOT / "feed.xml"
    if feed.exists():
        tree = ET.parse(feed)
        if len(tree.findall("{http://www.w3.org/2005/Atom}entry")) < 2:
            errors.append("News feed is missing migrated articles")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(documents)} HTML pages: URLs, local links, anchors, headings, images, equations and feed OK.")


if __name__ == "__main__":
    check()
