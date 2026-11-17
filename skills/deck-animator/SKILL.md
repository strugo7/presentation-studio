---
name: deck-animator
description: "Method for planning presentation motion and interaction — staged reveals, Morph transitions (PPTX), Zoom/hub navigation, and how quizzes, polls, activities and demos behave in each format (with static fallbacks and reduced motion) — as format-agnostic intent in blueprint.json. Use after structure and design are set. Pairs with references/techniques.md and references/interaction-patterns.md."
---

# deck-animator — motion that serves the argument

Motion has two legitimate jobs: **segmenting** (reveal one idea at a time so the room isn't reading
ahead) and **continuity** (carry the eye between related moments). Anything else is distraction. You
write `animation` per slide and `navigation` for the deck, and check each `engagement` has a working path
in every requested format.

## References — open when
- `references/techniques.md` — for reveals, Morph, Section Zoom, living backgrounds (the recipes).
- `references/interaction-patterns.md` — whenever a slide has `engagement`, the deck has a hub, or the
  brief mentions accessibility / reduced motion; read only the pattern sections you need.

## 1. Reveals (every content slide with >1 idea)
Stage the slide so bullets/exhibit appear in step order via `animation.reveals`. One idea per click.
Pose-then-reveal: show the question/exhibit, let it land, then reveal the interpretation. Use reveal
tokens from the spec (`bullet:N`, `exhibit`, `title`, `block:ID`). **Reveals are built only in HTML**
(click-stepped). PPTX shows the whole slide, and PDF prints the final state.

A reveal step's `zoom` field is accepted by the schema, but **no builder reads it yet**. Region zoom
is not an available capability. To push the eye to one detail today:
- set `exhibit.data.highlight` (the bar or point drawn in `accent2`);
- reveal the interpretation bullet after the exhibit;
- or split into two slides: the full exhibit, then a crop of the detail as its own image.

## 2. Transitions (continuity between slides)
Give every motion a job:
- **Reveal** sets the order in which things appear.
- **Morph** shows a change in an object the audience already recognises.
- **Zoom** orients: it moves between the whole and a part.

([BrightCarbon on Morph](https://www.brightcarbon.com/blog/using-powerpoint-morph/); Apple HIG motion
and Material motion as principles for keeping context.)

- `morph` between two slides that **share objects** — a divider's big number shrinking into a corner, a
  title persisting, a chart growing. Require shared object identity: the PPTX builder gives the
  kicker, title, big number and section numeral the same name on every slide (`!!title`, `!!kicker`,
  `!!bignum`, `!!secnum`), so those match. Other shapes get unique names and won't morph into each other.
- `fade` as the quiet default; `none` sparingly. `push` is accepted but **built as a fade** in PPTX.

Set `animation.transition` per slide (it describes how you arrive *at* this slide). What each builder does
with it, as checked in the code:

| `transition` | PPTX | HTML | PDF |
|---|---|---|---|
| `morph` | real Morph (PowerPoint 2019/365), fade fallback for older apps | ignored: every slide change is the same camera flight | static |
| `fade` / `push` | fade | ignored (camera flight) | static |
| `none` / absent | no transition (`navigation.mode:"zoom"` turns on Morph for every slide after the first) | camera flight | static |

**Morph has a static twin.** A morph carries meaning ("the number moved into the corner because it's now
context"). In HTML, PDF and reduced motion it doesn't play, so put the same change into words on the
slide: a kicker or caption like "Same chart, June only", or the persisted title.

## 3. Zoom navigation (multi-section decks)
When `navigation.mode:"zoom"`: the `hubSlideId` is a map slide with a tile per section; each
`zoomTargets` entry is a section's opening slide. The presenter clicks a tile, the camera flies in,
plays the section, and returns to the map. See `references/techniques.md` for the exact PPTX
Section-Zoom recipe (zoom background on, return-to-zoom on) and the HTML camera equivalent.

## 4. Payoff motion
Each section usually has one "payoff" slide (the result/root/ask). Give it a touch more — a morph in,
a warm-accent reveal — so the rhythm has peaks. Don't animate everything equally; uneven is good.

## 5. Format reality (write it into your hand-off)
Checked against `shared/render_html.py` and `shared/render_pptx.py`. The single source is
presentation-studio/references/format-capabilities.md.
- **HTML engine.** Built:
  - camera-flight navigation between all slides (a smooth zoom-out/zoom-in arc);
  - agenda tiles that fly to their section, `M` back to the map, `O` for the overview;
  - click-stepped reveals;
  - photo backgrounds behind a scrim (static).

  **Not built:** per-slide transitions (`animation.transition` is ignored), shared-element Morph,
  exhibit region zoom (reveal `zoom`), video or Ken-Burns backgrounds.
- **PPTX:** Morph on `transition:"morph"` (and on every slide in zoom mode), fade for `fade`/`push`;
  no generated entrance animations (reveals). Morph + Section/Slide Zoom need PowerPoint 2019 /
  Microsoft 365; older/other apps show the fade fallback. Zoom *objects* can't be created by script —
  builders set up Sections + a map slide so it's a 2-click manual step, and leave instructions.
- **PDF:** static — every reveal shown, motion flattened to each slide's final state.
- **Keynote / Google Slides:** come from the PPTX; Morph→"Magic Move"/transitions survive import
  imperfectly; Zoom does not. Note this.

Keep reduced motion sane: never rely on motion to convey meaning that isn't also in the static slide
([MDN, prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)).
The HTML engine honours `prefers-reduced-motion` and `meta.accessibility.reducedMotion`: no camera
flight (instant jump), and reveals fade only. `R` or the Motion button toggles it. Set
`meta.accessibility.reducedMotion:true` when the brief asks. When motion carries a change (a morph, a
zoom into a part), add a label or cue that says the same thing, so a still slide or a PDF page
communicates it too.

## 6. Interaction behaviour (interaction-patterns.md)
- Quiz: confirm `answerPlacement` per format (live → `next-slide`, `self-read` → `inline`); add a reveal
  step so the question lands before the options.
- Poll: HTML tallies locally on one device; a real class poll needs an external tool — say so.
- Demo: a screenshot fallback always; a link if live.
- Flag anything a target format can't do so the orchestrator can tell the user.
