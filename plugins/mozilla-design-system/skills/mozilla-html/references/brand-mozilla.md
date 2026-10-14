# Mozilla brand (`data-brand="mozilla"`)

Source: Mozilla Brand Guidelines, https://brand.mozilla.com/ (Visual
Elements and Voice & Message). Use it for Mozilla-the-organization
communication: corporate, policy, research, community, events, Mozilla
Builders and new products, and internal Mozillian materials. Use the Firefox
brand for anything about Firefox.

Mozilla Foundation (fellowships, advocacy campaigns, Foundation-run grants)
has its own, login-gated guide that this skill doesn't cover. If the
publisher is clearly the Foundation, tell the user, use this theme as the
closest match, and suggest a check with #brand. If it's unclear who
publishes, use this theme.

Brand questions and lockup requests go to #brand on Slack. The guidelines
grant no trademark permission to third parties.

## Setup

```html
<html lang="en" data-brand="mozilla">
<head>
  ...
  <link rel="stylesheet" href="tokens.css">
  <link rel="stylesheet" href="components.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mozilla+Headline:wdth,wght@75..100,200..700&family=Mozilla+Text:wght@200..700&display=swap">
</head>
```

## Two modes: "Governments" and "Grassroots"

The identity spans a range. Pick the end that fits the audience:
- **Governments** (the default for reports, policy, and professional
  audiences): iconic, focused, minimal. About 45% black, 45% white, and 10%
  green. Green is a pop, not a theme. This is what the theme does out of the
  box.
- **Grassroots** (community, events, podcasts): expressive and bold. About
  20% black, 20% white, and 60% vibrant color from the secondary palette. Use
  one color family with tints, or several pops separated by black or white
  fields. Build these sections with the `--mozilla-*` variables. Never flood
  large text areas with pop colors.

## Logo

- Use the primary lockup (`data-logo="mozilla-lockup"`, wordmark plus flag
  symbol) by default. Use the wordmark alone (`mozilla-wordmark`) sparingly.
  Use the symbol (`mozilla-symbol`) with the wordmark nearby, since it is
  still building recognition.
- Colorways: strong black `#000` or strong white `#fff` only. The logo SVGs
  use `currentColor` for this; don't set any other color.
- Clear space is the height of the lowercase "z" in the wordmark. The minimum
  height is 20px for the lockup and symbol and 12px for the wordmark.
- Anchor the lockup to the top-right or bottom-right corner (`.moz-masthead`
  does this in this theme). The wordmark can go in any corner.
- Don't angle, distort, outline, crop, recolor, or typeset the logo. Don't
  invent lockups such as "Mozilla Something"; request them in #brand.

## Color

| Name | Value | Use |
|---|---|---|
| White | `#fafafa` (`--mozilla-white`) | Light backgrounds |
| Black | `#161616` (`--mozilla-black`) | Dark backgrounds |
| Strong White / Strong Black | `#ffffff` / `#000000` | Text and logos only, never backgrounds |
| Green | `#00d230` (`--mozilla-green`) | Buttons, calls to action, highlights, focus areas |
| Green +1 / −1 / −2 | `#d6ffcd` / `#28733f` / `#022611` | Grassroots range; +1 is used for tinted surfaces |
| Pink +1 / Pink / −1 / −2 | `#fff1f8` / `#ff97e2` / `#ae49ec` / `#210340` | Grassroots |
| Orange +1 / Orange / −1 / −2 | `#faf0e6` / `#ff9456` / `#ff453f` / `#330505` | Grassroots |

Rules:
- **No colored text.** Text is strong black or strong white. Links are
  underlined text.
- Green on white is only 2:1, so never use it for text, thin lines, or focus
  rings on light backgrounds. Black on green (10:1) is the button style.
- Don't use colors outside the palette. When in doubt, use black and white.
- Charts: the brand's own data-viz palette (aqua, seed, grey, clay) is too
  low in chroma and too light or dark to pass color-vision and contrast
  checks. The theme therefore uses Green −1, Pink −1 and Orange −1 for
  `--chart-1` to `-3`, and greys for the rest. The house style is one green
  series against grey. With three series, label them directly, because
  green and orange are close for protan readers. Always separate adjacent
  fills with divider gaps (`class="mark-gap"`). See `charts.md`.

## Typography

| Role | Face | Notes |
|---|---|---|
| XL headline (61px+) | Mozilla Headline ExtraLight | `.moz-hero .display` (set by the theme); line height 90%, letter spacing up to −2% |
| Headline (24px+) | Mozilla Headline Regular, the "workhorse" | `h1`, `h2`; standard width |
| Subhead (19–23px) | Mozilla Text SemiBold | `h3` |
| Body (13–18px) | Mozilla Text Regular | Medium or SemiBold for emphasis |
| Large numbers | Mozilla Headline Condensed ExtraLight, −2% tracking | `.moz-stat .value` (set by the theme) |

- Standard width for everything except large numbers.
- Never use Headline below 24px, and never use Text for primary headlines.
- Left-align all text, including headlines. Use sentence case. Use at most
  three weights per layout.
- Captions go above or below images, never beside or over them. Set them
  with a bold title and a regular descriptor.

## Voice and writing style

"We serve up relatable expertise, with a dash of wit."
- **Passionate**, **Welcoming**, and **No bullsh\*t**. Fearless, optimistic,
  insightful. Humor is fine but never punches down.
- Governments mode: lead with real, tangible impact and cut to the chase.
  Grassroots mode: tell stories; "our 'we' is bigger than just Mozilla."
- House style, which differs from Firefox UI copy:
  - Write **"internet" rather than "web"**, lowercase.
  - **Avoid the Oxford comma** unless it's needed for clarity.
  - Format **dates as YYYY-MM-DD**.
  - Use sentence case everywhere, including CTAs and buttons.
  - Use contractions, clean punctuation, and American English.
- Avoid buzzwords, hype, and jargon. Prefer action-oriented language that
  emphasizes people's agency.
- The sign-off "Reclaim the internet with us" works best as a closing line,
  not as a headline.

## Imagery

- Illustration styles are pixelgrams, wireframes, 3D bitmap, and bitmap.
  Use one style and one illustration per composition, and never generate
  imitations. Leave a labeled placeholder for the brand team instead.
- The dino mascot complements the logo but never replaces it. Use only
  strong black or white.
- Photography puts people first and shows real moments in natural light.
  Use only approved sources with releases.
