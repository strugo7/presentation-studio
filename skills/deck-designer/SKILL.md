---
name: deck-designer
description: "Method for choosing a presentation's visual direction — a design system whose tokens change composition, typography and rhythm, a per-slide layout (statement, split, full-exhibit, big-number), a dark/light rhythm, and licensed, credited images/icons — and writing it into blueprint.json. Use after structure is set, to make a deck read as one designed system instead of a template, or to restyle an existing deck. Pairs with references/design-systems.md."
---

# deck-designer — one system, committed

You own `design`, each slide's `layout`/`background`/`dark`, and the visual `assets[]` (with provider,
licence, credit). Method below.

## References — open when
- `references/design-systems.md` — step 1 (systems, directions, tokens), step 1b (direction previews,
  lineage of the presets) and step 2 (Hebrew typography).
- `references/layout-patterns.md` — step 3, choosing a layout per slide; read only the patterns you use.
- `references/design-gallery.md` — when composing a custom direction, preparing direction previews, or when
  the user asks for "something like X". Start from its quick map (reference → preset → layout), find entries
  by tag (audience, slide role, format), and borrow the principle, never the asset.
- `references/asset-sources.md` — step 5, before adding any image or icon you didn't get from the user.

## 1. Read the topic, pick a direction
Design for *this* content and audience. Security report ≠ a wellness workshop ≠ an investor pitch. Pick
a preset (`signal`, `cobalt-grid`, `swiss`, `editorial`, `mono`) or a direction built on one
(`editorial-report`, `product-demo`, `executive-data-briefing`, `classroom-workshop`, `keynote`,
`technical-case`), or compose `custom` + `design.tokens`. The system sets type scale, alignment, motif,
exhibit frame and margins in both renderers. Commit to a thesis: a dominant colour (60–70% of the visual weight), 1–2
supporting tones, one sharp accent for emphasis, and a second warm accent reserved for the single
"payoff" moment per section.

## 1b. Optional: let the user choose by seeing (direction previews)
Use this path **only** when:
- the user asks to see directions or options; or
- the brief leaves open a visual decision that changes the result: two plausible directions that differ
  in composition, not just colour, with no brand guidelines to settle it.

Otherwise commit to one direction (step 1) and move on.

1. Pick 2–3 directions that differ in at least `titleScale`/`titleWeight`, `coverAlign` or `motif`, and
   `frame` (design-systems.md, "Direction previews", for default trios by deck type).
2. Pick the slides that show the difference: the cover plus one typical slide, the kind this deck has
   most (a chart, a process, a product screen). Use the slide ids from the blueprint.
3. Hand the orchestrator the systems and slide ids. It renders them from the same blueprint:
   ```bash
   python shared/preview_directions.py blueprint.json previews/ --systems=a,b,c --slides=id1 --png
   ```
   The renders use the user's real content, with every reveal shown. Direction names appear only on the
   comparison page, never on a slide.
4. The user compares composition, density and title size side by side, and picks one (or "A's cover with
   B's frame" → `custom` + `design.tokens`).
5. Write the chosen `design.system` (+ any tokens) into the blueprint and continue with step 2.

No blueprint field changes for this path. Old blueprints are untouched, because the script only sets
`design.system` on temporary copies.

## 2. Typography
Hebrew/RTL or another non-Latin script: choose a font that actually has those glyphs (e.g. **Assistant**,
Heebo, Noto) and set it as the body/display — never rely on a Latin display font for non-Latin text.
Otherwise pick a distinctive display face + a clean body (avoid Inter/Roboto/Arial *as the display*).
Use size and weight for hierarchy, one or two families max. Reserve a monospace only for code/command
tokens. Write `fonts.display/body/mono`.

## 3. The motif (pick ONE, repeat it)
A faint graph grid; big section numbers (01/02/03); framed screenshot cards; a consistent photo
treatment. Repeat it on every slide. **Not** an accent stripe/bar and **not** a line under the title —
those read as AI filler. Record it in `design.motif`.

## 3b. Layout per slide (composition)
Set `slide.layout` where the content job calls for it (layout-patterns.md): `big-number` for one
decisive figure, `full-exhibit` for an exhibit that must be read, `split` for a product screen or photo
plus meaning, `statement` for a single sentence or question. Leave it empty to use the role default.
Vary the rhythm deliberately; repeat a layout when the job repeats. One content job per slide.

## 4. Dark/light rhythm + backgrounds
Default sandwich: **dark** cover, section dividers, stakes, close; **light** content. Set each slide's
`dark` and `background.kind`:
- `grid` — light content slides (the motif grid).
- `navy`/`solid` — dark statement slides.
- `photo` — a dark slide with an atmospheric image behind a navy scrim (set `background.assetRef` to
  an `assets[]` id — or legacy `background.photo` path — and `background.scrim:true`). Use photos only
  when they add depth and never as filler on content slides. Builders crop to fill and apply the scrim,
  and print the credit on that slide and on the sources page.

## 5. Assets
Follow asset-sources.md: user material first; then a provider whose licence you record. Every image gets
an `assets[]` entry with `provider`, `sourceUrl`, `creator`, `license`, `licenseUrl`, `credit`, `alt`, and
a PNG `fallbackPath` for any SVG (PPTX can't place SVG). One icon family per deck (Tabler by default).
Keep files local with stable names so the deck works offline.

## 6. Hand off
Write back `design` + per-slide `layout`/`background`/`dark` + `assets[]`. State your system/direction,
palette hexes, fonts, motif, and the layout rhythm in one short summary. Don't change titles, bullets,
exhibit data, citations or animation. If the user gave brand guidelines or a font, apply them exactly
and skip the defaults. When only the style changes, you re-run alone (then animator and builders).
