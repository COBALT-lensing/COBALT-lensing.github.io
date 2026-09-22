from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
import xml.etree.ElementTree as ET

from plugins.cache_bust import AssetHTML, AssetURLs, version_assets


class CacheBustTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        (self.output / "theme/css").mkdir(parents=True)
        (self.output / "assets").mkdir()
        self.css = self.output / "theme/css/site.css"
        self.css.write_text("body { color: white; }")
        (self.output / "assets/star.svg").write_text("<svg/>")

    def test_versions_follow_contents_not_build_time(self):
        def version():
            return AssetURLs(self.output, "").version(
                "/theme/css/site.css", "http://localhost/"
            )

        original = version()
        self.css.touch()
        self.assertEqual(original, version())
        self.css.write_text("body { color: blue; }")
        self.assertNotEqual(original, version())

    def test_relative_absolute_external_urls_and_existing_parameters(self):
        assets = AssetURLs(self.output, "https://example.org")
        base = "https://example.org/news/index.html"
        value = assets.version("../assets/star.svg?size=2&v=old#star", base)
        self.assertTrue(value.startswith("../assets/star.svg?size=2&v="))
        self.assertTrue(value.endswith("#star"))
        self.assertNotIn("old", value)
        self.assertEqual(value, assets.version(value, base))
        self.assertIn("?v=", assets.version("https://example.org/assets/star.svg", base))
        for url in ["https://cdn.example.org/assets/star.svg", "data:image/svg+xml,test",
                    "#star", "/news/", "/assets/missing.png"]:
            self.assertEqual(url, assets.version(url, base))

    def test_preserves_markup_and_script_contents(self):
        assets = AssetURLs(self.output, "")
        script = '<script>const example = \'<img src="/assets/star.svg">\';</script>'
        html = '<!doctype html>\n<!-- keep -->\n' + script + '\n<img src="/assets/star.svg?x=1&amp;y=2" alt="Star"/>'
        result = AssetHTML(html, assets, "http://localhost/").rendered()
        self.assertIn(script, result)
        self.assertIn('x=1&amp;y=2&amp;v=', result)
        self.assertTrue(result.startswith('<!doctype html>\n<!-- keep -->\n'))
        self.assertTrue(result.endswith(' alt="Star"/>'))

    def test_build_versions_html_and_atom_and_can_run_twice(self):
        page = self.output / "index.html"
        page.write_text('<link href="/theme/css/site.css"><img src="/assets/star.svg">')
        feed = self.output / "feed.xml"
        feed.write_text('''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <link href="https://example.org/news/post.html"/>
          <content type="html">&lt;img src="/assets/star.svg"&gt;</content>
        </entry></feed>''')
        pelican = SimpleNamespace(settings={
            "OUTPUT_PATH": str(self.output), "SITEURL": "https://example.org",
            "FEED_ALL_ATOM": "feed.xml",
        })
        version_assets(pelican)
        first = page.read_text(), feed.read_text()
        self.assertEqual(page.read_text().count("?v="), 2)
        content = ET.parse(feed).find(".//{http://www.w3.org/2005/Atom}content")
        self.assertIn("?v=", content.text)
        version_assets(pelican)
        self.assertEqual(first, (page.read_text(), feed.read_text()))


if __name__ == "__main__":
    unittest.main()
