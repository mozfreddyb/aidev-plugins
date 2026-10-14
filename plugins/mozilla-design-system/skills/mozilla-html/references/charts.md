# Charts and data visualization

Charts are hand-built inline SVG that reads the chart tokens, so they follow
light/dark mode and the brand theme with no extra work. Avoid chart libraries
from CDNs; they break the single-file, offline page.

If a general data-visualization skill is also available, use its method for
choosing the form, mark specs, and an optional hover layer, kept inline and
small. **This file wins on colors and brand rules.** The `--chart-*`
palettes below were already run through that skill's palette validator, so
don't substitute its default palette.

## Pick the form

| Question | Form |
|---|---|
| One headline number | `.moz-stat` tile; no chart |
| Change over time | Line chart (or columns for ≤ 12 periods) |
| Compare categories | Horizontal bars, sorted, labeled at the bar end |
| Part of a whole | A single stacked bar, or a short table. Avoid pies; never more than 3 slices |
| Distribution | Histogram |
| Exact values matter | `.moz-table`, with `.num` columns |

## Color

- Categorical: use `--chart-1`, `--chart-2`, … in order, without skipping, and
  keep a series' color when filters remove others. Acorn and the Firefox
  brand have **5 slots**. The Mozilla brand has **3**: `--chart-4` and `-5`
  are grey there, so fold extra series into "Other". `--chart-neutral` is
  always "Other" or context.
- Highlight one series: give it `--chart-1` and make the rest
  `--chart-neutral`. This is the preferred Mozilla-brand style (green against
  grey).
- Ordered values: `--chart-seq-1` (low) to `--chart-seq-5` (high), one hue.
- Values around a midpoint: `--chart-diverging-low`, `-mid` (neutral),
  `-high`.
- Never use status colors (`--icon-color-critical` and so on) for
  categories. Use them only when the data *is* a status, and always with an
  icon and a word.
- Color is never the only encoding. With 2 or more series, show a legend
  (`.moz-legend`) and also label up to 4 series directly at the end of the
  line or bar. Use one series and no legend; the caption names it.
- A few slots dip just under 3:1 against some surfaces: `--chart-2` on
  light, and `--chart-1` and `--chart-3` on the Acorn dark card. Label marks
  directly or include the data table, which you should do anyway.
- Separate adjacent filled marks (stacked segments, touching bars) with a
  2px gap in the surface color: add `class="mark-gap"` to each mark, which
  sets `stroke: var(--chart-divider); stroke-width: 2`. The Mozilla brand
  requires this.
- With more than 3 series in a line chart, also vary the dash pattern
  (`stroke-dasharray`) or the marker shape.

## Marks and text

- Gridlines: horizontal only, `class="gridline"` (uses `--chart-gridline`).
  The baseline uses `class="axis"`.
- Lines: `stroke-width="2"`, `fill="none"`, `stroke-linejoin="round"`. Points
  are `r="3"`, and only where they mean something.
- Bars: a gap of at least a third of the bar width between bars, and no 3D or
  gradients.
- Text: **horizontal only**, never rotated (Mozilla brand rule). At least
  13px, with tick labels in `--text-color-deemphasized` (the default for
  `svg text` in `.moz-chart`). Give direct labels and key values
  `class="label"` so they use `--text-color`.
- Make the `viewBox` width match the rendered width, so one SVG unit is
  about one CSS pixel and `font-size="13"` renders at 13px. Typical widths:
  ≈ 640 for a chart across `.moz-main`, ≈ 1100 across `.moz-main.wide`, and
  ≈ 520 inside a card in a two-column `.moz-grid`.
- Small screens: the SVG scales down, and its text with it. For dense
  charts, set `style="--chart-min-width: 480px"` on the `.moz-chart`; it then
  scrolls sideways on phones rather than shrinking the text below legibility.
- Keep labels clear of gridlines and other labels. Put value labels above
  bars, but beside or below line points that sit near the top gridline.
  Leave about 24 units of headroom above the tallest mark.
- Round axis maxima to nice numbers, start bar axes at zero, and label units
  ("crashes per 1,000 hours", not "rate"). Never use two y-axes; make two
  charts.

## Accessibility

- Wrap the chart in `<figure class="moz-chart">`. The `<figcaption>` says
  what is shown ("Crashes per 1,000 hours by channel, last 6 weeks").
- Give the `<svg>` `role="img"` plus `aria-labelledby` pointing at a `<desc>`
  that states the takeaway in one or two sentences.
- Add `<p class="summary">` with the key takeaway in plain words.
- For anything beyond a handful of points, include the data as a table:
  `<details><summary>Show data</summary><table class="moz-table compact">…</table></details>`.
- Hover tooltips: put a `<title>` inside each mark. They're nice to have, but
  never the only way to read a value.

## Pattern: horizontal bars

```html
<figure class="moz-chart">
  <figcaption>Top crash signatures, last 7 days</figcaption>
  <svg viewBox="0 0 640 132" role="img" aria-labelledby="sig-desc" font-size="13">
    <desc id="sig-desc">OOM small leads with 9,112 crashes, about twice the next signature.</desc>
    <!-- label column 0–200, bars from x=210, 1px = 40 crashes -->
    <g>
      <text x="200" y="22" text-anchor="end">OOM | small</text>
      <rect x="210" y="8" width="228" height="22" fill="var(--chart-1)"><title>9,112 crashes</title></rect>
      <text class="label" x="446" y="24">9,112</text>
    </g>
    <g>
      <text x="200" y="62" text-anchor="end">nsThread::ProcessNextEvent</text>
      <rect x="210" y="48" width="118" height="22" fill="var(--chart-neutral)"><title>4,730 crashes</title></rect>
      <text class="label" x="336" y="64">4,730</text>
    </g>
    <line class="axis" x1="210" x2="210" y1="0" y2="120"/>
  </svg>
  <p class="summary">One signature accounts for more than half of all crashes.</p>
</figure>
```

## Pattern: line chart with direct labels

```html
<figure class="moz-chart">
  <figcaption>Daily active users, millions</figcaption>
  <svg viewBox="0 0 640 220" role="img" aria-labelledby="dau-desc" font-size="13">
    <desc id="dau-desc">Release grows from 180 to 196 million; beta stays near 12 million.</desc>
    <line class="gridline" x1="40" x2="560" y1="20" y2="20"/><text x="32" y="24" text-anchor="end">200</text>
    <line class="gridline" x1="40" x2="560" y1="100" y2="100"/><text x="32" y="104" text-anchor="end">100</text>
    <line class="axis" x1="40" x2="560" y1="180" y2="180"/><text x="32" y="184" text-anchor="end">0</text>
    <polyline fill="none" stroke="var(--chart-1)" stroke-width="2" stroke-linejoin="round"
              points="40,36 144,34 248,31 352,29 456,25 560,23"/>
    <text class="label" x="568" y="27">Release</text>
    <polyline fill="none" stroke="var(--chart-2)" stroke-width="2" stroke-linejoin="round"
              points="40,170 144,170 248,171 352,170 456,170 560,170"/>
    <text class="label" x="568" y="174">Beta</text>
    <text x="40" y="204">Sep 1</text><text x="560" y="204" text-anchor="end">Oct 12</text>
  </svg>
</figure>
```

Compute coordinates in code (e.g. a short Python snippet) rather than by
hand when there are more than a few points, and paste the result into the
page. Keep the SVG static unless interactivity is the point.
