# Render existing Markdown

`scripts/render_markdown.py` uses Pandoc to convert Markdown into the skill's
HTML components, then runs `bundle.py` and `check.py`. It requires Python 3.9+
and Pandoc in PATH. The existing HTML workflow still needs only Python 3.

Run scripts using absolute paths when outside this skill's directory:

```sh
python3 -I scripts/render_markdown.py report.md -o report.html
python3 -I scripts/render_markdown.py report.md --theme firefox --layout wide --tables accent -o firefox-report.html
python3 -I scripts/render_markdown.py report.md --theme mozilla --layout reading --no-toc -o mozilla-report.html
```

| Option | Choices | Default |
|---|---|---|
| `--theme` | `acorn`, `firefox`, `mozilla` | `acorn` |
| `--layout` | `reading`, `wide`, `sidebar` | `sidebar` |
| `--toc` / `--no-toc` | Show or hide links to level-two sections | Show |
| `--scheme` | `auto`, `light`, `dark` | `auto` |
| `--tables` | `plain`, `accent`, `compact` | `plain` |
| `-o` / `--output` | Output HTML path | Beside the input, with `.html` extension |

The renderer writes both `report.src.html` and the bundled `report.html`.
Regenerate from Markdown after edits. The source HTML records the selected
layout and can also be customized and re-bundled with the existing tools.
Brand themes load Mozilla fonts from Google Fonts, matching the HTML workflow;
offline they use fallback fonts. Acorn requires no external requests.

## Document structure

Use one `#` heading as the document title, or put a `title` in YAML metadata
and start sections with `##`. The original title formatting, section IDs,
prose, numbers, and links are preserved. The renderer does not edit the copy;
the checker may flag existing title case or other style choices.

Tables gain the Acorn table classes, header scopes, and a keyboard-focusable
scroll wrapper. Local images resolve relative to the Markdown file, even
when the script runs from another directory. Raster images become data URIs.
SVGs are embedded inline, retaining their geometry and colors; SVGs authored
with the skill's chart tokens follow the theme. Repeated SVGs get distinct
IDs for gradients and clip paths. Remote images must be downloaded and
referenced locally before rendering.

Pandoc fenced divs can carry component classes. For example:

```markdown
::: {.moz-message-bar}
::: {.icon-container}
<svg class="moz-icon" data-icon="information-fill"></svg>
:::
::: {.content}
::: {.text}
**Measurement context.** Explain the scope of the numbers here.
:::
:::
:::
```

Use native `<details class="moz-card accordion">` with a `<summary>` and
`<div class="moz-card-content">` for collapsible material; leave blank lines
around Markdown inside the content div. See `examples/report.md` for both
patterns and `references/components.md` for other component recipes.

Raw HTML in the source is retained, including any scripts it contains. This
renderer is intended for documents you trust; it is not an HTML sanitizer.
Mermaid fences remain code blocks. Pre-render them to local SVG images if
diagrams are needed. This adapter does not add a chart library or reinterpret
existing measurements.

## Compare themes and components

```sh
python3 -I scripts/build_demo.py --output /tmp/mozilla-demo
# Open /tmp/mozilla-demo/index.html in a browser.
```

The demo renders `examples/report.md` in all nine theme/layout combinations
and creates three component samplers. The gallery embeds every preview in
one HTML file. It supports side-by-side comparison, light/dark/system scheme,
narrow previews, and downloading the chosen preview. Standalone variants are
also written beside it for viewing without the gallery's JavaScript.

Run the adapter's integration tests with:

```sh
python3 -I scripts/test_render_markdown.py
```
