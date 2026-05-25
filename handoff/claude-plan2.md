# Human Question Page — Delivery Status & 404 Diagnosis

**Date:** 2026-05-22  
**Status:** Awaiting user review. No further implementation until approved.

---

## 1. Changes Implemented Since Last Callout

### Homepage (`src/pages/index.astro`)
- Removed the Hero component; rewrote hero section inline with the "nOS is more than a manifesto" platform text added below the subline inside the dark navy hero
- Published full manifesto content inline (all seven sections from source-material/manifesto/The_nOS_Manifesto_Final.md)
- Deleted the "Featured Domains" section (dark navy HQ card preview with four topic cards)
- Moved the Sign / Add Your Name CTA between the manifesto and the four platform cards
- Removed max-width constraints from hero headline, hero subline, section intro, and sign description
- Reordered manifesto: The Core Values of the nOS now appears first; The Inevitable Migration renamed to "Why? The Inevitable Migration"

### Width fixes (`src/styles/global.css`, `src/components/Hero.astro`)
- Removed `p { max-width: 68ch }` from global.css
- Removed `max-width: 18ch` from `.hero-headline` in Hero.astro
- Removed `max-width: 52ch` from `.hero-subline` in Hero.astro

### Faith & Identity pilot page (`public/human-question/faith-identity-human-condition/index.html`)
- File copied from source (immutable source file untouched)
- CSS appended to existing `<style>` block: Layer 1 (global nav), Layer 2 (topic nav), Layer 3 position override (`top: 80px`), scroll margin override (`130px`), responsive width strategy (`min(88vw, 1500px)`), bottom nav styles, mobile adjustments
- Layer 1 (global site nav) HTML injected after `<body>`
- Layer 2 (HQ topic nav with all 10 topics) HTML injected after Layer 1

### MDX placeholder deleted
- `src/pages/human-question/faith-identity-human-condition/index.mdx` — deleted

---

## 2. Files Edited

| File | Change |
|------|--------|
| `src/pages/index.astro` | Full rewrite — new structure, inline manifesto, section reorder |
| `src/styles/global.css` | Removed `p { max-width: 68ch }` |
| `src/components/Hero.astro` | Removed two max-width constraints |
| `public/human-question/faith-identity-human-condition/index.html` | Created (copy of source) + CSS append + two nav layers injected |
| `src/pages/human-question/faith-identity-human-condition/index.mdx` | Deleted |

---

## 3. Proposed Changes Still Pending

The faith-identity page is in a **partial state**. These edits have NOT been applied yet:

| Pending edit | Location in file |
|---|---|
| `.site-brand` link: `href="index.html"` → `href="/"` | Line ~140 (header section) |
| Glossary link in local question nav: `href="glossary.html"` → `href="/glossary/"` | Local nav |
| 10 batch navigator links: relative HTML filenames → site routes | Series Complete section |
| Bottom nav HTML injection (after `</main>`, before `<footer>`) | End of main content |
| Legacy footer links removed: `← Main Report`, `AI Glossary →`, `← Batch 1: Technical` | Footer |

These pending edits are functional/link fixes and the bottom nav addition. They do not affect the visual rendering of the nav layers or page width — the visual changes (CSS + nav HTML) are already in the file.

**The 404 is the blocking issue, not the pending edits.**

---

## 4. Why the Page Returns 404 — Diagnosis

The file exists at the correct path:
```
public/human-question/faith-identity-human-condition/index.html
```

Astro's dev server should serve files from `public/` as static assets at matching routes. The expected route is:
```
/human-question/faith-identity-human-condition/
```

The 404 is most likely caused by one of the following:

**Most likely cause — dev server not watching new public/ files:**  
The dev server was already running when the `public/` file was created. Astro's Vite-based dev server sometimes does not hot-reload new static files added to `public/` after startup. The file exists on disk but the dev server's file watcher did not register it. A restart should fix this.

**Secondary possible cause — empty src/pages directory:**  
After deleting the `index.mdx`, an empty directory remains at:
```
src/pages/human-question/faith-identity-human-condition/
```
It is unlikely but possible that an empty directory at that path interferes with Astro's routing resolution for the same route. Deleting the empty directory may help.

**Confirmed not the cause:**  
The MDX placeholder was successfully deleted. There is no competing page file at that route.

---

## 5. Risks

1. **Page in partial state:** If the 404 is resolved and you view the page, the link fixes and bottom nav are not yet applied. The nav layers and CSS are present. Links inside the page (glossary, batch navigator, site-brand) will point to old standalone HTML paths that do not exist on the new site. These are broken links, not broken layout.

2. **Ethics page still has two-layer nav:** `public/human-question/ethics-society-human-impact/index.html` was modified earlier with the old (pre-repair-plan) two-layer approach. It is not ready for review. It should be redone after the faith-identity pilot is approved.

3. **Nine remaining MDX placeholders:** The other eight HQ topics (excluding faith-identity and ethics) still have MDX placeholder pages in `src/pages/human-question/`. These will render with the wrong Astro layout (HumanQuestionLayout with left sidebar) if their routes are visited.

---

## 6. Verification Checklist

After the dev server is restarted:

- [ ] `http://localhost:4321/human-question/faith-identity-human-condition/` returns 200 (not 404)
- [ ] Page loads with three stacked horizontal nav bars visible at top
- [ ] Global nav (Layer 1, navy): `nOS | The Human Question | Case Study | Essays | About | Sign the Manifesto`
- [ ] Topic nav (Layer 2, slate): `Faith & Identity` label on left + 10 topic links
- [ ] Question nav (Layer 3, slate): `Q1 Faith Traditions | Q2 Cognitive Colonialism | Q3 Predictive Policing | Q4 AI Caregiving | Glossary →`
- [ ] Content uses broad desktop width (approx 88% of viewport)
- [ ] No nav bar overlaps body content on scroll
- [ ] Q1 anchor scrolls correctly with question title visible below all three nav layers
- [ ] Source page content (verdict legend, question cards, sidebars, callouts) appears unchanged from source
- [ ] Homepage still loads at `http://localhost:4321/`

---

## 7. Exact Commands to Run

**Step 1 — Stop the existing dev server**  
In your VS Code terminal (the one running the dev server), press `Ctrl+C`.

**Step 2 — Delete the empty src directory (optional but recommended)**
```bash
rmdir ~/projects/nosmanifesto-site/src/pages/human-question/faith-identity-human-condition
```

**Step 3 — Restart the dev server with network access**
```bash
cd ~/projects/nosmanifesto-site && npm run dev -- --host --port 4321
```

**Step 4 — Open the page**  
Once the server shows "ready", paste this into your browser:
```
http://localhost:4321/human-question/faith-identity-human-condition/
```

If localhost still does not resolve, run this in a second terminal tab to open it via Windows shell:
```bash
cmd.exe /c start http://localhost:4321/human-question/faith-identity-human-condition/
```

---

## 8. Approval Checkpoint

Do not implement any further changes until you confirm:

1. The page renders after the dev server restart
2. The three-layer nav structure looks correct
3. The width and body content are acceptable
4. You approve proceeding with the remaining five pending edits (links + bottom nav)

After that approval, the pending edits will be applied and a repair report written to `handoff/human-question-repair-report.md`.
