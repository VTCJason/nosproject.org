# Human Question Page Repair Plan

**Status:** Awaiting user approval before any implementation.  
**Pilot page:** `source-material/human-question/10_QA_Faith_Identity_Human_Condition.html`  
**Target route:** `/human-question/faith-identity-human-condition/`  
**Date drafted:** 2026-05-22

---

## 1. Diagnosis of Current Defects

### Defect 1 — Narrow content width

**Root cause:** Every source HTML file contains:
```css
.header-inner  { max-width: 1040px; margin: 0 auto; }
.page-nav-inner{ max-width: 1040px; margin: 0 auto; }
.page-body     { max-width: 1040px; margin: 0 auto; }
```
At a 1440px viewport, 1040px is 72% of width. At 1920px it falls to 54%. The evidence in `SizeChanges.jpg` shows content stopping well left of the right viewport edge. This is the source HTML constraint — it applies to all 10 files identically.

### Defect 2 — Navigation layer count and structure

The approved target (`new_Stacked_menus.jpg`) requires **three** stacked horizontal sticky nav layers. The previous implementation delivered **two** layers (global site nav + local question nav). The middle layer — the HQ topic nav showing all 10 topic links with the current topic highlighted — was missing entirely.

### Defect 3 — Nav top/z-index values now incorrect

With three layers instead of two, the sticky offsets must be recalculated:
- Layer 1 (global): `top: 0`, z-index 300
- Layer 2 (topic): `top: 40px`, z-index 200  
- Layer 3 (question): `top: 80px`, z-index 100

The previous implementation set Layer 3 (question nav) to `top: 40px`, which assumed only one layer above it. This causes it to collide with the topic nav in the new three-layer model.

### Defect 4 — Wrong bottom navigation

The `Claude_Delivered_Bottom_Nav_Human_Questions.jpg` shows the Astro MDX placeholder page rendering (not the public HTML approach). That page uses `HumanQuestionLayout.astro`, which wraps content in a left-sidebar layout and appends the full Astro `SiteFooter`. This was the wrong delivery because:

- The HQ pages must be served as static HTML from `public/` — not wrapped by any Astro layout.
- Nine of the ten MDX placeholder pages in `src/pages/human-question/*/index.mdx` are still active and will render with the wrong layout if their route is visited.

The ethics page I modified earlier (`public/human-question/ethics-society-human-impact/index.html`) used a two-layer approach with a `.page-nav-btm` bottom nav. That bottom nav approach may be close to correct but needs to be re-evaluated against the pilot page result before applying anywhere.

### Defect 5 — Scroll margin insufficient for three nav layers

The previous implementation set `.qa-card { scroll-margin-top: 120px }`. With three sticky nav bars at ~40px each, the anchor scroll position needs `scroll-margin-top: 130px` (120px of nav height plus ~10px of visual breathing room).

### Defect 6 — Relative links in source HTML

The source HTML files contain relative links for:
- `.site-brand href="index.html"` → should be `href="/"`
- `href="glossary.html"` → should be `href="/glossary/"`
- Batch navigator links (`href="QA_Technical_Demystification.html"` etc.) → should be proper site routes

---

## 2. Exact Files Causing the Defects

| File | Defect |
|------|--------|
| All source HTML in `source-material/human-question/*.html` | `max-width: 1040px` on three selectors |
| All source HTML in `source-material/human-question/*.html` | `.page-nav { top: 0 }` — assumes it is the topmost sticky element |
| All source HTML in `source-material/human-question/*.html` | `.qa-card { scroll-margin-top: 80px }` — assumes single sticky layer |
| `src/pages/human-question/*/index.mdx` (9 pages, excluding ethics which was deleted) | Still rendering with `HumanQuestionLayout.astro` — wrong Astro layout |
| `public/human-question/ethics-society-human-impact/index.html` | Two-layer nav approach; needs to wait for pilot approval before redoing |

**Source files are immutable.** All corrections are applied only to the copied output files in `public/`.

---

## 3. Exact Files to Edit for the Pilot

| Action | File |
|--------|------|
| **Create (copy from source)** | `public/human-question/faith-identity-human-condition/index.html` |
| **Append CSS + inject HTML** (inline in copied file) | Same file — no other files touched |
| **Do not touch** | `source-material/human-question/10_QA_Faith_Identity_Human_Condition.html` |
| **Do not touch yet** | All other `public/` or `src/` files |

---

## 4. Proposed Repair Approach

The repair is entirely scoped to the single copied output file. No Astro components, layouts, or MDX pages are modified. All CSS additions are appended to the existing `<style>` block; all HTML additions are injected at specific positions in `<body>`.

