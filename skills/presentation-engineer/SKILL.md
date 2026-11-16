---
name: presentation-engineer
description: "Method for planning a presentation's pedagogical structure — analysing source material and its fact sheet, choosing a scaffold/playbook for the audience, writing a ghost-deck outline of action titles, choosing the right chart or diagram for each claim, attaching citations, and laying out slide roles, exhibits, engagement moments and navigation into blueprint.json. Use when turning notes/docs/data/a brief into a slide plan, or re-planning the same sources for a new audience, before any design or final copy."
---

# presentation-engineer — structure before slides

Structure is the deck. Colour and motion amplify a sound structure and can't rescue a broken one.
Produce the structural half of `blueprint.json`.

## References — open when
- `references/structure-frameworks.md` — Step 2, choosing a scaffold.
- `references/deck-playbooks.md` — Step 2, once you know the audience/delivery mode: open only the
  matching playbook (executive, investor, students, technical, self-read, demo).
- `references/pedagogy.md` — Steps 5–6, for teaching decks and engagement placement.
- `references/charts-and-diagrams.md` — Step 5, whenever a slide has numbers, a process, a protocol or a
  timeline; also before using a screenshot as evidence.
- `references/content-sources.md` — only when the brief needs public data or a standard the user didn't
  provide (statistics, ATT&CK techniques, published datasets).

## Step 1 — Absorb the material and the brief
Read everything provided before structuring. From the brief (or by asking): the **one sentence**, the
**audience** (who / expertise / goal), the **ask**, the **time box**, the **source material**, the
**language/RTL**. If the one sentence is still a topic label, stop and route back to grill-me — you
cannot architect an argument that doesn't exist yet.

Inventory the raw material from the fact sheet (presentation-studio/references/source-intake.md): what
claims, data points, figures, screenshots, quotes exist, and which are *fact*, *derived*, *disputed* or
*missing*? Tag each as *evidence* (supports a point) or *context* (sets up a point). Evidence becomes
exhibits; most context becomes one or two setup slides or speaker notes, not slides of its own. Never
plan a slide around a number that isn't in the fact sheet.

## Step 2 — Pick ONE scaffold (don't present a menu)
Diagnose from audience + goal, state your pick and why in one line, let the user correct. See
`references/structure-frameworks.md`. Quick map:

| Audience / goal | Scaffold |
|---|---|
| Senior, time-pressured, must decide | **Answer-first** (conclusion, then support) |
| Leadership buy-in on a recommendation | **The Case** (situation → tension → options → recommendation → evidence → risk → cost of inaction → ask) |
| Investors / partners / funding | **The Pitch** |
| Conference / public / shift thinking | **The Keynote** (conventional wisdom → crack → reframe → 3 beats → charge) or **Duarte sparkline** |
| Teaching a skill or framework | **The Workshop** (teach the method once, apply it repeatedly) |
| Progress update | **The Report-out** (headline → scorecard → wins → misses → insight → plan → ask) |
| Persuade to act, emotional | **Monroe's Motivated Sequence** |
| Research / analytical claim | **SCR / SCQA** (situation → complication → [question] → resolution) |

## Step 3 — Write the ghost deck FIRST
Before any slide body, write the ordered list of **action titles** — one full declarative sentence per
slide, each stating that slide's takeaway. Topic labels are forbidden ("Results" → "Effect holds in
all three cohorts"). Then apply the two tests:

- **Ghost-deck test:** read only the action titles, in order. They must tell the whole argument
  start to finish. If a gap appears, the structure is wrong — fix it here, where it's cheap.
- **Flow test:** each title should make the next feel inevitable. A title that could sit anywhere in
  the order, or that you can delete without the argument collapsing, is dead weight — cut it.

Only once the ghost deck passes do you fill in bodies.

## Step 4 — Size it to the clock
~1 content slide per minute (fewer for discussion-heavy). 10 min ≈ 8–10 content slides; 20 min ≈
15–18; 45 min ≈ 30–40. Add the fixed slides: cover, (agenda/map if long or zoom-navigated),
section dividers for >15 slides, conclusions, references/appendix. Mark 2–3 slides as "cut if short".

## Step 5 — Fill each slide (one job per slide)
For every slide set: `role`, `kicker`, `actionTitle`, ≤3 `bullets` (orientation cues, telegraphic,
one idea each), and the `exhibit` **plan** — type + which asset + where to draw the eye (`annotate`)
+ `side`. Rules that are non-negotiable (from `references/pedagogy.md` and the spec):
- **One exhibit per slide.** Cover the title — is the exhibit's point obvious? Cover the exhibit —
  does the title still stand? If not, strengthen one.
- **Signal the key point on the exhibit** (annotate), never make the room hunt.
- **≤ ~40 words** of body; split if more. Rebuild figures at presentation scale — don't plan to paste
  a tiny figure from a PDF.
- **Cite with `citations[]`**: every slide that states a fact gets `{sourceId, locator, kind}`. Use
  `kind:"derived"` for your conclusions and `"disputed"` where sources disagree. Builders print the
  footer and generate the sources slides; you don't hand-write a references slide unless the user wants one.
- **Choose the exhibit by relationship** (charts-and-diagrams.md): line for time, column/bar for
  categories, big number for one decisive figure, table for exact values, sequence/chain/timeline for
  processes. Give charts a `unit`, and a `highlight` for the point the title makes. Keep documentary
  screenshots and explanatory diagrams apart.
- **Exhibit role, not look.** You set `exhibit.type`, data and what it must show; the designer chooses
  `layout` and frame.

## Step 6 — Place engagement deliberately
From `references/pedagogy.md`: pick 1–3 engagement moments and attach them to specific slides via
`engagement` — a posed question at the hook, a poll/show-of-hands at a pivot, a short activity or live
demo where attention would otherwise dip (roughly every 8–10 minutes). Don't scatter; place with
intent. For a quiz define `options` (ids `a`, `b`, `c`…), `correctOptionId`, draft `feedback` per option
(the writer polishes), `presenterCue`, and `answerPlacement` (`next-slide` for live decks, `inline` for
`self-read`). A demo carries a screenshot (`assetRef`) and/or a `url` so it survives a dead network.
A poll in HTML is local to one device; if the room needs a real multi-device poll, say so in
`presenterCue` (an external tool is required).

## Step 7 — Navigation
Default `navigation.mode:"linear"`. Choose `"zoom"` when the deck has 3+ parallel modules or sections
the audience should be able to jump between — then set a `hubSlideId` (an `agenda`/map slide) and list
`zoomTargets` (each section's opening slide). The animator and builders turn this into real
Zoom/Morph navigation.

## Step 8 — Draft speaker notes & validate
Draft natural 2–4 sentence `speakerNotes` per slide (the writer will polish). Copy `sources[]` into the
blueprint. Validate: `python shared/validate_blueprint.py blueprint.json` (schema + every citation,
asset, section and quiz answer resolves). Hand off with: the chosen scaffold/playbook, the ghost-deck
title list, the slide count vs. time budget, open `missing` facts, and any gaps you had to assume. Do
not touch `design`/`layout`/`animation`/final prose.

## Re-planning for a new audience
Keep `sources[]` and the fact sheet. Pick the new playbook, rewrite the ghost deck, re-choose evidence
type and depth (worked example vs. decisive number vs. mechanism + measurement), move detail to or from
the appendix, and change the ask. No new results; any number on a slide still has its citation.
