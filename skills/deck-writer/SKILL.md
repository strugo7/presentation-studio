---
name: deck-writer
description: "Method for writing on-slide copy and speaker notes — action titles, telegraphic bullets, captions, and natural speaker notes in the deck's language and voice — into blueprint.json. Use after structure is set. Pairs with references/writing-rules.md."
---

# deck-writer — words for the mouth, not the page

Slide copy is spoken. You own the wording of titles, bullets, captions, and speaker notes. See
`references/writing-rules.md`. Method:

1. **Titles → action titles.** Every content slide's `actionTitle` is one declarative sentence stating
   the takeaway, not a label. Re-run the ghost-deck test on your titles: read them in order, do they
   tell the whole argument? Fix wording so they do. 1–2 lines; if longer, the point isn't sharp yet.

2. **Bullets → telegraphic cues.** ≤3, one idea each, phrases not sentences, articles dropped where
   meaning survives ("Intervention cut cost 23% (p<.01)"). A bullet is a springboard for what you say,
   not the sentence you'll read. Mark a key term `bold`-worthy via `bullet.lead` only when it earns it.

3. **Captions + annotations.** Each exhibit gets a short caption naming what it is; the `annotate` hint
   (from the engineer) tells the builder where to draw the eye — make sure your caption agrees with it.

4. **Speaker notes.** 2–4 natural sentences per slide — what the presenter actually says, the *why*
   behind the slide, not a re-read of the bullets. Conversational. Include the oral attribution for any
   cited source ("Smith and colleagues found in 2022…").

5. **Voice + language.** Write in `meta.language`; for RTL keep Latin tokens (tool/command names)
   inline LTR. Match the presenter's voice if given. One moment of genuine personality every few slides;
   don't sand it flat.

6. **Cite.** Anything borrowed gets an on-slide citation (caption/bottom) and a line on the
   `references` slide. Ensure that slide exists if you cited anything.

Hand off the updated blueprint. Don't change structure, exhibits, design, or animation.
