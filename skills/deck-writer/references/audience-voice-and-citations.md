# Audience voice & citations — one claim, three registers; sources in the copy

Open this when you write copy for a specific audience, re-write a deck for a new audience, write speaker
notes, cite sources, or mix Hebrew with Latin terms, units, code or numbers.

---

## 1. The same claim in three registers

**Fact sheet entry:** median handshake time 179.9 → 96.3 ms (lab data, week 4), via TLS 1.3's single
round trip.

| | Pedagogical (beginner students) | Technical (engineers) | Managerial (executives) |
|---|---|---|---|
| **Title** | "Why does the new version connect faster? It skips one trip to the server" | "TLS 1.3 completes the handshake in one round trip (1-RTT)" | "Turning on TLS 1.3 makes new connections almost twice as fast, at no development cost" |
| **Evidence** | a worked sequence diagram, then a quiz | sequence diagram + latency line chart with units and source | one big number (−46.5%) + options/cost table |
| **Bullets** | "The client sends its key part in the first message" | "key_share in ClientHello; server Finished in flight 2" | "Server config only · rollout in staging this week" |
| **Notes** | "Ask: how many times do you think the browser waits? Take guesses before revealing." | "Note 0-RTT exists but carries replay risk; we didn't enable it." | "The cost is a config change; the risk is old clients, which we measured at under 1%." |
| **Ask** | "Explain the difference to your neighbour in one sentence" | "Review the config PR; flag any client you know still on 1.2" | "Approve staging rollout today" |

Same fact, same number, same source. What changed: the question asked, depth, the type of evidence, the
ask. Hebrew versions follow the same pattern (see §5 for mixed text).

## 2. Speaker notes that sound like a person
- 2–4 sentences, in the order you'd say them: the point → the why → the bridge to the next slide.
- Oral attribution before the citation appears: "Rescorla's spec puts it plainly…", "In our lab data…".
- Mark what to *do*: "[pause]", "[ask the room]", "[click: reveal the second line]". Presenter cues for
  quizzes go in `engagement.presenterCue`; the PPTX builder appends them to the notes.
- Write numbers the way you'd say them: "almost twice as fast", with the exact figure on the slide.
- `self-read` decks: no notes needed; the caption and headline must carry the slide.

## 3. Citations in the copy
- The slide footer is generated from `citations[]` (number + short title + locator). Don't type
  sources into bullets. Your job: make the caption agree with what the citation covers, and fill
  `citations[].claim` when one slide carries two claims from different sources.
- Verbatim quotes: quotation marks, speaker, source with page/timestamp. Never tidy a quote.
- The full list is generated as **Sources & credits** slides (numbered by first citation). A
  hand-written references slide is only needed if the user's field demands a specific format; then keep
  its numbering consistent with the generated one.
- Image credits come from `assets[].credit`; write `alt` text for every image: what it shows and why it's
  there, ≤ 125 characters ("Dashboard: latency bars before the change, long tail on the right").

## 4. Observation vs. hypothesis
- **Observation** (a `fact` citation): plain indicative. "Handshake time fell 46% in week 4."
- **Inference** (`derived`): signal it. "This suggests…", "Our reading:", "Likely because…".
- **Disputed / uncertain**: say so on the slide, not only in notes. "Two sources disagree: 38% (survey)
  vs. 44% (logs); we use the logs because…".
- **Missing**: an open question is an honest slide. "Not yet measured: mobile clients."
- Never upgrade a hedge between drafts ("may" → "will") without a new source.

## 5. Hebrew with terms, units, code and numbers
- Keep established English technical terms in English when your audience says them that way
  (handshake, TLS, API), and gloss on first use for beginners: "לחיצת יד (handshake)".
- Units: number + space + unit (`96.3 ms`, `6 שעות`); `%` attaches (`38%`). Keep one unit per
  chart; say it in the axis label.
- Numbers keep Western digits; thousands separator `,`; decimal point `.`. A minus sign in Hebrew text:
  write it with the number in one token (`−46.5%`); the big-number layout isolates it.
- Code, commands, file names, IDs (`T1566`, `screen.png`, `ClientHello`) → `bullet.mono: true` or keep
  them short inside the sentence; avoid starting a Hebrew bullet with a Latin token (it can flip the
  line's visual start) — lead with a Hebrew word: "הקובץ screen.png נשמר…" rather than "screen.png נשמר…".
- Brackets and punctuation next to Latin text are the usual bidi trouble spots; read the rendered slide.
- Gender-neutral address where possible (plural imperative: "בחרו", "שימו לב").

## 6. Re-writing for a new audience (checklist)
- [ ] titles re-written for the new playbook's ghost deck (deck-playbooks.md)
- [ ] jargon level matches `audience.priorKnowledge`; terms glossed for lay audiences
- [ ] evidence phrasing matches its new type (worked example / decisive number / mechanism)
- [ ] no new numbers; every figure still has its citation
- [ ] the ask fits what this audience can actually do
