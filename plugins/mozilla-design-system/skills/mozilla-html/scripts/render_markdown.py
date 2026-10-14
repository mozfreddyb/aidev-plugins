#!/usr/bin/env python3
"""Render Markdown as portable Mozilla HTML (requires Pandoc and Python 3).

Example: python3 -I render_markdown.py report.md --theme mozilla -o report.html
"""
import argparse
import base64
import copy
import html
from html.parser import HTMLParser
import json
import mimetypes
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET

SCRIPTS = pathlib.Path(__file__).resolve().parent
ASSETS = SCRIPTS.parent / "assets"
FONT_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mozilla+Headline:wdth,wght@75..100,200..700&family=Mozilla+Text:wght@200..700&display=swap">'
ET.register_namespace("", "http://www.w3.org/2000/svg")


def pandoc_html(document):
    return subprocess.check_output(
        ["pandoc", "--from=json", "--to=html5", "--section-divs", "--syntax-highlighting=none"],
        input=json.dumps(document), text=True,
    )


def plain_text(inlines):
    """Extract readable title text while retaining the original heading markup."""
    parts = []
    for node in inlines:
        kind, content = node["t"], node.get("c")
        if kind == "Str":
            parts.append(content)
        elif kind in ("Space", "SoftBreak", "LineBreak"):
            parts.append(" ")
        elif kind in ("Code", "Math"):
            parts.append(content[-1])
        elif kind in ("Link", "Image", "Span"):
            parts.append(plain_text(content[1]))
        elif kind == "Quoted":
            parts.append(plain_text(content[1]))
        elif kind in ("Emph", "Strong", "Strikeout", "Superscript", "Subscript", "SmallCaps", "Underline"):
            parts.append(plain_text(content))
    return "".join(parts)


def blocks_of_type(value, kind):
    if isinstance(value, dict):
        if value.get("t") == kind:
            yield value
        for child in value.values():
            yield from blocks_of_type(child, kind)
    elif isinstance(value, list):
        for child in value:
            yield from blocks_of_type(child, kind)


class DocumentHTML(HTMLParser):
    """Apply table recipes and embed images without touching document prose."""
    def __init__(self, source_dir, tables):
        super().__init__(convert_charrefs=False)
        self.source_dir = source_dir
        self.table_class = "moz-table striped" + {"plain": " plain", "accent": "", "compact": " compact plain"}[tables]
        self.parts = []
        self.image_number = 0
        self.in_thead = 0
        self.in_figure = 0
        self.ids = set()

    def image(self, attrs):
        src = attrs.get("src", "")
        if src.startswith("data:"):
            return None
        url = urllib.parse.urlsplit(src)
        if url.scheme or url.netloc:
            raise ValueError(f"Use a local image for portable output: {src}")
        path = self.source_dir / urllib.parse.unquote(url.path)
        if path.suffix.lower() != ".svg":
            mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
            attrs["src"] = f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"
            return None
        svg = ET.parse(path).getroot()
        self.image_number += 1
        # Multiple copies of an SVG may contain matching gradient/clip IDs.
        ids = {e.get("id"): f"md-image-{self.image_number}-{e.get('id')}" for e in svg.iter() if e.get("id")}
        for element in svg.iter():
            for name, value in list(element.attrib.items()):
                if name == "id":
                    element.set(name, ids[value])
                elif name.rsplit("}", 1)[-1] in ("href", "aria-labelledby", "aria-describedby"):
                    if value.startswith("#") and value[1:] in ids:
                        element.set(name, "#" + ids[value[1:]])
                    elif name.startswith("aria-"):
                        element.set(name, " ".join(ids.get(part, part) for part in value.split()))
                elif "url(#" in value:
                    element.set(name, re.sub(r"url\(#([^)]*)\)", lambda m: f"url(#{ids.get(m[1], m[1])})", value))
            if element.tag.rsplit("}", 1)[-1] == "style" and element.text:
                for old, new in ids.items():
                    element.text = element.text.replace(f"url(#{old})", f"url(#{new})")
        if not svg.get("viewBox") and svg.get("width", "").isdigit() and svg.get("height", "").isdigit():
            svg.set("viewBox", f"0 0 {svg.get('width')} {svg.get('height')}")
        svg.set("role", "img")
        svg.set("aria-label", attrs.get("alt", ""))
        svg.set("focusable", "false")
        for name in ("class", "id"):
            if name in attrs:
                svg.set(name, attrs[name])
        markup = '<div class="chart-scroll">' + ET.tostring(svg, encoding="unicode") + '</div>'
        # Pandoc already wraps standalone images in figures; inline images need
        # their own chart wrapper to get the component's responsive styling.
        if not self.in_figure:
            markup = '<span class="markdown-image">' + ET.tostring(svg, encoding="unicode") + '</span>'
        return markup

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "table":
            self.parts.append('<div class="moz-table-wrapper" tabindex="0" role="region" aria-label="Document data">')
            attrs["class"] = (attrs.get("class", "") + " " + self.table_class).strip()
        elif tag == "thead":
            self.in_thead += 1
        elif tag == "th" and "scope" not in attrs:
            attrs["scope"] = "col" if self.in_thead else "row"
        elif tag == "figure":
            self.in_figure += 1
            attrs["class"] = (attrs.get("class", "") + " moz-chart").strip()
        elif tag == "img":
            markup = self.image(attrs)
            if markup is not None:
                self.parts.append(markup)
                return
        rendered = "".join(f' {key}="{html.escape(value, quote=True)}"' if value is not None else f" {key}" for key, value in attrs.items())
        self.parts.append(f"<{tag}{rendered}>")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")
        if tag == "table":
            self.parts.append("</div>")
        elif tag == "thead":
            self.in_thead -= 1
        elif tag == "figure":
            self.in_figure -= 1

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")


