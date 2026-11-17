# Format capabilities — the single matrix every builder points to

What each output does with the same `blueprint.json`. "Local" = works with this repo's renderers and
no network. "Conversion" = needs another app. "User action" = a step the user must take. Update this
file (and only this file) when a renderer gains or loses a capability.

Verified in this repo's tests: HTML, PPTX (structure via python-pptx, visuals via LibreOffice), PDF (both
routes). Keynote and Google Slides are **not** verifiable here: they depend on the user's Mac or Google
account and must be checked in the target environment.

Motion rows were re-checked against the renderer code on 2026-11-17. "Not built" means the blueprint
field is accepted and validated but no builder acts on it yet. Don't promise it to the user.

## Matrix

| Capability | HTML (`render_html.py`) | PowerPoint (`render_pptx.py`) | PDF (`render_pdf.py`) | Keynote / Google Slides (via PPTX) |
|---|---|---|---|---|
| **Layouts** (`statement`, `split`, `full-exhibit`, `big-number`) + design tokens | Local | Local | Local (both routes) | Survive import as static shapes |
| **Charts** column / bar / line / scatter | Local inline SVG | Local native, editable chart (same values, units, series names) | html route: SVG; pptx route: LibreOffice renders the native chart (the `pptx_to_html` fallback drops charts) | Keynote re-renders native charts; Slides may turn them into images |
| Unsupported chart kind | Table + note | Table | Table | Table |
| **Diagrams** chain / timeline / sequence | Local SVG/HTML | Local shapes + connectors | Local | Shapes survive; check arrowheads |
| **Navigation** | Camera flight between every pair of slides (the same move whatever `transition` says); chapter map (`M`), overview (`O`); hub tiles are buttons (keyboard + click) | Linear; Morph on `transition:"morph"`; Sections + map slide when `navigation.mode:"zoom"`. **User action:** Insert → Zoom → Section Zoom (2 clicks) | Logical reading order, one page per slide | Morph → Magic Move (imperfect) in Keynote, fade in Slides; Zoom does not import. **User action:** check every link after import |
| **Quiz** (`correctOptionId`) | Radio buttons with local feedback, "reveal answer", focus kept on the control; Enter/Space/arrows inside the quiz never move the deck | Options are shapes hyperlinked to a generated **answer slide** (`answerPlacement`: next-slide / appendix / inline); presenter cue in notes | Question page, then answer page per `answerPlacement` (`self-read` defaults to inline) | Links usually survive in Keynote; Slides keeps internal links in most cases. Verify |
| **Poll** | Local single-device tally, labelled "local poll". A multi-device class poll needs a real collection service (not built in) | Static options + presenter cue (show of hands / external tool) | Static options | Static |
| **Question / activity** | Prompt card | Prompt card | Prompt card | Prompt card |
| **Demo** | Screenshot (`assetRef`) and/or safe link (`url`) | Screenshot + hyperlink run | Screenshot + printed link | Screenshot; link usually kept |
| **Transitions** (`animation.transition`) | **Not built**: ignored; camera flight instead | `morph` → Morph (`p159:morph`, fade fallback); `fade`/`push` → fade; zoom mode → Morph on every slide after the first. Kicker/title/big number/section numeral share names across slides so they match | n/a | Morph → Magic Move (imperfect) / fade |
| **Reveals** (`animation.reveals`) | Click-stepped | Not generated (static slide shows everything); add entrance animations in PowerPoint if wanted | Everything shown (print forces final state) | Static |
| **Region zoom** (reveal `zoom`) | **Not built** | **Not built** (manual crop or morph) | n/a | — |
| **Exhibit emphasis** | `highlight` bar/point in `accent2`; `annotate` is not drawn (planning note) | Same: `highlight` point coloured; `annotate` not drawn | Same as source route | Kept as chart formatting |
| **Reduced motion** | `prefers-reduced-motion` + `meta.accessibility.reducedMotion` + `R`/Motion toggle: no camera flight, reveals fade only | n/a (no generated animation besides transitions) | n/a | n/a |
| **Sources & credits** | Footer citation per slide + generated sources page with readable links (`rel="noopener"`) | Footer citation + sources slide with hyperlinks | Printed, links clickable on the html route | Kept as text; links usually kept |
| **Alt text** | `alt` on images, `aria-label` on charts | `descr` on pictures | Tagged-PDF quality depends on Chrome | Usually kept |
| **Fonts** | Bundled OFL Assistant embedded (no CDN; opens offline); `--font=` embeds another | Font *named*; user embeds via File → Options → Save → Embed fonts | Embedded | Install the font, or Keynote/Slides substitute; choose a Google Font for Slides |
| **RTL** | `dir="rtl"`; charts keep LTR axes with RTL labels; tables mirror column order | `rtl` + `cs` font + `lang` on every run; tables mirror | Same as the source route | Keynote good; Slides: check alignment of mixed Hebrew/English lines |
| **Speaker notes** | `N` key panel | Notes pane | Not printed | Kept |
| **Device frames** (`exhibit.device`, `devices`, `arrangement`, `loupe`) | Inline SVG: generic phone/tablet/laptop/browser, screenshot uncropped inside; row or overlap; round loupe | Editable shapes + picture (rounded screen corners); loupe = elliptical cropped picture | Same as source route | Shapes survive; check the screen corners |
| **Photo / living background** | Photo behind a scrim, **static** (no video, no pan) | Photo + scrim; video: insert manually | Still frame | — |

## Which export loses the least

- **Interactive talk, kiosk, async link:** HTML (only format with live quiz feedback and camera navigation).
- **Editable, corporate, projector:** PPTX.
- **Hand-in, email, print:** PDF from the **html route** (keeps charts, all reveal steps, answers,
  sources). Use the **pptx route** only when the PDF must mirror the PowerPoint, and prefer it with
  LibreOffice installed (the Chrome fallback drops native charts).
- **Keynote / Google Slides:** always from the PPTX; tell the user what degrades (row above).

## Fallback rules builders follow

1. Never show something wrong: an unsupported chart becomes a table, a missing image becomes a labelled
   placeholder with the alt text, an SVG with no raster `fallbackPath` becomes a placeholder in PPTX
   with a warning.
2. Meaning never lives only in motion or interaction: every quiz has a static answer path, every reveal
   is printed in PDF. A morph or zoom that shows a change has a label or kicker saying the same thing.
3. Report what was replaced in the hand-off message (the builders print warnings).
