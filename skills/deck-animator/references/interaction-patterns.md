# Interaction patterns — what each engagement does in each format

Open this when a slide has `engagement` (question, poll, quiz, activity, demo) or the deck uses a hub
or map, and when setting motion for accessibility. The engineer defines the interaction (type,
options, correct answer). The writer words it. You decide how it behaves and make sure every format
has a working path. The full matrix lives in presentation-studio/references/format-capabilities.md.

---

## 1. Quiz (`type: quiz`, `options`, `correctOptionId`, `feedback`)
**HTML (built in):**
- **Controls.** Options are real radio buttons in a `radiogroup`.
- **Keys.** ↑/↓ (and ←/→ by reading direction) move between options. Enter or Space chooses. Inside
  the quiz these keys never advance the slide; deck keys work again once focus leaves it.
- **Feedback.** Shown immediately in an `aria-live` line, specific to the option chosen. "Reveal
  answer" marks the correct option and moves focus to it.
- **Offline.** Everything runs locally: no network, no account.

**PPTX:**
- **Answer slide.** Each option is a shape hyperlinked to a generated answer slide, which carries
  the correct option, the explanation and a "back to the question" link.
- **Placement.** `answerPlacement` decides where the answer goes: `next-slide` (live default),
  `appendix` (answers at the end), or `inline` (answer printed on the question slide; `self-read`
  default).
- **Presenter cue.** `presenterCue` goes into the notes.

**PDF / Keynote / Slides:**
- **PDF.** Static question page, then the answer per `answerPlacement`.
- **Keynote / Slides.** Links usually survive the import; check them.

**Timing.**
- Place a quiz right after a worked example. Let the room answer before revealing.
- One quiz per 8–10 minutes in a workshop; none in an executive briefing.

## 2. Poll (`type: poll`, `options`, no correct answer)
- **HTML:** a **local** tally on the presenting device: click an option once per raised hand, and the
  bars and counts update. It is labelled "local poll". It is not a multi-device classroom poll. That
  needs a collection service (Mentimeter, Slido, Forms…); put the link in `presenterCue` or a `demo`
  `url`.
- **PPTX / PDF:** static options. The presenter counts hands; the cue goes in the notes.

## 3. Question / activity (`type: question | activity`, prompt only)
- **All formats:** a prompt card on the slide.
- **Pacing.** Pair it with a reveal step: show the question first, then the next step reveals the
  idea.
- **Activity timing.** For an activity, put the duration and instructions in `presenterCue`.

## 4. Demo (`type: demo`, `url`, `assetRef`)
- **Fallback first.** Always give a screenshot (`assetRef`) so a dead network doesn't kill the talk.
  Add the `url` if a live demo is planned.
- **HTML:** screenshot plus a safe link (http/https only; opens in a new tab with `rel=noopener`).
- **PPTX:** screenshot plus a hyperlink run.
- **PDF:** screenshot plus the printed link, clickable on the html route.

## 5. Hub / chapter navigation (`navigation.mode: zoom`, `hubSlideId`)
- **HTML:**
  - The agenda tiles are buttons, reachable by keyboard and mouse. Activating one flies the camera to
    that section.
  - `M` returns to the hub, `O` shows the overview.
  - Inactive slides are `inert`, so Tab doesn't wander into off-screen slides.
- **PPTX:** Morph between slides, plus Sections and a map slide. The user finishes Section Zoom in two
  clicks; see techniques.md §3.
- **PDF:** linear, in reading order.

## 6. Motion and reduced motion
- **Restraint.** Motion segments ideas and carries continuity (techniques.md). Never put meaning only
  in motion.
- **HTML respects** `prefers-reduced-motion` and `meta.accessibility.reducedMotion`; the presenter can
  also toggle with `R` or the Motion button. In reduced mode there is no camera flight and reveals are
  short fades with no movement.
- **PPTX:** apart from transitions, no animation is generated. If you specify entrance animations,
  describe them in `animation.notes` for the presenter to add. Keep them subtle.
- **PDF** captures every reveal step and every answer as static content.

## 7. Patterns from practice (candidate sources in design-gallery.md, not yet verified)
- **Show what changes, not that something moves.** Animate the one element that changes between two
  states (a bar growing, a step being added). A technical or process explanation should build up one
  step at a time, the way a presenter would draw it.
- **One payoff motion per section.** Everything else stays quiet.
- **Self-read decks have no reveals.** The reader can't click through steps; show the final state.

## 8. Checklist before hand-off
- [ ] every quiz has `correctOptionId`, per-option `feedback` and an `answerPlacement` that suits the format
- [ ] every demo has a screenshot fallback
- [ ] any poll that needs more than one device names the external tool in `presenterCue`
- [ ] no slide's meaning depends on an animation
- [ ] hub decks have a `hubSlideId` and `zoomTargets` that exist (`validate_blueprint.py`)
