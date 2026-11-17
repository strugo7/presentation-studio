# Design systems & reference libraries

## Ready-made systems (set `design.system` to one of these)

Each is a committed palette + type + motif. Hexes are defaults; tune to the topic.

### `signal` — institutional, weighty (reports, security, board, research)
Deep navy canvas on dark slides, bone/white content, one steel-blue accent, one warm amber reserved for
the "payoff" moment. Motif: big section numbers + framed exhibit cards. Reads credible, not loud.
`palette: bg FFFFFF · ink 1A2230 · mute 5B6472 · accent 2C5F7C · accent2 B4722E · hair E2E5EA · dark 1C2A3A`
`fonts: display/body Assistant (or Archivo + Inter for Latin) · mono JetBrains Mono`

### `cobalt-grid` — studious, modernist (teaching, design-research, technical)
Light slides on a faint graph-paper grid, a single cobalt accent, hairline rules, printed-ledger calm.
Pairs with `signal`'s dark slides for the sandwich. Great for process/evidence decks.

### `swiss` — Bauhaus, precise (analytical, minimalist)
White/near-black, one red accent, a visible grid, asymmetric layout, large section numbers. No ornament.

### `editorial` — magazine, warm (keynote, narrative, culture)
Warm paper, a distinctive display serif (Fraunces/Bodoni) + clean sans body, generous white space,
pull-quotes. Use for talks meant to move, not to brief.

### `mono` — ivory ledger, all-ink (whitepaper-feel, text-forward)
No colour; serif headline + sans body; the words are the design. For dense, sober, reading-first decks.

**Dark backgrounds for all systems:** deep navy `1C2A3A` (not pure black), optionally a muted photo
behind a navy scrim on cover/dividers/close.

---

## What a system changes in the output (tokens)

`design.system` is resolved by `shared/blueprint_lib.py` (`SYSTEM_TOKENS`, `SYSTEM_ALIASES`) into
tokens that both renderers apply, so a system changes **composition, typography and rhythm**, not just
the palette:

| Token | Effect |
|---|---|
| `titleScale` / `titleWeight` | title size and weight (keynote titles are big and light; executive titles compact and bold) |
| `coverAlign` | cover/statement text at the start edge or centred |
| `motif` | `grid` (graph paper) · `none` · `rule` (running head with deck/section name + page number) · `numbers` (large faint section numeral) |
| `frame` | exhibit treatment: `card` (white, rounded, shadow) · `hairline` (1 px border, square) · `bleed` (no frame) |
| `margin` | page margin in px at 1920 (airy 150 → compact 100) |
| `kicker` | `accent` · `caps` (tracked, muted) · `number` (section number + kicker) |
| `lightBg`, `bodyScale`, `radius` | content canvas colour, body size, corner radius |

Override any token per deck with `design.tokens`; describe the intent in `design.variant`.

## Directions (aliases built on the presets)

| `design.system` | Base preset | For | What visibly changes |
|---|---|---|---|
| `editorial-report` | editorial | annual/impact reports, narrative findings | light serif-like scale, running head, generous margins, bleed images |
| `product-demo` | cobalt-grid | demos, product reviews, launches | no grid, tinted canvas, large rounded cards, `split` slides with screens |
| `executive-data-briefing` | signal | board, management, decision briefs | compact titles, hairline frames, running head, `big-number` + `full-exhibit` rhythm |
| `classroom-workshop` | cobalt-grid | teaching, onboarding, workshops | warm green/orange palette, numbered kickers, rounder cards, slightly larger body |
| `keynote` | editorial | conference talks, inspire | very large light titles, centred statements, minimal chrome, photo dividers |
| `technical-case` | swiss | engineering case studies, incident reviews, research | asymmetric swiss grid, section numerals, hairline frames, steel/orange accents |

Use the preset directly when no direction fits; compose `custom` + `tokens` for brand work.

**Same content, two directions:** render the same blueprint with `executive-data-briefing` and
`keynote` — title size/weight, alignment, margins, frames and motif all change in both HTML and PPTX
(the test suite checks that two systems produce different title geometry and typography).

## Hebrew typography

- **Fonts (Google Fonts, SIL OFL 1.1):** Assistant (bundled, embedded automatically in HTML — offline),
  Heebo (neutral sans, product), Rubik (rounded, friendly, workshops), Frank Ruhl Libre (serif, editorial
  and keynote titles), Noto Sans Hebrew (widest coverage), Secular One (display only, short titles).
  Set `fonts.display/body`; for PPTX the font must be installed or embedded by the user (File → Options
  → Save → Embed fonts); Google Slides only matches Google Fonts.
- **Pairing:** one family is usually enough (weight carries hierarchy). For editorial: Frank Ruhl Libre
  titles + Assistant body. Avoid Latin-only display faces for Hebrew text — they fall back mid-word.
- **Mixed numbers and Latin terms:** check `−46.5%`, `TLS 1.3`, `179.9 ms`, version strings and dates
  render in the right order (renderers isolate big numbers and units; check the rest by eye). Keep
  code/commands in `mono` bullets (LTR-isolated).
- **Labels:** chart axes keep LTR geometry in both formats (time runs left → right); text labels are
  shaped as Hebrew. Tables mirror column order (row labels on the right). Process chains and timelines
  start on the right.
- **Line length:** Hebrew reads well at 45–75 characters per line; bullets wrap earlier than Latin.

---

## Reference libraries to pull looks from (research these when composing a custom system)

- **`design-gallery.md`** (this folder) — 13 real-world references, each opened and checked (links only), with what each teaches and how it maps to our layouts.
- **`zarazhangrui/frontend-slides`** — 12 presets + ~34 bold templates. Mine it for composition and
  type pairings. Fitting picks for serious/academic work: Swiss Modern, Cobalt Grid, Blue Professional,
  Signal, Monochrome, Electric Studio. **Avoid** its hacker/neon templates (Terminal Green, Neon Cyber,
  8-Bit Orbit, Studio) — exactly the look to never ship.
- The curated skill list at `tosea.ai/blog/best-claude-code-skills-powerpoint-2026` names other design
  skills (Office Kit component TSX, template-layout skills, HTML-first builders). Treat as a menu for
  where to borrow technique; the article is a vendor listicle, not a benchmark.

When you borrow, take the **composition** (layout archetype, type scale, grid, motif) — translate it
into our palette and fonts. Don't copy another deck's content or colours wholesale.

---

## Hard "don'ts" (these read as AI-generated filler — never do them)
- No accent **lines under titles**; no decorative **colour bars / edge stripes / one-side borders**.
- No neon, no cyberpunk, no black-background-green-text "hacker" look — even for a security/tech topic.
- No purple-gradient-on-white; no generic indigo `#6366f1`.
- No cream/beige default backgrounds when none was asked for — use white.
- No clip-art, no icons-in-coloured-circles as the motif, no stock-photo filler on content slides.
- Don't centre body text (centre only titles); don't fill every inch — white space is a signal.

## Layout defaults the builders already follow (so your `design` lines up)
- 16:9; margins from the `margin` token. Evidence slides: exhibit on `side` (default left), interpretation opposite.
- `slide.layout` (`statement`, `split`, `full-exhibit`, `big-number`) overrides the role default — see layout-patterns.md.
- Dark/light sandwich. Big numbers on dividers. Screenshot/figure in a bordered card with a caption.
- One font family per deck unless brand says otherwise; size+weight carry hierarchy.
