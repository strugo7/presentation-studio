---
name: deck-animator
description: "Method for planning presentation motion and interaction — staged reveals, Morph transitions, Zoom/hub navigation, and how quizzes, polls, activities and demos behave in each format (with static fallbacks and reduced motion) — as format-agnostic intent in blueprint.json. Use after structure and design are set. Pairs with references/techniques.md and references/interaction-patterns.md."
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
tokens from the spec (`bullet:N`, `exhibit`, `title`, `block:ID`). A reveal step may name a `zoom`
region on the exhibit to push the eye to the key detail (builders that support it honor it).

## 2. Transitions (continuity between slides)
- `morph` between two slides that **share objects** — a divider's big number shrinking into a corner, a
  title persisting, a chart growing. This is the single most powerful move; require shared object
  identity (builders name shared objects for you).
- `fade` as the quiet default; `push`/`none` sparingly.
Set `animation.transition` per slide (it describes how you arrive *at* this slide).

## 3. Zoom navigation (multi-section decks)
When `navigation.mode:"zoom"`: the `hubSlideId` is a map slide with a tile per section; each
`zoomTargets` entry is a section's opening slide. The presenter clicks a tile, the camera flies in,
plays the section, and returns to the map. See `references/techniques.md` for the exact PPTX
Section-Zoom recipe (zoom background on, return-to-zoom on) and the HTML camera equivalent.

## 4. Payoff motion
Each section usually has one "payoff" slide (the result/root/ask). Give it a touch more — a morph in,
a warm-accent reveal — so the rhythm has peaks. Don't animate everything equally; uneven is good.

## 5. Format reality (write it into your hand-off)
- **HTML engine:** does all of it natively — camera-flight zoom, staged reveals, exhibit region-zoom,
  looping video/photo backdrops, Morph-like shared-element transitions.
- **PPTX:** Morph + Section/Slide Zoom need PowerPoint 2019 / Microsoft 365; older/other apps show a
  fade fallback. Zoom *objects* can't be created by script — builders set up Sections + a map slide so
  it's a 2-click manual step, and leave instructions.
- **PDF:** static — motion is flattened to each slide's final state.
- **Keynote / Google Slides:** come from the PPTX; Morph→"Magic Move"/transitions survive import
  imperfectly; Zoom does not. Note this.
Keep `reduce-motion` sane: never rely on motion to convey meaning that isn't also in the static slide.
The HTML engine honours `prefers-reduced-motion` and `meta.accessibility.reducedMotion` (no camera
flight, fade-only reveals; `R` toggles). Set `meta.accessibility.reducedMotion:true` when the brief asks.

## 6. Interaction behaviour (interaction-patterns.md)
- Quiz: confirm `answerPlacement` per format (live → `next-slide`, `self-read` → `inline`); add a reveal
  step so the question lands before the options.
- Poll: HTML tallies locally on one device; a real class poll needs an external tool — say so.
- Demo: a screenshot fallback always; a link if live.
- Flag anything a target format can't do so the orchestrator can tell the user.
