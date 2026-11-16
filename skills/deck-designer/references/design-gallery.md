# Design gallery — real-world references, links only, with verification status

Open this when composing a custom direction, or when the user says "something like X". Find entries by
tag and borrow the **principle** (hierarchy, rhythm, relative scale, how evidence is staged), never the
asset. No images, templates or fonts from these sources are stored in this repo; see asset-sources.md §6.

## Verification status — read this first

**Checked 2026-11-16: no entry below has been verified yet.** The environment this gallery was built
in blocks every one of these hosts, so no page could be opened. Web search shows only titles and
snippets; that is not enough to confirm the creator, scope or the design decisions.

So every row is marked **UNVERIFIED**:
- **What it holds:** the link, why it was nominated, and the tags.
- **What it doesn't hold:** a claim about what the page actually shows.
- **"Lead"** marks a summary taken from search snippets. It is a hypothesis to check, not a finding.

Do not cite an UNVERIFIED entry to a user as evidence. To verify one, follow "How to verify an entry"
at the end, then move it to **Verified**.

Hosts to allow, so the next run can verify the gallery: `www.figma.com`, `dribbble.com`,
`guide.pinterest.com`, `www.behance.net`, `www.brightcarbon.com`, `www.liegeoisdesigns.com`,
`www.duarte.com`, `www.assertion-evidence.com`, `writing.engr.psu.edu`.

## Entry template (for a verified entry)
```
### <name>  ·  tags: <audience> / <slide role or deck type> / <format>
- Creator · Link · Checked: YYYY-MM-DD (opened by: who/what)
- Scope: what the page actually shows (n slides, whole deck vs. shots)
- Audience / purpose
- Structural decision: how the argument is ordered, what each slide's job is
- Visual decision: grid, type scale, colour, how evidence is staged
- RTL / format fit: what survives mirroring; HTML vs PPTX vs PDF
- Our mapping: which layout / token / playbook expresses the principle
- Basis for use: "link for analysis only" unless the item's own licence says otherwise
```

---

## Verified
*(none yet, see the status note above)*

## Unverified — nominated, not opened

| # | Item | Link | Nominated for | Tags |
|---|---|---|---|---|
| 1 | Figma Slides templates: Product Review, Design Review, Startup Pitch | figma.com/slides (templates) | Product-team review decks; recurring rituals | product, review, live-talk, pptx/html |
| 2 | Figma, "What is a slide deck" (Pitch, Roadmap, All Hands examples) | figma.com/resource-library/what-is-a-slide-deck/ | Deck types by purpose | general, playbooks |
| 3 | Dribbble, "Presentation Slides for a SaaS Web App" (creator reported as Excited) | dribbble.com (shot) | Product screens in a split layout | product-demo, split |
| 4 | Dribbble, "Pitch Deck for SaaS" (creator reported as Arounda) | dribbble.com (shot) | Pitch rhythm, big numbers | pitch, big-number |
| 5 | Pinterest Business guide: case-study deck | guide.pinterest.com | Case-study narrative | case, self-read |
| 6 | Pinterest Business guide: borders / frames for slides | guide.pinterest.com | Frame and margin system | tokens: frame, margin |
| 7 | Behance, "The Studio": a modular portfolio presentation system | behance.net (project) | A modular grid reused across slide types | system, grid |
| 8 | BrightCarbon case study, "next level presentations" | brightcarbon.com | Animation that explains | interaction, technical |
| 9 | BrightCarbon portfolio | brightcarbon.com/portfolio | Framework visuals revealed part by part | diagrams, reveals |
| 10 | Liégeois Designs, Marriott Luxury Group | liegeoisdesigns.com | Premium editorial brand deck | editorial, keynote |
| 11 | Duarte case study, Roger Sant / the carbon problem | duarte.com | One big idea for a lay audience | keynote, statement |
| 12 | Duarte blog, adapting visuals | duarte.com/blog | Re-cutting one visual for different audiences | audience re-cut |
| 13 | Duarte, *Slidedocs* (e-book) | duarte.com/resources/books/slidedocs/ | Decks meant to be read | self-read, pdf |
| 14 | Michael Alley, assertion–evidence model and research talks | assertion-evidence.com; writing.engr.psu.edu | Sentence headline + visual evidence | research, technical, students |

### Leads from search snippets (hypotheses, not findings)
- **Duarte, slidedocs (#13).** Snippets describe slidedocs as documents "handed out and read, not
  projected": about 150–200 words a page versus roughly 40 on a projected slide, and each page standing
  on its own. They are used as a pre-read or as the leave-behind.
  - *If confirmed, it backs:* our `self-read` delivery mode, which uses no reveals and a summary that
    stands alone (layout-patterns.md §9, interaction-patterns.md §7).
- **Alley, assertion–evidence (#14).**
  - Snippets describe a full-sentence headline (at most 2 lines, left-aligned) over visual evidence
    instead of bullets.
  - Studies by Alley's group report better understanding than topic-subtopic slides.
  - *If confirmed, it backs:* action titles plus `full-exhibit` (layout-patterns.md §3) and the
    ghost-deck test (deck-playbooks.md).
  - *Not known from snippets:* how his research talks move from question to result.
- **BrightCarbon (#8, #9).**
  - A snippet quotes them using animation "to show change, explain how things work, and tell a
    story".
  - A portfolio entry (Aegis) reportedly shows a framework whole first, then each part in turn.
  - *If confirmed, it backs:* interaction-patterns.md §7, "animate what changes".

These principles already stand in our references on their own reasoning. Each gallery entry is meant
to add real-world evidence for a principle, which none of them does until it is verified.

---

## How to verify an entry
1. Open the page itself, not a search result, and record the date.
2. Confirm the creator and what the page actually shows (number of slides, full deck or selected shots).
3. Fill in the entry template. Write the structural and visual decisions in your own words, and don't
   copy or screenshot the work into the repo.
4. Map the principle to something we implement: a `layout`, a design-system token or a playbook step.
   If nothing maps, say so: that is a candidate for a new pattern.
5. Move the row to **Verified**. If a page is gone or different from what was nominated, delete it and
   note that in the commit message.
