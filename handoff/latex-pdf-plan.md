# Case Study: LaTeX/PDF Implementation Plan

**Date:** 2026-05-24  
**Status:** Pending review before implementation

---

## Root Cause Analysis — Why the HTML Approach Failed

### 1. Echo bug (all sections)

`get(r'^## 1\.', ...)` matches only `## 1.` — 5 characters, ending at the period. `m1.end()` sits right after the dot, so the rest of the heading title (` The Question the Case Examines`) bleeds into the returned content and becomes a `<p>` paragraph. Same bug affects every `## N.` and `### N.` section call. The fix would be to advance `m1.end()` to the end of the matched line, but this is moot if we adopt the LaTeX approach.

### 2. Column-span:all breaks natural paper flow

All `h2.section-heading` elements have `column-span:all` in CSS. This forces every section heading to span the full card width, producing a "section-by-section" layout where columns reset at every `<h2>`. An academic paper should flow continuously across columns — text from one section continuing in the next column, only interrupted by page boundaries, not heading boundaries. This is an inherent structural limitation of CSS multi-column + column-span:all.

### 3. Fixed-height cards require manual pagination

Simulating printed pages with `height:11in; overflow:hidden` forces manual content splitting in Python. The build script currently has 21 hard-coded card splits. Every content edit risks overflow. This is perpetual maintenance work that LaTeX does automatically.

### 4. Firework chart iframe path

The embed uses `src="/case-study/paper_assets/firework-interactive.html"` — an absolute path that works only when served by the Astro dev server, not when index.html is opened directly via `file://`. The fix: use `src="paper_assets/firework-interactive.html"` (relative). This should be fixed regardless of which approach is adopted.

---

## Recommended Approach: LaTeX → PDF

**Tool chain:** `xelatex` (available at `/usr/bin/xelatex`, TeX Live 2023) invoked via `pandoc 3.1.3`

**Source:** `source-material/case-study/when_tenant_becomes_landlord_paper.md` (immutable — read only)

**Output:** `public/case-study/case-study.pdf` + updated `public/case-study/index.html`

**Why xelatex over pdflatex:** xelatex natively supports system fonts (EB Garamond, Linux Libertine) without the OTF/TTF conversion step that pdflatex requires. Better Unicode handling.

---

## Implementation Steps

### Step 1: Preprocessing script

Create `scripts/preprocess-case-study.py` that reads the immutable source and produces a clean markdown for pandoc. Transformations:
- Strip `<figure>...</figure>` HTML blocks and replace with pandoc-compatible `![caption](path)` figure syntax
- Remap image paths: `paper_assets/foo.png` → absolute path to `public/case-study/paper_assets/foo.png`
- Replace Exhibit 2 firework blockquote with a static note: "Exhibit 2. The Firework Chart is available as an interactive web chart at [link]."
- Transform `> **Title.** body` blockquote callouts into a custom pandoc div: `:::callout` blocks (pandoc fenced divs, which the LaTeX template converts to tcolorbox)
- Strip the HTML `<span class="category-number">` tags in the References section headings
- Output to a temp file (not a source file — temp files go in `/tmp/` or `scripts/.build/`)

### Step 2: LaTeX template

Create `templates/case-study-latex.tex` — a pandoc LaTeX template:
- Document class: `article` with `twocolumn` option
- Font: EB Garamond via `fontspec` (`\setmainfont{EB Garamond}`). Fallback: Linux Libertine O (ships with TeX Live, no install needed).
- Margins: 1in all sides (standard academic)
- Two-column body, single-column title + abstract
- `tcolorbox` for callout blocks (the "Case decision frame" and "Evidence discipline" boxes, plus committee checkpoints)
- Running footer: page number centered
- `hyperref` for PDF links (the firework chart reference becomes a clickable URL)
- Caption formatting matching the paper's style
- Section numbering: preserve existing numbers from source (don't auto-number)

### Step 3: Build script

Create `scripts/build-case-study-pdf.sh`:
```bash
#!/bin/bash
set -e
# 1. Preprocess markdown
python3 scripts/preprocess-case-study.py
# 2. Convert to PDF via pandoc + xelatex
pandoc /tmp/case-study-clean.md \
  --template templates/case-study-latex.tex \
  --pdf-engine=xelatex \
  --pdf-engine-opt=-output-directory=/tmp \
  -o public/case-study/case-study.pdf
echo "Built: public/case-study/case-study.pdf"
```

### Step 4: Update case study page

Replace `public/case-study/index.html` with a clean page that:
- Uses the same site nav/header as the rest of nosmanifesto.org
- Embeds the PDF: `<embed src="case-study.pdf" type="application/pdf" width="100%" style="height:90vh">`
- Includes a download link: `<a href="case-study.pdf" download>Download PDF</a>`
- Includes the Firework Chart as a separate section below the PDF embed (using the existing `firework-interactive.html`, with relative iframe src)
- No page cards, no two-column CSS simulation, no fixed-height containers

This is generated by the build script, not handwritten.

---

## Figures in Scope

| Exhibit | File | Treatment |
|---------|------|-----------|
| 1. Configuration Ladder | `paper_assets/configuration-ladder.png` | Include in PDF as figure |
| 2. Firework Chart | `paper_assets/firework-interactive.html` | Interactive-only; note in PDF, full embed on web page |
| 3. Vendor Positioning Matrix | `paper_assets/vendor-positioning-matrix.png` | Include in PDF as figure |
| 4. Cost-to-Value Migration | `paper_assets/cost-to-value-migration.png` | Include in PDF as figure |
| 5. Microsoft Trifurcation | `paper_assets/microsoft-trifurcation.png` | Include in PDF as figure |

---

## What This Does Not Change

- Source markdown at `source-material/case-study/when_tenant_becomes_landlord_paper.md` — untouched
- `public/case-study/paper_assets/` images — untouched
- `public/case-study/paper_assets/firework-interactive.html` — fix only the relative iframe path issue (one-line change)
- All other site pages

---

## Open Question: Firework iframe path fix

In the current `index.html`, the firework iframe uses `src="/case-study/paper_assets/firework-interactive.html"`. This absolute path works from the Astro dev server but not from `file://`. The new build should use `src="paper_assets/firework-interactive.html"` (relative). Should this same fix also be applied to the current `firework-wrap` iframe inside the existing HTML build, or only in the new build? (Recommendation: apply it in both, takes 30 seconds.)
