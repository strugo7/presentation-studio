---
name: build-google-slides
description: "Produce a Google Slides version of a deck. Google Slides has no offline file; it is created by uploading a PPTX to Google Drive and converting, or via the Slides API. This skill builds the PPTX and gives the import path (and an optional Apps Script). Use when the user wants an editable, collaborative Google Slides deck."
---

# build-google-slides

> **Paths.** This skill ships in the presentation-studio plugin. `shared/…` and `skills/…` paths are under
> `${CLAUDE_PLUGIN_ROOT}/` (in a plain checkout of the repo, the repo root); `references/…` is this skill's own
> folder. Write blueprints and builds in the user's project, never inside the plugin folder.

**Honest constraint:** a Google Slides deck lives in the user's Google account, not as a local file.
Two real routes; both start from the PPTX this studio builds (Google Slides imports `.pptx`).

## Build
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/render_pptx.py" blueprint.json out.pptx [assets_dir]
```

### Route A — upload & convert (no credentials, recommended)
1. Go to Google Drive → **New → File upload** → `out.pptx`.
2. Right-click the uploaded file → **Open with → Google Slides** (Drive converts it).
   (Or set Drive to auto-convert uploads: Settings → "Convert uploads".)
This gives a fully editable, shareable Google Slides deck. The user does this; you can't, because it
needs their Google sign-in — never ask for their credentials.

### Route B — Slides/Drive API (automated, needs the user's OAuth)
If a Google Drive/Slides connector or API credentials are available in the session, upload with
conversion: `files.create` with `mimeType: application/vnd.google-apps.presentation` and the PPTX as
media. Only do this with the user's connected account; don't handle raw credentials.

## Capabilities
What this format does with each blueprint feature (layouts, charts, quizzes, polls, reveals, sources,
fonts, RTL) and its fallbacks: **`${CLAUDE_PLUGIN_ROOT}/skills/presentation-studio/references/format-capabilities.md`** — the
single matrix for all builders. Read the row for this format before telling the user what they'll get.

## Validate first
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/validate_blueprint.py" blueprint.json [assets_dir]
```

## What survives, what to tell the user
- **Verify in the target environment:** this repo can't open Keynote or a Google account; check charts, links (quiz → answer slides, sources), and mixed Hebrew/English alignment after import.
- **Survives:** layout, text, tables, images, charts (often re-rendered as Google charts or images),
  speaker notes.
- **Degrades:** **Morph** → Google Slides has no Morph; transitions simplify to fades. **Zoom**
  navigation does not import. Some fonts substitute — pick a Google-Fonts face in `design.fonts`
  (Assistant, Heebo for Hebrew) so the match is exact after conversion.
- For motion, offer the **HTML** build alongside; Google Slides is the right pick when the goal is
  **collaborative editing**, not animation.

## Deliver
The `.pptx` plus the one-line import instruction, or (Route B) the Google Slides link.
