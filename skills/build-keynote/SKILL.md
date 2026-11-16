---
name: build-keynote
description: "Produce an Apple Keynote (.key) version of a deck. Keynote has no open file format and no headless generator, so this routes through PPTX: build the .pptx, then import it into Keynote (Keynote reads .pptx natively) — automated with AppleScript on macOS, or by hand. Use when the user specifically wants a Keynote file."
---

# build-keynote

**Honest constraint:** `.key` is a proprietary, undocumented bundle. Nothing can generate it headlessly
and no library writes it. The reliable path is **PPTX → open in Keynote → save as Keynote**. Keynote
imports `.pptx` with high fidelity (layouts, text, tables, images, charts). This is the standard route,
not a workaround.

## Build
1. Make the PPTX first (see build-pptx):
   ```bash
   python shared/render_pptx.py blueprint.json out.pptx [assets_dir]
   ```
2. **macOS, automated** (requires Keynote installed; the first run asks for Automation permission):
   ```bash
   osascript shared/pptx_to_keynote.applescript /abs/path/out.pptx /abs/path/out.key
   ```
   It opens the PPTX in Keynote and exports a `.key`.
3. **Any OS, by hand:** open `out.pptx` in Keynote → File → Save (keeps it as a Keynote document), or
   File → Export.

## Capabilities
What this format does with each blueprint feature (layouts, charts, quizzes, polls, reveals, sources,
fonts, RTL) and its fallbacks: **`skills/presentation-studio/references/format-capabilities.md`** — the
single matrix for all builders. Read the row for this format before telling the user what they'll get.

## Validate first
```bash
python shared/validate_blueprint.py blueprint.json [assets_dir]
```

## What survives the import
- **Verify in the target environment:** this repo can't open Keynote or a Google account; check charts, links (quiz → answer slides, sources), and mixed Hebrew/English alignment after import., and what to tell the user
- **Survives well:** slide layout, text, action titles, tables, images, generated backgrounds, native
  charts, speaker notes.
- **Degrades:** **Morph** transitions map imperfectly to Keynote's *Magic Move* — re-check the few
  slides that use them. **PowerPoint Zoom** navigation does **not** import — in Keynote, rebuild
  section navigation with hyperlinked objects or just present linearly.
- **Fonts:** install the deck font (e.g. Assistant) on the presenting Mac, or let Keynote substitute.
- For motion-heavy decks, the **HTML** build is the better "wow" deliverable; offer it alongside.

## Deliver
The `.key` (if produced on a Mac) or the `.pptx` with one line: "open in Keynote and Save as Keynote."
