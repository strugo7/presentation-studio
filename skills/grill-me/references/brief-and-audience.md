# Brief & audience — profiles, delivery modes, and when to ask

Use this to fill `brief.json → audience`, `deliveryMode`, `tone`, and to choose what (if anything) to ask.
Profiles are starting points, not boxes: write the real audience in your own words in `profile`.

---

## 1. Audience profiles

Each profile: what they already know · why they came · what holds their attention · what counts as
convincing evidence · what to avoid. `expertise` / `goal` map to the existing brief fields.

| Profile | Already knows | Came to… (`goal`) | Holds attention | Convincing evidence | Avoid |
|---|---|---|---|---|---|
| **Executives / management** (`informed`) | the business, not the method | **decide** | the decision, its cost, its risk | one decisive number with context; comparison of options; risk owned | method detail on slides (→ appendix); "journey" narratives |
| **Investors** (`informed`) | markets, patterns of failure | **buy-in** (fund) | traction, why now, size of prize | growth/retention data, customer names, unit economics | features lists; burying the ask |
| **Customers / buyers** (`lay`–`informed`) | their own problem | **buy-in** (buy) | their workflow made easier | before/after of their task, a demo, a peer customer | your org chart; your architecture |
| **Product team** (`informed`) | the product, the roadmap | **decide** / align | user evidence, trade-offs | usage data, research quotes, a prototype | marketing tone |
| **Technical audience / engineers** (`expert`) | the domain deeply | **learn** / evaluate | how it works, limits, numbers | diagrams of the mechanism, measurements, code, failure cases | hand-waving; hiding limitations |
| **Beginner students** (`lay`) | little or nothing about the topic | **learn** | a question they care about, doing something | a worked example, an analogy, a quick check of understanding | jargon before it's defined; walls of text; >1 new idea per slide |
| **Practitioners / professionals** (`informed`–`expert`) | the field, not your case | **learn** / adopt | what they can apply Monday | a case with numbers, a checklist, a before/after | basics they know; theory without application |
| **General public** (`lay`) | everyday experience | **inspire** / learn | a story, a surprise, relevance to them | a concrete person or scene, one memorable number | abbreviations; more than three points |

**Same facts, different decks.** The fact sheet doesn't change between audiences. What changes:
the **order** (decision first vs. question first), the **depth** (mechanism vs. outcome), the **type of
evidence** (worked example vs. one decisive number vs. diagram + measurement) and the **ask**
(decide / practise / try / fund).

## 2. Delivery modes (`meta.deliveryMode`)

| Mode | Shape | Text density | Interaction | Default format |
|---|---|---|---|---|
| `live-talk` (lecture, conference) | one idea per slide, presenter carries the words | low | posed question, optional quiz | HTML or PPTX |
| `pitch` | problem → solution → traction → ask, 10–15 slides | low | none or one demo | PPTX + PDF |
| `demo` | context → live product → what it means | low | demo slides with screenshot fallback | HTML |
| `workshop` | teach once, apply repeatedly, check understanding | medium | quiz/activity every 8–10 min | HTML (+ PDF handout) |
| `exec-briefing` | answer first, evidence, options, ask; appendix holds method | medium | none; decision slide stays up | PPTX + PDF |
| `research` (seminar, defense) | question → method → findings (assertion–evidence) → limits | medium | Q&A slide, backup slides | PPTX / PDF |
| `self-read` (slidedoc, async) | headlines that summarise, captions that stand alone, method in appendix | high but structured | answers shown inline | PDF / HTML |

## 3. Ask, infer, or default?

**Infer** (don't ask) when the request already implies it: "for my 1st-year students" → lay, learn,
workshop or live-talk; "board meeting Thursday" → executives, decide, exec-briefing, PPTX + PDF;
"send it to the client" → self-read, PDF.

**Default** when it barely matters: duration ≈ 1 slide/minute of stated time, else 10–12 slides;
language = the request's language; RTL for Hebrew/Arabic; format = HTML + PDF for sharing, PPTX for
"presentation in the office".

**Ask one deciding question** only when the answer changes the deck's structure:
- two audiences with opposite needs in one request (investors *and* an intro lecture → which one leads,
  or two cuts from the same sources?);
- the ask is missing and can't be inferred ("what should they do afterwards?");
- a format/environment conflict (live quiz requested but PDF-only delivery).

Never run rounds of preference questions about colours, fonts or tone you could choose sensibly.

## 4. Offering directions

Offer 2–3 directions **only** if the user asks to choose, or if the material honestly supports
substantially different decks. Each direction is a short card:

```
A · Executive decision brief  (recommended)
Audience/goal: management, decide · Sequence: decision → evidence → options & risks → next step
Visual: executive-data-briefing (hairline frames, big-number slides) · Exhibits: one decisive number, comparison table
Motion/interaction: minimal fades, no quiz · Formats: PPTX + PDF
```

Directions must differ in at least two of: audience/goal, sequence, visual direction, exhibit types,
interaction level. Three versions of the same deck in different colours is not a choice.

## 5. Tone (`meta.tone`) — free text, a few words

Examples: "direct, numbers first", "warm and curious, second person", "precise, technical, no hype",
"calm, reassuring", "playful but accurate". The writer uses it; the designer reads it as a hint.

## 6. Accessibility and interaction constraints

Record what you know in `brief.accessibility` → `meta.accessibility`: reduced motion requested, high
contrast (projector in a bright room), minimum font size, screen-reader users receiving the file
(alt text matters), whether attendees have devices (decides whether a poll is local or needs a tool).
