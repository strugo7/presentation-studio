# Animation & transition technique library

Recipes distilled from expert PowerPoint tutorials (One Skill PPT, youtube.com/@oneskill_ppt — the
Cinematic Slide Zooms, Master Morph, and Inverted Morph walkthroughs) plus the built-in HTML engine.
Each technique: what it's for, the PPTX steps, the HTML equivalent, and the blueprint field that
triggers it.

---

## 1. Morph transition (continuity)
**For:** carrying shared objects between two slides — resize/move/rotate, a number shrinking into a
corner, a chart growing, text boxes morphing smaller.
**PPTX:** duplicate the slide, change the shared objects on the second, set the second slide's
transition to **Morph** (Transitions → Morph; adjust duration ~1–2s). Needs PowerPoint 2019/365.
Morph matches objects by **name** — give shared objects the same name across both slides (via the
Selection Pane), and unique names to everything else so nothing morphs by accident. Going backwards
plays the morph in reverse.
**HTML:** shared elements with the same stable position/identity cross-fade+translate between slides;
the camera engine also morphs the kicker/title between a divider and its section.
**Blueprint:** `animation.transition:"morph"`. The PPTX builder auto-names shared frame objects
(kicker/title/number); name others in `animation.notes` if you need a specific morph.

## 2. Inverted / text-reveal morph (a signature look)
**For:** a title that appears to be "cut out" of a background, revealing a second state.
**PPTX:** background image cropped to 16:9, blurred (max); white text box; duplicate it black; draw a
circle; **Merge Shapes → Intersect** (text ∩ circle) to carve a shape; duplicate the slide, move the
carved piece, apply **Morph**. Produces the inverted reveal. *Technique credit: One Skill PPT.*
**HTML:** CSS `background-clip:text` + a masked layer animated on reveal.
**Blueprint:** a `quote`/`stakes`/`divider` slide with `animation.notes:"inverted-morph title"`.

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

## 4. Looping video / living background (depth on dark slides)
**For:** a cover/divider that breathes — subtle motion behind a scrim.
**PPTX:** insert a seamlessly-looping background video (lock the camera; pick matching start/end
frames if you generate it); Playback → **Loop until Stopped** + **Start Automatically**; put a 100%
transparent rectangle on top so clicks/hover still work; check layering in the Selection Pane.
**HTML:** a muted autoplay loop `<video>` or a slow Ken-Burns pan on a photo, both behind a navy scrim.
**Blueprint:** `background.kind:"photo"` (+ a video asset if provided); the HTML builder animates it,
the PDF flattens to a still.

## 5. Staged reveals (segmenting — the everyday workhorse)
**For:** showing one idea at a time so the room doesn't read ahead.
**PPTX:** entrance animations (Appear/Fade/Wipe) on each bullet/exhibit, sequenced On Click, with
small delays; group related objects so they animate together.
**HTML:** each element carries a reveal step; clicking advances the step before advancing the slide.
**Blueprint:** `animation.reveals:[{step, show:[...], zoom?}]`.

## 6. Exhibit region-zoom (signal the key detail)
**For:** pushing the eye to the one line/bar/cell that matters, live.
**PPTX:** a reveal step that scales/crops to the region, or a second slide morphing into the zoomed
view. **HTML:** the engine scales the exhibit image to a named region on a reveal step or on click.
**Blueprint:** a reveal with `zoom:"<region or annotate hint>"`, aligned with the exhibit's `annotate`.

---

## Restraint rules (so motion helps, not hurts)
- One payoff per section gets the richest motion; keep the rest quiet. Uneven rhythm > uniform.
- Never put meaning *only* in motion — the static slide must still carry the point (reduce-motion, PDF).
- Morph only between slides that truly share objects; otherwise it looks like random drift.
- Zoom navigation earns its cost at 3+ sections; below that, linear + fade is cleaner.
- Durations: morph ~1–1.6s; camera flight ~1.1–2.6s; reveals ~0.4–0.9s. Slower = more cinematic, to a
  point — past ~2.5s it drags.
