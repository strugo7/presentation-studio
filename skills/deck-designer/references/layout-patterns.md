# Layout patterns — original specs, one content job per slide

Nine patterns, a table of reference compositions (§10) and device frames (§11). Each one maps onto what the renderers actually implement: four `layout` values
(`statement`, `split`, `full-exhibit`, `big-number`), the role defaults, and the diagram kinds. Every
pattern lists:

- **Fit**: when to use it.
- **Grid**: how the 1920×1080 stage is divided.
- **Hierarchy**: what the eye reads first.
- **Long text**: what happens when copy runs long.
- **Static fallback**: the PDF/print state.
- **RTL check**: what to verify in right-to-left decks.

Margins come from the design-system token `margin` (110–150 px). "Start" means right in RTL, left in LTR.

---

### 1. Typographic cover — `role: cover` (no layout)
- **Fit:** every deck; the title is a claim or a question.
- **Grid:** dark canvas. A title block 60–75% wide, anchored to the start edge
  (`coverAlign: start`) or centred (`keynote`, `editorial`).
- **Hierarchy:** title (150 px × `titleScale`) → subtitle → authors/event.
- **Long text:** over ~48 characters, the title steps down by length (`title_scale_for`), never below
  the floor. If it's still too long, cut words. Never shrink to fit.
- **Static fallback:** identical.
- **RTL check:** Latin product names and versions inside the title keep their visual order
  (e.g. "TLS 1.3"); the eyebrow aligns with the title.

### 2. Split with a product screen — `layout: split`
- **Fit:** showing a product, interface or a single photo next to its meaning.
- **Grid:** 50/50.
  - The visual half holds a photo (`image`), which bleeds and crops, or a screenshot or chart, which
    sits whole on a `bgAlt` panel with 70 px padding. Never crop a screenshot.
  - The text half holds kicker → title (82% scale) → ≤ 2 bullets / engagement.
- **Hierarchy:** the image is seen first, then the title explains it.
- **Long text:** more than 2 bullets → move them to speaker notes, or switch to `full-exhibit`.
- **Static fallback:** identical.
- **RTL check:** `exhibit.side` names the physical side, the same in both formats. In RTL, `side:
  "right"` puts the image at the reading start (strong); `"left"` puts it after the text.

### 3. Big evidence with caption — `layout: full-exhibit`
- **Fit:** a chart, table, sequence diagram or screenshot that needs the full width to be read.
- **Grid:** small header (kicker + title ≤ 2 lines). The exhibit fills the width from y=250 to y=940.
  Bullets collapse into one line under it. Citation goes in the footer.
- **Hierarchy:** title (the claim) → exhibit's highlighted element → caption.
- **Long text:** caption ≤ 1 line on slide, more in notes. A table over 6 rows → split, or put the
  full table in the appendix.
- **Static fallback:** identical. For tables, print the full table in the appendix.
- **RTL check:** chart axes stay LTR (time runs left→right, the same in PPTX); labels are RTL text.
  Tables mirror column order.

### 4. Conclusion with one number — `layout: big-number`
- **Fit:** one decisive figure carries the slide: the executive summary, the payoff of a section.
- **Grid:** the number (290 px, `accent2`) sits at the start edge. Under it: a context line (what,
  where, when) → the title as the claim (58 px) → ≤ 2 bullets.
- **Hierarchy:** number → context → claim.
- **Long text:** the context line stays ≤ 90 characters. The claim must work without the number.
- **Static fallback:** identical.
- **RTL check:** the number is isolated LTR (so "−46.5%" keeps its sign and order). The unit
  follows the number.

### 5. Comparison — `role: comparison` + `table` (or two `split` slides)
- **Fit:** options × criteria, before/after, ours vs. theirs.
- **Grid:** a full-width table with the header row in `dark` and banded rows. ≤ 4 columns,
  ≤ 6 rows. One takeaway bullet under the table.
