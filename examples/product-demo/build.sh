#!/usr/bin/env bash
# Build the product-demo deck (HTML, PPTX, PDF) into examples/product-demo/build/ (git-ignored).
set -euo pipefail
cd "$(dirname "$0")"
S=../../shared
mkdir -p build
python3 $S/validate_blueprint.py demo-he.blueprint.json .
python3 $S/render_html.py demo-he.blueprint.json build/html .
python3 $S/render_pptx.py demo-he.blueprint.json build/demo-he.pptx .
python3 $S/render_pdf.py  demo-he.blueprint.json build/demo-he.pdf . --from=html
