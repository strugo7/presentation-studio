# Deck playbooks: short, reasoned sequences per audience and situation

A playbook is a scaffold (structure-frameworks.md) tuned to a delivery mode and an audience. Each one
gives:

- the beats, and why they come in that order;
- which `layout` and exhibit each beat usually takes;
- a ghost-deck example (action titles only, in order);
- the type of evidence that convinces this audience;
- what changes between the **live** version and the **read** version;
- the call to action, and the sources behind the playbook.

Pick one; don't merge two. The ghost deck must read as the argument even with every body removed.
Load only the playbook you're using. Ghost-deck numbers below are **illustrative**. A real deck
takes every number from the fact sheet, with its citation.

Real-world references for these sequences, with what each one teaches, are in
deck-designer/references/design-gallery.md.

---

## 0. Choose the playbook from the brief

Three brief fields decide it (grill-me/references/brief-and-audience.md §1–3):

- `audience.goal`: decide · learn · buy-in · inspire.
- `audience.expertise` / `priorKnowledge`: expert · informed · lay.
- `deliveryMode`: live, or `self-read`.

| Situation in the brief | Playbook | Scaffold underneath |
|---|---|---|
| Management must decide something | **1** Executive decision brief | Answer-first / The Case |
| Investors, on stage or in a sent deck | **2** Investor pitch (stage cut / send cut) | The Pitch |
| Lay learners meet a topic for the first time | **3** Beginner students | The Workshop |
| Engineers judging a mechanism and a measurement | **4** Technical team | SCQA + assertion–evidence |
| Nobody presents: pre-read, leave-behind, email | **5** Slidedoc, applied as an overlay on any playbook | (the playbook's own) |
| Showing the product working | **6** Product demo | job → task → result |
| Seminar, conference talk, defence, lab meeting | **7** Academic research talk | research question → evidence |
| Metrics review, analytics findings, dashboard read-out | **8** Data briefing | Report-out / answer-first |
| Launch event, campaign, positioning to a market | **9** Marketing and launch | Sparkline (what is ↔ what could be) |
| A meeting with one buyer about one deal | **10** Product sale | need → proof → next step |
| Design review, system onboarding, architecture decision | **11** Architecture overview | C4 zoom levels |
| Teaching a procedure step by step | **12** Tutorial / how-to | Workshop, with steps |

Close calls:

- **Demo (6) vs. sale (10).** A demo shows tasks being done. A sale is a conversation about one buyer's
  need, and it may contain a demo beat.
- **Marketing (9) vs. sale (10).** Marketing talks to a segment ("finance teams of 5–50"). A sale talks to
  one account ("your 9 branches").
- **Research (7) vs. technical (4).** Research answers a question with evidence and names threats to
  validity. Technical explains how a system works and what was measured.
- **Tutorial (12) vs. students (3).** A tutorial teaches a procedure the learner will repeat. Students
  learn a concept.

## Live vs. read: the rule every playbook follows

The same content is **re-cut**, not re-used (Duarte, *Slidedocs*:
[duarte.com/resources/books/slidedocs](https://www.duarte.com/resources/books/slidedocs/)).

- **Live.** A slide may be deliberately incomplete. The explanation moves to `speakerNotes`, which end
  with a bridge sentence to the next slide. Test each element with Reynolds' question: does it serve the
  message, or compete with the speaker?
  ([presentationzen.com](https://presentationzen.com/blog/the-signal-to-noise-ratio-activity))
- **Read** (`self-read` PDF/HTML). Whatever the presenter would have said goes on the page:
  - the context needed to read the slide;
  - definitions of terms and metrics;
  - where each number comes from (unit, period, baseline);
  - the interpretation ("what to notice") in the caption.

  Put long material in an appendix slide, not in the notes. Nobody opens the notes.
- **A static export of the stage version is not a read version.** A PDF of the live deck keeps the
  stage's gaps. If the brief needs both, build two cuts from the same blueprint sources. The facts
  and citations stay identical.

Each playbook below has a **Live vs. read** line that says what moves.

---

## 1. Executive decision brief (`exec-briefing`, management)
**Beats:** Decision → Evidence → Alternatives & risks → Next step.
**Why:**
- Executives allocate attention by decision, so give the answer first (Minto).
- Then show only the evidence that would change their mind.
- Alternatives show you considered them; owning the risk earns trust.
- Method and detail live in the appendix: reachable, but not presented.

When the brief is a strategy rather than a single decision, run audit → gap → decision → playbook as
the evidence beats (design-gallery.md #6).

| Beat | Layout / exhibit | Engagement |
|---|---|---|
| Decision (the recommendation in one sentence + the ask) | `statement` | — |
| The decisive number | `big-number` (value, unit, context, source) | — |
| 1–2 evidence slides | `full-exhibit` chart or table, one point each | — |
| Alternatives & risks | `comparison` table (option × cost × risk × time) | — |
| Next step (who, what, when) | `statement` close | decision stays on screen |
| Appendix: method, data definitions | `references`/`appendix` | — |

Ghost deck:
1. *Move onboarding to four 90-minute sessions next cohort*
2. *Two-week retention nearly doubles when sessions are spaced*
3. *The gain held across all three pilot groups*
4. *Cost: four calendar holds instead of one; risk: attendance drop, mitigated by fixed slots*
5. *Approve the pilot today; results in six weeks*

**Evidence:** one decisive number with context, and a comparison of options.
**Live vs. read:**
- Live: the decision slide stays up during discussion, and the method stays out of the talk.
- Read (pre-read): each evidence caption names the metric's definition and period. The appendix
  holds the method.

## 2. Investor pitch (`pitch`)
**Beats:** Problem → Solution → Proof of traction/progress → Ask.
**Why:**
- Investors pattern-match on a painful, large problem and on evidence that you're winning.
- The ask must be specific: "$X to reach Y by Z".
- Team and market slot in briefly, after the proof.

Sequoia's list of content elements is purpose, problem, solution, why now, market, competition,
product, business model, team and financials
([sequoiacap.com](https://sequoiacap.com/article/writing-a-business-plan)). YC's advice for Demo Day
slides is legibility: big text, one idea, simple enough to read from the back row
([ycombinator.com](https://www.ycombinator.com/blog/how-to-design-a-better-pitch-deck/)).

| Beat | Layout / exhibit |
|---|---|
| Problem (quantified, felt) | `statement` or `big-number` |
| Solution (one sentence, then show it) | `split` with product screenshot |
| How it works (just enough) | diagram `chain` |
| Traction | `full-exhibit` line chart (growth over time); customer logos only with permission |
| Why now / market / model / team | 1 slide each, `concept` |
| Ask | `statement` close: amount, milestone, date |

Ghost deck:
1. *Small clinics lose 11% of revenue to unpaid claims*
2. *ClaimPilot files and chases claims automatically*
3. *Monthly paid clinics grew from 12 to 140 in 10 months*
4. *A 2025 billing rule made manual filing unworkable*
5. *Raise $3M to reach 1,000 clinics by end of 2027*

**Evidence:** growth over time, retention, unit economics, named customers (with permission).
**Live vs. read (two cuts):**
- **Stage cut**, 10–12 slides. Built around what the investor must remember: the problem, the proof,
  the ask. Very few words, large type.
- **Send cut**: the same order, plus what is needed to check the claims without you:
  - each traction metric defined (what counts as "active", over which period);
  - cohort or retention tables;
  - market-size assumptions labelled **estimate**, with their inputs;
  - a financials appendix.

  Label every projection as a projection (`kind: "derived"`).

**Call to action:** the amount, the milestone it buys, the date.

## 3. Beginner students (`workshop` or `live-talk`, lay)
**Beats:** Question → Model → Worked example → Practice & feedback.
**Why:** novices learn from:
- a question they care about (activation);
- a simple model before details (schema);
- a fully worked example before solving alone (worked-example effect);
- immediate feedback (retrieval plus correction).

One new idea per slide; define every term at first use.

| Beat | Layout / exhibit | Engagement |
|---|---|---|
| Question (concrete, from their world) | `statement` | posed question; let them guess |
| Model (the mental picture) | diagram (`chain`/`sequence`) | — |
| Worked example, step by step | `full-exhibit` with reveals per step | — |
| Common mistake | `split` (wrong vs. right) | — |
| Practice | `concept` + `engagement.type:"quiz"` with option-level feedback | quiz, every 8–10 min |
| Summary they can keep | `statement` / self-contained summary | — |

**Live vs. read:**
- Live: the guess comes before the reveal, and the notes carry the explanation plus the bridge.
- Read (handout): the worked example is fully written out on the slides, and quiz answers are inline.

**Replacing a recorded lecture.** When the talk replaces a video for people starting from zero, the
presenter needs the whole explanation in the notes, not hints. See
deck-writer/references/audience-voice-and-citations.md §2b.

## 4. Technical team (`research` / `live-talk`, expert)
**Beats:** Context → How the system works → Observation → Limitation & what's next.
**Why:** experts want the mechanism and the measurement, and they trust a speaker who names limits.
Titles are assertions (Alley's assertion–evidence): a full-sentence claim, and a visual that proves it.

| Beat | Layout / exhibit |
|---|---|
| Context (what problem, what constraint) | `concept` |
| How it works | diagram `sequence` (messages between components) or `chain` |
| Observation (the measurement) | `full-exhibit` line/column chart with units and source |
| Comparison / ablation | `comparison` table |
| Limitation, open questions, next experiment | `concept`, then `close` |

**Live vs. read:**
- Live: one mechanism diagram, and the details in the notes.
- Read: every component labelled, test conditions in the caption, raw numbers in an appendix table.

## 5. Document for reading (`self-read`, slidedoc): an overlay on any playbook
**Beats:** Summary → sections with headline + evidence → method appendix.
**Why:** nobody is talking, so each page must stand alone (Duarte's slidedocs):
- headlines that summarise the page;
- captions that explain the exhibit without a narrator;
- method and definitions in the appendix.

The live version of the same content goes the other way: deliberately incomplete slides that the
presenter finishes out loud (design-gallery.md #7–8). Re-cut rather than reuse.

Text density can be higher, but structured: headline, 2–3 short paragraphs or bullets, one exhibit,
caption with source. Quiz answers are inline (`answerPlacement:"inline"` is the default).

| Beat | Layout / exhibit |
|---|---|
| Executive summary (3 findings, 1 recommendation) | `concept` with bullets |
| Each finding | `full-exhibit` or `split`, caption that stands alone, citation in footer |
| Method, data definitions, sources | `appendix` + generated sources slides |

To apply it to another playbook, keep that playbook's beats and apply its **Live vs. read** line.

## 6. Product demo (`demo`)
**Beats:** The user's job → Task → Action → Observed result → What changed for them → Try it.
**Why:**
- A demo convinces through an outcome the audience *sees*, not a feature tour.
- Gong's analysis of recorded sales calls suggests showing the buyer-relevant benefit early
  ([gong.io/blog/product-demo](https://www.gong.io/blog/product-demo)). This is observational data
  from sales calls, not a controlled study.

Each demo beat names three things: a task (what the user is trying to do), an action (what you
click or type) and the observed result (what appears on screen).

| Beat | Layout / exhibit | Engagement |
|---|---|---|
| The user's job (who, what they're trying to get done) | `statement` | — |
| Task → action → result (one per slide, 2–4 total) | `split` screenshot; title = the result ("The invoice matches itself to the payment") | `engagement.type:"demo"` + `assetRef` screenshot + `url` |
| What changed (before vs. after on their task) | `big-number` or `comparison` | — |
| Try it | `statement` close with link | — |

Every demo slide carries a screenshot fallback (`engagement.type:"demo"` + `assetRef`), so a dead
network never kills the talk.

**Live vs. read:**
- Live: the product is on screen, and the slide only frames the task.
- Read: the sequence of screenshots *is* the demo. Each caption says the action taken and the result
  shown.

## 7. Academic research talk (`research`, expert or mixed)
**Use:** seminar, conference talk, thesis defence, lab meeting.
**Beats:** Research question → Definitions the argument needs → Method → Findings (one per slide) →
Limits & threats to validity → Answer & contribution → Next step / ask.
**Why:**
- The structure follows the **research question and its evidence**, not a persuasion arc.
  Sparkline fits only when the talk argues for adopting a change.
- Finding slides use assertion–evidence: a claim title and a visual the audience can check together
  ([assertion-evidence.com](https://www.assertion-evidence.com/)).
- The model research talks on Alley's site include one whose first main point defines the core concept
  ([research models](https://www.assertion-evidence.com/research_models.html); design-gallery.md #3).
  Definitions and method details are slides with their own job. They don't need a claim title forced on
  them.

| Beat | Layout / exhibit |
|---|---|
| Research question (why it matters, the gap) | `statement`; a question title is right here |
| Definition of a core term | `split` or `concept` with an example or diagram |
| Method (design, sample, measures) | `chain` (pipeline) or `table` (groups × n × measure) |
| Finding *n* | `full-exhibit` chart; title = assertion; caption = n, unit, period, uncertainty |
| Robustness / comparison | `comparison` table |
| Limits | `concept`: what the data cannot say |
| Answer & contribution | `statement` |
| Backup | appendix: extra analyses, full tables |

Ghost deck:
1. *Does spacing onboarding sessions improve two-week retention?*
2. *"Retained" means active on day 14, read from login logs*
3. *412 new hires in three cohorts, assigned by start week*
4. *Spaced sessions raised day-14 retention from 41% to 68%*
5. *The effect held in all three cohorts, smallest in the remote one*
6. *We cannot yet separate spacing from session length*
7. *Next experiment: vary length with spacing held fixed*

**Evidence:** measured results with sample size and uncertainty, a method diagram, comparisons.
Show sample, uncertainty and limitations **when they change the interpretation**. The schema has no
error bars, so use charts-and-diagrams.md §2b.

**Live vs. read:**
- Live: the method on one slide, with details in backup slides and notes. The answer slide stays up
  during questions.
- Read (paper companion, poster PDF): every measure defined on the slide or in the appendix, the
  sample and any exclusions stated in captions, and full tables in the appendix.

**Call to action:** feedback on the next experiment, a data or code request, collaboration.

## 8. Data briefing (`exec-briefing` or `self-read`, informed)
**Use:** monthly metrics, analytics findings, a dashboard read-out where the question is "what changed,
and what do we do?".
**Beats:** Question & answer (headline) → Scorecard vs. baseline → 2–3 findings, one chart each →
What the data doesn't show → Decision / owner / date.
**Why:**
- The same data needs different charts for different takeaways, so write the takeaway first and then
  choose the chart
  ([Storytelling with Data](https://www.storytellingwithdata.com/blog/different-takeaway-different-graph)).
- The scorecard gives a 5-second scan. The findings explain only what moved.

| Beat | Layout / exhibit |
|---|---|
| Headline: the answer to the question the reader brought | `statement` or `big-number` |
| Scorecard | `table`: metric · now · baseline · change · period |
| Finding: a trend | `line` |
| Finding: a ranking of categories | `bar`, sorted, value at the end of each bar |
| Finding: a relationship | `scatter` (≥ 10 points), else a table |
| Data limits | `concept` |
| Decision | `statement` close |
| Appendix | the source table and metric definitions |

Ghost deck:
1. *Reporting rose for a third month; clicks are flat*
2. *Three of four metrics improved against the Q1 baseline*
3. *Report rate climbed from 12% to 31% since March*
4. *Finance and Sales report least of all teams*
5. *Clicks did not move: training changed reporting, not clicking*
6. *These numbers cover simulated phishing only*
7. *Next: run the drill for Finance and Sales in June (owner: IT)*

**Evidence:** charts chosen by question, each with unit, period and baseline, and a citation to the
cells they come from.

**Live vs. read:**
- Live: one chart per finding, with interpretation and bridge in the notes.
- Read: each caption states the unit, period, baseline, source and what to notice, and the appendix
  carries the source table.

## 9. Marketing and launch (`live-talk` or `self-read`, lay–informed customers / market)
**Use:** launch event, campaign narrative, positioning to a segment.
**Beats (launch):** What's new → For whom → Why it matters (what is → what could be) → Proof a customer
can repeat → How to get it.
**Beats (marketing message):** Promise → For whom → Reason to believe → Proof → Call to action.
**Why:**
- Duarte's Thermo Fisher launch case translated a complex technical advantage into simple
  comparison charts and product renders
  ([case study](https://www.duarte.com/approach/case-studies/delivering-complex-tech-as-an-engaging-product-launch-for-thermo-fisher/);
  results are studio-reported).
- Sparkline is for an audience that must adopt a change: alternate the current state and the possible
  one ([Duarte](https://www.duarte.com/blog/ultimate-guide-to-contrast/)).
- Marketing defines **who the promise is for** and **why to believe it**. Without both it is a slogan.

| Beat | Layout / exhibit |
|---|---|
| What's new (one line) | cover or `statement` |
| For whom (a specific user in a specific situation) | `split` with a photo that plays a story role; short title (Zappos pattern, design-gallery.md #15) |
| Why it matters | `statement` pair: what is → what could be |
| The product | `split` with the product image; ≤ 2 bullets name its parts in reading order (Thermo Fisher pattern, #16) |
| Proof | `full-exhibit` `column` with two bars on a shared zero baseline, values visible, `highlight` the leader (#17) |
| Availability, price, date | `statement` close |

Ghost deck:
1. *Ledger 2 closes the month in one afternoon*
2. *Built for finance teams of 5–50 who close in spreadsheets*
3. *Today close takes six days of copy-paste; it could take one*
4. *Reconciliation runs as you book, not at month-end*
5. *In the beta, close time fell from 6 days to 1.5 (12 teams)*
6. *Available 1 March; free migration for 90 days*

**Evidence:** a before/after on the customer's own task, one comparison chart with its conditions,
and a customer quote used with permission.

**Live vs. read:**
- Live: few words, the product visible, the proof as one chart.
- Read (a launch deck sent to partners): add the conditions of the proof (who, n, period), the
  pricing details and an FAQ appendix. Label estimates.

**Call to action:** try, pre-order, sign up, by a date.

## 10. Product sale (`pitch` or `demo`, one buyer, informed)
**Use:** a meeting with a specific account, and the deck sent after it.
**Beats:** Their need (what discovery found) → What it costs them today → How we meet that need (show
it) → Proof from a similar customer → Terms & implementation → Agreed next step.
**Why:**
- Open with the need the buyer confirmed, not with your company.
- Gong's call data points to presenting the relevant benefit early
  ([gong.io](https://www.gong.io/blog/product-demo)). This is an observation from sales calls.
- The deck ends on a step with an owner and a date, because a sale moves one step at a time.

| Beat | Layout / exhibit |
|---|---|
| Need (in their words; cite the discovery notes) | `statement` |
| Cost today | `big-number` (label as estimate if computed from their inputs) |
| How we meet it | `split` screenshot, or a demo beat (playbook 6) |
| Proof from a similar customer | `big-number` or `full-exhibit` |
| Terms & implementation | `table` (phase · duration · who) |
| Next step | `statement` close: what, who, by when |

Ghost deck:
1. *You told us a new branch takes three weeks of IT time*
2. *That is about 120 engineer-hours per branch, nine branches this year*
3. *Branch templates set up a site in one day*
4. *Here is a branch going live from a template*
5. *Northwind cut branch setup from 15 days to 2*
6. *Pilot: two branches, six weeks, fixed fee*
7. *Next: security review with your team by 20 June*

**Evidence:** their numbers (labelled as estimates), a peer customer's result, a demo.

**Live vs. read:**
- Live: conversation and demo, few slides.
- Sent after the meeting: add the discovery summary, the assumptions behind every cost figure, the
  implementation plan and references.

**Call to action:** one next step, with an owner and a date.

## 11. Architecture overview (`research` or `live-talk`, informed–expert)
**Use:** design review, onboarding to a system, an architecture decision.
**Beats:** Context (the system, its users, external systems) → Main parts → Zoom into the part the
decision concerns → The key interaction in order → Trade-offs & risks → Decision / ask.
**Why:**
- C4 lets you choose the level of detail by need: context → containers → components. Not every level
  is needed ([c4model.com](https://c4model.com/diagrams)).
- Start at context, and go deeper only where the decision is.
- Simplify the illustration and say in the caption what the reader should look at
  ([Google Technical Writing](https://developers.google.com/tech-writing/two/illustrations)).
- Use a sequence diagram when the question is *who talks to whom, in what order*.

| Beat | Layout / exhibit |
|---|---|
| Context | `chain` (users → system → external), or an exported Mermaid/C4 image with `alt` |
| Main parts (containers) | exported image, or `chain` when the parts form a pipeline |
| The part that changes | the same image with that part emphasised, or `split` image + 2 bullets |
| Key interaction | `sequence`, `emphasis:true` on the message the slide is about |
| Trade-offs | `comparison` table: option × latency × cost × risk |
| Decision | `statement` |

**Diagram limits.** The renderers have no native box-and-arrow graph diagram, so export C4/Mermaid
to SVG plus a PNG `fallbackPath` (charts-and-diagrams.md §4). With 3+ subsystems, a zoom hub
(`navigation.mode:"zoom"`) lets the room jump between levels.

Ghost deck:
1. *Orders flow through three services and one payment provider*
2. *Checkout owns the only write path to orders*
3. *Inside checkout, retries live in the payment adapter*
4. *A provider timeout triggers two retries before the user sees an error*
5. *Moving retries to a queue ends duplicate charges but adds 2 s*
6. *Approve the queue design for Q3*

**Live vs. read:**
- Live: one level per slide, the changed part emphasised, the walk-through in the notes.
- Read: a legend, every box labelled with its responsibility and technology, and a caption that says
  what to notice.

**Call to action:** approve the design, review the PR, name an owner.

## 12. Tutorial / how-to (`workshop` or `self-read`, lay–informed)
**Use:** teaching a procedure: setup, tool use, onboarding steps.
**Beats:** Goal (what you'll have at the end) → Prerequisites → Steps (action + expected result) →
Success check → Common errors → Next step.
**Why:**
- State prerequisites up front, and tell the reader what to look for in each illustration (Google
  Technical Writing, above).
- A worked procedure before practice (pedagogy.md).
- Titles are imperative + result ("Start the server; the login page appears"), so the ghost deck
  reads as the procedure.

| Beat | Layout / exhibit |
|---|---|
| Goal | `split` with a screenshot of the end result |
| Prerequisites | `concept`, ≤ 3 bullets; versions and commands as `mono` bullets |
| Step *n* | `split` screenshot (caption = what you should see), or `full-exhibit` for code |
| Success check | `split` with the expected output |
| Common errors | `table`: symptom · cause · fix |
| Practice | `engagement.type:"activity"` or a quiz |

Ghost deck:
1. *By the end, the dashboard runs on your laptop*
2. *You need Python 3.11, git and read access to the repo*
3. *Clone the repo; a `dashboard/` folder appears*
4. *Install dependencies; the last line says "Successfully installed"*
5. *Start the server; localhost:8000 shows the login page*
6. *"Port in use" means an old server is still running: stop it*
7. *Next: connect your own data source*

**Live vs. read:**
- Live: the presenter does each step, learners follow, and an activity checks the result.
- Read: each step is self-contained, with exact commands, expected output and the fix for the
  common error. Nothing depends on the notes.

---

## The ghost-deck test, per playbook
- **Executive:** could a board member who reads only the titles make the decision? If not, the
  decision or the evidence is missing from a title.
- **Investor:** do the titles say problem, proof and ask, with the amount?
- **Students:** do the titles read as a lesson: question, idea, example, try it, recap?
- **Technical:** is every title a falsifiable claim with a measurement behind it?
- **Self-read:** do headlines and captions alone carry the argument without speaker notes?
- **Demo:** does each title state an observed result, not a feature name?
- **Research:** do the titles state the question, the method, each finding, its limit and the answer?
- **Data briefing:** does each finding title state what moved, by how much, against what baseline?
- **Marketing / launch:** do the titles name what's new, for whom, the proof and how to get it?
- **Sale:** does the first title say the buyer's need, and the last a dated next step?
- **Architecture:** do the titles go from context down to the decision without skipping a level?
- **Tutorial:** could someone follow the procedure from the titles alone?

## Same sources, different playbook
When the audience changes, the fact sheet stays. Re-run this choice, then re-plan:

- The student deck explains the mechanism with a worked example and checks understanding.
- The executive deck opens with the decision and the one number, and moves the mechanism to the
  appendix.

No new numbers appear.
