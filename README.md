# presentation-studio

A reusable Claude Code plugin that turns source material into a finished presentation — **HTML, PPTX,
PDF, Keynote, or Google Slides** — through a small team of specialist agents that collaborate over one
shared `blueprint.json`.

It is opinionated about the thing that actually makes a deck good: **structure and pedagogy first**,
design and motion second. A Socratic skill (`grill-me`) makes sure the idea is sharp before a single
slide exists.

```
 topic / source material
        │
   grill-me ............ sharpen the one message, the audience, the ask  → brief.json
        │
   presentation-engineer  pedagogy + narrative scaffold → ghost-deck of action titles → structure
        │
   deck-designer  ┐ (parallel)   deck-writer
   (visual system)│               (on-slide copy + speaker notes)
        └─────────┴──► deck-animator  (reveals, Morph, Zoom navigation)
                           │
                   builders ──► HTML · PPTX · PDF · Keynote · Google Slides
```

Everything flows through **one contract**, `shared/blueprint-spec.md` + `blueprint.schema.json`, so a
blueprint renders to every format and any stage can be re-run without redoing the others.

## Install (Claude Code)
Add this repo as a plugin marketplace, then enable the plugin:
```
/plugin marketplace add <path-or-git-url-to-this-repo>
/plugin install presentation-studio
```
Or drop the `skills/`, `agents/`, and `commands/` folders into a project's `.claude/`.

## Use
- `/new-deck <what you want + point me at the source files>` — runs the whole pipeline.
- `/grill-me <your rough topic>` — just sharpen the idea first.
- Or say it in words: *"make a 15-minute PPTX + HTML from these notes for a lay audience."*
  The **presentation-studio** skill orchestrates; it calls the agents and builders for you.

## Run a builder directly (no agents, just render a blueprint)
```bash
python shared/render_html.py blueprint.json out_html   --font=/path/Assistant.ttf
python shared/render_pptx.py blueprint.json out.pptx
python shared/render_pdf.py  blueprint.json out.pdf     --from=html   # or --from=pptx
```
Try it on the included example:
```bash
python shared/render_pptx.py examples/sample-blueprint.json /tmp/demo.pptx examples
python shared/render_html.py examples/sample-blueprint.json /tmp/demo_html examples
```

## What each format gives you
| Format | Native? | Motion | Best for |
|---|---|---|---|
| **HTML** | yes (self-contained) | full: camera-zoom, reveals, living bg | web / browser-presented / the "wow" build |
| **PPTX** | yes (editable, native charts) | Morph + Zoom (Zoom = 2-click manual finish) | PowerPoint users, editing, projector |
| **PDF** | yes (static, fonts embedded) | flattened to final state | email / print / submission |
| **Keynote** | via PPTX import (AppleScript on macOS) | Morph→Magic Move (imperfect); no Zoom | Mac/Keynote users |
| **Google Slides** | via PPTX upload-and-convert | fades only; no Morph/Zoom | collaborative editing |

RTL / Hebrew is first-class: the renderers set the complex-script font + language on every run (the fix
for the "boxes" bug), embed the font, and lay out right-to-left.

## The pieces
- `skills/grill-me` — Socratic topic sharpening → `brief.json`.
- `agents/presentation-engineer` + `skills/presentation-engineer` — structure & pedagogy
  (`references/structure-frameworks.md`, `references/pedagogy.md`).
- `agents/deck-designer` + `skills/deck-designer` — visual system (`references/design-systems.md`).
- `agents/deck-animator` + `skills/deck-animator` — motion (`references/techniques.md`).
- `agents/deck-writer` + `skills/deck-writer` — copy (`references/writing-rules.md`).
- `skills/build-*` — one builder per format.
- `shared/` — the blueprint contract, schema, and the renderers (`render_html.py`, `render_pptx.py`,
  `render_pdf.py`, `pptx_to_html.py`, `pptx_to_keynote.applescript`).
- `examples/sample-blueprint.json` — a 6-slide deck that exercises every exhibit type.

## Dependencies
`python-pptx`, `Pillow` (PPTX); Google Chrome/Chromium (PDF; optional LibreOffice for the pptx→pdf
route); a Hebrew-capable font such as **Assistant** installed/embedded for Hebrew decks. Node is not
required. See `requirements.txt`.

## Credits & sources
Structure/pedagogy synthesised from Figma's *60 presentation ideas*, NIU's *Effective Presentation
Skills Tutorial*, the Minto Pyramid/SCQA, Monroe's Motivated Sequence, Duarte's sparkline,
assertion-evidence (Alley), and Mayer/Gagné multimedia-learning research. Animation technique library
distilled from **One Skill PPT** (youtube.com/@oneskill_ppt). Design references draw on
`zarazhangrui/frontend-slides` and the curated skill list at tosea.ai; writing rules adapt the
`Gabberflast/academic-pptx-skill`. Each reference file names its sources.

MIT licensed.
