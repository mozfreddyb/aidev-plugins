#!/usr/bin/env python3
"""Regenerate assets/tokens.css from the Firefox source tree.

Firefox's design tokens (toolkit/themes/shared/design-system/dist/) are built
for privileged Firefox pages: they @import chrome:// URLs, gate the Nova
refresh behind `@media -moz-pref("browser.nova.enabled")`, and spread values
across cascade layers. This script flattens the in-content ("brand") surface
into a single sheet that works in any browser:

  * tokens-shared.css + tokens-brand.css, plus the component token sheets of
    the widgets that references/components.md ports, are merged in Firefox's
    layer order, with Nova overrides applied unconditionally (Nova ships by
    default).
  * Chrome-only tokens (toolbar, toolbox, toolbarbutton) are dropped unless
    a kept token references them.
  * prefers-contrast and forced-colors overrides are kept as media queries.
  * Firefox-only system colors are mapped to standard CSS system colors.

Usage:
  python3 -I build_tokens.py                # fetch from mozilla-firefox/firefox@main
  python3 -I build_tokens.py --ref release  # fetch from another branch or tag
  python3 -I build_tokens.py --src DIR      # read local copies (flat directory)
"""

import argparse
import datetime
import pathlib
import re
import sys
import urllib.request

REPO = "mozilla-firefox/firefox"
DIST = "toolkit/themes/shared/design-system/dist"
WIDGETS = "toolkit/content/widgets"
# (path, extra selector). Firefox declares widget tokens on each widget's
# :host so that var() references resolve per instance (e.g. a warning message
# bar derives its border from its own icon color). The extra selector does the
# same for the class-based ports in assets/components.css.
# Source order matters: within one layer, later files win, as in Firefox.
FILES = [
    (f"{DIST}/tokens-shared.css", None),
    (f"{DIST}/tokens-brand.css", None),
    (f"{WIDGETS}/moz-box.tokens.css", ".moz-box-item, .moz-box-group"),
] + [
    (f"{WIDGETS}/{w}/{w}.tokens.css", f".{w}")
    for w in ["moz-badge", "moz-message-bar", "moz-page-nav", "moz-promo",
              "moz-segmented-control", "moz-select", "moz-toggle"]
]

# Precedence order from the @layer statement at the top of tokens-shared.css.
# The browser-theme layers only apply to the browser chrome and are skipped.
BASE_LAYERS = [
    "tokens-foundation",
    "tokens-foundation-brand",
    "tokens-foundation-nova",
    "tokens-foundation-brand-nova",
]
CONTRAST_LAYERS = ["tokens-prefers-contrast", "tokens-prefers-contrast-nova"]
FORCED_LAYERS = ["tokens-forced-colors", "tokens-forced-colors-nova"]
SKIPPED_LAYERS = ["tokens-browser-theme", "tokens-browser-theme-nova"]

CHROME_ONLY = re.compile(r"^--(toolbar|toolbox|toolbarbutton|toolbarseparator)(-|$)")

NONSTANDARD_VALUES = {
    "-moz-menuhovertext": "SelectedItemText",
    "-moz-menuhover": "SelectedItem",
    # Defined in browser chrome stylesheets, not in the token files.
    "var(--chrome-content-separator-color)": "var(--border-color-deemphasized)",
}

DECL = re.compile(r"^\s*(--[A-Za-z0-9-]+)\s*:\s*(.+?)\s*$", re.S)
VAR_REF = re.compile(r"var\(\s*(--[A-Za-z0-9-]+)")


