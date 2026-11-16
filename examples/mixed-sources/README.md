# One source set, two decks

A worked example of the studio's main promise: the same facts, cut for two audiences and in two visual
directions. Everything here is sample material: the organisation and its numbers are invented.

## Sources (`sources/`)
| id | file | kind | used for |
|---|---|---|---|
| `notes` | `notes.md` | text (Markdown) | background, team observations, costs, recommendation |
| `results` | `results.csv` | table (A–D, 6 months) | click and report rates; every chart and number |
| `dash` | `dashboard.png` | original screenshot (rendered locally from the CSV) | evidence slide (executive deck) |
| `attack` | attack.mitre.org/techniques/T1566 | public web page | naming the technique (student deck) |

Both blueprints carry the same `sources[]`. Each slide's `citations[]` points at a locator
(`results.csv!C2:C7`, `notes.md` section). Derived figures are marked `derived` (−67% is computed from two
cells), and the team's untested estimate is marked `disputed`.

## The two decks
| | `students-he.blueprint.json` | `exec-he.blueprint.json` |
|---|---|---|
| Audience | first-year students, lay, **learn** | management, informed, **decide** |
| Delivery mode | workshop (20 min) | exec-briefing (8 min) |
| Sequence | question → model (chain) → worked example (sequence) → trend (line) → quiz → summary → ask | decision → one number (big-number) → trend (column, two series) → options & risks (table) → evidence screenshot (split) → ask |
| Evidence type | worked example, guessing question, quiz with feedback per option | one decisive number, comparison of options, a dashboard |
| Direction | `classroom-workshop`: green/orange, numbered kickers, rounded cards, grid | `executive-data-briefing`: navy/amber, running head, hairline frames, compact titles |
| Interaction | posed question + quiz (live in HTML; answer slide in PPTX/PDF) | none |

## Build
```bash
examples/mixed-sources/build.sh      # HTML + PPTX + PDF for both decks → examples/mixed-sources/build/ (git-ignored)
```
Or by hand, e.g. `python shared/render_html.py examples/mixed-sources/exec-he.blueprint.json /tmp/exec examples/mixed-sources`.

To make another deck from these sources, run `/new-deck` with the files in `sources/` and a new
audience. The pipeline keeps the facts and rebuilds the sequence, depth and evidence.
