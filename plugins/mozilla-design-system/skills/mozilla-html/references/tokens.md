# Token cheat sheet

`assets/tokens.css` holds Firefox's own design tokens (Acorn, Nova values),
generated from `toolkit/themes/shared/design-system` in the Firefox source. It
has ~660 custom properties. Every value is a `light-dark()` pair, and the
sheet includes the `prefers-contrast` and `forced-colors` overrides. Page CSS
should only ever reference tokens.

Rules:
1. **Semantic over palette.** Use `--text-color`, `--color-accent-primary`,
   or `--background-color-box`, not `--color-violet-50`. Palette tokens
   (`--color-<hue>-<0..100>`) are for charts and illustrations only.
2. **No literal colors** in page CSS. If you truly need a new color, define
   it once as a local custom property built from tokens, e.g.
   `--my-highlight: color-mix(in srgb, var(--color-accent-primary) 12%, transparent)`.
3. **No literal spacing or font sizes.** rem-based tokens assume the 15px
   root that `components.css` sets.
4. **Don't fight the theme.** Never set `color-scheme` or hard-code a dark
   background to "make it look modern". Light and dark both work
   automatically.

## Need → token

### Color

| Need | Token |
|---|---|
| Page background | `--background-color-canvas` |
| Card, panel, input surface | `--background-color-box` |
| Subtle tinted surface (callout, code) | `--background-color-box-info` |
| Body text | `--text-color` |
| Secondary text | `--text-color-deemphasized` |
| Disabled text | `--text-color-disabled` |
| Error text | `--text-color-error` |
| Accent (links, focus, primary, selection) | `--color-accent-primary` (+ `-hover`, `-active`) |
| Text on an accent fill | `--text-color-accent-primary-selected` / `--button-text-color-primary` |
| Default border | `--border-color` |
| Subtle divider | `--border-color-deemphasized` |
| Control border (inputs, toggles) | `--border-color-interactive` |
| Error border | `--border-color-error` |
| Status surfaces | `--background-color-information`, `-success`, `-warning`, `-critical` |
| Status icons | `--icon-color-information`, `-success`, `-warning`, `-critical` |
| Default icon | `--icon-color` |
| Link colors | `--link-color`, `--link-color-hover`, `--link-color-active`, `--link-color-visited` |
| Modal backdrop | `--background-color-overlay` |
| Hover on list rows | `--background-color-list-item-hover` |

### Typography

Firefox in-content pages use the OS font and a 15px root. Brand themes swap
in Mozilla Headline and Mozilla Text.

| Need | Token |
|---|---|
| Body family | `--font-family` |
| h1 / h2 family | `--font-family-heading` (+ `--font-stretch-heading`) |
| Monospace | `--font-family-mono` |
| Small text (13px) | `--font-size-small` |
| Body (15px) | `--font-size-root` (inherit; don't restate) |
| Large text (17px) | `--font-size-large` |
| h3 (17px) | `--font-size-heading-medium` |
| h2 (22px) | `--font-size-heading-large` |
| h1 (24px) | `--font-size-heading-xlarge` |
| Big numbers (33px) | `--font-size-xxxlarge` |
| Weights | `--font-weight` (400), `--font-weight-semibold` (600), `--font-weight-bold` (700), `--font-weight-heading` |
| Line height | `--line-height-body`, `--line-height-heading` |

`h1`–`h3` are styled already. To make another element look like a heading,
use `.heading-xlarge`, `.heading-large` or `.heading-medium`.

### Space, size, shape

| Need | Token |
|---|---|
| Gaps, padding, margin | `--space-xxsmall` ≈2px · `--space-xsmall` ≈4px · `--space-small` 7.5px · `--space-medium` ≈11px · `--space-large` 15px · `--space-xlarge` 22.5px · `--space-xxlarge` 30px |
| Main column width | `--page-main-content-width` (664px); wide pages `--page-wide-content-width` |
| Page top padding | `--page-space-block-start` (64px) |
| Icon sizes | `--icon-size` (16) · `--icon-size-xsmall` 12 · `--icon-size-large` 24 · `--icon-size-xlarge` 32 |
| Avatar, logo, item sizes | `--size-item-small` 16 · `-medium` 24 · `-large` 32 · `-xlarge` 48 |
| Image sizes | `--size-image-xsmall` 40 … `--size-image-xxlarge` 96 |
| Corner radius | `--border-radius-xsmall` 4 · `-small` 8 · `-medium` 12 · `-large` 16 · `-xlarge` 24 · `-circle` |
| Border width | `--border-width` (1px) |
| Elevation | `--box-shadow-level-1` (tabs) · `-2` (cards) · `-3` (popups, dialogs) · `-4` (card hover) |
| Focus ring | `outline: var(--focus-outline); outline-offset: var(--focus-outline-offset);` |
| Control heights | `--button-min-height` (32) · `--button-min-height-small` (24) · `--input-min-height` |

The px values above assume the 15px root.

### Charts

Defined in `components.css` and remapped per brand: `--chart-1` … `--chart-5`
(categorical; Mozilla brand: 3), `--chart-neutral`, `--chart-gridline`, `--chart-divider`,
`--chart-seq-1` … `--chart-seq-5` (sequential), and `--chart-diverging-low`,
`-mid`, `-high`. See `charts.md`.

## Themes and color scheme

- `<html>` with no `data-brand`: the Firefox product (Acorn Nova) look:
  violet accent, gray canvas, OS font.
- `<html data-brand="firefox">`: the Firefox brand palette (cream, purples)
  with Mozilla Headline Condensed and Mozilla Text.
- `<html data-brand="mozilla">`: the Mozilla brand: black and white, a pop
  of green, Mozilla Headline and Mozilla Text.
- `data-color-scheme="light"` or `"dark"` on `<html>` pins the scheme.
  Otherwise it follows the OS. Print always uses light.
- To make a dark area inside a light page, set `color-scheme: dark` on a
  container. Tokens are `light-dark()` pairs, so everything inside follows.

## Overriding tokens

Layers are ordered `moz-tokens` < `moz-brand` < `moz-base` <
`moz-components`. Unlayered page CSS beats all of them, so overrides need no
`!important`.

Gotcha: tokens that reference other tokens (e.g.
`--button-background-color-primary: var(--color-accent-primary)`) are
resolved where they're declared, on `:root`. Redefining
`--color-accent-primary` on a nested element does *not* update the button.
Redefine the token the component reads (`--button-background-color-primary`)
on that element, or override on `:root`.

## Where values come from

- Global tokens: `tokens-shared.css` + `tokens-brand.css` (in-content
  surface).
- Component tokens: `moz-*/*.tokens.css` (badge, box, message bar, page nav,
  promo, segmented control, select, toggle). These are declared on their
  component class too, so they resolve per instance.
- Regenerate with `python3 -I scripts/build_tokens.py` (add `--ref release`
  to match the release channel).
