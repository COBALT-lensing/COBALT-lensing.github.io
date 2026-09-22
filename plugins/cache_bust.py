"""Version local asset references after Pelican has copied the final asset bytes."""
from hashlib import sha256
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urlencode, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

from pelican import signals


class AssetURLs:
    def __init__(self, output, siteurl):
        self.origin = (siteurl or "http://localhost").rstrip("/") + "/"
        self.hashes = {}
        for directory in ("theme", "assets"):
            for path in (output / directory).rglob("*"):
                if path.is_file():
                    url = urljoin(self.origin, path.relative_to(output).as_posix())
                    self.hashes[url] = sha256(path.read_bytes()).hexdigest()[:16]

    def version(self, value, document_url):
        if not value or value.startswith("#"):
            return value
        resolved = urlsplit(urljoin(document_url, value))
        key = urlunsplit((resolved.scheme, resolved.netloc, unquote(resolved.path), "", ""))
        digest = self.hashes.get(key)
        if not digest:
            return value
        original = urlsplit(value)
        query = [(key, val) for key, val in parse_qsl(original.query, keep_blank_values=True) if key != "v"]
        query.append(("v", digest))
        return urlunsplit(original._replace(query=urlencode(query)))


class AssetHTML(HTMLParser):
    # Parse real start tags, preserving all other HTML, SVG, scripts and whitespace.
    attributes = re.compile(r'''(\s(?:src|href|poster)\s*=\s*)(["'])(.*?)\2''', re.I | re.S)

    def __init__(self, text, assets, document_url):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.assets = assets
        self.document_url = document_url
        self.edits = []
        self.line_offsets = [0]
        for match in re.finditer("\n", text):
            self.line_offsets.append(match.end())
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        original = self.get_starttag_text()

        def replace(match):
            value = unescape(match[3])
            versioned = self.assets.version(value, self.document_url)
            if value == versioned:
                return match[0]
            return match[1] + match[2] + escape(versioned, quote=True) + match[2]

        updated = self.attributes.sub(replace, original)
        if updated != original:
            line, column = self.getpos()
            start = self.line_offsets[line - 1] + column
            self.edits.append((start, start + len(original), updated))

    handle_startendtag = handle_starttag

    def rendered(self):
        text = self.text
        for start, end, updated in reversed(self.edits):
            text = text[:start] + updated + text[end:]
        return text


def version_assets(pelican):
    output = Path(pelican.settings["OUTPUT_PATH"])
    assets = AssetURLs(output, pelican.settings["SITEURL"])
    for path in output.rglob("*.html"):
        original = path.read_text(encoding="utf-8")
        url = urljoin(assets.origin, path.relative_to(output).as_posix())
        updated = AssetHTML(original, assets, url).rendered()
        if updated != original:
            path.write_text(updated, encoding="utf-8")

    # Atom stores article HTML as escaped text, including images in summaries.
    feed_name = pelican.settings.get("FEED_ALL_ATOM")
    if feed_name and (output / feed_name).is_file():
        path = output / feed_name
        tree = ET.parse(path)
        namespace = "http://www.w3.org/2005/Atom"
        changed = False
        for entry in tree.findall(f"{{{namespace}}}entry"):
            link = entry.find(f"{{{namespace}}}link")
            url = link.get("href", assets.origin) if link is not None else assets.origin
            for name in ("content", "summary"):
                element = entry.find(f"{{{namespace}}}{name}")
                if element is not None and element.get("type") == "html" and element.text:
                    updated = AssetHTML(element.text, assets, url).rendered()
                    changed |= updated != element.text
                    element.text = updated
        if changed:
            ET.register_namespace("", namespace)
            tree.write(path, encoding="utf-8", xml_declaration=True)


def register():
    signals.finalized.connect(version_assets)
