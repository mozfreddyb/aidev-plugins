#!/usr/bin/env python3
"""Print Firefox (Acorn) icons as inline SVG that works in any browser.

Icons come from https://github.com/FirefoxUX/acorn-icons (MPL-2.0). The repo
SVGs use fill="context-fill", which only Firefox's privileged pages
understand; this script rewrites that to currentColor so the icon takes the
surrounding text color, strips the license comment (add one MPL notice per
page instead), and marks the icon decorative.

A curated set is vendored in assets/icons/ and works offline. Any other icon
is fetched from GitHub.

Usage:
  python3 -I icon.py information warning-fill    # 16px, from assets or GitHub
  python3 -I icon.py settings --size 20
  python3 -I icon.py --list [--size 16]          # every icon name in the repo
  python3 -I icon.py --vendor NAME... --size 16  # save into assets/icons/
  python3 -I icon.py --index                     # rewrite references/icon-names.md
"""

import argparse
import datetime
import json
import pathlib
import re
import sys
import urllib.request

REPO = "FirefoxUX/acorn-icons"
REF = "main"
SIZES = ["12", "16", "20"]
ICON_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "icons"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mozilla-html-skill"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def clean(svg, name, size):
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = re.sub(r'\s[a-z-]+-opacity="context-(fill|stroke)-opacity"', "", svg)
    svg = re.sub(r'"context-(fill|stroke)"', '"currentColor"', svg)
    if "context-" in svg:
        sys.exit(f"{name}-{size}: unhandled context property; inspect manually")
    svg = svg.replace(
        "<svg ",
        f'<svg class="moz-icon" data-icon="{name}" aria-hidden="true" focusable="false" ',
        1,
    )
    svg = re.sub(r">\s+<", "><", svg)
    return svg


def load(name, size):
    name = re.sub(rf"-{size}(\.svg)?$", "", name)
    local = ICON_DIR / f"{name}-{size}.svg"
    if local.exists():
        return local.read_text().strip()
    url = f"https://raw.githubusercontent.com/{REPO}/{REF}/icons/desktop/{size}/{name}-{size}.svg"
    try:
        return clean(fetch(url), name, size)
    except urllib.error.HTTPError as e:
        sys.exit(f"{name}-{size}: not found ({e.code}). Try --list --size {size}.")


def list_names(size):
    api = f"https://api.github.com/repos/{REPO}/contents/icons/desktop/{size}?ref={REF}"
    entries = json.loads(fetch(api))
    return sorted(re.sub(rf"-{size}\.svg$", "", e["name"]) for e in entries
                  if e["name"].endswith(".svg"))


def write_index():
    out = ICON_DIR.parent.parent / "references" / "icon-names.md"
    lines = [
        f"# Acorn desktop icon names ({REPO}@{REF}, {datetime.date.today()})",
        "",
        "Use as `<svg class=\"moz-icon\" data-icon=\"NAME\" data-size=\"SIZE\"></svg>`",
        "(size 16 is the default). Names in **bold** are vendored in `assets/icons/`",
        "and work offline; the rest are downloaded by `scripts/bundle.py`.",
        "Pick the literal meaning; don't repurpose icons.",
    ]
    for size in SIZES:
        local = {f.name.removesuffix(f"-{size}.svg") for f in ICON_DIR.glob(f"*-{size}.svg")}
        names = [f"**{n}**" if n in local else n for n in list_names(size)]
        lines += ["", f"## {size}px", "", " · ".join(names)]
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--size", default="16", choices=SIZES)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--index", action="store_true",
                    help="rewrite references/icon-names.md from the repo listing")
    ap.add_argument("--vendor", action="store_true",
                    help="write the icons into assets/icons/ instead of printing")
    args = ap.parse_args()

    if args.list:
        print(" ".join(list_names(args.size)))
        return
    if args.index:
        write_index()
        return
    if not args.names:
        ap.error("give at least one icon name, or --list")
    for name in args.names:
        svg = load(name, args.size)
        if args.vendor:
            ICON_DIR.mkdir(parents=True, exist_ok=True)
            base = re.sub(rf"-{args.size}(\.svg)?$", "", name)
            (ICON_DIR / f"{base}-{args.size}.svg").write_text(svg + "\n")
        else:
            print(svg)


if __name__ == "__main__":
    main()
