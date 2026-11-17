---
name: build-html
description: "Render a finished blueprint.json into a self-contained, animated HTML presentation (single index.html + assets): fixed 16:9 stage, camera-flight/zoom navigation, staged reveals, layouts, inline charts/tables/diagrams, live quizzes and local polls, sources and credits, embedded font (opens offline), reduced-motion support, RTL-aware. Use when the user wants an HTML/web deck or a browser-presented talk."
---

# build-html

> **Paths.** This skill ships in the presentation-studio plugin. `shared/…` and `skills/…` paths are under
> `${CLAUDE_PLUGIN_ROOT}/` (in a plain checkout of the repo, the repo root); `references/…` is this skill's own
> folder. Write blueprints and builds in the user's project, never inside the plugin folder.

HTML is the native home for this studio's motion: camera-flight navigation between slides (hub
tiles fly into their section), click-stepped reveals, local quiz feedback and reduced motion all run
in the browser with no dependencies.

Not built in HTML: per-slide `animation.transition` (every slide change is the camera flight),
shared-element Morph, exhibit region zoom (a reveal's `zoom` is ignored), and video or animated
backgrounds (photo backgrounds are static). See format-capabilities.md.

## Build
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/render_html.py" blueprint.json OUT_DIR [assets_dir] [--font=path.ttf]
```
- Produces `OUT_DIR/index.html` (self-contained: CSS + JS inline) and `OUT_DIR/assets/` (copied images).
- The bundled OFL font (`${CLAUDE_PLUGIN_ROOT}/shared/fonts/Assistant[wght].ttf`) is embedded automatically, so the deck opens
  offline and Hebrew never falls back; there is no CDN request. `--font=path.ttf` embeds a different font
  under the deck's display-font name; `--no-embed-font` skips embedding (system fonts only).
- Reads `design` (system tokens), per-slide `layout`, `navigation`, `animation.reveals`, `engagement`,
  `citations`, `sources`, `assets`, and every role/exhibit. Prints a warning for any asset it had to
  replace.

## Capabilities
What this format does with each blueprint feature (layouts, charts, quizzes, polls, reveals, sources,
fonts, RTL) and its fallbacks: **`${CLAUDE_PLUGIN_ROOT}/skills/presentation-studio/references/format-capabilities.md`** — the
single matrix for all builders. Read the row for this format before telling the user what they'll get.

## Validate first
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/validate_blueprint.py" blueprint.json [assets_dir]
```

## Deliver
Ship the whole `OUT_DIR` (extract before opening; keep `index.html` next to `assets/`). Opens by
double-click in Chrome / Edge / Safari / Firefox, offline. Controls: →/Space next step-or-slide, ←
back, **M** map, **O** overview, **N** speaker notes, **R** reduced motion, **F** fullscreen. Inside a
quiz, arrows/Enter/Space operate the options and never move the deck.

## QA (required)
Open it in a browser (or headless). Verify: no console errors, the cover + one evidence slide + the hub
render, reveals advance, charts match the data and units, a quiz answers without advancing, the sources
page lists every citation, RTL and mixed Hebrew/English read correctly. `tests/js/interaction_check.js`
automates the quiz/poll/reduced-motion/offline checks. Fix and re-render.

## Notes
- It's the only target that realises the full animation plan natively; the others degrade (see each).
- For a print/PDF of the same deck, hand the same blueprint to **build-pdf** (html route).
- Credits come from `assets[]` (footer of the slide that uses the image + the generated sources page).
