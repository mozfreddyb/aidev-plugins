# Component recipes

Plain-HTML ports of Firefox's `moz-*` reusable components
(https://firefoxux.github.io/firefox-desktop-components/). Styles live in
`assets/components.css`; the markup below is the contract. Class names mirror
the Firefox component names, and modifier classes mirror their `type=` /
`size=` attributes.

Icons are placeholders that `scripts/bundle.py` expands:
`<svg class="moz-icon" data-icon="NAME"></svg>` (16px; add `data-size="12"` or
`"20"`). The icon is decorative unless you give the placeholder an
`aria-label`. Names: see `assets/icons/` or `python3 -I scripts/icon.py --list`.

Contents: [Layout](#layout) · [Page header](#page-header) ·
[Buttons](#buttons) · [Card](#card) · [Message bar](#message-bar) ·
[Form controls](#form-controls) · [Badge](#badge) · [Box group](#box-group) ·
[Page nav](#page-nav) · [Segmented control](#segmented-control) ·
[Promo](#promo) · [Dialog](#dialog) · [Table](#table) · [Stat tile](#stat-tile) ·
[Pull quote](#pull-quote) · [Empty state](#empty-state) · [Brand hero and masthead](#brand-hero-and-masthead) ·
[Utilities](#utilities)

## Layout

```html
<!-- Single column (about: page width, 664px): reports, docs, forms -->
<main class="moz-main">...</main>

<!-- Wide (1200px): dashboards, tables, grids -->
<main class="moz-main wide">...</main>

<!-- Sidebar navigation + content -->
<div class="moz-page">
  <nav class="moz-page-nav" aria-label="Sections">...</nav>
  <main class="moz-main wide">...</main>
</div>
```

- `.moz-section` spaces top-level sections; give each an `<h2>`.
- `.moz-grid` is a responsive grid: columns at least `--grid-min` wide
  (16rem by default), sharing the space evenly and collapsing to one column
  on small screens. Set `style="--grid-min: 24rem"` for two wide columns, such
  as charts.
- `.moz-stack` is a vertical flex column with `--space-large` gaps;
  `.moz-row` is a wrapping horizontal row with `--space-small` gaps.
- Full-bleed: `.moz-main.full`.

## Page header

`moz-page-header`. One `<h1>` per page.

```html
<header class="moz-page-header">
  <div class="heading">
    <h1>Crash rate review</h1>
    <span class="moz-badge">Draft</span>
  </div>
  <p class="description">Weekly stability summary for release, beta, and nightly.</p>
  <p class="meta">Data through 2026-10-12 · Source: Socorro</p>
</header>
```

## Buttons

`moz-button`. Bare `<button>` elements already get the default style.

```html
<button class="moz-button" type="button">Cancel</button>
<button class="moz-button primary" type="button">Save changes</button>
<button class="moz-button destructive" type="button">Delete profile</button>
<button class="moz-button ghost" type="button">Show details</button>
<button class="moz-button small" type="button">Edit</button>
<button class="moz-button" type="button"><svg class="moz-icon" data-icon="downloads"></svg>Export CSV</button>
<button class="moz-button ghost icon" type="button" aria-label="More options" title="More options">
  <svg class="moz-icon" data-icon="page-actions"></svg>
</button>
<button class="moz-button" type="button" aria-pressed="true">Show nightly</button>
<a class="moz-button primary" href="https://www.firefox.com/">Download Firefox</a>
```

Modifiers: `primary`, `destructive`, `ghost`, `icon` (square, icon only), `small`,
`large`, `attention` (green dot on icon buttons). `aria-pressed`,
`aria-expanded` or `aria-selected` give the selected look. `disabled` dims it.

Rules (Acorn):
- One primary button per view at most. Many screens need none.
- Destructive only for hard-to-undo actions, usually inside a confirmation.
- Buttons act, links navigate. Use `<a class="moz-button">` only when a
  navigation must look like a call to action (brand pages).
- Labels: sentence case, start with a verb, no "OK", no end punctuation, no
  fixed widths. Icon-only buttons need `aria-label` and `title`.
- Don't change a button's label or type on hover, and never hide buttons
  until hover.

Groups (`moz-button-group`): primary last, which is the macOS and Linux
convention. Use `.start` to left-align.

```html
<div class="moz-button-group">
  <button class="moz-button" type="button">Cancel</button>
  <button class="moz-button primary" type="submit">Save</button>
</div>
```

## Card

`moz-card`. Use cards to group a section's content (Acorn: "use cards to
contain settings categories"). Card headings are body-size semibold, not
`h3`-size.

```html
<article class="moz-card">
  <h3 class="moz-card-heading"><svg class="moz-icon" data-icon="lock"></svg>Passwords</h3>
  <div class="moz-card-content">
    <p>Saved logins sync across your devices.</p>
  </div>
</article>
```

Variants:
- `.moz-card.compact` (13px text, tighter padding)
- `.moz-card.interactive` (deeper shadow on hover; wrap the card in a link or
  put a link inside it)
- Cover image: `<div class="moz-card-cover"><img src="data:..." alt="..."></div>` as the first child
- Accordion:

```html
<details class="moz-card accordion" open>
  <summary>Advanced options</summary>
  <div class="moz-card-content">...</div>
</details>
```

## Message bar

`moz-message-bar`. Types: info (default), `warning`, `success`, `critical`.
Always pair the color with the matching icon and with words.

| Type | Icon | Use |
|---|---|---|
| info | `information-fill` | Helpful context; no action needed |
| `warning` | `warning-fill` | Might become a problem; say how to prevent it |
| `critical` | `error-fill` | Blocking, or privacy/security impact; say how to fix it |
| `success` | `checkmark-circle-fill` | Confirms something the reader did |

```html
<div class="moz-message-bar warning" role="status">
  <span class="icon-container"><svg class="moz-icon" data-icon="warning-fill" aria-label="Warning"></svg></span>
  <div class="content">
    <div class="text">
      <strong class="heading">Partial data</strong>
      <span class="message">macOS numbers for 2026-10-11 are still processing. <a class="support-link" href="...">Learn more about data delays</a></span>
    </div>
    <span class="actions"><button class="moz-button small" type="button">Refresh</button></span>
  </div>
  <button class="moz-button ghost icon small close" type="button" aria-label="Close" title="Close">
    <svg class="moz-icon" data-icon="close"></svg>
  </button>
</div>
```

`.heading`, `.actions` and the close button are optional. Use `role="alert"`
only for urgent messages that appear after load; static messages use
`role="status"` or none. Message bars sit in the flow near what they describe.
They aren't page-wide banners, and they aren't for urgent blocking alerts
(use a dialog).

## Form controls

Every control needs a visible label. Placeholders are not labels. Mark the
minority with "(required)" or "(optional)".

Checkbox or radio with description (the `moz-checkbox` / `moz-radio` layout):

```html
<div class="moz-field">
  <label><input type="checkbox" name="beta" checked> <span class="text">Include beta</span></label>
  <p class="description">Developer Edition counts as beta.</p>
</div>
```

Nested options (shown under a parent checkbox): add
`<div class="nested">...more .moz-field...</div>` inside the parent
`.moz-field`.

Group related controls with a fieldset (`moz-fieldset`):

```html
<fieldset class="moz-fieldset">
  <legend>Channels</legend>
  <p class="description">Choose which channels appear in the charts.</p>
  <div class="inputs">
    <div class="moz-field"><label><input type="radio" name="ch" value="release" checked> <span class="text">Release</span></label></div>
    <div class="moz-field"><label><input type="radio" name="ch" value="beta"> <span class="text">Beta</span></label></div>
  </div>
</fieldset>
```

Add `.horizontal` to `.inputs` for a single row. Never offer a single radio
button; put the default first.

Toggle (`moz-toggle`), for immediate on/off switches only. Inside forms, or
when in doubt, use a checkbox.

```html
<div class="moz-field">
  <label class="moz-toggle"><input type="checkbox" role="switch" checked><span class="track"></span><span class="text">Auto refresh</span></label>
  <p class="description">Reloads data every five minutes.</p>
</div>
```

Text input, textarea, select (label above the control: `moz-input-text`,
`moz-select`):

```html
<div class="moz-input">
  <label for="filter">Signature filter <span class="required">(optional)</span></label>
  <input id="filter" type="text" name="filter">
  <p class="description">Matches anywhere in the signature.</p>
</div>

<div class="moz-input">
  <label for="range">Date range</label>
  <div class="moz-select">
    <select id="range" name="range">
      <option>Last 6 weeks</option>
      <option>Last 12 weeks</option>
    </select>
  </div>
</div>

<div class="moz-input">
  <label for="search">Search signatures</label>
  <input id="search" type="search">
</div>
```

Always wrap `<select>` in `.moz-select`, which draws the chevron. Add
`.small` to `.moz-select` for the compact size. An error message goes in
`<p class="error">` after the control, with `aria-invalid="true"` and
`aria-describedby` on the input.

## Badge

`moz-badge`. A short status label. `.new` is green and only means new.

```html
<span class="moz-badge">Beta</span>
<span class="moz-badge new">New</span>
<span class="moz-badge"><svg class="moz-icon" data-icon="globe" data-size="12"></svg>Public</span>
```

## Box group

`moz-box-item`, `moz-box-group`, `moz-box-button`, `moz-box-link`. These are
settings-style rows.

```html
<div class="moz-box-group">
  <div class="moz-box-item">
    <svg class="moz-icon" data-icon="email"></svg>
    <div class="text">
      <span class="label">Weekly email</span>
      <span class="description">Sent Mondays to stability-team</span>
    </div>
    <div class="actions"><button class="moz-button small" type="button">Edit</button></div>
  </div>
  <button class="moz-box-item" type="button">
    <div class="text"><span class="label">Manage subscriptions</span></div>
    <svg class="moz-icon nav-icon" data-icon="chevron-right"></svg>
  </button>
  <a class="moz-box-item" href="https://crash-stats.mozilla.org/">
    <div class="text"><span class="label">Open Crash Stats</span></div>
    <svg class="moz-icon" data-icon="external-link"></svg>
  </a>
</div>
```

`.moz-box-item` works alone too. Use `.medium-icon` / `.large-icon` for
24px / 32px icons. Use a `<ul class="moz-box-group">` with `<li>` rows for
real lists.

## Page nav

`moz-page-nav`. This is the about:preferences-style sidebar; put it in
`.moz-page`. Links mark the current section with `aria-current`. Labels are
wrapped in `.label` so they collapse to icons on narrow screens.

```html
<nav class="moz-page-nav" aria-label="Report sections">
  <p class="heading"><svg data-logo="firefox-symbol"></svg><span class="label">Stability</span></p>
  <div class="group">
    <a class="moz-page-nav-button" href="#summary" aria-current="true"><svg class="moz-icon" data-icon="dashboard"></svg><span class="label">Summary</span></a>
    <a class="moz-page-nav-button" href="#trends"><svg class="moz-icon" data-icon="arrow-trending"></svg><span class="label">Trends</span></a>
  </div>
  <hr>
  <div class="group">
    <a class="moz-page-nav-button" href="https://support.mozilla.org/"><svg class="moz-icon" data-icon="help"></svg><span class="label">Get help</span></a>
  </div>
</nav>
```

To highlight the section in view while scrolling, a small
IntersectionObserver that moves `aria-current` is fine. Keep it inline.

## Segmented control

`moz-segmented-control`. Use it for a few mutually exclusive views; it needs
no script.

```html
<div class="moz-segmented-control" role="radiogroup" aria-label="Chart type">
  <label><input type="radio" name="chart" value="bars" checked>Bars</label>
  <label><input type="radio" name="chart" value="lines">Lines</label>
</div>
```

## Promo

`moz-promo`. Use it to highlight a feature or benefit, never for feedback
(use a message bar). At most 3 actions. `.vibrant` is the stronger variant.

```html
<div class="moz-promo">
  <div class="text">
    <h3 class="heading">Get alerts for new signatures</h3>
    <p class="message">Subscribe to hear about spikes as soon as they happen.</p>
  </div>
  <button class="moz-button" type="button">Subscribe</button>
</div>
```

You can put an image first or last: `<img src="data:..." alt="">`, 80px wide
(`.image-large` on the promo gives 160px).

## Dialog

```html
<dialog class="moz-dialog" id="confirm-delete" aria-labelledby="confirm-title">
  <h2 id="confirm-title">Delete this report?</h2>
  <p>You can’t undo this.</p>
  <form method="dialog" class="moz-button-group">
    <button class="moz-button" value="cancel">Cancel</button>
    <button class="moz-button destructive" value="delete">Delete report</button>
  </form>
</dialog>
<button class="moz-button" type="button" onclick="document.getElementById('confirm-delete').showModal()">Delete report</button>
```

## Table

These use Acorn's table tokens: the accent-colored header row is the Firefox
look, and `.plain` is a quieter variant for dense data. Wrap tables in
`.moz-table-wrapper` so they scroll horizontally on small screens.

```html
<div class="moz-table-wrapper">
  <table class="moz-table">
    <caption>Top crash signatures this week</caption>
    <thead>
      <tr><th scope="col">Signature</th><th scope="col" class="num">Crashes</th><th scope="col" class="num">Change</th></tr>
    </thead>
    <tbody>
      <tr><td><code>OOM | small</code></td><td class="num">9,112</td><td class="num">−4%</td></tr>
    </tbody>
  </table>
</div>
```

Modifiers: `.striped`, `.compact`, `.plain`. `.num` right-aligns numeric
columns (tabular figures are on by default). Use a real minus sign (−) for
negative numbers.

## Stat tile

A dashboard number. It isn't a Firefox component; it's built from tokens.
Put it alone or inside a `.moz-card`.

```html
<article class="moz-card moz-stat">
  <span class="label">Daily active users</span>
  <span class="value">212.4M</span>
  <span class="delta good"><svg class="moz-icon" data-icon="arrow-trending"></svg>Up 2.1% from last week</span>
</article>
<article class="moz-card moz-stat">
  <span class="label">Median time to first review</span>
  <span class="value">22<span class="unit"> hours</span></span>
  <span class="delta good"><svg class="moz-icon flip-y" data-icon="arrow-trending"></svg>Down 6 hours from last week</span>
</article>
```

`.delta.good`, `.delta.bad` and `.delta.neutral` color only the icon. The
words carry the meaning: "Up 2.1%", not just "2.1%" in green. Whether up is
good depends on the metric; for crashes, up is `.bad`. For a downward trend,
flip the icon with `.flip-y`. The number styling follows the brand
(condensed on brand pages). Set `style="--stat-font-size: 4rem"` for a hero
number.

## Pull quote

For brand pages and reports. Always attribute the quote: name, then title or
role. Mark placeholder quotes visibly.

```html
<figure class="moz-pull-quote">
  <blockquote><p>“Patient data never leaves the building, and anyone can check how the model works.”</p></blockquote>
  <figcaption><span class="moz-badge">Placeholder quote</span> <span class="name">[Grantee name]</span>, [project], local-first AI grantee</figcaption>
</figure>
```

## Empty state

```html
<div class="moz-empty-state">
  <svg class="moz-icon large" data-icon="search"></svg>
  <h3 class="heading">Try a broader filter</h3>
  <p>Nothing matches “nsThread” in the last 7 days.</p>
  <button class="moz-button" type="button">Clear filter</button>
</div>
```

## Brand hero and masthead

Only on `data-brand` pages. The masthead anchors the logo to a corner
(top-left for Firefox, top-right for Mozilla, which the CSS handles). The hero
is always a dark field: the Firefox dark gradient, or Mozilla black.

```html
<header class="moz-masthead">
  <svg data-logo="firefox-lockup"></svg>
  <span class="moz-badge">Firefox 158</span>
</header>
<section class="moz-hero" aria-labelledby="hero-title">
  <h1 class="display" id="hero-title">Two sites, one window</h1>
  <p class="lede">One or two sentences that lead with the benefit.</p>
  <div class="moz-row">
    <a class="moz-button primary large" href="...">Get Firefox</a>
    <a class="moz-button large" href="#details">See how it works</a>
  </div>
</section>
<main class="moz-main wide">...</main>
```

Logos (`assets/logos/`): `firefox-lockup`, `firefox-lockup-stacked`,
`firefox-symbol`, `mozilla-lockup`, `mozilla-wordmark`, `mozilla-symbol`.
Set the size with `style="--logo-height: 40px"`; the minimum is 20px. See
the brand references for the rules.

## Utilities

- `.text-deemphasized`: small, secondary text
- `.text-error`
- `.text-truncated-ellipsis`
- `.tabular-nums`
- `.visually-hidden`: screen-reader-only text
- `.no-print`: hidden when printing
- `.moz-icon.xsmall|medium|large`: 12 / 20 / 24px icons
- `.flip-y`: flips an icon vertically (trend down)
- `<kbd>`: keyboard keys
- `<code>` / `<pre>`: code
- `<blockquote>`: quotes, with an accent rule