**Zero changes to the existing source HTML structure.** The only modifications are:
1. Appended CSS overrides (scoped to new selectors, plus targeted overrides of `.page-nav` top/z-index and `.qa-card` scroll-margin)
2. Injected HTML (two new `<nav>` elements; one at top of body, one at bottom of main)
3. Four attribute changes (`href` values for brand link, glossary, and batch navigator links)

---

## 5. How Source HTML Fidelity Will Be Preserved

- The file is copied byte-for-byte from source before any edits.
- No existing CSS rules are deleted or rewritten; only appended overrides are added.
- No existing HTML elements are removed or restructured, except:
  - `href="index.html"` → `href="/"` on the `.site-brand` link
  - `href="glossary.html"` → `href="/glossary/"` on glossary links
  - Batch navigator `href` values updated to site routes (content of the batch blocks is unchanged)
  - Legacy footer nav links (`← Main Report | AI Glossary → | ...`) removed from the `<footer>` (these are the old standalone-HTML navigation links, not content)
- Question cards, sidebars, callouts, verdict badges, verdict legend, section intro, typography, colors, spacing, and responsive grid are entirely untouched.

**Open question for user confirmation:** The review evidence images (`HumanQuestion_Desired_Format_Changes.jpg`, `SizeChanges.jpg`) show green Xs crossing out the `.header-meta` meta pills ("4 Questions", "April 2026", "Faith · Language · Policing · Elder Care", "Final Batch"). Are the meta pills an authorized removal? They are in the page header, not the question body. If yes, I will add a CSS rule `display:none` to `.header-meta` (no HTML deletion). If no, they remain unchanged.

---

## 6. How the Desired Stacked Top Navigation Will Be Implemented

Reference: `new_Stacked_menus.jpg` and `SizeChanges.jpg`.

### Three-layer structure

**Layer 1 — Global site nav**
- Position: `sticky; top: 0; z-index: 300`
- Background: `var(--navy)` (`#0d1b2a`)
- Bottom border: `2px solid var(--gold)`
- Height: ~40px
- Content: `nOS` wordmark (serif, gold) | `The Human Question | Case Study | Essays | About | Sign the Manifesto`
- Nav order from user instructions (2026-05-22): `nOS | The Human Question | Case Study | Essays | About | Sign the Manifesto`
- "Sign the Manifesto" rendered as a gold accent link/button on the right (as shown in `SizeChanges.jpg`)

**Layer 2 — HQ topic nav**
- Position: `sticky; top: 40px; z-index: 200`
- Background: `var(--slate)` (`#1c2f45`)
- Bottom border: `2px solid var(--gold)` (or `1px solid rgba(201,146,42,.3)` — will match the image closely)
- Height: ~40px
- Content: Current topic label on left (e.g., "Faith & Identity" in serif, gold) + 10 topic links across:
  `Technical | Economics | Geopolitics & AI | Ethics | Existential | Regulatory | Safety & Security | Infrastructure | Faith & Identity | Science & Domains`
- Current topic link is visually distinguished (gold color, no underline)
- All topic links have full site routes (`/human-question/technical-demystification/` etc.)
- Overflow: `overflow-x: auto; scrollbar-width: none` for narrow viewports

**Layer 3 — Question anchor nav (existing `.page-nav`)**
- Override existing CSS: `top: 0` → `top: 80px`; `z-index: 100` → `z-index: 100` (unchanged)
- This layer already exists in the source HTML; only the `top` value changes

### CSS addition summary (appended to existing `<style>`)

