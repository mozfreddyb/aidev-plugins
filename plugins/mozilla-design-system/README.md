# mozilla-design-system

A Claude Code plugin that makes the HTML Claude generates for you
(dashboards, reports, prototypes, internal tools, one-pagers) look like it
came from Mozilla. It follows the
[Acorn design system](https://acorn.firefox.com/) and, when asked, the
[Firefox](https://brand.firefox.com) or [Mozilla](https://brand.mozilla.com)
brand guidelines.

## Installation

```
/plugin marketplace add mozilla/aidev-plugins
/plugin install mozilla-design-system@aidev-plugins
```

## Usage

The `mozilla-html` skill activates whenever Claude is about to produce HTML
for Mozilla work. Just ask:

```
Make an HTML dashboard of these crash numbers
Build a one-pager announcing split view, Firefox brand
Prototype a settings page for a new privacy feature
Turn this CSV into a report I can share with the team
```

You get a single self-contained `.html` file (about 110 KB, no external
requests apart from brand fonts) that:

- uses Firefox's real design tokens, generated from the Firefox source tree
  with the current Nova look;
- adapts to light, dark, and high-contrast modes and prints cleanly;
- builds on plain-HTML versions of the `moz-*` reusable components (button,
  card, message bar, toggle, select, box group, page nav, badge, promo,
  segmented control, and more) plus tables, stat tiles, and charts;
- uses Acorn icons and the official Firefox and Mozilla logos;
- follows Acorn's content and accessibility guidelines.

Three looks:

| Look | When | How |
|---|---|---|
| Acorn (default) | Tools, reports, dashboards, prototypes | nothing to do |
| Firefox brand | Firefox-facing communication | ask for "Firefox brand" |
| Mozilla brand | Mozilla organization communication | ask for "Mozilla brand" |

## What's inside

```
skills/mozilla-html/
├── SKILL.md                 # workflow and core rules
├── assets/
│   ├── tokens.css           # generated: Firefox design tokens (Nova), standalone
│   ├── components.css       # moz-* component ports, base styles, brand themes
│   ├── template.html        # starting point for new pages
│   ├── icons/               # vendored Acorn icons (currentColor)
│   └── logos/               # official Firefox and Mozilla logos
├── references/              # loaded on demand: components, tokens, content,
│                            # charts, brand-firefox, brand-mozilla, icon names
├── examples/                # complete pages and a sample Markdown report
└── scripts/
    ├── bundle.py            # inline CSS and expand icon/logo placeholders
    ├── check.py             # lint a page against the design system rules
    ├── icon.py              # list, print, or vendor Acorn icons
    ├── render_markdown.py   # Markdown to bundled HTML (requires Pandoc)
    ├── build_demo.py        # portable theme/layout comparison gallery
    ├── test_render_markdown.py # Markdown adapter integration tests
    └── build_tokens.py      # regenerate tokens.css from mozilla-firefox/firefox
```

The original HTML scripts need only the Python 3 standard library.

### Render Markdown

The optional Markdown adapter additionally needs Pandoc in PATH:

```sh
python3 -I plugins/mozilla-design-system/skills/mozilla-html/scripts/render_markdown.py report.md --theme acorn --layout sidebar -o report.html
python3 -I plugins/mozilla-design-system/skills/mozilla-html/scripts/build_demo.py --output /tmp/mozilla-demo
```

The adapter preserves the document's content and adds the selected theme,
layout, section navigation, and table styles. It embeds local images and runs
the existing bundler and checker. Options and supported Markdown patterns are
documented in `skills/mozilla-html/references/markdown.md`. Open the demo's
`index.html` to compare nine layouts/themes and three component samplers.

## Keeping it current

The design tokens are generated, so don't edit `tokens.css` by hand:

```sh
python3 -I plugins/mozilla-design-system/skills/mozilla-html/scripts/build_tokens.py           # from main
python3 -I plugins/mozilla-design-system/skills/mozilla-html/scripts/build_tokens.py --ref release
```

The script flattens `tokens-shared.css`, `tokens-brand.css`, and the
component token sheets into one file. It applies the Nova overrides
unconditionally, because `-moz-pref()` media queries only work inside
Firefox, and keeps the high-contrast layers.

`components.css` is a hand port of `toolkit/content/widgets/moz-*/*.css`.
When a component's CSS changes upstream, port the change by hand.

## Sources

- Acorn: https://acorn.firefox.com/latest/get-started/resources/developer-MjYKs2SN
- Firefox desktop components Storybook: https://firefoxux.github.io/firefox-desktop-components/
- Design tokens: https://firefox-source-docs.mozilla.org/toolkit/themes/shared/design-system/docs/README.design-tokens.stories.html
- Acorn icons: https://github.com/FirefoxUX/acorn-icons
- Firefox brand: https://brand.firefox.com
- Mozilla brand: https://brand.mozilla.com
- Fonts: Mozilla Headline and Mozilla Text, [SIL Open Font License](https://github.com/mozilla/mozilla-type-family)

## License

The tokens, component CSS, and icons are derived from Firefox and Acorn
sources under the [Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/).
The Firefox and Mozilla logos in `assets/logos/` are trademarks of the
Mozilla Foundation. They're included for use in Mozilla's own materials under
the [trademark policy](https://www.mozilla.org/foundation/trademarks/policy/)
and are not covered by the MPL.
