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
- Or say it in words. The **presentation-studio** skill orchestrates; it calls the agents and builders.

### Examples
**Mixed input** — notes, a spreadsheet, a screenshot and a web page, one deck:
```
/new-deck 15-minute Hebrew talk for first-year students on phishing awareness.
Sources: notes.md, results.csv (sheet = campaign results), dashboard.png, https://attack.mitre.org/techniques/T1566/
```
Every source becomes a `sources[]` record; every number on a slide carries a citation (`Sheet!A1:C9`,
page, timestamp), and the deck ends with generated **Sources & credits** slides.

**Same sources, new audience** — the facts stay, the sequence, depth, evidence and ask change:
```
Now cut the same material for management: decision first, one number, options and risks, 6 slides.
```

**Choose a visual direction** — composition, type and rhythm change, not just colours:
```
Show me two directions for this deck, then build the executive-data-briefing one.
(other directions: editorial-report, product-demo, classroom-workshop, keynote, technical-case)
```

**Export to two formats**:
```
Build it as HTML (with the quiz live) and PPTX; also give me a PDF handout.
```

## Run a builder directly (no agents, just render a blueprint)
```bash
python shared/render_html.py blueprint.json out_html   --font=/path/Assistant.ttf
python shared/render_pptx.py blueprint.json out.pptx
python shared/render_pdf.py  blueprint.json out.pdf     --from=html   # or --from=pptx
```
Try it on the included examples:
```bash
python shared/validate_blueprint.py examples/features-blueprint.json          # schema + cross-references
python shared/render_pptx.py examples/sample-blueprint.json /tmp/demo.pptx examples
python shared/render_html.py examples/sample-blueprint.json /tmp/demo_html examples
python shared/render_html.py examples/features-blueprint.json /tmp/feat_html examples   # Hebrew, every new field
python shared/render_pdf.py  examples/features-blueprint.json /tmp/feat.pdf examples
```
`examples/mixed-sources/` holds two Hebrew decks built from one mixed source set (students vs.
management) — see its README.

## What each format gives you
| Format | Native? | Interaction & motion | Best for |
|---|---|---|---|
| **HTML** | yes (self-contained, offline) | camera zoom, reveals, live quiz feedback, local poll, reduced motion | browser-presented talks, sharing a link |
| **PPTX** | yes (editable, native charts) | Morph; quiz → linked answer slides; Zoom = 2-click manual finish | PowerPoint users, editing, projector |
| **PDF** | yes (static, fonts embedded) | every reveal + answers printed | email / print / submission |
| **Keynote** | via PPTX import | Morph→Magic Move (imperfect); no Zoom | Mac/Keynote users |
| **Google Slides** | via PPTX upload-and-convert | fades only | collaborative editing |

The full, maintained capability matrix (layouts, charts, quizzes, polls, sources, fonts, RTL, fallbacks)
is **`skills/presentation-studio/references/format-capabilities.md`**.

RTL / Hebrew is first-class: the renderers set the complex-script font + language on every run (the fix
for the "boxes" bug), embed an OFL Hebrew font (bundled in `shared/fonts/`), keep numbers and units in
order, and lay out right-to-left.

## The pieces
- `skills/presentation-studio` — the conductor (`references/source-intake.md`,
  `references/format-capabilities.md`).
- `skills/grill-me` — Socratic topic sharpening → `brief.json` (`references/brief-and-audience.md`).
- `agents/presentation-engineer` + `skills/presentation-engineer` — structure, pedagogy, evidence
  (`structure-frameworks.md`, `deck-playbooks.md`, `pedagogy.md`, `charts-and-diagrams.md`,
  `content-sources.md`).
- `agents/deck-designer` + `skills/deck-designer` — visual direction, layouts, assets
  (`design-systems.md`, `layout-patterns.md`, `design-gallery.md`, `asset-sources.md`).
- `agents/deck-writer` + `skills/deck-writer` — copy (`writing-rules.md`, `audience-voice-and-citations.md`).
- `agents/deck-animator` + `skills/deck-animator` — motion & interaction (`techniques.md`,
  `interaction-patterns.md`).
- `skills/build-*` — one builder per format.
- `shared/` — the blueprint contract (`blueprint-spec.md`, `blueprint.schema.json`), the shared library
  (`blueprint_lib.py`: validation, assets, sources, tokens, charts, merge), `validate_blueprint.py`, the
  renderers (`render_html.py`, `render_pptx.py`, `render_pdf.py`, `pptx_to_html.py`,
  `pptx_to_keynote.applescript`) and `fonts/` (Assistant, SIL OFL).
- `examples/sample-blueprint.json` — the original 6-slide deck (kept working unchanged).
- `examples/features-blueprint.json` — a Hebrew fixture exercising every newer field.
- `examples/mixed-sources/` — one mixed source set → two decks for two audiences.

## Tests
```bash
python -m unittest discover tests -v
```
Contract (schema, back-compat, cross-references, asset names, merge, charts) and renderer tests (HTML,
PPTX, chart parity, no text overlaps). If `node` + Playwright are present, a headless check drives the
quiz with the keyboard, the local poll, reduced motion and offline loading; if Chrome + `pdftotext` are
present, the PDF is checked for reveal text, answers and sources. Missing tools skip those tests.

## Dependencies
`python-pptx`, `Pillow` (PPTX); Google Chrome/Chromium (PDF; optional LibreOffice for the pptx→pdf
route); `jsonschema` (optional, schema validation). The Assistant font ships in `shared/fonts/` and is
embedded in HTML automatically; install it (or another Hebrew font) on machines that open the PPTX.
Node + Playwright are only used by the optional interaction test. See `requirements.txt`.

## Credits & sources
Structure/pedagogy synthesised from Figma's *60 presentation ideas*, NIU's *Effective Presentation
Skills Tutorial*, the Minto Pyramid/SCQA, Monroe's Motivated Sequence, Duarte's sparkline,
assertion-evidence (Alley), and Mayer/Gagné multimedia-learning research. Animation technique library
distilled from **One Skill PPT** (youtube.com/@oneskill_ppt). Design references draw on
`zarazhangrui/frontend-slides` and the curated skill list at tosea.ai; writing rules adapt the
`Gabberflast/academic-pptx-skill`. Chart choice follows the FT Visual Vocabulary and Datawrapper's
guidance; design references are catalogued with links (not copies) and an honest verification status in
`skills/deck-designer/references/design-gallery.md` (none verified yet: the build environment blocked those sites). Each reference file names its sources. Font:
Assistant, © The Assistant Project Authors, SIL Open Font License 1.1 (`shared/fonts/OFL.txt`).

MIT licensed.