```css
/* === GLOBAL NAV (Layer 1) === */
#nos-snav {
  background: var(--navy);
  border-bottom: 2px solid var(--gold);
  position: sticky; top: 0; z-index: 300;
  padding: 0 40px;
}
#nos-snav-inner {
  max-width: 1400px; margin: 0 auto;
  display: flex; align-items: center; gap: 0;
  overflow-x: auto; scrollbar-width: none;
}
#nos-snav-inner::-webkit-scrollbar { display: none; }
.snav-wordmark {
  font-family: 'Libre Baskerville', serif;
  font-size: 15px; font-weight: 700;
  color: var(--gold); text-decoration: none;
  padding: 12px 14px 12px 0;
  border-right: 1px solid rgba(201,146,42,.3);
  margin-right: 6px; white-space: nowrap;
}
.snav-link {
  font-family: 'Courier Prime', monospace;
  font-size: 9px; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: rgba(245,240,232,.55); text-decoration: none;
  padding: 12px 11px; white-space: nowrap;
  border-bottom: 2px solid transparent; margin-bottom: -2px;
  transition: color .2s, border-color .2s;
}
.snav-link:hover { color: var(--amber); border-bottom-color: var(--amber); }
.snav-sign {
  margin-left: auto;
  font-family: 'Courier Prime', monospace;
  font-size: 9px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--navy); background: var(--gold);
  text-decoration: none; padding: 6px 14px;
  border-radius: 2px; white-space: nowrap;
}
.snav-sign:hover { background: var(--amber); }

/* === TOPIC NAV (Layer 2) === */
#nos-topicnav {
  background: var(--slate);
  border-bottom: 1px solid rgba(201,146,42,.35);
  position: sticky; top: 40px; z-index: 200;
  padding: 0 40px;
}
#nos-topicnav-inner {
  max-width: 1400px; margin: 0 auto;
  display: flex; align-items: center; gap: 0;
  overflow-x: auto; scrollbar-width: none;
}
#nos-topicnav-inner::-webkit-scrollbar { display: none; }
.tnav-current {
  font-family: 'Libre Baskerville', serif;
  font-size: 11px; font-weight: 700;
  color: var(--gold); white-space: nowrap;
  padding: 11px 14px 11px 0;
  border-right: 1px solid rgba(201,146,42,.25);
  margin-right: 4px;
}
.tnav-link {
  font-family: 'Courier Prime', monospace;
  font-size: 8.5px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
  color: rgba(245,240,232,.45); text-decoration: none;
  padding: 11px 10px; white-space: nowrap;
  transition: color .2s;
}
.tnav-link:hover, .tnav-link.active { color: var(--amber); }

/* === OVERRIDE: Layer 3 question nav position === */
.page-nav { top: 80px !important; z-index: 100 !important; }

/* === SCROLL MARGIN: accounts for all three sticky layers === */
.qa-card { scroll-margin-top: 130px !important; }

/* === WIDTH OVERRIDE (minimal, scoped) === */
.header-inner, .page-body, .page-nav-inner { max-width: 1400px !important; }

/* === BOTTOM NAV === */
.page-nav-btm {
  background: var(--slate);
  border-top: 2px solid var(--gold);
  padding: 0 40px;
}
.page-nav-btm .page-nav-inner a {
  border-bottom: none; margin-bottom: 0;
  border-top: 2px solid transparent; margin-top: -2px;
}
.page-nav-btm .page-nav-inner a:hover {
  border-top-color: var(--amber); border-bottom: none;
}

/* === MOBILE ADJUSTMENTS === */
@media (max-width: 680px) {
  #nos-snav, #nos-topicnav { padding: 0 20px; }
  .snav-link { padding: 12px 8px; font-size: 8px; }
  .tnav-link { padding: 11px 7px; font-size: 7.5px; }
  .page-nav-btm { padding: 0 20px; }
  .page-nav { top: 76px !important; } /* narrower bars on mobile */
}
```

### HTML injected after `<body>` tag (before `<header class="page-header">`)

```html
<nav id="nos-snav" aria-label="Site navigation">
  <div id="nos-snav-inner">
    <a class="snav-wordmark" href="/">nOS</a>
    <a class="snav-link" href="/human-question/">The Human Question</a>
    <a class="snav-link" href="/case-study/">Case Study</a>
    <a class="snav-link" href="/essays/">Essays</a>
    <a class="snav-link" href="/about/">About</a>
    <a class="snav-sign" href="/sign/">Sign the Manifesto</a>
  </div>
</nav>

<nav id="nos-topicnav" aria-label="Human Question topics">
  <div id="nos-topicnav-inner">
    <span class="tnav-current">Faith &amp; Identity</span>
    <a class="tnav-link" href="/human-question/technical-demystification/">Technical</a>
    <a class="tnav-link" href="/human-question/economics-labor-industry/">Economics</a>
    <a class="tnav-link" href="/human-question/geopolitics-national-security/">Geopolitics &amp; AI</a>
    <a class="tnav-link" href="/human-question/ethics-society-human-impact/">Ethics</a>
    <a class="tnav-link" href="/human-question/existential-frontier/">Existential</a>
    <a class="tnav-link" href="/human-question/regulatory-legal-governance/">Regulatory</a>
    <a class="tnav-link" href="/human-question/safety-security-information-integrity/">Safety &amp; Security</a>
    <a class="tnav-link" href="/human-question/infrastructure-environment/">Infrastructure</a>
    <a class="tnav-link active" href="/human-question/faith-identity-human-condition/">Faith &amp; Identity</a>
    <a class="tnav-link" href="/human-question/science-knowledge-domains/">Science &amp; Domains</a>
  </div>
</nav>
```

