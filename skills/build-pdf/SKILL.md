---
name: build-pdf
description: "Render a blueprint.json into a static PDF (one 16:9 page per slide, fonts embedded) — either from the HTML build or from the PPTX build. Use when the user wants a PDF of the deck to email, print, or submit."
---

# build-pdf

> **Paths.** This skill ships in the presentation-studio plugin. `shared/…` and `skills/…` paths are under
> `${CLAUDE_PLUGIN_ROOT}/` (in a plain checkout of the repo, the repo root); `references/…` is this skill's own
> folder. Write blueprints and builds in the user's project, never inside the plugin folder.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/render_pdf.py" blueprint.json out.pdf [assets_dir] --from=html --font=path.ttf   # clean, matches HTML deck
python3 "${CLAUDE_PLUGIN_ROOT}/shared/render_pdf.py" blueprint.json out.pdf [assets_dir] --from=pptx                    # matches the PPTX deck
```

- **`--from=html`** (default): blueprint → print HTML → headless Chrome `--print-to-pdf`. Fonts are
  embedded in the HTML, so the PDF is self-contained and RTL-correct. Best when the deliverable is the
  web deck's look.
- **`--from=pptx`**: blueprint → PPTX → (LibreOffice `soffice` if installed, else `pptx_to_html` →
  Chrome) → PDF. Use when the PDF must mirror the PowerPoint file exactly. Without LibreOffice the
  fallback drops native charts — prefer the html route then.
- Both routes print every reveal step, quiz answers (per `answerPlacement`) and the sources pages, so no
  evidence is hidden behind a click. The html route loses the least information.

## Capabilities
What this format does with each blueprint feature (layouts, charts, quizzes, polls, reveals, sources,
fonts, RTL) and its fallbacks: **`${CLAUDE_PLUGIN_ROOT}/skills/presentation-studio/references/format-capabilities.md`** — the
single matrix for all builders. Read the row for this format before telling the user what they'll get.

## Validate first
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/validate_blueprint.py" blueprint.json [assets_dir]
```

## Dependencies
Google Chrome or Chromium (for either route; set `CHROME_PATH` if it isn't on PATH; runs as root with
`--no-sandbox` automatically). LibreOffice `soffice` optional (raises pptx-route fidelity). No
PowerPoint/Keynote needed. The bundled font is embedded on both routes.

## Notes
- PDF is **static** — all motion flattens to each slide's final (fully-revealed) state. That's expected.
- Verify page count == slide count (including generated answer and sources pages) and page size
  1440×810pt (= 1920×1080px, 16:9). Check with `pdftotext` that reveal text, answers and sources are
  present; spot-check RTL and that no exhibit is clipped.
- The two routes can differ (e.g. HTML omits a slide the deck chose to keep PPTX-only). Pick the one
  that matches what the user is handing in; you can produce both.