- **Hierarchy:** title states the winner or trade-off → the decisive row or column.
- **Long text:** abbreviate criteria. Move detail to the appendix.
- **Static fallback:** identical.
- **RTL check:** the first column (row labels) sits on the right. Numbers in cells stay LTR.

### 6. Timeline — `diagram`, `kind: timeline`
- **Fit:** dated events, a project plan, a history with ≤ 6 moments.
- **Grid:** a horizontal rule at the top of the body. Each event has a dot, a date (accent, bold) and
  a label (≤ 6 words). The last event is in `accent2`.
- **Hierarchy:** the sequence first, then the event the title is about.
- **Long text:** over 6 events → two slides (e.g. before/after the turning point).
- **Static fallback:** identical.
- **RTL check:** events run from the reading start (right in RTL), matching chain diagrams.

### 7. Technical diagram — `diagram`, `kind: sequence` / `chain` (usually in `full-exhibit`)
- **Fit:** protocols, request flows, pipelines, cause → effect.
- **Grid:**
  - Sequence: actors as dark boxes at the top with dashed lifelines, and messages as arrows top to
    bottom, ~96 px apart.
  - Chain: ≤ 6 equal cards; the last card is dark.
- **Hierarchy:** the emphasised message or step (`emphasis: true`, or the last card) is what the title names.
- **Long text:** message labels ≤ ~40 characters. Abbreviate payloads, explain them in notes.
- **Static fallback:** identical.
- **RTL check:** the first actor is on the right. Arrow directions follow the actors' positions.
  Protocol tokens stay LTR.

### 8. Practice slide — `concept` + `engagement.type: quiz`
- **Fit:** checking understanding right after a worked example; every 8–10 minutes in a workshop.
- **Grid:** the question card (prompt + 3–4 options as full-width buttons) on the text side. Any
  exhibit the question refers to goes on the other side.
- **Hierarchy:** prompt → options → feedback line.
- **Long text:** options ≤ 1 line each. Explanations go in `feedback`, not in the option text.
- **Static fallback:** the answer slide follows (or goes to the appendix / inline) per `answerPlacement`.
- **RTL check:** arrow keys move between options in reading order. Mixed Latin answers render correctly.

### 9. Self-contained summary — `layout: statement` (light) or `concept`
- **Fit:** the last content slide; the slide a reader of the PDF keeps.
- **Grid:** one sentence that states the conclusion, plus ≤ 3 short lines: what, why, next step.
  No exhibit.
- **Hierarchy:** the conclusion sentence.
- **Long text:** if it needs more than 3 lines, the argument isn't finished. Go back to the ghost deck.
- **Static fallback:** identical.
- **RTL check:** alignment matches the design system (start or centre).

### 10. Reference compositions → our layouts (from the viewed slides)
Slides viewed for design-gallery.md #14–19, translated into what the renderers can do. Use them as
**role pairs**: an explanation slide followed by an evidence slide reads better than either alone.