---

## 7. How the Desired Bottom Navigation Will Be Implemented

Reference: `HumanQuestion_Desired_Format_Changes.jpg`.

The desired bottom nav mirrors the local question nav (Layer 3, `.page-nav`), placed at the bottom of `<main>` before `<footer>`, with:
- Same slate background as the top local nav
- Gold border on the **top** edge (bookending the gold border on the bottom of the top nav)
- Same question links as the top local nav
- No sticky positioning — it is in normal flow

This replaces the legacy footer nav links (`← Main Report | AI Glossary →`).

### HTML injected after `</main>` (before `<footer class="page-footer">`)

```html
<nav class="page-nav-btm" aria-label="Faith &amp; Identity topic navigation">
  <div class="page-nav-inner">
    <span class="page-nav-brand">Faith &amp; Identity</span>
    <a href="#q1">Q1 Faith Traditions</a>
    <a href="#q2">Q2 Cognitive Colonialism</a>
    <a href="#q3">Q3 Predictive Policing</a>
    <a href="#q4">Q4 AI Caregiving</a>
    <a href="/glossary/">Glossary</a>
  </div>
</nav>
```

### Legacy footer links to remove

In the `<footer class="page-footer">`, remove:
```html
<a href="index.html">← Main Report</a> &nbsp;·&nbsp;
<a href="glossary.html">AI Glossary →</a> &nbsp;·&nbsp;
```
(and any remaining batch navigation link in the footer)

---

## 8. Width Correction Plan

**Method:** Append a three-selector override to the end of the existing `<style>` block.

```css
.header-inner, .page-body, .page-nav-inner { max-width: 1400px !important; }
```

**Why 1400px:**  
At 1440px viewport → 97% of width (leaves 20px padding each side).  
At 1920px viewport → 73% of width.  
At 1280px viewport → full width minus padding.  
This satisfies "at least two-thirds" at common desktop sizes while not overflowing on mid-range displays.

**What is NOT changed:**
- `.header-desc { max-width: 660px }` — retained as a typographic constraint for the lede paragraph
- `.section-intro p { max-width: 780px }` — retained (editorial measure for the intro prose)
- `.qa-body { grid-template-columns: 1fr 300px }` — retained; the sidebar stays at 300px, the main column expands

The new global nav, topic nav, and bottom nav all use the same `max-width: 1400px` on their inner containers, keeping all layers visually aligned.

---

## 9. Batch Navigator Link Updates

The faith-identity source HTML contains a "batch navigator" section at the bottom of `<main>` with relative links to all 10 HTML files. These will be updated to site routes:

| Old | New |
|-----|-----|
| `QA_Technical_Demystification.html` | `/human-question/technical-demystification/` |
| `QA_Economics_Labor_Industry.html` | `/human-question/economics-labor-industry/` |
| `QA_Geopolitics_National_Security.html` | `/human-question/geopolitics-national-security/` |
| `QA_Ethics_Society_Human_Impact.html` | `/human-question/ethics-society-human-impact/` |
| `QA_Existential_Frontier.html` | `/human-question/existential-frontier/` |
| `QA_Regulatory_Legal_Governance.html` | `/human-question/regulatory-legal-governance/` |
| `QA_Safety_Security_Information_Integrity.html` | `/human-question/safety-security-information-integrity/` |
| `QA_Infrastructure_Environment.html` | `/human-question/infrastructure-environment/` |
| `QA_Science_Knowledge_Domains.html` | `/human-question/science-knowledge-domains/` |
| `QA_Faith_Identity_Human_Condition.html` | `/human-question/faith-identity-human-condition/` |

---

## 10. Anchor Verification Plan

The faith-identity page has four question anchors: `#q1`, `#q2`, `#q3`, `#q4`.

After implementation, verify each anchor by:
1. Opening the page in the dev server at `http://localhost:432x/human-question/faith-identity-human-condition/`
2. Clicking `Q1 Faith Traditions` in the local question nav → confirm Q1 scrolls to view with the question title visible below all three nav layers (not hidden behind them)
3. Repeat for Q2, Q3, Q4
4. Confirm `Glossary →` link routes to `/glossary/` (will 404 until the glossary page is built — expected)
5. Scroll to bottom and verify the bottom nav's question links jump correctly
6. Check mobile: on viewport ≤ 680px, confirm no nav layers overlap content and horizontal scroll on navs works

