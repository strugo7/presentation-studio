#!/usr/bin/env bash
# Build both decks (HTML, PPTX, PDF) into examples/mixed-sources/build/ (git-ignored).
set -euo pipefail
cd "$(dirname "$0")"
S=../../shared
mkdir -p build
for deck in students-he exec-he; do
  python3 $S/validate_blueprint.py $deck.blueprint.json
  python3 $S/render_html.py $deck.blueprint.json build/$deck-html .
  python3 $S/render_pptx.py $deck.blueprint.json build/$deck.pptx .
  python3 $S/render_pdf.py  $deck.blueprint.json build/$deck.pdf . --from=html
done
