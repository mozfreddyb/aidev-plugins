# Firefox brand (`data-brand="firefox"`)

Source: Firefox Brand Guidelines, https://brand.firefox.com (=
https://brand.mozilla.com/d/5UkPdpbtt8LS). The brand system covers marketing
and communication. Product UI follows Acorn, the default theme.

Use it for pages that represent Firefox to an audience: launch one-pagers,
feature explainers, release highlights, event or campaign pages, and
partner-facing summaries. Internal dashboards and tools about Firefox should
stay on the default Acorn theme.

The guidelines are for Mozilla staff and licensed partners. They grant no
trademark permission to third parties
(https://www.mozilla.org/foundation/trademarks/policy/). Brand reviews happen
in #firefox-brand-reviews on Slack.

## Setup

```html
<html lang="en" data-brand="firefox">
<head>
  ...
  <link rel="stylesheet" href="tokens.css">
  <link rel="stylesheet" href="components.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mozilla+Headline:wdth,wght@75..100,200..700&family=Mozilla+Text:wght@200..700&display=swap">
</head>
```

The fonts are the only network dependency. Without them, type falls back to
Helvetica or Arial and the condensed display face is lost. If the page must
work offline, say so and accept the fallback. Don't substitute another
typeface (Inter is explicitly listed as wrong).

## Logo

- Use the primary lockup (`data-logo="firefox-lockup"`, symbol plus
  wordmark) by default. Use `firefox-lockup-stacked` in narrow spaces.
- Use the symbol alone (`firefox-symbol`) only where the brand is already
  established: favicons, the page-nav heading, small badges.
- The wordmark never appears without the symbol. Never type "Firefox" in a
  font as a logo.
- Clear space is the height of the lowercase "x" in the wordmark. The minimum
  height is 20px.
- Anchor the logo to the top-left (or bottom-left) corner. `.moz-masthead`
  does this. Inline in a headline, the symbol goes before the word "Firefox".
- Don't angle, distort, outline, recolor, crop, or add effects. Approved
  backgrounds: dark purple, purple, cream, soft purple, black, white, the dark
  gradient.

## Color

The theme maps these onto the tokens. Use the tokens, or the
`--firefox-*` variables for brand surfaces.

| Name | Value | Use |
|---|---|---|
| Midnight Purple | `#210340` (`--firefox-midnight-purple`) | Dark backgrounds (dark-mode canvas) |
| Dark Purple | `#3a0f6e` (`--firefox-dark-purple`) | Dark backgrounds, dark surfaces |
| Purple | `#7543e3` (`--firefox-purple`) | Buttons, calls to action, accents |
| Soft Purple | `#f1e7f8` (`--firefox-soft-purple`) | Light backgrounds, tinted surfaces |
| Pink | `#ffeafe` (`--firefox-pink`) | Light backgrounds |
| Cream | `#fcf5f0` (`--firefox-cream`) | Light backgrounds (light-mode canvas) |
| Black 4 | `#15141a` (`--firefox-black`) | Text |
| White | `#ffffff` | Text on dark, card surfaces |

Gradients, for hero areas and illustration only, used sparingly:
- `--firefox-gradient-dark`: the dark gradient, used by `.moz-hero`.
- `--firefox-gradient`: yellow → orange → pink, the Firefox flame. Use it
  for accents such as a thin rule or a large decorative shape.
- `--firefox-gradient-world`: blue → magenta, the pictogram gradient.

Rules:
- Text is always Black 4 or White. **No colored text**, which is why links
  are text-colored and underlined in this theme.
- No gradients on type. Don't use the secondary purple scale for primary
  placements.
- Every pairing must meet WCAG 2.2 AAA where possible. White on Purple is
  only AA (5.7:1), so it's fine for buttons but not for body text.
- When in doubt, use black and white.
- Charts use the Acorn chart palette (`--chart-1` is the Acorn violet, which
  is close to Firefox Purple). It was validated on the cream and purple
  surfaces as well. See `charts.md`.

## Typography

| Role | Face | Notes |
|---|---|---|
| Display / XL headline (61px+) | Mozilla Headline Condensed, Bold | `.moz-hero .display`; line height 90%, letter spacing up to −2% |
| Headline (24px+) | Mozilla Headline Condensed, Bold or SemiBold | `h1`, `h2` |
| Subhead (19–23px) | Mozilla Text SemiBold | `h3`, card and section labels |
| Body (13–18px) | Mozilla Text Regular | Medium or SemiBold for emphasis |

- Firefox uses only the condensed width (`font-stretch: 75%`, set by the
  theme) and doesn't animate the variable axes.
- Never use Mozilla Headline below 24px. Never use Mozilla Text for primary
  headlines. Never set Headline and Text at the same size side by side.
- Left-align all text. Use sentence case everywhere. Use at most three
  weights per layout.

## Voice

Firefox is **Genuine**, **Playful**, and **Fiery**.
- Genuine, always: "We write like a wise friend." Clear, grounded, useful
  over flashy, calm rather than loud.
- Fiery: conviction and a clear stance, for mission, choice, and campaign
  moments. Dial it down for privacy, terms, and warnings.
- Playful: warm, knowing wit that reflects real internet culture, without
  corny wordplay. Use it for welcomes, discovery, and celebration.
- Fox puns: at most one, and never invented words ("foxtastic"). Don't
  speak as the fox. Avoid sly or cunning associations.
- "Run free" is an internal line and not external copy.

## Imagery

- Kit is the Firefox mascot. Use only approved artwork and never redraw it.
  Don't put text over Kit, combine Kit with pictograms, or use more than one
  Kit. Don't generate Kit artwork.
- Pictograms are 60px or larger only. At smaller sizes use product icons
  (`data-icon`).
- Don't invent illustrations in the brand style. If an image is needed,
  leave a clearly labeled placeholder for the brand team, or use simple
  geometric shapes in palette colors.