**Expected scroll-margin-top:** With three layers at ~40px each = 120px + 10px buffer = 130px set on `.qa-card`. If any Q-card header is clipped, increase by 10px increments.

---

## 11. Risks and Uncertainties

**1. Three-layer nav height may not be exactly 40px per layer.**  
The nav bar height depends on padding. The current `.page-nav` uses `padding: 13px` top/bottom on links, making the bar ~38-40px. All three layers are built to the same spec, so 40px × 3 = 120px should be accurate. Will verify by inspection.

**2. The topic nav overflows on mid-width screens.**  
All 10 topic labels are long. The `overflow-x: auto; scrollbar-width: none` treatment hides scrollbars but allows horizontal scroll on the topic bar on narrow screens. This is the same approach used for the existing question nav and is acceptable.

**3. `!important` overrides on `.page-nav` top/z-index.**  
The existing CSS has `.page-nav { top: 0 }`. We cannot edit the existing rule (it must remain to preserve source fidelity for the CSS that's there). The appended `!important` override is the minimal-impact method. If the user prefers removing `!important` and instead editing the existing rule in place, that can be done — but it requires removing a single property value from the source-copied inline CSS, which is a slightly more invasive edit.

**4. Meta pill removal — not yet confirmed.**  
The evidence images cross out `.header-meta` (the small tag pills). This plan does NOT remove them unless the user explicitly confirms. If confirmed, the implementation is `display: none` on `.header-meta` — no HTML deletion.

**5. Ethics page now has the old two-layer approach.**  
The ethics page (`public/human-question/ethics-society-human-impact/index.html`) was modified in the previous session with the two-layer (global + question) approach. Once the pilot (faith-identity) is approved, the ethics page will need to be redone with the three-layer approach. Do not use the ethics page for review until it is re-done.

**6. Nine MDX placeholder pages still live.**  
`src/pages/human-question/[9 topic dirs]/index.mdx` will render with `HumanQuestionLayout.astro` if their routes are visited. These pages should be deleted or disabled once the corresponding `public/` HTML files are ready. For the pilot, only the faith-identity MDX placeholder needs to be deleted — after review confirms the public HTML approach is correct.

**7. Nav order.**  
Previous session approved: `nOS | Case Study | The Human Question | Essays | About`.  
Current instructions specify: `nOS | The Human Question | Case Study | Essays | About | Sign the Manifesto`.  
This plan uses the current instructions. If the order has changed, `SiteHeader.astro` will also need updating for consistency across the Astro-rendered site.

---

## 12. Commands to Run

After approval, in order:

```bash
# 1. Copy source file (do not edit source)
mkdir -p ~/projects/nosmanifesto-site/public/human-question/faith-identity-human-condition
cp ~/projects/nosmanifesto-site/source-material/human-question/10_QA_Faith_Identity_Human_Condition.html \
   ~/projects/nosmanifesto-site/public/human-question/faith-identity-human-condition/index.html

# 2. Delete the MDX placeholder for this route
rm ~/projects/nosmanifesto-site/src/pages/human-question/faith-identity-human-condition/index.mdx

# 3. Start dev server (if not already running)
cd ~/projects/nosmanifesto-site && npm run dev

# 4. Open in browser to verify
# http://localhost:432x/human-question/faith-identity-human-condition/
```

All subsequent edits are applied to the copied file only via Claude's Edit tool.

---

## 13. Explicit Approval Checkpoint

**Do not implement until you review and approve this plan.**

Specific items that require your confirmation before proceeding:

1. **Meta pill removal** — Are the `.header-meta` pill tags authorized for removal? (Evidence images show green Xs, but user instructions name only two authorized changes: navigation.)

2. **Nav order** — Confirming current order: `nOS | The Human Question | Case Study | Essays | About | Sign the Manifesto`. Does "Sign the Manifesto" appear as a gold button/accent (as in `SizeChanges.jpg`) or as a plain text link?

3. **Width target** — Is `max-width: 1400px` the right target, or do you prefer a different value (e.g., 1280px, 1440px, or `none`)?

4. **Topic nav active state** — Should the current topic ("Faith & Identity") appear twice in Layer 2 (once as the left-side current label, once as a link in the topic list)? The mockup suggests yes — the current page label on the left is a fixed identifier, and the same topic also appears as a link in the horizontal list for consistency.

5. **Ethics page** — Confirm that the previously modified ethics page should be left as-is until the pilot is approved, then redone.

Once you approve, implementation begins with the faith-identity pilot only.
