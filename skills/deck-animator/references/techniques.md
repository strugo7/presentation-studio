# Animation & transition technique library

Recipes distilled from expert PowerPoint tutorials (One Skill PPT, youtube.com/@oneskill_ppt — the
Cinematic Slide Zooms, Master Morph, and Inverted Morph walkthroughs; BrightCarbon's Morph guide,
[brightcarbon.com/blog/using-powerpoint-morph](https://www.brightcarbon.com/blog/using-powerpoint-morph/))
plus the built-in HTML engine. Each technique gives:
- what it's for;
- the manual PowerPoint steps;
- the HTML equivalent;
- the blueprint field that triggers it;
- a **Built** line saying what the builders in this repo generate today.

The Built lines were checked against `shared/render_html.py` and `shared/render_pptx.py` (2026-11-17).
Where a technique is not built, the PPTX steps are a manual finish for the user, and the HTML line is
a design note, not a feature.

| Technique | HTML | PPTX | PDF |
|---|---|---|---|
| 1 Morph | not built (camera flight instead) | **built** (`transition:"morph"`, fade fallback) | static |
| 2 Inverted morph | not built | manual | static |
| 3 Section zoom | **built** (camera flight, hub tiles) | Sections + map slide **built**; zoom objects manual | static |
| 4 Living background | photo + scrim only (no video, no pan) | manual | still |
| 5 Staged reveals | **built** | not built (static slide; add entrance animations by hand) | all steps shown |
| 6 Region zoom | not built | manual | static |

---

## 1. Morph transition (continuity)
**For:** carrying shared objects between two slides — resize/move/rotate, a number shrinking into a
corner, a chart growing, text boxes morphing smaller.
**PPTX:** duplicate the slide, change the shared objects on the second, set the second slide's
transition to **Morph** (Transitions → Morph; adjust duration ~1–2s). Needs PowerPoint 2019/365.
Morph matches objects by **name** — give shared objects the same name across both slides (via the
Selection Pane), and unique names to everything else so nothing morphs by accident. Going backwards
plays the morph in reverse.
**HTML:** *not built.* The engine ignores `animation.transition` and flies the camera between every
pair of slides, so nothing morphs between two slides. Continuity comes from the camera arc and from
keeping the title in the same position.
**Blueprint:** `animation.transition:"morph"`.
**Built:**
- PPTX writes a real Morph transition (`p159:morph`, byObject) with a fade fallback for apps without
  Morph.
- The builder names the kicker, title, big number and section numeral identically on every slide
  (`!!kicker`, `!!title`, `!!bignum`, `!!secnum`), so those morph. All other shapes get unique names
  (`s<slide>_<n>`).
- To morph another object, name it in PowerPoint's Selection Pane after export, and note it in
  `animation.notes`.

**Static twin:** say the change on the slide (kicker or caption), since HTML, PDF and reduced motion
won't play it.

## 2. Inverted / text-reveal morph (a signature look)
**For:** a title that appears to be "cut out" of a background, revealing a second state.
**PPTX:** background image cropped to 16:9, blurred (max); white text box; duplicate it black; draw a
circle; **Merge Shapes → Intersect** (text ∩ circle) to carve a shape; duplicate the slide, move the
carved piece, apply **Morph**. Produces the inverted reveal. *Technique credit: One Skill PPT.*
**HTML:** a possible approach is CSS `background-clip:text` plus a masked layer. *Not built.*
**Blueprint:** a `quote`/`stakes`/`divider` slide with `animation.notes:"inverted-morph title"`.
**Built:** nothing. It's a manual PowerPoint finish; the note tells the user where.

## 3. Cinematic Section Zoom (navigation for multi-section decks)
**For:** a map slide where each section is a clickable tile; click → camera flies in, plays the
section, flies back.
**PPTX (exact recipe):**
1. Make the home/map slide. Put a placeholder shape where each section tile goes.
2. Right-click the slide panel → **Add Section** for each module; put the section's slides inside it.
3. On the map slide: **Insert → Zoom → *Section* Zoom** (not Slide Zoom — Section Zoom is for
   multi-slide sections). Pick the sections.
4. For each inserted zoom object: remove the outline, turn on **Zoom Background** (makes it
   transparent so your tile shows through), and turn on **Return to Zoom** (flies back to the map after
   the section's last slide).
5. Optional auto-advance inside a section: set a slide's transition to advance **After 00:00**.
*Credit: One Skill PPT, "Cinematic Slide Zooms".* Script can't create the Zoom object; the PPTX builder
pre-makes the Sections + map slide so this is a ~2-click manual finish, documented in the output README.
**HTML:** the camera engine does this natively — the map's tiles carry `data-goto`, and moving between
slides flies the camera with a smooth zoom-out/zoom-in arc; `M` returns to the map.
**Blueprint:** `navigation.mode:"zoom"`, `hubSlideId`, `zoomTargets`.
**Built:**
- HTML: camera flight and hub tiles. Under reduced motion the camera jumps without flying.
- PPTX: Sections, plus Morph on every slide after the first.
- The Zoom objects themselves are a manual 2-click step for the user.

## 4. Looping video / living background (depth on dark slides)
**For:** a cover/divider that breathes — subtle motion behind a scrim.
**PPTX:** insert a seamlessly-looping background video (lock the camera; pick matching start/end
frames if you generate it); Playback → **Loop until Stopped** + **Start Automatically**; put a 100%
transparent rectangle on top so clicks/hover still work; check layering in the Selection Pane.
**HTML:** possible as a muted autoplay `<video>` or a slow pan behind a scrim. *Neither is built.*
**Blueprint:** `background.kind:"photo"` + `background.assetRef`.
**Built:** HTML draws the photo, cropped to fill, behind the navy scrim, **static**. PPTX places the
photo and scrim. PDF prints it. A looping video is a manual PowerPoint step (recipe above).

## 5. Staged reveals (segmenting — the everyday workhorse)
**For:** showing one idea at a time so the room doesn't read ahead.
**PPTX:** entrance animations (Appear/Fade/Wipe) on each bullet/exhibit, sequenced On Click, with
small delays; group related objects so they animate together.
**HTML:** each element carries a reveal step; clicking advances the step before advancing the slide.
**Blueprint:** `animation.reveals:[{step, show:[...]}]`.
**Built:**
- HTML: click-stepped (fade + rise; opacity only under reduced motion).
- PPTX: not generated. The slide shows everything, so add entrance animations in PowerPoint if they're
  wanted.
- PDF: every step shown.

## 6. Exhibit region-zoom (signal the key detail)
**For:** pushing the eye to the one line/bar/cell that matters, live.
**PPTX:** a reveal step that scales/crops to the region, or a second slide morphing into the zoomed
view (manual).
**HTML:** *not built.* The engine does not read the reveal's `zoom` field.
**Blueprint:** a reveal with `zoom:"<region>"` is accepted by the schema and ignored by every builder.
**Today, instead:**
- `exhibit.data.highlight` on charts (drawn in `accent2`);
- a reveal of the interpretation bullet after the exhibit;
- or a second slide that shows the cropped detail as its own image, with a kicker naming what it
  zooms into ("Detail: June"). That last option is also the static twin for PDF.

---

## Restraint rules (so motion helps, not hurts)
- One payoff per section gets the richest motion; keep the rest quiet. Uneven rhythm > uniform.
- Never put meaning *only* in motion — the static slide must still carry the point (reduce-motion, PDF).
  When the motion *is* the message (a morph showing change, a zoom into a part), add a label that says
  it. Interaction (quiz/poll/demo) behaviour per format: interaction-patterns.md.
- Morph only between slides that truly share objects; otherwise it looks like random drift.
- Zoom navigation earns its cost at 3+ sections; below that, linear + fade is cleaner.
- Durations: morph ~1–1.6s; camera flight ~1.1–2.6s; reveals ~0.4–0.9s. Slower = more cinematic, to a
  point — past ~2.5s it drags.
