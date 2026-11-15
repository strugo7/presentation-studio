---
name: build-google-slides
description: "Produce a Google Slides version of a deck. Google Slides has no offline file; it is created by uploading a PPTX to Google Drive and converting, or via the Slides API. This skill builds the PPTX and gives the import path (and an optional Apps Script). Use when the user wants an editable, collaborative Google Slides deck."
---

# build-google-slides

**Honest constraint:** a Google Slides deck lives in the user's Google account, not as a local file.
Two real routes; both start from the PPTX this studio builds (Google Slides imports `.pptx`).

## Build
```bash
python shared/render_pptx.py blueprint.json out.pptx [assets_dir]
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

## What survives, what to tell the user
- **Survives:** layout, text, tables, images, charts (often re-rendered as Google charts or images),
  speaker notes.
- **Degrades:** **Morph** → Google Slides has no Morph; transitions simplify to fades. **Zoom**
  navigation does not import. Some fonts substitute — pick a Google-Fonts face in `design.fonts`
  (Assistant, Heebo for Hebrew) so the match is exact after conversion.
- For motion, offer the **HTML** build alongside; Google Slides is the right pick when the goal is
  **collaborative editing**, not animation.

## Deliver
The `.pptx` plus the one-line import instruction, or (Route B) the Google Slides link.
