---
name: deck-designer
description: "Method for choosing a presentation's visual system — a content-informed palette, a distinctive type pairing, one repeated motif, and a dark/light slide rhythm — and writing it into blueprint.json. Use after structure is set, to make a deck read as one designed system instead of a template. Pairs with references/design-systems.md."
---

# deck-designer — one system, committed

You own `design` and each slide's `background`/`dark`. See `references/design-systems.md` for ready
systems and the reference libraries. Method:

## 1. Read the topic, pick a direction
Design for *this* content. Security report ≠ a wellness workshop ≠ an investor pitch. Pick one of the
ready systems in `references/design-systems.md` (Signal, Cobalt-Grid, Swiss, Editorial, Mono) or
compose a custom one — but commit to a thesis: a dominant colour (60–70% of the visual weight), 1–2
supporting tones, one sharp accent for emphasis, and a second warm accent reserved for the single
"payoff" moment per section.

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

## 4. Dark/light rhythm + backgrounds
Default sandwich: **dark** cover, section dividers, stakes, close; **light** content. Set each slide's
`dark` and `background.kind`:
- `grid` — light content slides (the motif grid).
- `navy`/`solid` — dark statement slides.
- `photo` — a dark slide with an atmospheric image behind a navy scrim (set `background.photo`,
  `background.scrim:true`). Source photos only when they add depth and never on content slides.
  Free sources: Unsplash (credit the photographer in the blueprint `assets[].credit` and on the close
  slide). Mute and scrim them so text stays readable (builders apply the scrim).

## 5. Hand off
Write back `design` + per-slide `background`/`dark`. State your system, palette hexes, fonts, and motif
in one short summary. Don't change titles, bullets, exhibits or animation. If the user gave brand
guidelines or a font, apply them exactly and skip the defaults.
