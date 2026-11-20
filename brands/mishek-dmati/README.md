# משק דמתי · בית לכלבים — brand kit

Every dog-training deck for the school carries this logo.

- `logo.svg` — the logo as a vector (a redraw from the school's logo image; replace with the original
  artwork when it's available and re-render the PNGs).
- `logo-ink.png` — transparent, dark green `#17322B` (the classroom-workshop `dark` colour), for light slides.
- `logo-light.png` — transparent, white, for dark slides, photo backgrounds and photos that bleed into the logo corner.
- `brand.json` — what to merge into a deck's blueprint: `design.logo` plus the two `assets[]` entries,
  and which files to copy into the deck's `assets/` folder.

The renderers place the logo in the bottom corner at the end of the reading direction (bottom-left in
Hebrew decks), 84 px high on the 1920×1080 stage, at 90% opacity, and shorten the citation line so the
two never overlap. HTML and PPTX both support it (`design.logo` in `shared/blueprint-spec.md`).
