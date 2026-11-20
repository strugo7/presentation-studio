# The Blueprint — the one contract every agent and builder shares

`blueprint.json` is the single source of truth for a deck. It is **format-agnostic**:
the same blueprint renders to HTML, PPTX, PDF, Keynote or Google Slides. Agents fill in
different parts of it; builders only ever read it. If a field is missing, builders fall back
to a sane default — the blueprint is always renderable, even half-filled.

**Who writes what**

| Field group | Owner |
|---|---|
| `meta` (incl. `audience.profile`, `deliveryMode`, `tone`, `accessibility`), `narrative`, `sections`, `sources[]`, each slide's `role` / `section` / `exhibit` (type, data, ref, `bigNumber`) / `engagement` (type, options, `correctOptionId`, `answerPlacement`) / `citations` / draft `speakerNotes` | **presentation-engineer** |
| `design` (system, palette, fonts, motif, `tokens`, `variant`), each slide's `layout` / `background` / `dark`, visual `assets[]` (path, provider, licence, credit, fallbackPath) | **deck-designer** |
| each slide's `animation`, deck `navigation` | **deck-animator** |
| final wording of `actionTitle` / `kicker` / `bullets` / `speakerNotes` / `exhibit.caption`, `engagement.prompt` / `feedback` / `presenterCue`, `assets[].alt`, `meta.title` / `subtitle` | **deck-writer** |

Every agent **reads the whole blueprint and writes back only its fields.** Never drop another
agent's fields. When stages run in parallel, the orchestrator combines them with
`blueprint_lib.merge(base, {"designer": bp_d, "writer": bp_w})`, which applies only each stage's own
fields. Validate at every hand-off:

```bash
python shared/validate_blueprint.py blueprint.json [assets_dir]   # schema + cross-references
```
It checks: every `citations[].sourceId` resolves to one `sources[]` entry; every image `exhibit.ref`,
`background.assetRef`, `engagement.assetRef` resolves to `assets[]`; `sections[].slideIds` and
`slide.section` agree; `correctOptionId` is one of the options; chart series match their categories;
`navigation` ids exist; URLs are http(s). Warnings flag missing units/credits and overlong text.

---

## Top-level shape

```jsonc
{
  "meta": {
    "title": "string",            // the deck's claim or question, not a topic label
    "subtitle": "string",
    "authors": ["string"],
    "event": "string",            // course / conference / meeting
    "date": "YYYY-MM-DD",
    "language": "he" | "en" | "...",
    "rtl": true,                  // right-to-left layout
    "aspect": "16:9" | "4:3",
    "durationMinutes": 20,
    "audience": { "who": "string", "expertise": "expert|informed|lay", "goal": "decide|learn|buy-in|inspire",
                  // optional, free text (older blueprints without these keep working; profile defaults to who)
                  "profile": "string", "priorKnowledge": "string", "motivation": "string", "convincingEvidence": "string" },
    "deliveryMode": "live-talk|pitch|demo|workshop|exec-briefing|research|self-read",   // optional
    "tone": "string",                                                                   // optional, free text
    "accessibility": { "reducedMotion": false, "highContrast": false, "minFontPt": 20 }, // optional
    "autoSources": true,          // append generated "Sources & credits" slides (default true)
    "sourcesPerSlide": 7          // split long source lists across slides
  },

  "narrative": {
    "scaffold": "workshop|pitch|case|keynote|report|close|SCR|funnel|answer-first|sparkline|monroe",
    "throughline": "one sentence the whole deck proves",
    "ask": "the single action/belief the audience should leave with"
  },

  "design": {
    "system": "signal|cobalt-grid|swiss|editorial|mono|custom",   // see deck-designer
    "palette": { "bg":"FFFFFF","bgAlt":"F6F7F9","ink":"1A2230","mute":"5B6472",
                 "accent":"2C5F7C","accent2":"B4722E","hair":"E2E5EA","dark":"1C2A3A" },
    "fonts":   { "display":"Assistant","body":"Assistant","mono":"JetBrains Mono" },
    "motif":   "faint graph grid + big section numbers",
    "gridBackground": true,
    "variant": "free text: how this deck departs from its preset",       // optional
    "tokens":  { "titleScale": 1.1, "motif": "rule" },                    // optional per-deck overrides
    "logo":    { "assetRef": "brand_logo", "assetRefOnDark": "brand_logo_light",   // optional brand logo:
                 "height": 84, "aspect": 1.1, "opacity": 0.9, "skipRoles": [] }    // bottom corner at the end of
  },                                                                               // the reading direction, every slide

  "sources": [                    // optional: everything the deck's claims rest on
    { "id": "rfc8446", "title": "RFC 8446 …", "shortTitle": "RFC 8446",
      "kind": "text|markdown|pdf|docx|pptx|sheet|csv|image|web|transcript|dataset|other",
      "url": "https://…",  "file": { "name": "latency.csv", "path": "sources/latency.csv" },
      "creator": "IETF", "publishedAt": "2018-08", "accessedAt": "2026-11-16",
      "license": "…", "licenseUrl": "https://…", "notes": "" }
  ],

  "sections": [
    { "id": "s_intro", "title": "פתיח", "slideIds": ["cover","stakes","method"] }
  ],

  "slides": [ /* see below */ ],

  "navigation": { "mode": "linear|zoom", "hubSlideId": "map", "zoomTargets": ["vnc_open","smb_open"] },

  "assets": [ { "id":"scan1", "path":"assets/scan.png", "kind":"screenshot", "credit":"",
                // optional provenance (designer fills these when sourcing an image)
                "provider":"unsplash|pexels|wikimedia|openverse|smithsonian|nasa|user|original|…",
                "sourceUrl":"https://…", "creator":"…", "license":"…", "licenseUrl":"https://…",
                "alt":"what the image shows, for screen readers", "fallbackPath":"assets/scan.png",
                "usedIn":["slide ids"] } ]
}
```

