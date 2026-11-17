# Design gallery: real-world references (links only) and what each one teaches

Open this when you are composing a custom direction, when the user says "something like X", or when
you prepare direction previews (deck-designer SKILL §1b). Find
entries by tag and borrow the **principle** (sequence, hierarchy, how evidence is staged, live vs.
read), never the asset. No images, templates or fonts from these sources are stored in this repo (see
asset-sources.md §6). Every entry is **link for analysis only**: none of these pages grants reuse of
its slides.

## How these were checked
Every entry records its **unit of checking**, because the unit limits what the entry can claim:

- **Page text (#1–13).** On 2026-11-17 each page was opened with a plain HTTP fetch and its text was
  read. The slides weren't looked at. "Visual decision" there records only what the page *says*
  about the visuals. Where the page says nothing about a field, it is marked "not stated".
- **Slide screenshot (#14–33).** On 2026-11-17 the published image of **one slide** was downloaded and
  looked at. These entries describe that slide's composition and density, and nothing about the rest of
  the deck or its order.

Sites that block automated readers were not worked around; they are listed under "Not verified".

**Quick map: reference → what to use here**

| Reference | Slide role | Local preset / direction | Layout or exhibit |
|---|---|---|---|
| #14 Signal, cover | cover | `signal`, `executive-data-briefing` | role `cover` |
| #15 Zappos, statement + photo | statement with a story image | `keynote` | `split` (photo bleeds) |
| #16 Thermo Fisher, product + notes | product explanation | `product-demo` | `split` (image + ≤ 2 bullets) |
| #17 Thermo Fisher, comparison | proof / evidence | `product-demo`, `executive-data-briefing` | `full-exhibit` `column` + `highlight` |
| #18 Cobalt Grid, index of six | overview / agenda | `cobalt-grid` | role `agenda` (≤ 4 sections) or a `table`; no 2×3 grid layout yet |
| #19 Blue Professional, ranking | ranking evidence | `cobalt-grid`, `signal` | `full-exhibit` `bar`, sorted |
| #20–21, #30 keynote setup and reveal | setup → reveal | `keynote`, `product-demo` | `statement` |
| #24, #27 device pair / overlap | cross-platform, integration | `product-demo` | `exhibit.devices` (+ `arrangement`) |
| #26 loupe | one detail of a dense screen | `product-demo` | `exhibit.loupe` |

---

## Verified

### 1. Assertion–evidence approach (Michael Alley) · tags: research, technical, students / every content slide / live
- **Source:** assertion-evidence.com (home and the tutorial overview).
- **Scope:** a site that teaches a slide structure, with a tutorial, PowerPoint templates and a collection of model talks.
- **Audience / purpose:** engineers and scientists giving technical talks.
- **Structural decision:**
  - Each slide is built on a succinct **assertion** (a sentence that states the takeaway), supported
    by **visual evidence**.
  - It replaces the default of a phrase headline plus a bullet list.
  - The page names the problem with the default: the headline carries no takeaway, and bullets
    produce clutter, so the audience doesn't know where to look.
- **Visual decision:** a sentence headline and visual evidence instead of bullets. Further detail is in the tutorial, which was not opened.
- **RTL / format:** the structure is language-neutral. Sentence headlines work in Hebrew; keep the evidence's internal axes LTR (layout-patterns.md §3).
- **Our mapping:** action titles plus `full-exhibit`; the ghost-deck test (deck-playbooks.md); the writer's title rules.

### 2. Garner, Alley et al.: effect of slide design on understanding · tags: research, students / evidence for #1
- **Source:** writing.engr.psu.edu/research.html (list of studies with abstracts).
- **What it reports:**
  - **Audience study.** Two audiences heard the same words with different slides: topic headline plus
    bullets, or sentence headline plus visual evidence. The assertion–evidence audience understood
    and remembered more (reported p < .01).
  - **Presenter study.** Students who *built* assertion–evidence slides understood their content
    better. The study attributes this to deeper thinking while preparing.
- **Limit:** these studies are by the method's own authors.
- **Our mapping:** this is the evidence behind requiring claim titles. In a workshop deck, having learners write their own claim titles is itself a learning task (pedagogy.md).

### 3. Model research presentations, assertion–evidence (graduate students) · tags: research, technical / whole talk / live
- **Source:** assertion-evidence.com/research_models.html.
- **Scope:** filmed research talks by PhD students (wind turbines, additive manufacturing, gas turbines, and tensors in computer science), all using assertion–evidence. They come from industry and conference talks.
- **Structural decision:** the page notes one talk whose first main point is built around defining a single concept (a tensor). That suggests a pattern: in a mathematical talk, define the core term as the first assertion. The talks' full sequence was not checked: they are videos.
- **Our mapping:** `research` playbook; the `technical-case` direction.

### 4. Figma Slides product page · tags: product, design review, pitch / live, interactive
- **Source:** figma.com/slides.
- **Scope:** a product page listing templates (**Product review**, **Design review**, **Startup pitch**) and features. The templates themselves were not opened.
- **Structural decision:** the deck is treated as a live working session, not a broadcast:
  - presenter notes and co-presenting;
  - **live polls and voting** saved into the deck;
  - an **alignment scale** that shows where a team agrees;
  - interactive prototypes the audience can click.
- **RTL / format:** not stated.
- **Our mapping:**
  - Supports `engagement` poll and quiz (interaction-patterns.md §1–2) and a `demo` with a URL plus a screenshot fallback.
  - Our poll is local to one device. For a team-alignment vote, name a multi-device tool in `presenterCue`.

### 5. Figma resource library, "What is a slide deck" · tags: general, business, education / deck types
- **Source:** figma.com/resource-library/what-is-a-slide-deck/.
- **Scope:** an explanatory article.
- **The standard components it lists:** title, agenda, content, data and charts, graphics, interactivity, summary.
- **Its five steps:** outline or storyboard first; consistent design; brief text; visuals with alt text and chart contrast; rehearse (aim for under 20 minutes).
- **Five template types:** pitch, product roadmap, marketing strategy, all-hands, project review.
- **Structural decision:** decide the takeaway and the audience (background, knowledge, setting) *before* any slide.
- **Visual decision:** break up text with images and charts without clutter; accessible visuals.
- **Note:** this is generic baseline advice. Use it as the floor, not as the distinctive move.
- **Our mapping:** the brief (grill-me), the outline-first pipeline, `alt` on every asset.

### 6. Liégeois Designs, Marriott Luxury Group: YouTube content strategy · tags: executive, brand, strategy / exec briefing
- **Source:** liegeoisdesigns.com/work/marriott-luxury-group.
- **Scope:** a case-study page for a 2025 executive strategy deck aligning leaders across 8 luxury hotel brands.
- **Structural decision:** diagnosis before recommendation, in this order:
  1. competitive benchmarking and a portfolio audit;
  2. the gaps found (storytelling, consistency, channel impact);
  3. the solution (one unified channel, flagship content franchises);
  4. a playbook (architecture, categories, frequency, amplification).

  The page reports the strategy was approved at senior executive level.
- **Visual decision:** described only as "cinematic", matching the brands. Not otherwise stated.
- **Our mapping:** the `exec-briefing` playbook (audit → gap → decision → playbook as next step); the `editorial-report` / `keynote` direction for premium brands.

### 7. Liégeois Designs, "Slides Don't Present Themselves" (Philips Healthcare example) · tags: sales, live vs. read
- **Source:** liegeoisdesigns.com/blog/slides-as-speaker-support.
- **Argument:**
  - A deck the audience understands without the presenter is a *document*.
  - A dense slide splits attention, because people read instead of listening.
- **Example:** a sales-enablement deck for non-technical executives was rebuilt with "deliberate incompleteness":
  - a dramatic visual and one question headline per slide;
  - the presenter completes the story in conversation.

  The page reports that meetings felt like conversations instead of demonstrations. It is a practitioner's account, not a study.
- **Our mapping:**
  - For `live-talk` / `pitch`, prefer `statement` and `big-number`, and move the explanation into notes.
  - For `self-read`, do the opposite (see #8). The same content is cut differently for each mode (presentation-studio's re-cut table).

### 8. Duarte, *Slidedocs*® · tags: self-read, pre-read, leave-behind / pdf
- **Source:** duarte.com/resources/books/slidedocs/. There is also a guide at duarte.com/resources/guides-tools/how-to-improve-dense-slides-with-slidedocs/, but its body did not appear in the fetched text.
- **Scope:** the page for Nancy Duarte's free e-book, plus training and templates.
- **Structural decision:** slidedocs are visual documents built with slide software. Teams read them at their own pace, as **pre-reads** or **leave-behinds**, so the message works when the presenter isn't in the room.
- **Not verified:** word counts per page (seen only in search snippets).
- **Our mapping:** `deliveryMode: self-read`:
  - no reveals;
  - `answerPlacement: inline`;
  - a stand-alone summary (layout-patterns.md §9);
  - fuller captions are allowed.

### 9. Duarte case study: Zappos "walking deck" · tags: keynote, thought leadership / reusable deck
- **Source:** duarte.com/approach/case-studies/designing-a-workhorse-walking-deck-for-zappos-to-quickly-share-their-brand/.
- **Scope:** a case-study page about one reusable keynote deck, presented worldwide and later refreshed.
- **Structural decision:** one deck that works for diverse audiences, carrying the speaker's point of view.
- **Visual decision:** simple **statement slides** combined with visuals that communicate "without requiring a shared language". The brand is described as bright, vibrant and quirky.
- **Our mapping:** the `keynote` direction; `statement` slides; image-led meaning. Also a reason to keep text out of images, so a Hebrew or English re-cut doesn't need new art. One slide from this case was viewed: #15.

### 10. Duarte case study: VMware ESG report as a data story · tags: report, data, self-read
- **Source:** duarte.com/approach/case-studies/reimagining-vmwares-high-stakes-industry-report-as-a-stunning-data-story/.
- **Scope:** a case-study page about an annual ESG report.
- **Structural decision:** a content-strategy phase produced a **narrative framework** before any design. The aim was to turn a long list of dry data points into a story of impact.
- **Visual decision:** charts, diagrams and custom illustrations, designed so they can be reused on the website and social media.
- **Our mapping:**
  - The `editorial-report` direction.
  - The engineer's outline comes before the designer.
  - One `chart_spec` feeds every format, so exhibits can be reused.

### 11. Duarte case study: Thermo Fisher product launch · tags: product, technical → customers / data story
- **Source:** duarte.com/approach/case-studies/delivering-complex-tech-as-an-engaging-product-launch-for-thermo-fisher/.
- **Scope:** a case-study page about a mass-spectrometry launch deck for customers.
- **Structural decision:** the content team first pulled the most important messages out of complex charts. The design then showed how the product outperforms competitors.
- **Visual decision:** bold text, bright colours, **simple charts**, and 3D product renders with animation.
- **Result (company-reported):** sales beat projections several times over, and the visuals were reused across the website and collateral.
- **Our mapping:** charts-and-diagrams.md (one message per chart, highlight the comparison); the `product-demo` direction. Two slides from this case were viewed: #16–17.

### 12. BrightCarbon portfolio: Aegis AI partnership presentation · tags: technical, partnership / framework diagram, animation
- **Source:** brightcarbon.com/portfolio/aeigs-ai-partnership-presentation/ (sic: the URL slug reads "aeigs").
- **Scope:** a portfolio entry for a trade-show presentation.
- **Structural decision:** one **flexible framework visual**. It shows the big picture at a glance, then serves as the map for explaining each component in turn.
- **Motion:** animation keeps the audience oriented in the whole while they follow the data through the technology layers.
- **Our mapping:**
  - The `navigation.mode: zoom` hub (agenda/map slide → section → back).
  - A diagram reused across slides with one part emphasised.
  - interaction-patterns.md §7 ("animate what changes").

### 13. BrightCarbon portfolio: Eigen Technologies overview · tags: sales, multi-industry / live and leave-behind
- **Source:** brightcarbon.com/portfolio/eigen-technologies-overview-presentation/.
- **Scope:** a portfolio entry for a core sales story tailored to different industry customers.
- **Structural decision:** delivered **both** as an animated presentation and as a static document circulated after the meeting.
- **Our mapping:** this is exactly our one-blueprint, many-formats model:
  - HTML or PPTX with reveals for the meeting;
  - PDF with every reveal shown and answers placed for the leave-behind;
  - an audience re-cut per industry (playbooks).

---

## Slide screenshots viewed (one slide each, 2026-11-17)

These are compositions to translate, not assets. Images aren't stored in this repo. The template
screenshots (#14, #18, #19) come from `zarazhangrui/beautiful-html-templates` (MIT), a library of
34 HTML slide templates. It is a sibling of Frontend Slides, not the same thing: Frontend Slides'
own `STYLE_PRESETS.md` has a preset called "Bold Signal" (charcoal and orange, Archivo Black). That is a
different design from the template called "Signal" here.

### 14. Signal, slide 1 (cover) · tags: executive, report, research / cover / live and read
- **Source:** [signal-1.png](https://raw.githubusercontent.com/zarazhangrui/beautiful-html-templates/main/screenshots/signal-1.png).
  The library describes the template as "deep navy canvas with bone paper and a single muted-gold
  accent; institutional with quiet weight".
- **Unit checked:** one cover screenshot, 1920×1080.
- **What the slide shows:**
  - A very large serif title, set at the start edge in the lower half, two lines.
  - A wide empty field above it.
  - A faint square grid over a deep navy canvas.
  - A monospace caps metadata line above the title (period · audience · deck type), with a short gold
    rule between the two.
  - A muted serif subtitle under the title.
  - A hairline footer rule with author on one side and version/status on the other.
- **Role:** cover; sets an institutional, unhurried tone.
- **What to translate:**
  - Generous empty space above a start-aligned title. Our cover already anchors to the start edge
    (`coverAlign: start`).
  - The grid as an *optional* anchor. In our `signal` it's a light-slide motif (`motif: grid` in
    `cobalt-grid`); the dark cover stays plain.
  - Use a Hebrew font (Assistant, or Frank Ruhl Libre for a serif feel), never a Latin serif for Hebrew
    text.
  - Enlarge secondary details if they matter: the metadata line is tiny at projection distance.
    In our cover it's the `kicker`/eyebrow and `meta.authors`, at readable sizes.
- **Differs from our `signal`:** ours uses Assistant (sans), a steel-blue accent (`2C5F7C`) and amber
  for the payoff, and has no grid on the cover. The shared idea is the navy canvas, the restraint and
  the start alignment.
- **RTL / format:** in RTL the title block anchors right. The short rule above the title is a
  decorative bar, which design-systems.md's "don'ts" exclude, so skip it. Identical in HTML, PPTX, PDF.

### 15. Duarte, Zappos walking deck: statement with photo · tags: keynote, brand, marketing / statement / live
- **Source:** [Zappos block image 2](https://www.duarte.com/wp-content/uploads/2024/05/Duarte-Case-study-zappos-Block-image-2-1.jpg), from #9.
- **Unit checked:** one slide image, 1000×563.
- **What the slide shows:** a cut-out photo of a person looking at a phone fills one half. A short claim
  in two lines of spaced caps sits on the other half, on a deep blue field. The first word is in a
  contrasting colour (pink), so the eye lands on the key word first. Hand-drawn line accents surround
  the person.
- **Role:** a statement slide where the image plays a story role (the consumer); the claim is short.
- **What to translate:**
  - `split` in a marketing or keynote deck: a photo that bleeds on one half and a title of ≤ 6 words on
    the other.
  - Emphasis by colour on one word isn't something our renderers do per word. Put the key word first,
    and let weight and size carry it.
  - On an **evidence** slide, prefer an illustration that explains the claim over a mood photo.
- **RTL / format:** in RTL put the photo with `exhibit.side:"left"` so the text starts on the right; or
  `"right"` when the image should be read first (layout-patterns.md §2). Keep text out of the photo so
  a language re-cut doesn't need new art.

### 16. Duarte, Thermo Fisher launch: product with nearby notes · tags: product, launch, technical → customers / explanation
- **Source:** [Thermo Fisher block image 1](https://www.duarte.com/wp-content/uploads/2024/07/Duarte-Case-study-ThermoFisher-block-image-1-1.jpg), from #11.
- **Unit checked:** one slide image, 1000×563.
- **What the slide shows:**
  - A 3D render of the instrument fills most of the slide.
  - Two short labelled notes sit right next to the components they describe: a bold name, then 2–4
    short lines, joined to the part by a thin leader line.
  - The slide title sits in a corner, in large white type.
- **Role:** explaining a component: where it is and what it does.
- **What to translate:** a **pair of slide roles**: this one (component + notes close to it), followed
  by a comparison-evidence slide (#17). This is a reading of two slides, not the order of the original
  deck.
- **How to build it here:**
  - Our renderers can't place call-outs on an image. Use `split` with the image, and ≤ 2 bullets on the
    text half, each starting with the part's name, in the image's reading order (`bullet.lead` for the
    name).
  - If the call-outs must sit on the image, bake them into the image asset. Its `alt` then names the
    parts, and a Hebrew cut needs its own image.
- **RTL / format:** the bullet order follows reading order (right to left). Identical in all formats.

### 17. Duarte, Thermo Fisher launch: two-bar comparison · tags: product, data, launch / evidence
- **Source:** [Thermo Fisher block image 3](https://www.duarte.com/wp-content/uploads/2024/07/Duarte-Case-study-ThermoFisher-block-image-3-1.jpg), from #11.
- **Unit checked:** one slide image, 1000×563.
- **What the slide shows:**
  - Two columns on a shared baseline: grey for current methods, a saturated gradient for the product.
  - The value is printed on top of each column.
  - A dashed line carries the shorter column's height across to the taller one. A bracket marks the
    difference, labelled with the gain.
  - Each column has a large text statement beside it, the leading side in the accent colour.
  - In the image the column heights look proportional to the values, read from a zero baseline.
- **Role:** proof: one comparison, one message.
- **What to translate:** `full-exhibit` with `chart.kind:"column"`, two categories, `highlight` on the
  leader. Our renderers print values and colour the highlight in `accent2`, with bars from zero.
  - The dashed reference line and bracket aren't drawn by our renderers. State the gain in the title
    ("40% deeper coverage in the same hour") and in the caption.
  - Keep the claim's conditions (same time, same sample) in the caption.
- **RTL / format:** column charts keep LTR geometry. Put the baseline category first (left) and the
  leader second, so time and "better" read left → right as the axis does. Native editable chart in
  PPTX.

### 18. Cobalt Grid, slide 3: an index in six entries · tags: overview, agenda, editorial / index
- **Source:** [cobalt-grid-3.png](https://raw.githubusercontent.com/zarazhangrui/beautiful-html-templates/main/screenshots/cobalt-grid-3.png).
  The library describes the template as "electric cobalt italic serifs on a graph-paper canvas,
  anchored by stair-stepped pixel-glitch decorations and slim hairline rules".
- **Unit checked:** one content slide, 1920×1080.
- **What the slide shows:**
  - Six items in two columns × three rows, separated by hairline rules.
  - Each item has a small monospace number (01.–06.), a short serif heading and one explanatory line.
  - Everything is in one cobalt ink on a warm paper canvas. No graph-paper grid shows on this slide at
    this size.
  - The large title sits at the top, with a small tracked caps label at the opposite end.
- **Role:** an index or overview of topics.
- **What to translate:**
  - Use it for an agenda or a "what's in this report" slide: number + short heading + one line.
  - **Gap:** our renderers have no 2×3 index layout. The `agenda` role draws one row of tiles per
    section, which works up to about 4 sections. A `table` (number · heading · line) keeps all six in
    reading order.
  - A dedicated index layout is a candidate for a new layout value.
- **Differs from our `cobalt-grid`:** ours is a sans (Assistant) system on white with a faint graph
  grid, a steel-blue default accent and rounded cards. The shared ideas are the ledger calm, the hairline
  rules and a single accent.
- **RTL / format:** in a Hebrew deck, item 01 starts at the **right** column, top. Check the reading order
  in the output (a `table` mirrors column order in both HTML and PPTX).

### 19. Blue Professional, slide 6: horizontal ranking · tags: data, executive, report / ranking evidence
- **Source:** [blue-professional-6.png](https://raw.githubusercontent.com/zarazhangrui/beautiful-html-templates/main/screenshots/blue-professional-6.png).
  The library describes the template as "cream paper background with electric cobalt blue accents".
- **Unit checked:** one content slide, 1920×1080.
- **What the slide shows:**
  - Seven categories ranked top to bottom, largest first.
  - The label is at the start of each row and the percentage at its end, in the accent colour.
  - All bars start from the same baseline, each on a pale full-length track.
  - A small caps kicker and a topic title above ("Most important … concerns").
  - A "Ranking" tag at the far end of the header.
- **Role:** ranking evidence.
- **What to translate:**
  - `full-exhibit` with `chart.kind:"bar"`: categories pre-sorted, `unit:"%"`, values printed, and the
    title stating the takeaway ("Inflation leads investor concerns at 79%"), not the topic.
  - Use the user's own data with its unit and source citation.
  - The pale track isn't drawn by our renderers. It isn't needed for honesty: bars from zero already
    are.
- **RTL / format:** labels are Hebrew text; the bar geometry stays LTR in both formats (as all our
  charts). Check long labels: they're why `bar` beats `column` here.

---

## Keynote product slides: software companies (one slide image each, 2026-11-17)

Source of the images: Duarte's published case studies of keynotes it designed. They are clean slide
exports, not photos of a stage screen, so they show composition but not how the slides read in the
hall. Pages (all under duarte.com/approach/case-studies/):
- **E** = salesforce-bringing-einstein-to-life/ (Dreamforce; the page gives no year; the slides' UI
  dates and "since DF15" point to 2016, which is our inference);
- **D** = creating-an-immersive-3d-keynote-experience-for-salesforces-biggest-stage/ (Dreamforce 2023);
- **M** = driving-market-leadership-with-innovation-stories/ (a Microsoft conference and customer-event
  deck; not stated to be Build or Ignite);
- **H** = crafting-an-unforgettable-keynote-for-hubspots-inbound/ (INBOUND 2022).

All 14 images were viewed by a research pass. #24 and #27 were re-checked when this was written.
Links are for analysis only: no logos, mascots, product photos or screenshots are copied.

**Apple, Google and Sony: not verified yet.** This environment's network policy refuses apple.com,
blog.google, storage.googleapis.com, blog.playstation.com, sony.com and the other newsrooms (proxy 403).
Duarte's Apple page says it works on Apple launches but "can't show much", and its only image is an
interview still. To add those entries, allow the hosts in the environment's network settings and
re-run the research. Record each slide in this format.

| # | Slide (page) | Role | What it shows | What to translate here |
|---|---|---|---|---|
| 20 | Einstein: "Einstein taught us…" (E) | setup before the reveal | ~8 words on a dark sky, one formula, an illustration | `statement` right before the reveal: one idea, dark field. Live only; in a read cut, fold it into the reveal's subtitle |
| 21 | "Introducing Salesforce Einstein" (E) | product reveal | small "Introducing" kicker → large light product name → one-line descriptor; quote and benefits crowd the rest | reveal = kicker ("חדש") + name + one descriptor (`statement`). Move benefits to the next slide |
| 22 | "How it works" (E) | mechanism | three labelled stages with arrows; a person-with-phone cut-out | `full-exhibit` + 3-step `chain`, last card = outcome. Drop the mood cut-out on an explanation slide |
| 23 | "Everyone's data scientist" (E) | ecosystem | five identical phones straight on, each captioned; "30+" with a small label beside them | a device **row** says "everywhere"; the captions carry meaning, the screens are texture. ≤ 3 devices here; the number on its own `big-number` slide |
| 24 | "Sales Cloud Einstein" (E) | feature + customer + proof | laptop straight on, **phone overlapping its front corner**, customer cut-out, "+25%" sign, **source footnote** (survey years, n) | `arrangement: "overlap"`; split the proof figure onto a `big-number` with its source in the footer; name the customer in the caption |
| 25 | "Service Cloud Einstein" (E) | next product in a series | the same composition as #24; only content and one accent change | parallel products → reuse one layout exactly (§ "Choosing per slide") |
| 26 | Quip (E) | new feature + availability | desktop + phone; a **round magnifier** enlarges one UI panel; store badges for availability | `exhibit.loupe`; availability as text ("iOS · Android · Web"), never badges |
| 27 | LiveMessage (E) | integration | phone with an SMS thread on one side, laptop console on the other, **the same conversation on both**, loupe on the laptop, a label under each | `devices` row with the same content on both screens + labels ("לקוח" / "נציג"); source device at the reading start (right in RTL) |
| 28 | Commerce Cloud (E) | feature + customers | three phones in a shallow overlapping fan, front one legible | "front = hero, back = many". **Not built**: candidate `arrangement: "stack"` |
| 29 | "True to the Core" (E) | numbers + breadth | "750K" and "500+" with side labels; a wall of feature names, most dimmed, a few white | one figure per `big-number`; "a lot, and these matter" → put the 3 highlights in the caption. The dimmed wall isn't a layout here |
| 30 | "Announcing Einstein 1 Platform" (D; a wide crop, not the full frame) | reveal with no UI | pill kicker, very heavy two-line name, one descriptor, five one-word attributes | when there's no hero screen, reveal with type alone (`statement`). Compared with #21, seven years later: heavier name, no quote |
| 31 | "$12 BILLION" (M) | big number | a light-weight figure across the slide, one context line, nothing else | `big-number`; weight can be light when size carries it. In Hebrew keep "$12B" as one LTR run, or write "12 מיליארד $" |
| 32 | Xbox Adaptive Controller evolution (M) | product story | three dated milestones over a flat-lay photo of sketches and parts | `timeline` for origin stories, with imagery as a strip, not a device frame. Our timeline needs a date on every event |
| 33 | "You belong." (H) | emotional peak | two words in one shape on a dark field; the talk's single motif | `statement` at its purest, once or twice per talk; one motif through the deck (`design.motif`) |

**Patterns across #20–33** (software companies only; re-test once Apple/Google/Sony are viewed):
1. Live launches go **setup → reveal**. The reveal is kicker + name + one line, with no proof on the same slide.
2. Devices are **straight on, no hands, no tilt** in 9 of 10 device slides (one slightly angled laptop).
   Our frames are straight on by design.
3. **Laptop + phone overlapping** = cross-platform. **Same content on two devices** = integration.
4. A **row** of devices shows breadth. A **fan** shows volume. Neither is evidence.
5. A **loupe** keeps the screenshot honest (whole) and makes the point legible.
6. A proof figure travels with its **source line**, even on a show slide (#24–25).
7. Parallel products share **one template**.
8. Scenery and mascots are brand IP and add density. Don't translate them; keep one visual world instead.

---

## To check next (found, not yet viewed)

| Item | Status 2026-11-17 | What a future entry must record |
|---|---|---|
| Arounda, "Pitch Deck for SaaS" (Dribbble) | The research brief reports the project page was found and opened. The slide visuals haven't been viewed, and dribbble.com challenges automated readers. | Open it in a browser. Record whether you saw the project page only, specific slides, or the full sequence. |
| Figma Slides (figma.com/slides) | Checked as a source of ideas for **live discussion** (polls, alignment scale; #4), not as a finished deck. | If a template is opened, name it and the slides viewed. |
| Pinterest | Useful for *discovering* examples, never as the reference itself. | After discovering, link the designer's or studio's own page, record the insight in your own words, and add any reusable asset through asset-sources.md. |

## Not verified (nominated, could not be confirmed)

| Item | Status 2026-11-17 |
|---|---|
| Dribbble "Presentation Slides for a SaaS Web App" (Excited); Dribbble "Pitch Deck for SaaS" (Arounda) | dribbble.com serves a JavaScript anti-bot challenge to automated readers, which was not bypassed. Open in a browser. |
| Behance "The Studio" modular presentation system | behance.net answers automated readers with 403 (the site's own block). Open in a browser. |
| Pinterest guide: case-study deck; borders for slides | guide.pinterest.com is Pinterest's consumer how-to site ("Pinterest Guides"). No pages matching these titles were found from its home page. Probably the wrong host; removed until a URL is given. |
| BrightCarbon "next level presentations" case study | Not found among the portfolio links. The portfolio itself is represented by #12–13. |
| Duarte: Roger Sant / carbon problem case study | Not on Duarte's case-study index, and site search runs on JavaScript. Replaced by #9–11. |
| Duarte blog: adapting visuals | Not located (site search runs on JavaScript). |

## Adding an entry
1. Open the page itself and record the date.
2. Fill in the template in your own words:
   - source;
   - **unit checked**: case page text, specific slides (which ones), or the full sequence;
   - scope;
   - audience and purpose;
   - structural decision;
   - visual decision ("not stated" if the page doesn't say);
   - role (which slide job it serves);
   - RTL / format fit;
   - our mapping (local preset or direction, layout, exhibit), and how it differs from the reference.
3. Don't copy images or long quotes.
4. If the principle maps to nothing we implement, note it: that is a candidate for a new layout or token.
