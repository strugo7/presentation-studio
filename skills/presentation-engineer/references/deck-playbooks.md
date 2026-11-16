# Deck playbooks — short, reasoned sequences per audience

A playbook is a scaffold (structure-frameworks.md) tuned to a delivery mode and audience. Each has: the
beats, why they're in that order, which `layout` and exhibit each beat usually takes, and a ghost-deck
example. Pick one; don't merge two. The ghost deck — action titles only, in order — must read as the
argument even with every body removed.

Load only the playbook you're using. Design references for these sequences (with what each teaches):
deck-designer/references/design-gallery.md.

---

## 1. Executive decision brief (`exec-briefing`, management)
**Beats:** Decision → Evidence → Alternatives & risks → Next step.
**Why:** executives allocate attention by decision; give the answer first (Minto), then only the
evidence that would change their mind. Alternatives show you considered them; owning the risk earns
trust. Method and detail live in the appendix, reachable but not presented.

| Beat | Layout / exhibit | Engagement |
|---|---|---|
| Decision (the recommendation in one sentence + the ask) | `statement` | — |
| The decisive number | `big-number` (value, unit, context, source) | — |
| 1–2 evidence slides | `full-exhibit` chart or table, one point each | — |
| Alternatives & risks | `comparison` table (option × cost × risk × time) | — |
| Next step (who, what, when) | `statement` close | decision stays on screen |
| Appendix: method, data definitions | `references`/`appendix` | — |

Ghost deck: *Move onboarding to four 90-minute sessions next cohort* → *Two-week retention nearly
doubles when sessions are spaced* → *The gain held across all three pilot groups* → *Cost: four calendar
holds instead of one; risk: attendance drop, mitigated by fixed slots* → *Approve the pilot today; results
in six weeks.*

## 2. Investor pitch (`pitch`)
**Beats:** Problem → Solution → Proof of traction/progress → Ask.
**Why:** investors pattern-match on a painful, large problem and evidence that you're winning; the ask
must be specific ("$X to reach Y by Z"). Team and market slot in after proof, briefly.

| Beat | Layout / exhibit |
|---|---|
| Problem (quantified, felt) | `statement` or `big-number` |
| Solution (one sentence, then show it) | `split` with product screenshot |
| How it works (just enough) | diagram `chain` |
| Traction | `full-exhibit` line chart (growth over time), customer logos only with permission |
| Market / model / team | 1 slide each, `concept` |
| Ask | `statement` close: amount, milestone, date |

## 3. Beginner students (`workshop` or `live-talk`, lay)
**Beats:** Question → Model → Worked example → Practice & feedback.
**Why:** novices learn from a question they care about (activation), a simple model before details
(schema), a fully worked example before solving alone (worked-example effect), and immediate feedback
(retrieval + correction). One new idea per slide; define every term at first use.

| Beat | Layout / exhibit | Engagement |
|---|---|---|
| Question (concrete, from their world) | `statement` | posed question; let them guess |
| Model (the mental picture) | diagram (`chain`/`sequence`) | — |
| Worked example, step by step | `full-exhibit` with reveals per step | — |
| Common mistake | `split` (wrong vs. right) | — |
| Practice | `concept` + `engagement.type:"quiz"` with option-level feedback | quiz, every 8–10 min |
| Summary they can keep | `statement` / self-contained summary | — |

## 4. Technical team (`research` / `live-talk`, expert)
**Beats:** Context → How the system works → Observation → Limitation & what's next.
**Why:** experts want the mechanism and the measurement, and they trust a speaker who names limits.
Titles are assertions (Alley's assertion–evidence): a full-sentence claim, a visual that proves it.

| Beat | Layout / exhibit |
|---|---|
| Context (what problem, what constraint) | `concept` |
| How it works | diagram `sequence` (messages between components) or `chain` |
| Observation (the measurement) | `full-exhibit` line/column chart with units and source |
| Comparison / ablation | `comparison` table |
| Limitation, open questions, next experiment | `concept`, then `close` |

## 5. Document for reading (`self-read`, slidedoc)
**Beats:** Summary → sections with headline + evidence → method appendix.
**Why:** nobody is talking, so each page must stand alone (Duarte's slidedocs): headlines that summarise
the page, captions that explain the exhibit without a narrator, and method/definitions in the appendix.
Text density can be higher, but structured: headline, 2–3 short paragraphs or bullets, one exhibit,
caption with source. Quiz answers are inline (`answerPlacement:"inline"` is the default).

| Beat | Layout / exhibit |
|---|---|
| Executive summary (3 findings, 1 recommendation) | `concept` with bullets |
| Each finding | `full-exhibit` or `split`, caption that stands alone, citation in footer |
| Method, data definitions, sources | `appendix` + generated sources slides |

## 6. Product demo (`demo`)
**Beats:** The user's job → Live demo (or recorded path) → What changed for them → Try it.
Demo slides carry a screenshot fallback (`engagement.type:"demo"` + `assetRef`) so a dead network never
kills the talk.

---

## The ghost-deck test, per playbook
- Executive: could a board member who reads only the titles make the decision? If not, the decision or
  the evidence is missing from a title.
- Students: do the titles read as a lesson — question, idea, example, try it, recap?
- Technical: is every title a falsifiable claim with a measurement behind it?
- Self-read: do headlines + captions alone carry the argument without speaker notes?

## Same sources, different playbook
When the audience changes, the fact sheet stays. Re-run this choice, then re-plan: the student deck
explains the mechanism with a worked example and checks understanding; the executive deck opens with
the decision and the one number, and moves the mechanism to the appendix. No new numbers appear.
