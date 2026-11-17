# Design gallery: real-world references (links only) and what each one teaches

Open this when you are composing a custom direction, or when the user says "something like X". Find
entries by tag and borrow the **principle** (sequence, hierarchy, how evidence is staged, live vs.
read), never the asset. No images, templates or fonts from these sources are stored in this repo (see
asset-sources.md §6). Every entry is **link for analysis only**: none of these pages grants reuse of
its slides.

## How these were checked
**2026-11-17:** each page below was opened with a plain HTTP fetch and its **text** was read. Two
limits follow from that:

- **The slides themselves weren't looked at.** "Visual decision" records only what the page says
  about the visuals; it is not a description of the slides.
- **Gaps are marked "not stated"** wherever the page says nothing about a field.

Sites that block automated readers were not worked around; they are listed under "Not verified".

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
- **Our mapping:** the `keynote` direction; `statement` slides; image-led meaning. Also a reason to keep text out of images, so a Hebrew or English re-cut doesn't need new art.

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
- **Our mapping:** charts-and-diagrams.md (one message per chart, highlight the comparison); the `product-demo` direction.

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
   - scope;
   - audience and purpose;
   - structural decision;
   - visual decision ("not stated" if the page doesn't say);
   - RTL / format fit;
   - our mapping.
3. Don't copy images or long quotes.
4. If the principle maps to nothing we implement, note it: that is a candidate for a new layout or token.
