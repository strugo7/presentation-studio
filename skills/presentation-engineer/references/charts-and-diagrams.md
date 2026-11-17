# Charts & diagrams — choose the exhibit by what it must show

Pick the exhibit from the **relationship** in the data, not from habit. Two well-known guides organise
this: the **FT Visual Vocabulary** (Financial Times, github.com/Financial-Times/chart-doctor — groups
charts by relationship: deviation, correlation, ranking, distribution, change over time, magnitude,
part-to-whole, spatial, flow) and **Datawrapper Academy**'s chart-type guidance
(academy.datawrapper.de). This file turns them into rules our renderers support.

## 0. Write the question before you pick the chart
The same data can need different charts for different takeaways
([Storytelling with Data, "Different takeaway, different graph"](https://www.storytellingwithdata.com/blog/different-takeaway-different-graph)).
So, in this order:

1. Write the question the slide answers ("Which teams report least?").
2. Write the takeaway as the action title ("Finance and Sales report least of all teams").
3. Only then pick the exhibit from the table below.

A chart chosen before the question tends to show everything and say nothing.

## 1. Decision rule

| What the slide must show | Exhibit | Blueprint |
|---|---|---|
| Change over time (trend, before/after across periods) | **Line** | `chart`, `kind:"line"` |
| Compare categories (magnitude, ranking) | **Column** (few, short labels) or **bar** (long labels, many items, ranking) | `kind:"column"` / `"bar"` |
| Rank categories (which is biggest, in order) | **Horizontal bar**, sorted largest first, label at the start of each bar, value at its end | `kind:"bar"`, categories pre-sorted, `highlight` the one the title names |
| Relationship between two measures | **Scatter**, only with enough points (≳ 10) | `kind:"scatter"`, `points` |
| One unambiguous number that carries the slide | **Big number** with unit, context, source | `layout:"big-number"`, `exhibit.bigNumber` |
| Exact values the audience must read or compare cell by cell | **Table** | `table` |
| Process, sequence, causal chain | **Chain** diagram | `diagram`, `kind:"chain"` |
| Messages between actors over time (protocols, handoffs) | **Sequence** diagram | `diagram`, `kind:"sequence"` |
| Events on a time axis | **Timeline** | `diagram`, `kind:"timeline"` |
| Part-to-whole | Column/bar of shares (sorted) or a table; pie is not supported and falls back to a table | `column` + `unit:"%"` |

One exhibit per slide. One message per exhibit: say it in the title, point at it with `highlight` (bar or
point index) and `annotate`.

## 2. When each choice misleads (check before you hand off)
- **Truncated axis on bars/columns.** Bar length encodes value, so bars start at zero. The renderers
  enforce zero for column/bar; validation warns if `yMin` is set. Lines may start above zero when the
  change is the point — say so in the caption.
- **Mixed units or periods** in one chart (ms and %, monthly and yearly). Split into two slides or convert.
- **Missing categories** (dropping the bad quarter, the one cohort that failed). Show all, or state what's
  excluded and why in the caption.
- **Uneven time steps** drawn as even categories on a line. Use actual dates or a column chart.
- **Dual axes.** Not supported on purpose: two charts or an indexed line (base = 100).
- **Too many series.** More than 3–4 lines → highlight one, grey the rest, or split.
- **Precision theatre.** `decimals` should match the measurement's real precision.
- **Correlation dressed as cause** in the title. "X rose as Y fell" ≠ "X cut Y" without design that shows cause.
- **Scatter with five points.** Use a table.

## 2b. Sample size, uncertainty and limits
The schema has **no error bars, intervals or confidence bands**, and none of the renderers draws them.
When uncertainty changes how the result should be read, show it another way:

- **Caption.** Give n and the interval in words: "n = 412; 95% CI 61–74%".
- **Table.** Add `low` / `high` columns next to the estimate, when exact bounds matter.
- **Separate series.** Draw an estimate or projection as its own series, named "estimate", with
  `kind:"derived"` on the citation.
- **Limits slide.** Use one when exclusions or a small sample change what the result means
  (deck-playbooks.md #7).

If a field needs real interval graphics, export the chart as an image from the analysis tool
(with `alt` and a PNG `fallbackPath`). Note the gap in the hand-off.

## 3. Data hygiene the renderers rely on
- Every chart carries `unit` (and `yLabel` when the unit alone isn't clear) and a citation on the slide.
- **Unit, period, baseline.** The title or caption says what is measured, over which period, compared
  with what ("vs. Q1", "vs. the old method"). A number without a baseline can't be judged.
- **Respect the axis range.** Bars and columns start at zero. A line's range is stated when it doesn't
  start at zero.
- **Let the reader check the source.** The citation `locator` points to the cells (`results.csv!C2:C7`).
  In `self-read` decks, also put the chart's numbers in an appendix table.
- **`highlight` is drawn; `annotate` is not.** The renderers colour the `highlight` bar or point in
  `accent2`. `annotate` is a planning note for the writer and designer. Put the words it implies into the
  caption or a bullet.
- Series lengths equal category counts (validation errors otherwise).
- Category labels short; long ones → `bar`.
- HTML and PPTX read the same spec (`blueprint_lib.chart_spec`): values, units, categories, series names
  and number format match across formats. PPTX charts stay native and editable.

## 4. Diagrams: structure, not decoration
- **Chain** — steps in order (≤ 6). The last step is emphasised as the outcome.
- **Sequence** — actors left/right (reading start = first actor; RTL decks place it on the right), messages
  top to bottom, `emphasis:true` on the message the slide is about. Example (TLS 1.3 handshake):

  ```json
  { "kind": "sequence", "actors": ["Client", "Server"], "messages": [
    { "from": "Client", "to": "Server", "label": "ClientHello + key_share" },
    { "from": "Server", "to": "Client", "label": "ServerHello + key_share, {Finished}" },
    { "from": "Client", "to": "Server", "label": "{Finished} + HTTP request", "emphasis": true } ] }
  ```
- **Timeline** — dated events; keep ≤ 6 per slide; split long histories.
- **Mermaid** is optional: if a Mermaid CLI (`mmdc`) is available, you may export complex flows to SVG +
  a PNG `fallbackPath`, add the file as an asset with `alt`, and reference it as an `image` exhibit. Without
  it, use the native `diagram` kinds above — they render in HTML and PPTX with no extra tools.

## 4b. Architecture and procedures: choose the level first
- **Architecture (C4).** Pick the level the question needs ([c4model.com/diagrams](https://c4model.com/diagrams)):
  - **context**: the system, its users and the external systems;
  - **containers**: apps, services and stores;
  - **components**: inside one container, and only where the decision is.

  Start at context and go one level deeper per slide. There is no native box-and-arrow diagram, so
  export complex C4 or Mermaid views as an image (§4). Use a `chain` when the parts form a pipeline.
- **Interaction order.** Use `sequence` when the question is who calls whom, in what order. Mark the
  message the slide is about with `emphasis`.
- **Procedures.** A tutorial step is a screenshot or a code block, with a caption that says what the
  reader should see
  ([Google Technical Writing, illustrations](https://developers.google.com/tech-writing/two/illustrations)).
  Keep a `chain` for the overview of all the steps.

## 5. Documentary image vs. explanatory diagram
Keep them apart and say which is which:
- A **screenshot or photo** is evidence that something happened or looks a certain way (kind `screenshot`,
  credited, captioned with where/when it was taken).
- A **diagram** explains structure; it's a model, not evidence.
Example — a talk on the Petya ransomware: the ransom screen is a documentary screenshot (cite its
source); the explanation of how it overwrote the disk's boot structures is a diagram you draw (a `chain`:
MBR overwritten → fake CHKDSK → MFT encrypted → ransom screen). Don't present the diagram as if it were a
captured artefact, and don't stretch a screenshot to explain internals it doesn't show.

## 6. Assertion–evidence check (from Michael Alley's research-talk models)
For each evidence slide: the title is a full-sentence claim; the exhibit alone would let a sceptic check
the claim; the bullets (if any) only point at what to look at. If the title could be swapped onto another
slide without lying, it isn't an assertion yet.