## A slide

```jsonc
{
  "id": "vnc_identify",
  "section": "s_vnc",
  "role": "cover|stakes|agenda|divider|concept|evidence|process|comparison|quote|close|references|appendix",
  "dark": false,                         // dark background slide (dividers, cover, close, stakes)
  "layout": "statement|split|full-exhibit|big-number",   // optional composition; absent = by role (below)

  "kicker": "VNC · זיהוי",               // small eyebrow label
  "actionTitle": "פורט 5900 פתוח, פרוטוקול 3.3",   // a full sentence stating the takeaway (NOT a topic label)
  "bullets": [                            // max 3; each is { text, lead?, mono?, warm? }
    { "text": "nmap נתן את הגרסה המדויקת", "lead": "הגרסה היא החוט" }
  ],

  "exhibit": {                            // at most ONE per slide
    "type": "screenshot|image|chart|diagram|table|code",
    "ref": "scan1",                       // assets[].id, or inline data for chart/table
    "caption": "nmap -p 5900 · VNC protocol 3.3",
    "annotate": "highlight the 'protocol 3.3' line",   // where to draw the eye
    "side": "left",                       // figure side; text goes opposite
    "alt": "text alternative",            // optional; else assets[].alt
    "assetRefs": ["iconA"],               // optional: assets embedded inside a diagram (credit still tracked)
    "device": "laptop|phone|tablet|browser|none",   // optional: generic device frame around the screenshot (designer)
    "devices": [ { "device": "phone", "ref": "ios", "label": "iOS" },
                 { "device": "phone", "ref": "android", "label": "Android" } ],   // optional: ≤ 3 screens, each framed
    "arrangement": "row|overlap",         // devices side by side, or the 2nd over the 1st's front start corner
    "loupe": { "x": 0.6, "y": 0.1, "w": 0.2, "h": 0.15 },   // optional: round magnifier over a region (fractions)
    "url": "app.example.com",             // optional: text in a browser frame's address bar (display only)
    "bigNumber": { "value": "−46.5%", "unit": "", "context": "what, where, when" }   // for layout big-number
  },

  "citations": [                          // optional: which sources back this slide
    { "sourceId": "rfc8446", "locator": "§2, Figure 1 | p.4 | slide 7 | Sheet1!A1:C9 | 12:40",
      "claim": "optional: the specific claim", "kind": "fact|derived|disputed" }
  ],

  "background": { "kind": "grid|solid|navy|photo", "photo": "assets/door.jpg", "assetRef": "door", "scrim": true },

  "engagement": { "type": "none|question|poll|activity|demo|quiz", "prompt": "",
                  "options": [ { "id": "a", "text": "…" } ],     // optional
                  "correctOptionId": "a",                         // quiz with a right answer
                  "feedback": { "a": "why a is right", "b": "why not b", "correct": "…", "incorrect": "…" },
                  "presenterCue": "what the presenter does here", // appended to speaker notes
                  "answerPlacement": "next-slide|appendix|inline", // static formats (PPTX/PDF)
                  "url": "https://… (demo)", "assetRef": "screenshot id (demo)" },

  "animation": {
    "transition": "none|fade|morph|push",
    "reveals": [ { "step": 1, "show": ["bullet:0"] }, { "step": 2, "show": ["exhibit"], "zoom": "annotate" } ],
    "notes": "morph the kicker+title from the divider; stagger bullets"
  },

  "speakerNotes": "what the presenter actually says, 2-4 natural sentences"
}
```

