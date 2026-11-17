# Asset sources — where images, illustrations and icons come from, and how to credit them

Use when a slide needs an image, illustration or icon the user didn't supply. For each provider: what
it has, when to pick it, how to search, access method, licence, credit, and a fallback. Record every
asset you use in `assets[]` with `provider`, `sourceUrl`, `creator`, `license`, `licenseUrl`, `credit`,
`alt` — the builders print the credit next to the slide and on the generated sources page.

**Image licence ≠ API terms.** A photo's licence says what you may do with the picture. An API's terms
say how your software must fetch, display and credit it. Check both separately.

**Verification status (checked 2026-11-16).** This environment blocks most provider sites, so each
row says how its terms were checked:
- **read**: the licence text itself was read (usually its copy on GitHub).
- **search**: the official page was seen only in search results. Open it before relying on it.

Licences change. Re-check the official page before you publish a deck externally.

Work offline-first: the user's files, or images already approved and saved locally, always come first.
An API is used only if the user already has access configured. Never paste a key into a blueprint.

---

## 1. Picking an image (any provider)
1. **Name the image's job.** Possible jobs: cover atmosphere, section opener, story moment, evidence
   (a screenshot of the real thing), or explanation (better as a diagram). Content slides rarely need
   stock photos.
2. **Write the query from the slide's claim or task, not its topic word.** For example, "empty
   lecture hall morning light" for a slide about attendance, not "education".
3. **Judge each candidate on:**
   - Framing and calm space for text, on the side text goes (the opposite side in RTL).
   - Sharpness at 1920 px.
   - Whether the subject actually matches the case (no generic handshake for a specific event).
   - Consistency with the rest of the deck (colour temperature, people/no people, illustration
     vs photo).
4. **If no image fits**, use a quiet fallback: a solid or `grid` background, or a big-number or
   statement layout. A bad photo is worse than none.
5. **Save it locally**, if the licence and provider terms allow, under a stable unique name such as
   `assets/<slide-id>-<subject>.jpg`. Add an `assets[]` entry. The builders copy files under
   collision-free names, so the deck and its credits work offline.
6. **Format needs.**
   - PPTX can't place SVG. Give a PNG `fallbackPath` (1600–2400 px) for every SVG.
   - HTML uses the SVG directly.
   - Never stretch a raster below its native width.

## 2. Stock photography

| | Unsplash | Pexels |
|---|---|---|
| Has | High-quality editorial and lifestyle photos | Photos and video; broad commercial subjects |
| Pick for | Cover/section atmosphere, story moments | Same, plus short background video |
| Licence | Unsplash License (not CC). Free use including commercial, no permission needed (**read**, licence text). Not allowed: selling unmodified copies; compiling images into a competing service. Unsplash+ images have a separate licence. | Pexels License. Free use including commercial (**search**). Restrictions as reported: don't sell or redistribute unaltered copies; don't show identifiable people in a bad light or imply endorsement. Check the license page. |
| Licence URL | unsplash.com/license | pexels.com/license |
| Credit (appreciated, not required by the licence) | `Photo: {Name} / Unsplash` | `Photo: {Name} / Pexels` |
| API | unsplash.com/documentation. Needs an app Access Key. API guidelines (**search**): use the returned `urls` (no re-hosting in apps); call `links.download_location` when a photo is chosen or inserted; credit photographer and Unsplash with links. An offline PPTX/PDF needs a local copy, so trigger the download endpoint and keep the credit. Whether a local copy in an exported file meets the API guidelines is **unverified**; check help.unsplash.com's API guidelines. | pexels.com/api/documentation. Needs an API key in the `Authorization` header. Show a link to Pexels and credit photographers (**search**). Default rate limit 200/hour, 20,000/month (**search**). |
| Fallback | Pexels, then solid or grid background | Unsplash, then solid or grid |

## 3. Documentary images

