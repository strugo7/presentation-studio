---
name: build-pptx
description: "Render a finished blueprint.json into a native editable PowerPoint (.pptx): roles and layouts, design-system tokens, native editable charts (column/bar/line/scatter with units), tables, diagram shapes, quiz options linked to answer slides, citations + generated sources slides with links, alt text, RTL-correct Hebrew (complex-script font + language on every run), Morph transitions, and Sections + a map slide for Zoom navigation. Use when the user wants a PPTX / PowerPoint file."
---

# build-pptx

Produces a genuinely editable PowerPoint from the blueprint — native charts (not images), real tables,
and the RTL fixes that stop Hebrew rendering as tofu boxes.

## Build
```bash
python shared/render_pptx.py blueprint.json out.pptx [assets_dir]
```
Then always validate:
```bash
python <pptx-skill>/scripts/office/validate.py out.pptx
```
(The Anthropic `pptx` skill's validator catches chart/XML faults PowerPoint would silently repair.)

## What it does for you
- **RTL / Hebrew:** sets `<a:cs>` (complex-script) typeface + `lang` on every run, and rewrites the
  theme fonts to the deck font — the reliable fix for the "boxes" bug. Reverses table column order and
  right-aligns for RTL.
- **Exhibits:** chart→native, editable pptx chart (column/bar/line/scatter; number format, unit, axis
  titles from the same spec as HTML; unsupported kinds → table), table→native table, diagram→shapes
  (chain, timeline, sequence with arrows), image/screenshot→picture with alt text (SVG uses its PNG
  `fallbackPath`, else a labelled placeholder + warning), code→mono box.
- **Layouts & tokens:** `statement`, `split`, `full-exhibit`, `big-number`; the design system sets title
  size/weight, margins, frame style and motif (grid, running head, section numerals).
- **Quizzes:** options hyperlink to a generated answer slide (`answerPlacement`), which links back;
  `presenterCue` goes into the notes.
- **Sources:** a citation footer on each slide and generated "Sources & credits" slides with hyperlinks.
- **Backgrounds:** generated grid (light) / navy (dark); a photo asset gets a navy scrim.
- **Motion:** `animation.transition:"morph"` and, when `navigation.mode=="zoom"`, Morph on every slide
  + **Sections** + a map slide, named objects so Morph only matches what it should.

## Capabilities
What this format does with each blueprint feature (layouts, charts, quizzes, polls, reveals, sources,
fonts, RTL) and its fallbacks: **`skills/presentation-studio/references/format-capabilities.md`** — the
single matrix for all builders. Read the row for this format before telling the user what they'll get.

## Validate first
```bash
python shared/validate_blueprint.py blueprint.json [assets_dir]
```

## The Zoom caveat (tell the user)
PowerPoint **Zoom objects cannot be created by any script.** This builder pre-makes the Sections and
the map/agenda slide, so finishing the zoom is a ~2-click manual step in PowerPoint 2019/365:
`Insert → Zoom → Section Zoom`, pick the sections, turn on *Zoom Background* + *Return to Zoom*
(see deck-animator/references/techniques.md). Morph needs 2019/365 too; older/other apps show a fade.

## Fonts
Name the font in `design.fonts`. For portability, tell the user to enable **File → Save → Embed fonts
in the file** (PowerPoint embeds reliably; script-side variable-font embedding is not reliable).

## Deliver
The `.pptx` (and the credits/README if photos were used). For a PDF of it, use **build-pdf** `--from=pptx`.
