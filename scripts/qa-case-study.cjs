#!/usr/bin/env node
/**
 * Headless QA for the case study page.
 * Checks each .case-page card for clipped content using Playwright.
 * Clipped = element exists in DOM but its bounding box bottom exceeds the card's visible bottom.
 */
const { chromium } = require('playwright');
const path = require('path');

const FILE_URL = 'file://' + path.resolve(__dirname, '../public/case-study/index.html');
// Tolerance: elements within this many px of the card boundary are flagged as warnings, not errors.
const CLIP_TOLERANCE_PX = 4;

async function run() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  // A4-ish viewport — wide enough to trigger two-column layout
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(FILE_URL, { waitUntil: 'load' });

  const results = await page.evaluate((tolerance) => {
    const cards = Array.from(document.querySelectorAll('.case-page'));
    const report = [];

    cards.forEach((card, idx) => {
      const cardRect = card.getBoundingClientRect();
      // The visible bottom of the card, relative to the document
      const cardTop    = card.offsetTop;
      const cardBottom = cardTop + card.clientHeight;  // clientHeight respects overflow:hidden

      // Walk every descendant element and check if it's clipped
      const clipped = [];
      const all = card.querySelectorAll('*');
      all.forEach(el => {
        // Skip elements that are themselves layout containers (we want leaf-ish content)
        const tag = el.tagName.toLowerCase();
        if (['div', 'section', 'article', 'figure'].includes(tag) && el.children.length > 0) return;

        const rect = el.getBoundingClientRect();
        if (rect.height === 0 && rect.width === 0) return; // invisible/zero-size

        // getBoundingClientRect is relative to viewport — convert to document coords
        const elBottom = card.offsetTop + (rect.bottom - cardRect.top);

        if (elBottom > cardBottom + tolerance) {
          const text = (el.textContent || '').trim().slice(0, 80);
          clipped.push({
            tag,
            class: el.className || '',
            text,
            overflowPx: Math.round(elBottom - cardBottom),
          });
        }
      });

      // Collect headings present in DOM for this card (to cross-check visibility)
      const headings = Array.from(card.querySelectorAll('h1,h2,h3,h4')).map(h => ({
        tag: h.tagName,
        text: h.textContent.trim().slice(0, 80),
      }));

      report.push({
        card: idx + 1,
        type: card.className,
        cardHeightPx: card.clientHeight,
        clippedCount: clipped.length,
        clipped,
        headings,
      });
    });

    return report;
  }, CLIP_TOLERANCE_PX);

  await browser.close();

  let hasErrors = false;
  results.forEach(card => {
    const pageNum = card.card;
    if (card.clippedCount === 0) {
      console.log(`  Card ${String(pageNum).padStart(2)}: OK  (${card.headings.map(h => h.text).join(' | ') || 'no headings'})`);
    } else {
      hasErrors = true;
      console.log(`\n  Card ${String(pageNum).padStart(2)}: *** ${card.clippedCount} CLIPPED ELEMENT(S) ***`);
      card.clipped.forEach(el => {
        console.log(`    [${el.tag}${el.class ? '.' + el.class.split(' ')[0] : ''}] overflows by ${el.overflowPx}px: "${el.text}"`);
      });
      console.log(`    Headings on this card: ${card.headings.map(h => h.text).join(' | ') || '(none)'}`);
    }
  });

  console.log('');
  if (hasErrors) {
    console.log('RESULT: FAIL — clipped content detected. Cards above need content split or reduced.');
    process.exit(1);
  } else {
    console.log('RESULT: PASS — no clipped content detected across all 18 cards.');
  }
}

run().catch(err => {
  console.error('QA script error:', err);
  process.exit(1);
});