### Reveal tokens (used by `animation.reveals[].show`)
`bullet:N` · `exhibit` · `title` · `kicker` · `block:ID` (any element given an id). `zoom` on a
reveal step names a region to zoom the exhibit to. It is reserved: **no builder reads it yet**, so
use `exhibit.data.highlight` or a second, cropped slide instead. `transition` is honoured by the PPTX
builder (`morph` → Morph with fade fallback; `fade`/`push` → fade). The HTML builder ignores it and uses
its camera flight for every slide change.

### Chart and diagram data (`exhibit.data`)
```jsonc
// chart — one spec, rendered identically by HTML (SVG) and PPTX (native, editable chart)
{ "kind": "column|bar|line|scatter", "categories": ["W1","W2"],
  "series": [ { "name": "TLS 1.3", "values": [121.4, 104.2] } ],     // scatter: "points": [[x,y,"label?"], …]
  "unit": "ms", "decimals": 1, "yLabel": "milliseconds", "xLabel": "", "title": "",
  "highlight": 1,          // index or category name: the one bar/point to draw the eye to
  "yMin": null }           // line only; bars/columns always start at zero
// any other kind (pie, area, …) renders as a table so no format shows a wrong chart
// diagram
{ "kind": "chain", "steps": ["A","B","C"] }
{ "kind": "timeline", "events": [ { "when": "2017", "label": "…" } ] }
{ "kind": "sequence", "actors": ["Client","Server"],
  "messages": [ { "from": "Client", "to": "Server", "label": "ClientHello", "emphasis": false } ] }
```

### Layouts (`slide.layout`, optional; implemented in HTML and PPTX)
- `statement` — one sentence carries the slide (light or dark); bullets become supporting lines.
- `split` — half the slide is the exhibit (a photo bleeds and crops; screenshots/charts sit whole on
  a tinted panel); the other half holds kicker, title, bullets, engagement. `exhibit.side` picks the half.
- `full-exhibit` — small header, the exhibit takes the full width; bullets collapse to one line under it.
- `big-number` — `exhibit.bigNumber` huge, its context line, then the title as the claim.

### Design-system tokens (`design.system`)
`blueprint_lib.SYSTEM_TOKENS` turns a system into composition, not only colour: title scale and
weight, cover alignment, background motif (`grid` · `none` · `rule` running head · `numbers`
section numerals), exhibit frame (`card` · `hairline` · `bleed`), margins, kicker style. Presets:
`signal`, `cobalt-grid`, `swiss`, `editorial`, `mono` (+ `custom`). Directions layered on them:
`editorial-report`, `product-demo`, `executive-data-briefing`, `classroom-workshop`, `keynote`,
`technical-case` (see deck-designer/references/design-systems.md). `design.tokens` overrides any token.

### Generated slides
Builders add, without touching the blueprint: a **Sources & credits** section built from `sources[]`
and credited `assets[]` (numbered by first citation; duplicate credits merged with the slide numbers
that use them; split across slides), and — in PPTX/PDF, where live feedback is impossible — an
**answer slide** for each quiz per `answerPlacement` (`self-read` decks default to `inline`).
Hand-written `references` slides are kept as they are.

### Roles → default layout (builders map these)
- `cover` / `close` / `divider` / `stakes` / `quote` → dark, centered statement, optional photo.
- `agenda` → the navigation map (zoom hub when `navigation.mode=zoom`).
- `concept` → text-led, optional small figure.
- `evidence` → one exhibit on `side`, interpretation opposite (figure-left by default).
- `process` → numbered steps / chain.
- `comparison` → table or side-by-side.
- `references` / `appendix` → list; appendix clearly labeled.

---

## Hard rules builders and agents both honor
1. **One exhibit per slide.** Two exhibits → split into two slides.
2. **Action titles, not topic labels.** "Results" → "Treatment effect holds across all cohorts".
3. **≤ 3 bullets**, ≤ ~40 words of body text per content slide. Overflow → split.
4. **Body ≥ 20pt** (PPTX) / ≥ 28px at 1920 (HTML). If it doesn't fit, cut words — never shrink below the floor.
5. **Dark slides** for cover, dividers, stakes, close only; light for content ("sandwich").
6. **End on conclusions**, never on "Thank You" / blank. Cited material is listed: through `sources[]`
   + `citations[]` (preferred; builders generate the sources slides) or a hand-written `references` slide.
7. **Language + RTL** come from `meta`; every text run is tagged with the language so renderers pick a script-correct font.
8. **Facts are traceable.** A number, quote or result on a slide has a `citations[]` entry; a derived
   figure says `"kind": "derived"`; contested material says `"disputed"` and the copy says so.
9. **Same data, same picture.** HTML and PPTX read one chart spec (`blueprint_lib.chart_spec`), so
   values, units, categories and series names match across formats.
