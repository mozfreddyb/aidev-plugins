#!/usr/bin/env python3
"""Integration tests for Markdown conversion (requires Pandoc)."""
import base64
from html.parser import HTMLParser
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / "render_markdown.py"


class Page(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.tags = []
        self.text = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, text):
        self.text.append(text)

    def find(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


@unittest.skipUnless(shutil.which("pandoc"), "requires Pandoc")
class RenderMarkdown(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.source = self.root / "documents" / "sample.md"
        self.source.parent.mkdir()
        self.source.write_text("# A **formatted** title\n\n## Results {#measurements}\n\nWords & numbers: 64 ms.\n\n| Path | Median |\n|---|---:|\n| A | 64 ms |\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def run_renderer(self, *options, succeeds=True):
        output = self.root / "elsewhere" / "output.html"
        proc = subprocess.run([sys.executable, "-I", str(SCRIPT), str(self.source), "-o", str(output), *options], cwd=self.root, text=True, capture_output=True)
        if succeeds:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            return Page(output.read_text()), output.read_text()
        self.assertNotEqual(proc.returncode, 0)
        return proc

    def test_theme_layout_matrix(self):
        original = self.source.read_bytes()
        for theme in ("acorn", "firefox", "mozilla"):
            for layout in ("reading", "wide", "sidebar"):
                with self.subTest(theme=theme, layout=layout):
                    page, markup = self.run_renderer("--theme", theme, "--layout", layout)
                    self.assertEqual(len(page.find("h1")), 1)
                    self.assertEqual(page.find("html")[0].get("data-brand"), None if theme == "acorn" else theme)
                    self.assertNotIn("data-color-scheme", page.find("html")[0])
                    self.assertIn('href="#measurements"', markup)
                    self.assertIn("<strong>formatted</strong>", markup)
                    self.assertIn("64 ms", "".join(page.text))
                    self.assertTrue(all("scope" in attrs for attrs in page.find("th")))
                    self.assertFalse([attrs for attrs in page.find("link") if attrs.get("href", "").endswith(".css")])
                    self.assertFalse([attrs for attrs in page.find("svg") if "data-icon" in attrs and "viewbox" not in attrs])
                    self.assertEqual("wide" in page.find("main")[0]["class"].split(), layout != "reading")
        self.assertEqual(self.source.read_bytes(), original)

    def test_options_and_yaml_title(self):
        self.source.write_text('---\ntitle: A metadata title\n---\n\n## Content\n\n| Value |\n|---|\n| 42 |\n')
        page, markup = self.run_renderer("--no-toc", "--scheme", "dark", "--tables", "accent", "--layout", "reading")
        self.assertEqual(page.find("nav"), [])
        self.assertEqual(page.find("html")[0]["data-color-scheme"], "dark")
        self.assertEqual(len(page.find("h1")), 1)
        self.assertIn("A metadata title", "".join(page.text))
        self.assertNotIn("plain", page.find("table")[0]["class"])
        self.assertNotIn("wide", page.find("main")[0]["class"])
        _, markup = self.run_renderer("--tables", "compact")
        self.assertIn('class="moz-table striped compact plain"', markup)

    def test_images_are_relative_embedded_and_svg_ids_are_unique(self):
        image = self.source.parent / "chart with spaces.svg"
        image.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><linearGradient id="shade"><stop stop-color="#abcdef"/></linearGradient></defs><rect fill="url(#shade)" width="64" height="77"/></svg>')
        raster = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a1XkAAAAASUVORK5CYII=")
        (self.source.parent / "pixel.png").write_bytes(raster)
        self.source.write_text('# Images\n\n## Figures\n\n![Chart one](chart%20with%20spaces.svg)\n\n![Chart two](chart%20with%20spaces.svg)\n\n![Pixel](pixel.png)\n')
        page, markup = self.run_renderer()
        ids = [a["id"] for _, a in page.tags if "id" in a]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn('fill="url(#md-image-1-shade)"', markup)
        self.assertIn('fill="url(#md-image-2-shade)"', markup)
        self.assertIn('stop-color="#abcdef"', markup)
        self.assertIn('width="64" height="77"', markup)
        self.assertTrue(page.find("img")[0]["src"].startswith("data:image/png;base64,"))
        self.assertIn('aria-label="Chart one"', markup)

    def test_bad_input_leaves_no_output(self):
        for source in ("No title\n", "# One\n\n# Two\n", "# Image\n\n![Remote](https://example.com/image.png)\n"):
            with self.subTest(source=source):
                self.source.write_text(source)
                self.run_renderer(succeeds=False)
                self.assertFalse((self.root / "elsewhere/output.html").exists())

    def test_source_cannot_be_overwritten(self):
        original = self.source.read_bytes()
        result = subprocess.run([sys.executable, "-I", str(SCRIPT), str(self.source), "-o", str(self.source)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.source.read_bytes(), original)

    def test_heading_links_and_landmark_ids(self):
        self.source.write_text('# Title {#markdown-document}\n\n## [Results](https://example.com) {#results}\n\nA paragraph.\n')
        page, markup = self.run_renderer()
        ids = [a["id"] for _, a in page.tags if "id" in a]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(page.find("main")[0]["id"], "markdown-document-main")
        nav = markup.split('<nav ', 1)[1].split('</nav>', 1)[0]
        self.assertNotIn('href="https://example.com"', nav)
        self.assertIn('href="#results"', nav)


if __name__ == "__main__":
    unittest.main()
