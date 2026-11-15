---
name: build-pptx
description: "Render a finished blueprint.json into a native editable PowerPoint (.pptx): roles, action titles, one-exhibit slides, native charts/tables, generated grid/photo backgrounds, RTL-correct Hebrew (sets complex-script font + language on every run), Morph transitions, and Sections + a map slide for Zoom navigation. Use when the user wants a PPTX / PowerPoint file."
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
- **Exhibits:** chart→native pptx chart (bar/column/line), table→native table, diagram→shape chain,
  image/screenshot→picture, code→mono box.
- **Backgrounds:** generated grid (light) / navy (dark); a photo asset gets a navy scrim.
- **Motion:** `animation.transition:"morph"` and, when `navigation.mode=="zoom"`, Morph on every slide
  + **Sections** + a map slide, named objects so Morph only matches what it should.

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
