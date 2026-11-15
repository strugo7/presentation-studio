---
name: build-html
description: "Render a finished blueprint.json into a self-contained, animated HTML presentation (single index.html + assets): fixed 16:9 stage, camera-flight/zoom navigation, staged reveals, inline charts/tables/diagrams, embedded font, RTL-aware. Use when the user wants an HTML/web deck or a browser-presented talk."
---

# build-html

HTML is the native home for this studio's motion — camera-flight zoom, staged reveals, exhibit
region-zoom, living backgrounds all run in the browser with no dependencies.

## Build
```bash
python shared/render_html.py blueprint.json OUT_DIR [assets_dir] [--font=path.ttf]
```
- Produces `OUT_DIR/index.html` (self-contained: CSS + JS inline) and `OUT_DIR/assets/` (copied images).
- `--font=path.ttf` embeds a font as base64 so the deck needs no install and never falls back — **do
  this for Hebrew/RTL or any non-system font** (e.g. Assistant). Without it, the deck pulls Assistant
  from Google Fonts (needs network on first open).
- Reads `design`, `navigation` (linear vs zoom), per-slide `animation.reveals`, and every role/exhibit.

## Deliver
Ship the whole `OUT_DIR` (extract before opening; keep `index.html` next to `assets/`). Opens by
double-click in Chrome / Edge / Safari / Firefox, offline. Controls: →/Space next step-or-slide, ←
back, **M** map, **O** overview, **N** speaker notes, **F** fullscreen.

## QA (required)
Serve it (`python -m http.server`) and open in a browser; or headless-check the DOM. Verify: no
console errors, the cover + one evidence slide + the hub render, reveals advance, RTL reads correctly.
Fix and re-render.

## Notes
- It's the only target that realises the full animation plan natively; the others degrade (see each).
- For a print/PDF of the same deck, hand the same blueprint to **build-pdf** (html route).
- Credit any Unsplash/photographer in `assets[].credit`; the close slide shows credits.
