# Navigation Alignment Plan — CONFIRMED APPROACH

**Status:** Approved by user 2026-05-22. Implementing now.

---

## Layer 1 — Global Site Nav

- `nOS` wordmark: unchanged
- All other links: font-size × 1.5 (from 13px → 20px); padding reduced to keep bar height unchanged (~40px)
- Active section link gets `color: var(--gold)` — on Human Question pages, "The Human Question" is gold
- "Sign the Manifesto" stays as plain text link, same style as other items, pushed right with `margin-left: auto`

## Layer 2 — HQ Topic Nav

- Remove the left-side current topic label entirely (`<span class="tnav-current">`) — no longer needed
- Remove the vertical gold separator line that went with it
- Topics displayed: `TECHNICAL | ECONOMICS | GEOPOLITICS | ETHICS | EXISTENTIAL | REGULATORY | SAFETY & SECURITY | INFRASTRUCTURE | FAITH & IDENTITY | SCIENCE & DOMAINS`
- Font-size × 1.5 (from 12px → 18px); padding reduced to keep bar height unchanged (~33px)
- Text uppercase; vertically centered (equal padding above/below via flexbox align-items:center)
- Active topic (the current page's group) in `var(--gold)`; all others in muted opacity

## Layer 3 — Question Nav

- Remove left-side topic brand label (`<span class="page-nav-brand">`) — hidden via CSS
- Remove vertical gold separator that came with it
- As user scrolls, the question currently in the active frame is highlighted in `var(--gold)`
- Implemented via IntersectionObserver / scroll listener in injected JavaScript

## Bottom Nav

- Accepted as-is per user confirmation

## Active State Color Rule (all layers)

- Active item: `var(--gold)` (#c9922a)
- All others: existing muted opacity color — no new colors introduced

## Pending Functional Edits Applied in Same Pass

1. `.site-brand` href: `index.html` → `/`
2. Glossary link in question nav: `glossary.html` → `/glossary/`
3. Ten batch navigator links: relative HTML filenames → site routes
4. Bottom nav HTML injected after `</main>`
5. Legacy footer links removed

## File Changed

`public/human-question/faith-identity-human-condition/index.html` only.  
Source file remains untouched.