| Provider | Has | Licence handling | Credit |
|---|---|---|---|
| **Wikimedia Commons** (commons.wikimedia.org) | Historical, scientific, places, people, artefacts | **Per file.** On the file page, read *Author* (credit the author, not the uploader) and the *Licensing* template: CC0, PD, CC BY, CC BY-SA, GFDL… CC BY-SA means adaptations keep the licence (**search**). | `{Author}, {licence + link}, via Wikimedia Commons` |
| **Openverse** (openverse.org) | Search index across many open sources | Openverse **doesn't verify** licences (its terms say so; **search**). Always open the source page and confirm author and licence there. | Follow the source's licence |
| **Smithsonian Open Access** (si.edu/openaccess) | Museum objects, natural history, archives | Use only items marked **CC0** (CC0 icon on the site; in data, `usage.access = "CC0"`). Anything else is "usage conditions apply". Some CC0 records lack the media file (**search**). | Not required. Suggested: `Smithsonian {unit}, CC0` |
| **NASA Image and Video Library** (images.nasa.gov) | Space, Earth, missions | Generally not copyrighted in the US (**search**). **Not free:** the NASA insignia, logotype and identifiers; implying endorsement; commercial use of identifiable people; third-party items credited to others. JPL has its own policy. | `Credit: NASA` or the item's line (e.g. `NASA/JPL-Caltech`) |

Documentary images are evidence. Caption them with what, where and when. Don't crop away the context
a sceptic would need.

## 4. Illustration
- **Open Peeps** (openpeeps.com, Pablo Stanley). Hand-drawn people for training and human situations.
  Licence **CC0** (**search**). Optional credit: `Open Peeps by Pablo Stanley (CC0)`. Keep one
  illustration style per deck.
- To show a specific product, observation or event, use **original screenshots or the user's
  material**, never stock. Mark it `provider: "user"` or `"original"`.

## 5. Icons

| Set | Licence (**read** from the repo's LICENSE) | Use |
|---|---|---|
| **Tabler Icons** (default) | MIT, © Paweł Kuna | Outline, 24 px grid, consistent 2 px stroke |
| **Lucide** | ISC (Feather-derived icons MIT, © Cole Bemis) | Close to Tabler; pick one, never mix |
| **Phosphor** | MIT | Six weights (thin to fill). Good when the design wants a lighter or bolder line |
| **Iconify** (search across sets) | **Per set.** Some sets need attribution (CC BY), some are SA or GPL. *Custom Brand Icons* is **CC BY-NC-SA** (non-commercial). Read the set's `license` field; exclude NC and SA sets for client decks. | Search only within the approved sets above |

**Rules.**
- One family, one stroke weight, one style per deck.
- Icons label things; they're not the motif (no icons in coloured circles).
- If you ship icon files with the deck, keep the set's licence notice (MIT/ISC require it in
  copies). Note the set in `assets[]`.
- Brand logos are trademarks: use them only to refer to that company, unaltered.

**Cloud architecture diagrams.** Use the provider's official icons, and follow their rules:
- **AWS Architecture Icons** (aws.amazon.com/architecture/icons): allowed in diagrams and
  presentations (**search**). Trademark guidelines apply beyond that.
- **Azure** (learn.microsoft.com/azure/architecture/icons): allowed in diagrams, training and
  documentation. Don't crop, flip, rotate or distort; don't use them for your own product (**search**).
- **Google Cloud** (cloud.google.com/icons): official library for diagrams and documentation. Check
  the page's terms (**search**).

Don't mix providers' icon styles in one diagram unless the architecture really spans them.

## 5b. Device mockups (laptop, phone, tablet, browser) — checked 2026-11-17
**Default: the built-in generic frames** (`exhibit.device` / `exhibit.devices`, layout-patterns.md §11).
They're original drawings in `shared/blueprint_lib.py`, with no logos, no notch/island/Home-button
shapes, no brand colours and neutral browser dots. So they need no licence and imply no endorsement.
The user's screenshot is placed inside, uncropped.

Apple's own guidelines expect this approach. Generic device illustrations must not "include details
that are unique to Apple products, such as the iPhone Home button, sensor housing, Ring/Silent switch,
or volume controls" (App Store marketing guidelines, **read**).

