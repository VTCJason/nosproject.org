#!/usr/bin/env bash
# Build case study PDF from markdown source via pandoc + xelatex.
# Usage: bash scripts/build-case-study-pdf.sh [--open]
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROCESSED="/tmp/case-study-pandoc.md"
TEMPLATE="$REPO_ROOT/templates/case-study-latex.tex"
OUT_DIR="$REPO_ROOT/public/case-study"
OUT_PDF="$OUT_DIR/case-study.pdf"
TEXLOG="/tmp/case-study-xelatex.log"

echo "==> Step 1: Preprocess markdown"
python3 "$REPO_ROOT/scripts/preprocess-case-study.py"

echo ""
echo "==> Step 2: pandoc → xelatex → PDF"
pandoc "$PROCESSED" \
  --template "$TEMPLATE" \
  --from markdown-smart+raw_tex \
  --pdf-engine=xelatex \
  --pdf-engine-opt=-halt-on-error \
  --pdf-engine-opt=-interaction=nonstopmode \
  -o "$OUT_PDF" \
  2>&1 | tee "$TEXLOG"

echo ""
echo "==> Built: $OUT_PDF"
ls -lh "$OUT_PDF"

if [[ "${1:-}" == "--open" ]]; then
  xdg-open "$OUT_PDF" &
fi
