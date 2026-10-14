#!/usr/bin/env python3
"""Bundle an HTML page into a single portable file.

* <link rel="stylesheet" href="..."> pointing at a local file is replaced by
  a <style> element with the file's (compacted) contents. Bare names such as
  href="tokens.css" that don't exist next to the page resolve to this skill's
  assets/ directory. Remote stylesheets (https:, //) are left alone.
* <svg data-icon="NAME" [data-size="12|16|20"] ...></svg> is replaced by the
  Acorn icon (assets/icons, or fetched from FirefoxUX/acorn-icons). Classes
  and attributes on the placeholder are kept; aria-label makes it role="img".
* <svg data-logo="NAME" ...></svg> is replaced by assets/logos/NAME.svg.

Usage:
  python3 -I bundle.py page.html              # rewrite in place
  python3 -I bundle.py page.html -o out.html  # write elsewhere
"""

import argparse
import pathlib
import re
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parent
ASSETS = SCRIPTS.parent / "assets"
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True  # keep the installed plugin directory clean
import icon  # noqa: E402  (sibling script; -I drops the script dir from sys.path)

LINK = re.compile(r"<link\b[^>]*>", re.I)
PLACEHOLDER = re.compile(r"<svg\b([^>]*\bdata-(?:icon|logo)\s*=[^>]*)>\s*</svg>", re.I)
ATTR = re.compile(r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*(?:=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?""")


def attrs(text):
    out = {}
    for m in ATTR.finditer(text):
        name = m.group(1)
        if name in ("link", "svg"):
            continue
        out[name] = next((g for g in m.groups()[1:] if g is not None), "")
    return out


def compact(css):
    """Drop comments, indentation and blank lines; keep the MPL notice."""
    notice = "/* MPL-2.0: http://mozilla.org/MPL/2.0/ */\n" if "Mozilla Public" in css else ""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    lines = (line.strip() for line in css.splitlines())
    return notice + "\n".join(line for line in lines if line)


def inline_stylesheets(html, base, minify, done):
    def replace(m):
        a = attrs(m.group(0))
        href = a.get("href", "")
        if "stylesheet" not in a.get("rel", "").lower().split():
            return m.group(0)
        if re.match(r"^([a-z][a-z0-9+.-]*:|//)", href, re.I) and not href.startswith("file:"):
            return m.group(0)
        path = pathlib.Path(href.removeprefix("file://"))
        candidates = [path] if path.is_absolute() else [base / path, ASSETS / path.name]
        found = next((c for c in candidates if c.is_file()), None)
        if not found:
            sys.exit(f"stylesheet not found: {href}")
        done.append(found.name)
        css = found.read_text(encoding="utf-8")
        css = compact(css) if minify else css.strip()
        css = css.replace("</style", "<\\/style")
        media = f' media="{a["media"]}"' if "media" in a else ""
        return f"<style{media}>\n/* {found.name} */\n{css}\n</style>"

    return LINK.sub(replace, html)


def merge_svg(svg, extra):
    """Copy placeholder attributes onto the real <svg> root."""
    m = re.match(r"<svg\b([^>]*)>", svg)
    root = attrs(m.group(1))
    for key in ("data-icon", "data-logo", "data-size"):
        extra.pop(key, None)
    classes = " ".join(dict.fromkeys(
        (root.get("class", "") + " " + extra.pop("class", "")).split()))
    root.update(extra)
    if classes:
        root["class"] = classes
    if "aria-label" in extra or "aria-labelledby" in extra:
        root.pop("aria-hidden", None)
        root["role"] = "img"
    rendered = " ".join(f'{k}="{v}"' if v != "" else k for k, v in root.items())
    return f"<svg {rendered}>" + svg[m.end():]


def expand_placeholders(html, done):
    def replace(m):
        a = attrs(m.group(1))
        if "data-icon" in a:
            name, size = a["data-icon"], a.get("data-size", "16")
            svg = icon.load(name, size)
            done.append(f"icon:{name}-{size}")
        else:
            name = a["data-logo"].removesuffix(".svg")
            path = ASSETS / "logos" / f"{name}.svg"
            if not path.is_file():
                choices = ", ".join(sorted(p.stem for p in path.parent.glob("*.svg")))
                sys.exit(f"unknown logo {name!r}; choose one of: {choices}")
            svg = path.read_text(encoding="utf-8").strip()
            a.setdefault("class", "moz-logo")
            done.append(f"logo:{name}")
        return merge_svg(svg, a)

    return PLACEHOLDER.sub(replace, html)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("html", type=pathlib.Path)
    ap.add_argument("-o", "--out", type=pathlib.Path)
    ap.add_argument("--no-minify", action="store_true",
                    help="inline stylesheets verbatim instead of compacting them")
    args = ap.parse_args()

    html = args.html.read_text(encoding="utf-8")
    styles, svgs = [], []
    html = inline_stylesheets(html, args.html.resolve().parent, not args.no_minify, styles)
    html = expand_placeholders(html, svgs)
    if svgs and "MPL" not in html.split("</head>")[0]:
        notice = ("<!-- Icons: Firefox Acorn icons, MPL-2.0, "
                  "https://github.com/FirefoxUX/acorn-icons -->\n")
        html = re.sub(r"(<head\b[^>]*>)", r"\1\n" + notice, html, count=1, flags=re.I)

    out = args.out or args.html
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html.encode()) // 1024} KB): "
          f"{len(styles)} stylesheet(s) [{', '.join(styles) or 'none'}], "
          f"{len(svgs)} icon/logo placeholder(s)")


if __name__ == "__main__":
    main()