| Source | What it is | Terms (status) | Use in a shipped deck? |
|---|---|---|---|
| Built-in generic frames | phone, tablet, laptop, browser; side by side or overlapping | this repo, MIT | **Yes**, the default |
| Apple Product Bezels (developer.apple.com/design/resources) | real iPhone/iPad/Mac bezels | App Store Marketing Artwork License: only for **your own App Store app**, only while in the Apple Developer Program; use "as is" (no tilt, crop, shadow, flip, animation), no competitor devices beside them, no blank or Home screens (**read**) | Only when the user markets their own App Store app and accepts those rules. Never as a default, never mirrored for RTL |
| Android device art generator (developer.android.com) | wraps screenshots in device art | page content CC BY 2.5, but Google trademarks and brand features are excluded. Pixel hardware images need written permission (**read**; the permission rule is **search**) | Not by default. Generic frames instead |
| Meta "Devices" (Design at Meta) | real-device mockups | commercial use needs written permission (**search**, site blocked) | **No** |
| MIT/ISC CSS device kits (marvelapp/devices.css, picturepan2/devices.css) | CSS drawings of real iPhones, Pixels, Galaxies, MacBooks | code MIT (**read**), but the drawings imitate real products' trade dress | Technique reference only. Don't ship the branded look-alikes |
| html5-device-mockups (pixelsign) | PNG frames of real devices | code MIT, but the PNGs come from third-party freebies with unknown terms (**read**: CREDITS.txt) | **No** |
| Figma Community mockup files | many kits | licence comes from the creator. Free files reportedly default to CC BY 4.0 (**search**); paid files allow no redistribution (**read**) | Free CC BY files with **generic** devices, with credit ("Device frame: {creator}, CC BY 4.0"). A file showing real iPhones/MacBooks has the Apple problem whatever its licence |
| Mockup tools (Mockuuups, Shots.so, Rotato, Previewed) | photo-real scenes and 3D renders | free tiers: personal use and/or credit; paid tiers commercial (**search**, sites blocked) | The user's own exports on a paid plan. Record as `provider: "user"` with their plan noted. Not bundled |
| Unsplash / Pexels "device in hand" photos | photos to composite a screen onto | licence allows modification (**read**), but trademarks and logos in the photo aren't cleared (**search**) | Only photos where no logo or distinctive branded device shows. Never cover or edit out a logo |

Rules that follow:
- Never mirror a device frame or a screenshot for RTL. Only the order of devices flips.
- In copy, don't call the generic phone "iPhone". If the deck names a platform, write it as text
  ("iOS · Android · Web"), never as a store badge or logo.
- A frame is decoration around evidence. The screenshot inside still gets its own `assets[]` entry,
  `alt` and credit.

## 6. Inspiration vs. embedding
Figma Community, Dribbble, Pinterest, Behance and designer portfolios are for **design research
only**. Take principles from them (hierarchy, rhythm, relative scale, grid) and turn them into our
own layouts and tokens; see design-gallery.md. Don't embed their images, templates or fonts unless the
item's own licence allows it and you credit it as required. Never commit copies of commercial
projects to the repo.

## 7. Fonts (Hebrew-capable, Google Fonts, SIL OFL 1.1; **read** from github.com/google/fonts)
Assistant (bundled in `shared/fonts/`), Heebo, Rubik, Frank Ruhl Libre (serif), Noto Sans Hebrew,
Secular One (display). OFL allows embedding in documents. Keep `OFL.txt` with any font file you
redistribute; don't sell the fonts alone.

## 8. `assets[]` entry template
```json
{ "id": "cover_hall", "path": "assets/cover-hall.jpg", "kind": "photo",
  "provider": "unsplash", "sourceUrl": "https://unsplash.com/photos/…", "creator": "Jane Doe",
  "license": "Unsplash License", "licenseUrl": "https://unsplash.com/license",
  "credit": "Jane Doe / Unsplash", "alt": "Empty lecture hall in morning light" }
```
