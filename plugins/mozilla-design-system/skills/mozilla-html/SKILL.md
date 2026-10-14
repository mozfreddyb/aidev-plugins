---
name: mozilla-html
description: >
  Make any HTML that Claude produces for Mozilla or Firefox work follow
  Mozilla's design system: Acorn (Firefox's product design system, current
  Nova look) by default, or the Firefox or Mozilla brand for
  communication pieces. Use whenever you create or restyle an HTML page,
  report, dashboard, status page, prototype, mockup, internal tool,
  one-pager, launch page, or HTML artifact for Mozilla or Firefox, or when
  asked to use Acorn, Firefox styles, design tokens, moz-* components, or
  Mozilla branding. Provides Firefox's design tokens, ported components,
  Acorn icons, official logos, a bundler that makes a single portable file,
  and a checker.
---

# Mozilla HTML

Produce self-contained HTML that looks like it came from Mozilla. It uses
Firefox's real design tokens (`assets/tokens.css`), plain-HTML ports of the
`moz-*` components (`assets/components.css`), Acorn icons, and official
logos. Light and dark mode, high contrast, and RTL come with it.

All paths below are relative to this skill's base directory. Use absolute
paths when running scripts.

## 1. Pick the look

| Output | Look | `<html>` attribute |
|---|---|---|
| Dashboards, reports, internal tools, status pages, docs, data explorers, prototypes of Firefox UI | **Acorn**, the Firefox product look (default) | none |
| Pieces that present Firefox to people: launch or feature one-pagers, release highlights, campaign or event pages | **Firefox brand** | `data-brand="firefox"` |
| Mozilla-the-organization pieces: policy, research, community, events, Mozilla Builders, corporate updates | **Mozilla brand** | `data-brand="mozilla"` |

When unsure, use Acorn; it's never wrong for a working document. Ask only
if a piece is clearly external-facing and the brand is ambiguous. For a
brand look, read `references/brand-firefox.md` or
`references/brand-mozilla.md` first, and load the fonts as shown there.

## 2. Build the page

1. Copy `assets/template.html` to a source file next to the output, such
   as `report.src.html`. Keep its two stylesheet links (`tokens.css`,
   `components.css`); the bundler resolves them. Edit the source and
   re-bundle; never hand-edit the bundled file.
2. Read `references/components.md` and compose the page from those recipes:
   page header, cards, message bars, buttons, form fields, tables, stat
   tiles, page nav, and so on. Complete pages to imitate:
   `examples/dashboard.html` (Acorn), `examples/one-pager.html` (Firefox
   brand) and `examples/mozilla-brief.html` (Mozilla brand).
3. Icons and logos are placeholders that the bundler fills in:
   `<svg class="moz-icon" data-icon="warning-fill"></svg>` and
   `<svg data-logo="firefox-lockup"></svg>`. Valid icon names are in
   `references/icon-names.md`. Names marked there as vendored work offline;
   others are downloaded at bundle time. Never draw icons or logos yourself,
   and never type out a wordmark.
4. Put page-specific CSS in the template's `<style>` using **tokens only**
   (`var(--space-large)`, `var(--text-color)`, `var(--border-radius-medium)`).
   `references/tokens.md` maps needs to tokens. Charts follow
   `references/charts.md`.
5. Write every visible string by `references/content.md` (sentence case,
   verbs on buttons, curly quotes, no emoji).

## 3. Bundle and check

```sh
python3 -I scripts/bundle.py report.src.html -o report.html  # inline CSS, expand icons/logos
python3 -I scripts/check.py report.html                      # fix errors; review warnings
```

The bundled file is self-contained, about 110 KB, with no external requests
except the Google Fonts link on brand pages. The checker catches structural
mistakes; it can't see layout. If you can render the page (headless Chrome
`--screenshot`, or Firefox `--headless --screenshot`), look at it in both
schemes before you hand it over. Pin each scheme explicitly with
`data-color-scheme="light"` or `"dark"` on a throwaway copy of `<html>`,
because an unpinned page follows the OS. Also try a narrow window (about
500px). Deliver the file without the pin, so it follows the reader's
setting.

If you cannot run scripts, paste the contents of `assets/tokens.css` and
`assets/components.css` into `<style>` elements in that order, and paste the
SVGs from `assets/icons/` and `assets/logos/` in place of the placeholders.

## Rules that matter most

- **Tokens, not values.** No hex, rgb, or named colors and no px font sizes
  in page CSS. Use semantic tokens (`--text-color`, `--color-accent-primary`)
  over palette tokens (`--color-violet-50`), which are for charts only.
- **Don't break theming.** Never hard-code a background, a `color-scheme`, or
  white text to look "modern". Never remove focus outlines.
- **One primary button per view.** Buttons act and links navigate.
  Destructive styling is only for hard-to-undo actions.
- **Color is never the only signal.** Status uses icon, color, and words
  together. Charts use direct labels.
- **Accessible structure.** Use `lang`, one `<h1>`, ordered headings,
  landmarks (`header`, `nav`, `main`), a visible label for every control,
  `alt` on every image, and `scope` on table headers.
- **Single file.** No CDNs, frameworks, or remote images; inline small
  images as `data:` URIs. Any JavaScript is small and inline, and the page
  must still read correctly without it.
- **Don't fake Firefox.** Don't reference `chrome://` URLs or try to load
  the real `moz-*` elements; they only work inside Firefox. Don't invent new
  components when a recipe exists, and don't generate mascot or brand
  illustrations.

## Maintenance

`assets/tokens.css` is generated from the Firefox source tree. Rerun
`python3 -I scripts/build_tokens.py` after design token changes land. Run
`python3 -I scripts/icon.py --vendor NAME…` to add offline icons.
