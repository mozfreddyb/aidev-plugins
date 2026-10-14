#!/usr/bin/env python3
"""Check a generated HTML page against the Mozilla design system rules.

Reports errors (the page is broken or not self-contained) and warnings
(likely departures from Acorn / brand guidance). Exit status is 1 if there
are errors. Heuristic: read each warning and decide; don't silence by rote.

Usage:
  python3 -I check.py page.html
"""

import html.parser
import pathlib
import re
import sys

BRANDS = {"firefox", "mozilla"}
FONT_HOSTS = ("https://fonts.googleapis.com", "https://fonts.gstatic.com",
              "https://cdn.jsdelivr.net/gh/mozilla/mozilla-type-family")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "source", "track", "wbr"}
SMALL_WORDS = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of",
               "on", "or", "the", "to", "vs", "via", "with", "per"}
BAD_LABELS = {"ok", "okay", "submit", "click here", "click", "yes", "no"}
VAGUE_LINKS = {"here", "click here", "this", "link", "more", "read more"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F1E6-\U0001F1FF]")
COLOR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch|hwb)\(")
PX_FONT = re.compile(r"font(?:-size)?\s*:[^;{}]*\b\d+(?:\.\d+)?px")


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors, self.warnings = [], []
        self.html_attrs = {}
        self.title = ""
        self.viewport = False
        self.styles = []          # (line, css) for page-authored <style>
        self.labels_for = set()
        self.ids = {}
        self.controls = []        # (line, attrs, inside_label)
        self.headings = []        # (line, level, text)
        self.buttons = []         # (line, attrs, text)
        self.links = []           # (line, attrs, text)
        self.capture = []         # open elements collecting text
        self.text_runs = []       # (line, text) visible text
        self.font_link = False

    def err(self, line, msg):
        self.errors.append((line, msg))

    def warn(self, line, msg):
        self.warnings.append((line, msg))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if "id" in a:
            self.ids[a["id"]] = tag
        if tag == "html":
            self.html_attrs = a
        elif tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        elif tag == "link" and "stylesheet" in (a.get("rel") or "").split():
            href = a.get("href") or ""
            if href.startswith(FONT_HOSTS):
                self.font_link = True
            elif re.match(r"^(https?:)?//", href):
                self.warn(line, f"remote stylesheet {href!r}: the page depends on the network")
            else:
                self.err(line, f"stylesheet {href!r} is not inlined; run scripts/bundle.py")
        elif tag == "script" and a.get("src"):
            self.warn(line, f"external script {a['src']!r}: inline it or drop it so the file stays portable")
        elif tag == "img":
            if "alt" not in a:
                self.err(line, "<img> without alt (use alt=\"\" if decorative)")
            src = a.get("src") or ""
            if src and not re.match(r"^(data:|https?:)", src):
                self.warn(line, f"<img src={src!r}> is a local path; embed it as a data: URI or SVG")
        elif tag == "svg" and ("data-icon" in a or "data-logo" in a) and "viewbox" not in a:
            self.err(line, "icon/logo placeholder not expanded; run scripts/bundle.py")
        elif tag == "label" and a.get("for"):
            self.labels_for.add(a["for"])
        elif tag in ("input", "select", "textarea"):
            if a.get("type") not in ("hidden", "submit", "button", "reset", "image"):
                self.controls.append((line, a, any(t == "label" for t, *_ in self.stack)))
        if tag == "style":
            self.capture_style = (line, [])
        if a.get("style"):
            self.check_css(line, a["style"], inline=True)

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "button", "a", "title"):
            self.capture.append([tag, line, a, []])
        if tag not in VOID:
            self.stack.append((tag, a))

    def handle_endtag(self, tag):
        if tag == "style" and getattr(self, "capture_style", None):
            line, parts = self.capture_style
            css = "".join(parts)
            # Inlined design-system sheets are marked by bundle.py.
            if not re.match(r"\s*/\* (tokens|components)\.css \*/", css):
                self.styles.append((line, css))
            self.capture_style = None
        for i in range(len(self.capture) - 1, -1, -1):
            if self.capture[i][0] == tag:
                t, line, a, parts = self.capture.pop(i)
                text = " ".join("".join(parts).split())
                if t == "title":
                    self.title = text
                elif t.startswith("h"):
                    self.headings.append((line, int(t[1]), text))
                elif t == "button":
                    self.buttons.append((line, a, text))
                elif t == "a":
                    self.links.append((line, a, text))
                break
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if getattr(self, "capture_style", None):
            self.capture_style[1].append(data)
            return
        for c in self.capture:
            c[3].append(data)
        tags = {t for t, _ in self.stack}
        if tags & {"script", "style", "code", "pre", "kbd", "samp", "svg", "title"}:
            return
        if data.strip():
            self.text_runs.append((self.getpos()[0], data))

    def check_css(self, line, css, inline=False):
        where = "style attribute" if inline else "<style>"
        stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        for m in COLOR_LITERAL.finditer(stripped):
            ctx = stripped[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")
            if re.search(r"--[\w-]+\s*:\s*[^;]*$", stripped[:m.start()].rsplit(";", 1)[-1]):
                continue  # defining a custom property is fine (e.g. a local alias)
            self.warn(line, f"color literal in {where}: …{ctx.strip()}… use a token such as var(--text-color)")
            break
        if PX_FONT.search(stripped):
            self.warn(line, f"px font size in {where}; use var(--font-size-*) tokens")


def sentence_case_problem(text):
    words = re.findall(r"[A-Za-z][A-Za-z’'-]*", text)
    rest = [w for w in words[1:] if w.lower() not in SMALL_WORDS and len(w) > 3]
    if len(rest) < 2:
        return False
    caps = [w for w in rest if w[0].isupper() and not w.isupper()]
    return len(caps) >= 2 and len(caps) / len(rest) > 0.6


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = pathlib.Path(sys.argv[1])
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))

    if not p.html_attrs.get("lang"):
        p.err(1, "<html> needs a lang attribute")
    brand = p.html_attrs.get("data-brand")
    if brand is not None and brand not in BRANDS:
        p.err(1, f"unknown data-brand={brand!r}; use firefox, mozilla, or omit it")
    if brand in BRANDS and not p.font_link:
        p.warn(1, "brand page without the Mozilla Headline/Text font link; type falls back to Helvetica/Arial")
    if not p.title:
        p.err(1, "missing <title>")
    if not p.viewport:
        p.warn(1, "missing <meta name=viewport>")

    for line, css in p.styles:
        p.check_css(line, css)

    for line, a, inside_label in p.controls:
        named = (inside_label or a.get("id") in p.labels_for
                 or a.get("aria-label") or a.get("aria-labelledby") or a.get("title"))
        if not named:
            p.err(line, f"<{a.get('type', 'input')}> control without a label")
        if a.get("placeholder") and not (inside_label or a.get("id") in p.labels_for):
            p.warn(line, "placeholder is not a label; add a visible <label>")

    primaries = [l for l, a, _ in p.buttons + p.links
                 if "primary" in (a.get("class") or "").split()]
    if len(primaries) > 1:
        p.warn(primaries[1], f"{len(primaries)} primary buttons; Acorn allows one per view (lines {primaries})")

    for line, a, text in p.buttons:
        label = text or a.get("aria-label") or a.get("title") or ""
        if not label.strip():
            p.err(line, "button without text or aria-label")
        elif label.strip().lower() in BAD_LABELS:
            p.warn(line, f"button label {label!r}: use a verb that says what happens")
        elif label.endswith((".", "!")):
            p.warn(line, f"button label {label!r} ends with punctuation")
    for line, a, text in p.links:
        if text.strip().lower() in VAGUE_LINKS:
            p.warn(line, f"link text {text!r} doesn't say where it goes")

    last = 0
    for line, level, text in p.headings:
        if last and level > last + 1:
            p.warn(line, f"heading level skips from h{last} to h{level}")
        last = level
        if sentence_case_problem(text):
            p.warn(line, f"heading {text!r} looks like Title Case; use sentence case")
        if text.endswith(".") and not text.endswith("..."):
            p.warn(line, f"heading {text!r} ends with a period")
    if not any(level == 1 for _, level, _ in p.headings):
        p.warn(1, "no <h1>")
    if sentence_case_problem(p.title):
        p.warn(1, f"title {p.title!r} looks like Title Case; use sentence case")

    straight = [(l, t.strip()) for l, t in p.text_runs if re.search(r"[A-Za-z]'[A-Za-z]|\"", t)]
    if straight:
        l, t = straight[0]
        p.warn(l, f"straight quotes in text ({len(straight)} places), e.g. {t[:60]!r}; use ’ “ ”")
    emoji = [(l, t.strip()) for l, t in p.text_runs if EMOJI.search(t)]
    if emoji:
        p.warn(emoji[0][0], f"emoji in text ({len(emoji)} places); Firefox desktop copy uses none")

    for kind, items in (("error", p.errors), ("warning", p.warnings)):
        for line, msg in sorted(items):
            print(f"{path}:{line}: {kind}: {msg}")
    print(f"{len(p.errors)} error(s), {len(p.warnings)} warning(s)")
    sys.exit(1 if p.errors else 0)


if __name__ == "__main__":
    main()