| Composition seen | Use here | What our renderers can't do (and the workaround) |
|---|---|---|
| Spacious start-aligned cover over a faint grid (#14) | role `cover`, `coverAlign: start` | no grid on dark slides; the empty space is the point |
| Photo of a person on one half, ≤ 6-word claim on the other (#15) | `split`, photo bleeds | no per-word colour: put the key word first |
| Product image filling the slide, short notes next to the parts (#16) | `split`, image + ≤ 2 bullets naming the parts in reading order | no call-outs on the image: bake them into the asset (then `alt` names them; a re-cut needs new art) |
| Two columns on one baseline, values shown, leader emphasised (#17) | `full-exhibit`, `column`, `highlight` | no dashed reference line or bracket: the gain goes in the title and caption |
| Six numbered entries in a 2×3 index (#18) | role `agenda` (≤ 4 tiles), or a `table` | **gap**: no index-grid layout; candidate for a new layout value |
| Ranked horizontal bars, value at the end (#19) | `full-exhibit`, `bar`, categories sorted | no pale track behind bars (not needed) |

**Check at display size.** A detail that reads on a laptop disappears on a projector. Small caps
metadata, axis labels and footers must hold at the room's distance. Look at the rendered slide full screen
(or the direction preview's full-size view) before hand-off, in RTL as well as LTR.

### 11. Device frames — `exhibit.device` / `exhibit.devices`
- **Fit:** product demos, launches and sales decks where *where* the product runs matters (desktop,
  phone, web), or where a bare screenshot would read as a document scan.
- **Don't frame:**
  - dense evidence that must be read cell by cell (use `full-exhibit` without a frame, or a table);
  - a UI that is the hero and fills the slide (show the screen alone, no frame);
  - a mood photo.
- **Which device:**

  | The screenshot is… | Frame |
  |---|---|
  | a mobile app | `phone` |
  | a desktop app or a dashboard | `laptop` |
  | a web app the audience will open | `browser` (+ `exhibit.url`, display only) |
  | an iPad-style app | `tablet` |
- **Several devices:** `exhibit.devices` takes up to 3 screens, each `{device, ref, label}`.
  - `arrangement: "row"` (default): side by side on one baseline. Phones are drawn smaller than
    laptops, as in life. Use it for the same app on iOS and Android, or one capability across
    products. Keep labels short ("iOS", "Android").
  - `arrangement: "overlap"` (2 devices): the second sits over the first's front **start** corner
    (bottom-right in RTL). Use it for "same product on desktop and phone".
  - Put the **same content** on both screens to prove an integration or a handoff. Different
    content on two screens is two slides.
- **Loupe:** `exhibit.loupe` (or `devices[i].loupe`) = `{x, y, w, h}` as fractions of the screenshot.
  It draws a round magnifier over that region, so the one detail the title names is legible at
  projection distance while the screenshot stays whole. One loupe per slide. It also serves as the
  static twin of a region zoom (which isn't built).
- **Grid:** in `split`, the frame fills the visual half on the `bgAlt` panel. In `full-exhibit`, the
  row is centred under the title, with the caption below.
- **Hierarchy:** device (seen first) → the loupe detail → title.
- **Long text:** frames take ≤ 2 bullets in `split`. Feature lists go to notes or the next slide.
- **Static fallback:** identical in HTML, PPTX (editable shapes + picture) and PDF.
- **RTL check:**
  - The order of devices flips: the first device sits at the reading start (right).
  - **The device art and the screenshots are never mirrored.**
  - The loupe stays on the region it magnifies.
  - `exhibit.url` stays LTR.
- **Screenshots:**
  - Use fictional data.
  - No blank screens.
  - Export phones at 2× (e.g. 780×1688 for a 390×844 design) so text survives projection.
  - The screen takes the screenshot's own aspect ratio (within a sensible range per device), so it's
    never cropped.

---

## Choosing per slide (designer's quick rule)
1. Is there one number that carries it? → `big-number`.
2. Must the exhibit be read in detail? → `full-exhibit`.
3. Is it an image or product plus meaning? → `split`.
4. Is it a single sentence, a question, or a transition? → `statement`.
5. Otherwise, leave `layout` empty: the role default (title on top, exhibit on its side, bullets
   opposite) is right.

Vary the rhythm. Three `full-exhibit` slides in a row read like a report; insert a `statement` or
`big-number` beat. Don't give every slide a different layout either. Repeat a layout when the content
job repeats.

**Live vs. read density** (design-gallery.md #7–9). In a `live-talk` or `pitch`, a slide that explains
everything competes with the speaker: prefer `statement` / `big-number` and put the explanation in the
notes. In `self-read`, the slide must carry the explanation: fuller captions and `full-exhibit`/`split`.
Pick images that work without on-image text, so a language re-cut doesn't need new art.
