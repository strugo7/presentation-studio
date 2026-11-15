---
name: build-pdf
description: "Render a blueprint.json into a static PDF (one 16:9 page per slide, fonts embedded) — either from the HTML build or from the PPTX build. Use when the user wants a PDF of the deck to email, print, or submit."
---

# build-pdf

```bash
python shared/render_pdf.py blueprint.json out.pdf [assets_dir] --from=html --font=path.ttf   # clean, matches HTML deck
python shared/render_pdf.py blueprint.json out.pdf [assets_dir] --from=pptx                    # matches the PPTX deck
```

- **`--from=html`** (default): blueprint → print HTML → headless Chrome `--print-to-pdf`. Fonts are
  embedded in the HTML, so the PDF is self-contained and RTL-correct. Best when the deliverable is the
  web deck's look.
- **`--from=pptx`**: blueprint → PPTX → (LibreOffice `soffice` if installed, else `pptx_to_html` →
  Chrome) → PDF. Use when the PDF must mirror the PowerPoint file exactly.

## Dependencies
Google Chrome or Chromium (for either route). LibreOffice `soffice` optional (raises pptx-route
fidelity). No PowerPoint/Keynote needed.

## Notes
- PDF is **static** — all motion flattens to each slide's final (fully-revealed) state. That's expected.
- Verify page count == slide count and page size 1440×810pt (= 1920×1080px, 16:9). Spot-check RTL and
  that no exhibit is clipped.
- The two routes can differ (e.g. HTML omits a slide the deck chose to keep PPTX-only). Pick the one
  that matches what the user is handing in; you can produce both.