def bundle(source, output):
    subprocess.run([sys.executable, "-I", str(SCRIPTS / "bundle.py"), str(source), "-o", str(output)], check=True)
    subprocess.run([sys.executable, "-I", str(SCRIPTS / "check.py"), str(output)], check=True)


def render(source, output, theme="acorn", layout="sidebar", toc=True, scheme="auto", tables="plain"):
    if not shutil.which("pandoc"):
        raise ValueError("Markdown rendering requires Pandoc in PATH; the HTML workflow does not.")
    source, output = pathlib.Path(source).resolve(), pathlib.Path(output).resolve()
    src = output.with_suffix(".src.html")
    if source in (output, src):
        raise ValueError("Output paths must differ from the Markdown source")
    document = json.loads(subprocess.check_output(["pandoc", str(source), "--from=markdown", "--to=json"], text=True, cwd=source.parent))
    headings = list(blocks_of_type(document["blocks"], "Header"))
    h1s = [node for node in headings if node["c"][0] == 1]
    if len(h1s) > 1:
        raise ValueError("Use one level-one heading, or a YAML title with level-two sections")
    if h1s:
        heading_block = copy.deepcopy(h1s[0])
        title = plain_text(heading_block["c"][2])
        h1s[0].clear()
        h1s[0].update({"t": "RawBlock", "c": ["html", ""]})
    else:
        metadata_title = document["meta"].get("title", {})
        if metadata_title.get("t") == "MetaInlines":
            inlines = metadata_title["c"]
        elif metadata_title.get("t") == "MetaString":
            inlines = [{"t": "Str", "c": metadata_title["c"]}]
        else:
            raise ValueError("Markdown needs a level-one heading or a YAML title")
        title = plain_text(inlines)
        heading_block = {"t": "Header", "c": [1, ["document-title", [], []], inlines]}
    if not title.strip():
        raise ValueError("Document title must contain text")
    heading_doc = {**document, "meta": {}, "blocks": [heading_block]}
    # Without section-divs here: the header must contain only the original h1.
    heading = subprocess.check_output(["pandoc", "--from=json", "--to=html5"], input=json.dumps(heading_doc), text=True).strip()
    navigation = []
    for node in headings:
        if node.get("t") == "Header" and node["c"][0] == 2:
            target = html.escape(node["c"][1][0], quote=True)
            # A heading may itself contain a link; navigation labels must not
            # introduce nested anchors.
            label = html.escape(plain_text(node["c"][2]))
            navigation.append(f'<a class="moz-page-nav-button" href="#{target}"><span class="label">{label}</span></a>')
    parser = DocumentHTML(source.parent, tables)
    parser.feed(pandoc_html(document))
    parser.close()
    main_id = "markdown-document"
    while main_id in parser.ids or main_id == heading_block["c"][1][0]:
        main_id += "-main"
    nav = ""
    if toc and navigation:
        nav_class = "moz-page-nav markdown-nav" if layout == "sidebar" else "markdown-toc moz-card"
        nav = f'<nav class="{nav_class}" aria-label="Document sections"><p class="heading"><svg class="moz-icon" data-icon="list"></svg><span class="label">On this page</span></p><div class="group">{"".join(navigation)}</div></nav>'
    print_button = '<button class="moz-button no-print" type="button" onclick="window.print()"><svg class="moz-icon" data-icon="print"></svg>Print document</button>'
    header = f'<header class="moz-page-header markdown-header"><div class="heading">{heading}</div>{print_button}</header>'
    masthead = ""
    if theme != "acorn":
        brand_name = "Firefox" if theme == "firefox" else "Mozilla"
        masthead = f'<header class="moz-masthead"><svg data-logo="{theme}-lockup" aria-label="{brand_name}"></svg>{print_button}</header>'
        header = f'<section class="moz-hero markdown-hero">{heading}</section>'
    attributes = f' data-brand="{theme}"' if theme != "acorn" else ""
    if scheme != "auto":
        attributes += f' data-color-scheme="{scheme}"'
    values = {
        "title": html.escape(title), "attributes": attributes,
        "fonts": FONT_LINK if theme != "acorn" else "",
        "masthead": masthead, "header": header, "body": "".join(parser.parts),
        "outer_class": "moz-page" if layout == "sidebar" else "markdown-page",
        "main_class": "moz-main markdown-content" + (" wide" if layout != "reading" else ""),
        "sidebar": nav if layout == "sidebar" else "",
        "toc": nav if layout != "sidebar" else "",
        "tokens": str(ASSETS / "tokens.css"), "components": str(ASSETS / "components.css"),
        "css": str(ASSETS / "markdown.css"),
        "main_id": main_id,
    }
    template = (ASSETS / "markdown-template.html").read_text(encoding="utf-8")
    rendered = re.sub(r"\$([a-z_]+)\$", lambda m: values[m[1]], template)
    output.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(rendered, encoding="utf-8")
    bundle(src, output)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=pathlib.Path)
    parser.add_argument("-o", "--output", type=pathlib.Path, help="default: beside input, with .html extension")
    parser.add_argument("--theme", choices=["acorn", "firefox", "mozilla"], default="acorn")
    parser.add_argument("--layout", choices=["reading", "wide", "sidebar"], default="sidebar")
    parser.add_argument("--toc", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--scheme", choices=["auto", "light", "dark"], default="auto")
    parser.add_argument("--tables", choices=["plain", "accent", "compact"], default="plain")
    args = parser.parse_args()
    try:
        render(args.markdown, args.output or args.markdown.with_suffix(".html"), args.theme, args.layout, args.toc, args.scheme, args.tables)
    except (OSError, ValueError, ET.ParseError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"render_markdown: {exc}\n")


if __name__ == "__main__":
    main()
