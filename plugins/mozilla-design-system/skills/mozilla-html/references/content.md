# Writing for Mozilla HTML assets

Condensed from Acorn's content guidelines
(https://acorn.firefox.com/latest/content/content-overview-ww9dIoVj). These
rules are written for en-US Firefox UI; apply them to every visible string in a
generated page: headings, buttons, labels, table headers, captions, alt text.

On `data-brand="mozilla"` pages the Mozilla house style differs in three
places (see `brand-mozilla.md`): avoid the Oxford comma unless needed for
clarity, write dates as YYYY-MM-DD, and prefer "internet" over "web".
Everywhere else, write dates unambiguously (2026-10-12 or Oct 12, 2026; never
10/12/26).

**Audience decides the vocabulary.** The word list and product names below
are for copy that people outside the team read. In internal reports and
tools, keep the team's own established terms ("add-on review queue", "AMO",
"Socorro") where readers expect them. Still apply the style rules: sentence
case, plain language, curly quotes.

## Voice

Firefox and Mozilla copy is sincere, encouraging, and confident without
overselling. "Firefox uses the language of people, not technology."

Pick a tone by context:

| Context | Tone |
|---|---|
| Reports, dashboards, settings-like tools, tables | Neutral. Just enough information. |
| Errors, warnings, risk explanations | Reassuring but plain. Clarity first, no drama. |
| Feature intros, onboarding, launch one-pagers | Slightly upbeat. Encouraging, never sales-y. |
| Thank-you and celebration moments | Enthusiastic. Rare. |

UX writing heuristics:
- Write the way people talk. No technical jargon or "browser-speak".
- Lead with the value. Outcomes over explanations.
- Every word has a purpose. Trim hard, but not at the expense of meaning.
- Make it scannable: headings, short sections, lists, bold for the key point.

## Capitalization

- **Sentence case by default**: page titles, headings, buttons, labels, table
  headers, tabs, legends. Capitalize the first word and proper nouns only.
- Title case only for brand and product names (Mozilla, Firefox, Mozilla VPN)
  and proprietary feature names (Enhanced Tracking Protection,
  Picture-in-Picture, Reader View, Total Cookie Protection).
- Generic features stay lowercase: new tab, shortcuts, passwords, private
  browsing, sync, settings.
- Acronyms in all caps (URL, VPN). Spell out uncommon acronyms on first use
  with the abbreviation in parentheses.

## Punctuation

- Curly quotes and apostrophes: ’ “ ” — never straight `'` or `"` in visible
  text. (Firefox enforces this for UI strings.)
- Oxford comma: "tabs, bookmarks, and history".
- Em dash with spaces — like this. En dash without spaces for ranges: 1–9.
- No end punctuation on titles, headings, buttons, labels, list items,
  tooltips, or error text under fields. Use periods in full sentences in body
  copy and descriptions.
- Ellipsis only on a control that leads to a further step ("Save as…"). Never
  on "Learn more".
- Exclamation points sparingly, only for genuine excitement.
- Avoid "&" unless space is truly constrained.
- Use contractions (you’re, it’s, don’t).
- No emoji in desktop-style UI or in reports.

## Buttons and links

- Buttons are verbs that describe the outcome: "Export report", "Save
  changes", "Remove account". Never "OK", "Submit", "Click here".
- Use "select" or "choose", not "click" or "tap".
- No articles in labels ("Add filter", not "Add a filter").
- Links navigate, buttons act. Do not style a link as a button to perform
  an action, or a button to navigate.
- Link text must make sense out of context. "Learn more" is acceptable only
  when the surrounding sentence makes its target clear; prefer "Learn more
  about data collection".
- Leave room for translation: copy can grow 50% or more. No fixed widths on
  buttons.

## Form controls

- Every input has a visible label (or `aria-label` if a visible one is truly
  impossible). Placeholders are never labels.
- Mark the minority: "(required)" if few fields are required, "(optional)" if
  most are.
- Checkbox and radio labels: imperative, parallel construction, no terminal
  punctuation ("Use smooth scrolling", "Use autoscrolling").
- Toggle labels: a short name for the thing being switched ("Autoplay",
  "Rejection details"), not an action ("Show rejection details"). Put any
  explanation in the description line.
- Never offer a single radio button.

## Messages and feedback

- Information: passive, helpful, no action required.
- Warning: something may become a problem; say how to prevent it.
- Critical: task-blocking or privacy/security impact; say how to fix it.
- Success: confirms an action the reader took.
- Errors and warnings are non-expressive; success and info may be warmer.
- Pair every status color with an icon and words. Color alone is never the
  signal.

## Empty states

- Title: concise, sentence case, no end punctuation (unless a question). Lead
  with what is possible, not with "No …".
- Body: one or two sentences, don't repeat the title.
- Action: a strong verb plus a noun ("Create a collection").

## Inclusive and global language

- Say "people" (or a specific role), not "users" or "customers".
- Gender-neutral language. Avoid idioms, sports analogies, and slang.
- Replace: master password → primary password; blacklist/whitelist → block
  list/allow list; dark pattern → deceptive design pattern; native feature →
  built-in feature; guys → everyone, folks. Avoid "dumb", "crazy", "sanity
  check", "insane".
- Plain language, active voice, articles before nouns.
- Alt text describes the image's purpose; repeat any text that appears in it.
  Mark decorative images `alt=""`.

## Word list highlights

| Write | Not |
|---|---|
| settings | options, preferences |
| sign in (verb), sign-in (noun) | login, sign into |
| email | e-mail |
| website, webpage, web, internet | web site, Internet |
| extensions and themes | add-ons |
| address bar, toolbar | awesome bar |
| application menu | hamburger menu, app menu |
| Firefox for desktop, Firefox for Android, Firefox for iOS | desktop Firefox, Firefox desktop |
| select, choose | click, tap |
| touch and hold | long press |
| OK | Okay, O.K. |
| US | U.S. |

Internal names such as SUMO, AMO, ETP, or PiP should not appear in copy meant
for people outside the team; write Mozilla Support, addons.mozilla.org,
Enhanced Tracking Protection, Picture-in-Picture.

## Keyboard shortcuts

Describe the action in sentence case and put the shortcut in parentheses:
"Reload page (Ctrl + R)" on Windows and Linux, "Reload page (⌘R)" on macOS.
Wrap keys in `<kbd>`.
