# The Blueprint — the one contract every agent and builder shares

`blueprint.json` is the single source of truth for a deck. It is **format-agnostic**:
the same blueprint renders to HTML, PPTX, PDF, Keynote or Google Slides. Agents fill in
different parts of it; builders only ever read it. If a field is missing, builders fall back
to a sane default — the blueprint is always renderable, even half-filled.

**Who writes what**

| Field group | Owner |
|---|---|
| `meta`, `narrative`, `sections`, each slide's `role` / `actionTitle` / `bullets` / `exhibit` / `engagement` / `speakerNotes` | **presentation-engineer** |
| `design`, each slide's `background`, `dark` | **deck-designer** |
| each slide's `animation`, `navigation` | **deck-animator** |
| final wording of `actionTitle` / `bullets` / `speakerNotes`, `meta.title` | **deck-writer** |
| `assets` | whoever introduces an image (engineer references, designer sources) |

Every agent **reads the whole blueprint and writes back only its fields.** Never drop another
agent's fields. Validate against `blueprint.schema.json` before handing off.

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
    "audience": { "who": "string", "expertise": "expert|informed|lay", "goal": "decide|learn|buy-in|inspire" }
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
    "gridBackground": true
  },

  "sections": [
    { "id": "s_intro", "title": "פתיח", "slideIds": ["cover","stakes","method"] }
  ],

  "slides": [ /* see below */ ],

  "navigation": { "mode": "linear|zoom", "hubSlideId": "map", "zoomTargets": ["vnc_open","smb_open"] },

  "assets": [ { "id":"scan1", "path":"assets/scan.png", "kind":"screenshot", "credit":"" } ]
}
```

## A slide

```jsonc
{
  "id": "vnc_identify",
  "section": "s_vnc",
  "role": "cover|stakes|agenda|divider|concept|evidence|process|comparison|quote|close|references|appendix",
  "dark": false,                         // dark background slide (dividers, cover, close, stakes)

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
    "side": "left"                        // figure side; text goes opposite
  },

  "background": { "kind": "grid|solid|navy|photo", "photo": "assets/door.jpg", "scrim": true },

  "engagement": { "type": "none|question|poll|activity|demo|quiz", "prompt": "" },

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
reveal step names a region to zoom the exhibit to (builders that support it honor it; others ignore).

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
6. **End on conclusions**, never on "Thank You" / blank. A `references` slide exists if anything is cited.
7. **Language + RTL** come from `meta`; every text run is tagged with the language so renderers pick a script-correct font.
