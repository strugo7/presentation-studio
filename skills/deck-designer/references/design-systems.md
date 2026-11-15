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

## Reference libraries to pull looks from (research these when composing a custom system)

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
- 16:9, ~0.5" / 56px margins. Evidence slides: exhibit on `side` (default left), interpretation opposite.
- Dark/light sandwich. Big numbers on dividers. Screenshot/figure in a bordered card with a caption.
- One font family per deck unless brand says otherwise; size+weight carry hierarchy.
