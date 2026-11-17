# Product demo with device frames

A short Hebrew launch/demo deck for an invented accounting app ("פנקס"). It exercises the device
frames: one laptop, one phone, an iOS/Android pair, laptop + phone together, and a browser window.
Everything here is sample material: the product, the teams and the numbers are invented.

## Files
| path | what |
|---|---|
| `demo-he.blueprint.json` | the deck (playbook 6 demo + 9 launch, `product-demo` direction) |
| `sources/notes.md` | the only source; every slide cites it |
| `assets/*.png` | original screenshots of the sample app (MIT, this repo) |
| `screens-src/*.html` | the HTML the screenshots were rendered from (Chromium, 2× for phones) |

## Device frames
`exhibit.device` (`laptop` · `phone` · `tablet` · `browser`) frames one screenshot;
`exhibit.devices` (up to 3, each with `device`, `ref`, `label`) puts screens side by side on one
baseline, first item at the reading start (right in RTL). The frames are generic drawings from
`shared/blueprint_lib.py` (`device_geometry`): no logos, no notch or island shapes, no brand
colours, so they need no licence. The screen takes the screenshot's own aspect ratio, so screenshots
are never cropped. HTML draws them as SVG; PPTX draws editable shapes with the picture inside.

## Build
```bash
examples/product-demo/build.sh     # HTML + PPTX + PDF → examples/product-demo/build/ (git-ignored)
```
To re-render a screenshot after editing its HTML (needs node + playwright), screenshot
`screens-src/phone.html` at 390×844 with deviceScaleFactor 2, and `laptop.html` at 1440×900.
