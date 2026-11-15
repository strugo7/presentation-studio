---
name: presentation-studio
description: "Orchestrates a full presentation build from source material to finished files. Use whenever the user wants to create a presentation / deck / slides / talk from notes, docs, data, a paper, or just a topic — in HTML, PPTX, PDF, Keynote, or Google Slides. Runs the pipeline: sharpen the topic (grill-me) → plan structure (presentation-engineer) → design + write in parallel (deck-designer, deck-writer) → motion (deck-animator) → build the chosen formats. The agents collaborate through one shared blueprint.json."
---

# presentation-studio — the conductor

You coordinate specialists; you don't do their jobs. Everything flows through one **`blueprint.json`**
(contract: `shared/blueprint-spec.md`, schema: `shared/blueprint.schema.json`). Each stage reads the
whole blueprint and writes back only its own fields.

## The pipeline

```
 source material / topic
        │
   [0] intake ─ is the message sharp? ── no ──► grill-me ──► brief.json
        │ yes                                        │
   [1] presentation-engineer  ◄───────────────────── ┘
        │  (meta, narrative, sections, slide roles/titles/bullets/exhibits/engagement, notes)
        │  → ghost-deck test must pass; confirm outline with user if >10 slides
        ▼
   [2] deck-designer ───┐ (parallel)   [2] deck-writer
        │ (design,      │                   │ (final titles/bullets/captions/notes)
        │  backgrounds) │                   │
        └──────┬────────┘───────────────────┘
               ▼
   [3] deck-animator  (per-slide animation, navigation mode + zoom hub/targets)
               ▼
   [4] builders  ─ for each requested format: build-html / build-pptx / build-pdf /
                   build-keynote / build-google-slides  (all read the same blueprint.json)
               ▼
   [5] QA + deliver  (render, eyeball, fix, package, README)
```

## How to run it

0. **Intake.** Gather source material (read it all). Decide if the one message / audience / ask are
   sharp. If not, invoke the **grill-me** skill first and let it produce `brief.json`. If the user is
   already clear, skip it.

1. **Engineer.** Spawn the **presentation-engineer** agent with the brief + source material. It writes
   the structural blueprint and runs the ghost-deck test. For decks >10 slides or complex content,
   surface the outline (action titles in order) to the user and get a yes before continuing.

2. **Design + Write in parallel.** Spawn **deck-designer** and **deck-writer** at the same time (they
   touch disjoint fields — design/backgrounds vs. copy). Merge both returns into the blueprint.

3. **Animate.** Spawn **deck-animator** to add `animation` + `navigation`.

4. **Build.** For each format the user asked for, invoke the matching builder skill. All builders take
   the same `blueprint.json` and an output dir. Default to the format the deck is actually for (projector
   → PPTX or HTML; share link → HTML/PDF; collaborative edit → Google Slides via PPTX import).

5. **QA + deliver.** Each builder self-QAs (render to images, check overflow/RTL). Fix and re-render
   only what changed. Package the outputs (and a README per the build skills). Report what each format
   does and doesn't support (e.g. PPTX Zoom is a 2-click manual finish; PDF is static).

## Running the agents
In Claude Code, spawn each agent by name with the Task/Agent tool (`presentation-engineer`,
`deck-designer`, `deck-writer`, `deck-animator`). Give each: the path to `blueprint.json`, the paths to
`shared/` and its own skill, and the source material. Agents run in subagents so their file reads stay
out of your context; you keep the conclusions and the merged blueprint. If subagents aren't available,
run each stage inline by reading that agent's `.md` and following it — the pipeline is identical.

## Scale discipline
- Don't build before the outline is agreed (step 1). A wrong structure is the expensive mistake.
- One exhibit per slide; ~1 slide/minute; dark/light sandwich; end on the ask. The agents enforce these;
  you catch anything that slips.
- Keep the blueprint valid against the schema at every hand-off. A half-filled blueprint still renders.

## What each piece is
- **grill-me** — sharpen the topic (message/audience/ask) → `brief.json`.
- **presentation-engineer** — pedagogical structure → the skeleton of `blueprint.json`.
- **deck-designer** — visual system + backgrounds.
- **deck-writer** — on-slide copy + speaker notes.
- **deck-animator** — reveals, Morph, Zoom navigation.
- **build-\*** — render one format each from the blueprint.
