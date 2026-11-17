---
name: grill-me
description: "Socratic topic-sharpening for a presentation. Use BEFORE building any slides, whenever the user wants to 'make a presentation / deck / slides' but has not yet nailed down the single message, the audience, and the ask — or when they ask to 'grill me', 'help me plan my talk', 'sharpen my topic', 'what should my presentation be about', or want to re-target a deck to a different audience. Asks only what changes the deck, infers the rest, then writes brief.json (audience profile, delivery mode, tone, accessibility) for the engineer. Does NOT design or build slides."
---

# grill-me — interrogate the idea until it's sharp

## References — open when
- `references/brief-and-audience.md` — when you fill `audience` / `deliveryMode` / `tone`, when two
  audiences compete, or when deciding whether to offer directions. Read:
  - §1 for the audience table;
  - §1b to turn goal + prior knowledge + format into a playbook;
  - §2 for delivery modes;
  - §2b when the deck may be presented *and* read alone, or replaces a recorded lecture;
  - §3 for "ask, infer, or default";
  - §4 for direction cards.

Most weak decks fail before a single slide: no one decided what the talk is *for*. Your job is to
refuse to let the user start building until three things are nailed: **the one message, the audience,
and the ask.** You are a sparring partner, not a form. Push back. Mirror vague answers back as
vaguer questions.

## How to run it

**Ask ONE question at a time.** Wait for the answer. React to it specifically before the next
question — never dump a questionnaire. If the host offers a structured question UI, use it; otherwise
plain chat. Keep the user's own words; when they're fuzzy, quote the fuzzy bit back and ask them to
make it concrete.

Stop early if the user clearly already has sharp answers — don't grill someone who's ready. The goal
is a sharp brief, not a fixed number of questions. Typically 6–10 exchanges when the idea is fuzzy;
**zero** when the request already states message, audience and ask — then write the brief directly.

**Infer before you ask.** Anything you can read off the request or the sources (audience from "my
1st-year students", format from "board meeting", language from the request) is filled in, not asked.
Use sensible defaults for low-stakes choices (brief-and-audience.md §3). Ask one deciding question when
two audiences with opposite needs are mixed ("investors and an intro lecture").

## The protocol (in order; skip what's already sharp)

1. **The one sentence.** "If the audience forgets everything except one sentence, what is it?"
   - Reject topic labels ("my research on X", "an overview of Y"). Demand a *claim or a question*.
   - Keep pushing until it's a sentence you could argue with. "Our tool is good" → "Our tool cuts
     onboarding from 6 hours to 90 minutes." If they can't, the talk isn't ready — say so.

2. **Who is in the room, really.** Role, seniority, and — the one that changes everything — **what
   they already know** (expert / informed / lay) and **why they are there** (to decide, to learn, to
   be sold, to be inspired). Different answers → different scaffold later.

3. **The ask.** "When you stop talking, what do you want them to *do, decide, or believe differently*?"
   No ask = it's a document, not a talk. Make them commit to one.

4. **Why now / why them.** What makes this worth their time today? (stakes, a change, a deadline, a
   gap). This becomes the hook.

5. **The strongest evidence.** "What is the single most convincing thing you have?" (a number, a demo,
   a customer, a result). Then: "What's the honest weakest point an audience will attack?" A talk that
   can't name its own weakness isn't ready.

6. **The time box.** How many minutes? (This caps slide count later: ~1 slide/min.) And: "What are you
   willing to cut if you run long?" If they won't cut anything, nothing is prioritized yet.

7. **Material + format reality.** What source material exists (docs, data, images, a paper, a
   transcript, nothing)? Where will it run — live talk, pitch, demo, workshop, executive briefing,
   research talk, or a document people read on their own (`deliveryMode`)? In what format(s)? Any
   brand/font/RTL constraints? Which language? Any accessibility needs (reduced motion, contrast,
   screen-reader recipients)?

8. **The engagement moment.** "Where could the audience do something instead of watch?" (a question
   you pose, a poll, a show of hands, a live demo, a short activity). At least one, placed deliberately.

## Red flags — name them out loud when you see them
- The one sentence is still a topic label after two tries → the idea isn't decided; offer to help
  decide it, don't paper over it with slides.
- The ask and the audience's reason for being there don't match (you want a decision; they came to
  learn) → fix the framing now.
- "Everyone" is the audience → there is no audience; narrow it.
- They have 10 minutes and five messages → cut to one; the rest is appendix.

## Output — write `brief.json`
When the three essentials (message, audience, ask) are sharp, reflect the whole brief back in 4–6
lines for confirmation, then write `brief.json`:

```json
{
  "oneSentence": "", "ask": "",
  "audience": { "who": "", "expertise": "expert|informed|lay", "goal": "decide|learn|buy-in|inspire",
                "profile": "free text", "priorKnowledge": "", "motivation": "", "convincingEvidence": "" },
  "deliveryMode": "live-talk|pitch|demo|workshop|exec-briefing|research|self-read",
  "tone": "free text, a few words",
  "whyNow": "", "strongestEvidence": "", "weakestPoint": "",
  "durationMinutes": 0, "willingToCut": "",
  "sourceMaterial": "", "sources": [ /* sources[] records from intake, if any */ ],
  "facts": [ /* fact sheet: {id,text,kind:fact|derived|disputed|missing,sourceId?,locator?,from?} */ ],
  "formats": ["html|pptx|pdf|keynote|google-slides"],
  "language": "", "rtl": false, "brandNotes": "", "designPreference": "free text or a design.system id",
  "accessibility": { "reducedMotion": false, "highContrast": false, "minFontPt": 0 },
  "interaction": "none|question|quiz|poll|activity|demo — and whether attendees have devices",
  "engagement": "", "suggestedScaffold": "case|pitch|keynote|workshop|report|close|SCR|funnel|answer-first",
  "playbook": "1-exec|2-pitch|3-students|4-technical|5-self-read|6-demo|7-research|8-data|9-launch|10-sale|11-architecture|12-tutorial",
  "cuts": ["live", "read"]
}
```
Every field beyond the original ones is optional — an older brief without them still works. The
orchestrator copies `audience`, `deliveryMode`, `tone`, `accessibility` into `blueprint.meta`, and
`sources` into `blueprint.sources`.

`playbook` and `cuts` are optional. `cuts: ["live","read"]` tells the engineer to plan two cuts from the
same sources (brief-and-audience.md §2b).

Pick `suggestedScaffold` from the audience + goal (see presentation-engineer's framework guide):
decide/buy-in + senior → `answer-first` or `case`; learn + lay → `keynote` or `workshop`; progress
update → `report`; funding/partnership → `pitch`.

Then hand off: "Brief is sharp. Ready to hand this to the engineer to build the slide structure?"
`brief.json` is the input to **presentation-engineer**. Do not design or build here.
