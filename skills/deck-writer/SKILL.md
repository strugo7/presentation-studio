---
name: deck-writer
description: "Method for writing on-slide copy and speaker notes — action titles, telegraphic bullets, captions, alt text, quiz feedback and natural speaker notes in the deck's language, tone and audience register — into blueprint.json, with claims that match their citations. Use after structure is set, or to re-write a deck for a new audience. Pairs with references/writing-rules.md."
---

# deck-writer — words for the mouth, not the page

> **Paths.** This skill ships in the presentation-studio plugin. `shared/…` and `skills/…` paths are under
> `${CLAUDE_PLUGIN_ROOT}/` (in a plain checkout of the repo, the repo root); `references/…` is this skill's own
> folder. Write blueprints and builds in the user's project, never inside the plugin folder.

Slide copy is spoken (or, in `self-read` decks, read without a narrator). You own the wording of titles,
kickers, bullets, captions, speaker notes, `engagement.prompt`/`feedback`/`presenterCue`, and
`assets[].alt`.

## References — open when
- `references/writing-rules.md` — always: titles, bullets, notes, voice, AI tells.
- `references/audience-voice-and-citations.md` — open the section you need:
  - §1: writing for a specific audience register;
  - §2: speaker notes and the bridge sentence;
  - §2b: deciding what goes on the slide vs. in the notes for a live or a read cut, and checking a
    talk that replaces a recorded lecture;
  - §3–4: wording claims against their citations;
  - §5: mixing Hebrew with Latin terms, units, code and numbers;
  - §6: any re-write for a new audience.

Method:

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
   cited source ("Smith and colleagues found in 2022…"). End with a bridge sentence to the next slide.
   In a `self-read` cut, move that explanation into the caption instead (audience-voice-and-citations.md §2b).

5. **Voice + language.** Write in `meta.language`, in `meta.tone`, at the register of
   `meta.audience` (audience-voice-and-citations.md §1). For RTL keep Latin tokens (tool/command names)
   inline LTR and don't start a Hebrew line with one. Match the presenter's voice if given. One moment of
   genuine personality every few slides; don't sand it flat.

6. **Claims match sources.** Every factual sentence must be covered by the slide's `citations[]`; the
   builders print the footer and the sources slides. Say "suggests"/"our reading" for `derived`, name the
   disagreement for `disputed`, and never add a number that isn't in the fact sheet.

7. **Interaction copy.** Quiz prompt: one clear question. Options: short, parallel, plausible. `feedback`
   per option explains *why* (the right one reinforces, the wrong ones correct the specific mistake).
   `presenterCue`: what the presenter does ("let them choose for 20s, then reveal").

8. **Alt text.** For each image asset: what it shows and why it's on the slide, ≤ 125 characters.

Hand off the updated blueprint. Don't change structure, exhibits, design, or animation.
