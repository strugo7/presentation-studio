# How people actually learn from slides — and how to engage them

The engineer uses this to decide what goes on a slide vs. in the mouth, how much per slide, and where
to put engagement. Grounded in cognitive-load and multimedia-learning research; treat specific
numbers as guidance, mechanisms as reliable.

## The core mechanism: split attention and overload
Working memory is tiny. A slide that makes the audience **read dense text while also listening** forces
them to do two things at once and they do neither well. The presenter's voice and the slide must
*complement*, not duplicate. This is the single most violated rule in real decks.

### Mayer's multimedia principles that change slide structure
*(R. E. Mayer, evidence-based; ~11–12 principles. The ones that touch structure:)*
- **Signaling:** highlight the essential bit — colour, contrast, an arrow, a boxed region. People learn
  more when the organisation of the material is cued. → every exhibit gets an `annotate`.
- **Redundancy:** narration + identical on-screen text hurts. Don't put your script on the slide; put
  the evidence. → the "slides carry evidence, presenter carries argument" rule.
- **Segmenting:** break a long flow into learner-paced chunks rather than one continuous dump. → reveal
  bullets/steps one at a time (`animation.reveals`); split dense slides; use section dividers.
- **Coherence:** cut anything that doesn't serve the point — decorative images, extra data, chartjunk.
  Every element must carry content.
- **Spatial/temporal contiguity:** put a label next to the thing it labels, and show words and the
  matching visual together, not on separate slides.
*Source: Mayer, Multimedia Learning; summaries at Dartmouth/Buffalo/UCSD teaching centres.*

### Practical limits (converging craft + research)
- ≤ ~40 words of body text per content slide; ≤ 3 bullets, one idea each.
- One exhibit per slide. Two charts = two points = two slides (or one combined comparison).
- Body ≥ 20pt (PPTX) / ≥ 28px@1920 (HTML); titles larger. If it doesn't fit, cut words.
- Rebuild figures at presentation resolution; never paste a print-size figure from a PDF.

## Structuring the teaching itself: Gagné's nine events
*(R. Gagné, 1965 — a checklist for an instructional segment; events overlap and nest.)*
1. **Gain attention** — the hook (a question, a stat, a scene). → the opener slide.
2. **State the objective** — what they'll be able to do. → one explicit "here's the claim/question" slide.
3. **Recall prior knowledge** — connect to what they already know (ties to audience expertise).
4. **Present the content** — segmented, signalled (see Mayer).
5. **Provide guidance** — worked examples, analogies, a visible framework.
6. **Elicit performance** — the audience does something (→ engagement moments below).
7. **Give feedback** — respond to their attempt / poll result.
8. **Assess** — a quick check (quiz, show of hands, "what would you predict?").
9. **Enhance retention & transfer** — summary, call to action, "where you'll use this."
Map loosely: events 1–2 = opening; 3–5 = body; 6–8 = engagement beats; 9 = conclusion/ask. Don't force
all nine; use it to spot what's missing (most decks skip 3, 6, and 8).

## Engagement — pick 1–3, place with intent
Attention sags roughly every 8–10 minutes; put an engagement beat near each sag, not randomly.
From Figma's idea set and NIU, ranked by how reliably they re-engage a room:
- **Pose a question** the audience answers (aloud or mentally) — cheapest, works anywhere; put one at
  the hook and one before the key result ("what would you predict?").
- **Poll / show of hands** at a pivot — commits people before you reveal the answer.
- **Live demo or prototype** — highest impact when the thing is the point; rehearse a fallback.
- **Short activity / think-pair-share** — for workshops; needs time budget.
- **Quiz** (incl. Jeopardy-style) — good for teaching/retention checks (Gagné event 8).
- **Relatable analogy / personal story** — re-engages without stopping the flow.
- **Props / multiple senses / surprise guest** — situational, memorable, use sparingly.
Each chosen moment → a slide's `engagement` field + a note in `speakerNotes` on what the presenter does.

## Accessibility & international (always on)
- Don't rely on colour alone — pair with labels/shapes/patterns.
- High contrast; ≥20pt body; alt text on figures if the deck is shared as PDF.
- For mixed/international audiences: define acronyms on first use, avoid idioms, plainer sentences.
- RTL languages (Hebrew/Arabic): right-aligned, reading order right-to-left, Latin tokens stay LTR
  inline; tag every text run with its language so renderers choose a script-correct font (see builders).

## See also
- deck-playbooks.md §3 — the beginner-student sequence (question → model → worked example → practice).
- deck-animator/references/interaction-patterns.md — how a quiz/poll/activity behaves in each format.
- Quiz fields: `engagement.options`, `correctOptionId`, per-option `feedback`, `presenterCue`, `answerPlacement`.