def fetch(ref, path):
    url = f"https://raw.githubusercontent.com/{REPO}/{ref}/{path}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def parse(css):
    """Yield (preludes, name, value) for every custom property declaration.

    `preludes` is the stack of enclosing block headers, outermost first. The
    generated token files contain no strings or nested braces in values, so
    a brace/semicolon scanner is sufficient.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    stack = []
    buf = ""
    for ch in css:
        if ch == "{":
            stack.append(buf.strip())
            buf = ""
        elif ch == "}":
            yield from _decl(stack, buf)
            stack.pop()
            buf = ""
        elif ch == ";":
            yield from _decl(stack, buf)
            buf = ""
        else:
            buf += ch


def _decl(stack, text):
    m = DECL.match(text)
    if m and stack:
        yield tuple(stack), m.group(1), " ".join(m.group(2).split())


def layer_of(preludes):
    for p in preludes:
        if p.startswith("@layer "):
            return p[len("@layer "):].strip()
    return None


def collect(sources):
    """Return ({layer: {name: value}}, {name: scope}) in source order."""
    layers = {}
    scopes = {}
    for css, scope in sources:
        for preludes, name, value in parse(css):
            if not preludes[0].startswith(":root"):
                continue
            layer = layer_of(preludes)
            if layer in SKIPPED_LAYERS:
                continue
            if layer not in BASE_LAYERS + CONTRAST_LAYERS + FORCED_LAYERS:
                sys.exit(f"Unknown layer {layer!r} for {name}; update build_tokens.py")
            for bad, good in NONSTANDARD_VALUES.items():
                value = value.replace(bad, good)
            layers.setdefault(layer, {})[name] = value
            if scope:
                scopes[name] = scope
    return layers, scopes


def merge(layers, order):
    out = {}
    for layer in order:
        out.update(layers.get(layer, {}))
    return out


def prune(base, contrast, forced):
    """Drop chrome-only tokens that nothing we keep depends on."""
    keep = {n for n in base if not CHROME_ONLY.match(n)}
    keep |= {n for n in list(contrast) + list(forced) if not CHROME_ONLY.match(n)}
    pending = list(keep)
    every = {**base, **contrast, **forced}
    while pending:
        name = pending.pop()
        for mode in (base, contrast, forced):
            for ref in VAR_REF.findall(mode.get(name, "")):
                if ref not in keep and ref in every:
                    keep.add(ref)
                    pending.append(ref)
    return [{n: v for n, v in m.items() if n in keep} for m in (base, contrast, forced)]


def check_refs(base, *modes):
    defined = set(base)
    missing = set()
    for mode in (base, *modes):
        for value in mode.values():
            missing |= {r for r in VAR_REF.findall(value) if r not in defined}
    if missing:
        print("warning: references to undefined tokens:", ", ".join(sorted(missing)),
              file=sys.stderr)
    leftovers = [v for m in (base, *modes) for v in m.values() if "-moz-" in v]
    if leftovers:
        sys.exit(f"Non-standard values remain: {leftovers}")


def rules(decls, scopes, indent):
    """Group declarations into one rule per scope, global tokens first."""
    groups = {}
    for name, value in sorted(decls.items()):
        groups.setdefault(scopes.get(name), {})[name] = value
    pad = " " * indent
    out = []
    for scope in sorted(groups, key=lambda s: (s is not None, s or "")):
        selector = ":root" if scope is None else f":root, {scope}"
        body = "\n".join(f"{pad}  {n}: {v};" for n, v in groups[scope].items())
        out.append(f"{pad}{selector} {{\n{body}\n{pad}}}")
    return "\n\n".join(out)


def render(base, contrast, forced, scopes, ref):
    today = datetime.date.today().isoformat()
    return f"""/* Mozilla Acorn design tokens, flattened for standalone HTML.
 * Generated by scripts/build_tokens.py from {REPO}@{ref}
 * (tokens-shared, tokens-brand and widget *.tokens.css; Nova enabled) on {today}.
 * Do not edit by hand; rerun the script instead.
 *
 * Source: This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

@layer moz-tokens {{
{rules(base, scopes, 2)}

  @media (prefers-contrast) {{
{rules(contrast, scopes, 4)}
  }}

  @media (forced-colors) {{
{rules(forced, scopes, 4)}
  }}
}}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", default="main", help="git ref of mozilla-firefox/firefox")
    ap.add_argument("--src", type=pathlib.Path, help="directory with local dist files")
    ap.add_argument("--out", type=pathlib.Path,
                    default=pathlib.Path(__file__).resolve().parent.parent / "assets" / "tokens.css")
    args = ap.parse_args()

    if args.src:
        sources = [((args.src / pathlib.Path(f).name).read_text(), s) for f, s in FILES]
        ref = f"local:{args.src}"
    else:
        sources = [(fetch(args.ref, f), s) for f, s in FILES]
        ref = args.ref

    layers, scopes = collect(sources)
    base = merge(layers, BASE_LAYERS)
    contrast = merge(layers, CONTRAST_LAYERS)
    forced = merge(layers, FORCED_LAYERS)
    base, contrast, forced = prune(base, contrast, forced)
    check_refs(base, contrast, forced)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(base, contrast, forced, scopes, ref))
    print(f"wrote {args.out} ({len(base)} tokens, {len(contrast)} contrast, "
          f"{len(forced)} forced-colors overrides)")


if __name__ == "__main__":
    main()
