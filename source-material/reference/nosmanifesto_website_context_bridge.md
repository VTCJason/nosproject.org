# nOS Manifesto Website — Context Bridge Document

## Purpose

This document is a seed brief for a new project to build **nosmanifesto.org**. It captures the website-specific context, decisions, information architecture, design direction, technical approach, and implementation priorities discussed so far.

Use it as a starting context for a new ChatGPT project, Claude Code session, Cline task, GitHub README, or product requirements document.

---

## 1. Project Overview

The site is not merely a landing page for a manifesto. It is a broader AI thought-leadership and public-intelligence platform organized around three major pillars:

1. **The nOS Thesis**
   - The nOS Manifesto.
   - The companion business case, *When the Tenant Becomes the Landlord*.
   - Signatures and rollcall for the manifesto.

2. **The Human Question**
   - A deep, question-led body of analysis about what AI means for modern society.
   - This is not FAQ content and not a simple Q&A help center.
   - It is a structured public inquiry into knowledge, power, ethics, labor, education, identity, governance, and human meaning in an AI-shaped world.

3. **Author Platform**
   - Essays, papers, and thought-leadership pieces not necessarily limited to nOS.
   - Possible future videos, public commentary, and related writing.
   - Author bio and credentials.

The site should establish brand, authority, and recognition in the AI strategy / public-intelligence / executive-education space. Monetization is not a priority, especially not on the manifesto tree.

---

## 2. Domain and Primary Property

**Target domain:** `www.nosmanifesto.org`

The website should be designed as a fast, editorial, static-first site suitable for GitHub Pages hosting.

---

## 3. Core Positioning

The site examines AI as:

- Infrastructure.
- Institution.
- Labor force.
- Interface.
- Risk surface.
- Epistemic pressure.
- Civilizational transition.
- A force reshaping the boundary between human judgment and machine capability.

The nOS Manifesto is the flagship declaration. The companion business case provides empirical and strategic grounding. The Human Question section expands beyond the manifesto into the broader implications of AI for society.

---

## 4. Naming Decision: The Human Question

Earlier candidate labels for the broader question-led section included:

- Q&A
- Briefings
- Field Guide
- Epistemology
- The Question Atlas
- The Inquiry
- The Human Question

The preferred direction is **The Human Question**.

Rationale:

- “Q&A” undersells the depth and seriousness of the section.
- “Briefings” is accurate but sounds political, news-cycle-ish, and insufficiently magnetic.
- “Epistemology” is intellectually strong but too narrow on a single axis.
- “The Human Question” has broader sphere of influence.
- It captures ethics, identity, purpose, labor, meaning, education, social cohesion, governance, and human judgment.
- It is provocative without being obscure.
- It positions the section as inquiry into what remains human, what changes, and what must be defended or reimagined as AI expands.

Recommended top-nav label:

```text
The Human Question
```

Potential section page title:

```text
The Human Question in an AI World
```

Potential subtitle:

```text
Deep questions on knowledge, power, identity, labor, ethics, society, and human judgment in an AI-mediated world.
```

Potential section intro:

```text
This is not a FAQ. It is a structured inquiry into the questions public debate keeps flattening: what AI changes, what it reveals, what it threatens, and what it makes newly possible.
```

---

## 5. Proposed Top-Level Navigation

Recommended primary navigation:

```text
nOS | The Human Question | Case Study | Essays | About
```

Alternate if shorter navigation is preferred:

```text
Manifesto | Human Question | Case Study | Essays | About
```

Suggested route structure:

```text
/
  Homepage

/manifesto/
  The nOS Manifesto

/case-study/
  When the Tenant Becomes the Landlord

/human-question/
  Landing page for the deep AI question-led analysis library

/human-question/ethics-society-human-impact/
  Example topic page

/human-question/economics-labor-industry/
/human-question/security-governance-risk/
/human-question/education-human-development/
/human-question/geopolitics-national-power/
/human-question/infrastructure-energy-compute/
/human-question/enterprise-adoption-strategy/
/human-question/creativity-media-culture/
/human-question/law-regulation-liability/
/human-question/future-scenarios-speculation/
  Additional topic clusters

/essays/
  Standalone essays, papers, and possible future video embeds

/about/
  Author bio and credentials

/sign/
  Sign the manifesto

/signatories/
  Manifesto rollcall

/references/
  Optional source spine / citation library
```

---

## 6. Homepage Direction

The homepage should not simply reproduce the manifesto. It should function as the front door to the broader intellectual project.

Suggested homepage structure:

```text
Hero
  The nOS Manifesto
  A thesis on where platform power moves when AI becomes the operating layer.

Primary CTAs
  Read the Manifesto
  Read the Business Case
  Explore The Human Question

Featured Modules
  Latest Human Question topic
  Latest Essay
  Sign the Manifesto / View Rollcall

Positioning Statement
  This site examines AI as infrastructure, institution, labor force, interface, risk surface, and civilizational pressure.

Secondary CTAs
  Read the Case Study
  Browse Essays
  About the Author
```

The manifesto remains central, but the site should not feel like a single-page campaign microsite. It should feel like the beginning of an expanding public-intelligence platform.

---

## 7. The nOS Manifesto Page

Purpose:

- Present the manifesto as a polished public declaration.
- Prioritize speed, readability, and shareability.
- Include clear CTAs to the business case and signature page.
- Preserve the editorial restraint and typographic seriousness of the current HTML preview.
- Avoid clutter, heavy interaction, or monetization.

Design requirements:

- Full-width or wide editorial reading surface, not a narrow blog column.
- Strong typographic hierarchy.
- Responsive mobile rendering.
- Minimal JavaScript.
- Anchor links optional, but useful.
- CTA to sign the manifesto.
- CTA to read the case study.
- CTA to explore The Human Question.

---

## 8. The Companion Business Case Page

Purpose:

- Present *When the Tenant Becomes the Landlord* as the empirical and strategic companion to the manifesto.
- Maintain Harvard Business Case / graduate business course credibility.
- Support two reading modes if possible:
  - Web reading mode.
  - Downloadable PDF or print-optimized version.

Requirements:

- Fast-loading page.
- Linked references as real outbound anchor links.
- Exhibits and visuals should be optimized and lazy-loaded.
- The interactive Firework Chart may be loaded separately or embedded as a lazy-loaded iframe/static preview.
- Public page should exclude private instructor framing.
- Instructor framing should remain a separate PDF available by request.

---

## 9. The Human Question Section

This is a major independent pillar.

It is not tied only to nOS or the business case. It is a broader, deeper topological analysis of what AI means to modern society: implications, conflicts, tensions, opportunities, risks, and possibilities.

The section is intended to address gaps in current public AI discourse, especially where conversation cycles are shallow, repetitive, or fail to engage the deeper implications.

### Content Style

Each Human Question topic page should support:

- Long-form question-led analysis.
- A strong topic header.
- Topic metadata.
- A sticky local topic navigation bar.
- Evidence/verdict labels.
- Question cards.
- Sidebars.
- Source blocks.
- Callout boxes.
- Acronym/tooltips if useful.
- Footer references.
- Mobile-first rendering.

The example page, **Ethics, Society & Human Impact**, includes 13 questions, verdict badges such as Verified Fact, Reasoned Analysis, Informed Speculation, and Genuinely Contested, sidebars with sources/data, and deep discussion of creativity, the Turing Trap, alignment, hyper-reality, AI companions, loneliness, relationships, work, education, children, human advantage, cognitive bandwidth, cognitive offloading, and algorithmic bias.

### Human Question Landing Page

Suggested structure:

```text
Hero
  The Human Question in an AI World
  Deep questions on knowledge, power, identity, labor, ethics, society, and human judgment in an AI-mediated world.

Intro
  This is not a FAQ. It is a structured inquiry into the questions public debate keeps flattening.

Topic Grid
  Ethics, Society & Human Impact
  Economics, Labor & Industry
  Education & Human Development
  Security, Governance & Risk
  Geopolitics & National Power
  Infrastructure, Energy & Compute
  Enterprise Adoption & Strategy
  Creativity, Media & Culture
  Law, Regulation & Liability
  Future Scenarios & Speculation

Each topic card:
  - Topic title.
  - Short description.
  - Number of questions.
  - Themes.
  - Read link.

Optional:
  - Evidence legend.
  - Search/filter by theme.
  - “Start here” recommended reading path.
```

### Topic Page Template

Suggested components:

```text
HumanQuestionLayout
HumanQuestionHero
TopicNav
VerdictLegend
QuestionCard
VerdictBadge
QuestionSidebar
SidebarBlock
SourceBlock
Callout
AcronymTooltip
FooterReferences
```

The existing example page should be converted into reusable components rather than maintained as a one-off HTML island.

---

## 10. Essays Section

“Blog” is not the preferred label. Use **Essays**.

Purpose:

- House standalone papers and thought pieces not specific to the nOS manifesto.
- Possible examples:
  - The Million Dollar Keystroke paper.
  - AI strategy essays.
  - Future video embeds or transcripts.
  - Public commentary.

Design:

- Editorial index page.
- Article cards.
- Tag/topic filtering optional.
- Individual essays use ArticleLayout.
- Avoid monetization at launch.

---

## 11. About Page

Purpose:

- Establish author credibility without overdoing credentials.
- Provide the human context behind the work.

Author credentials to include:

- MS in Finance, Johns Hopkins University, Carey Business School.
- BS in Mechanical Engineering.
- Work history across defense, manufacturing, technology, consulting.
- Adjunct Professor at Dallas Baptist University.
- Experience in technology strategy, consulting, sales, product thinking, and executive education.

Potential structure:

```text
Who I Am
Why This Site Exists
Background and Credentials
What I Am Trying to Build
Contact
```

Tone:

- Direct.
- Credible.
- Not inflated.
- Avoid corporate blandness.

---

## 12. Signature and Rollcall System

Desired feature:

- Visitors can sign the manifesto.
- A rollcall page shows approved public signatories.
- Clicking or navigating to rollcall lets visitors see who has signed.

Recommended implementation:

- GitHub Pages frontend.
- Supabase backend for dynamic signature data.
- Use public anon key only.
- Enforce Supabase Row Level Security.
- Never expose service-role keys.

Recommended signature workflow:

```text
User signs → Supabase insert → status = pending
Author/admin reviews in Supabase dashboard
Approved signatures appear on /signatories/
```

Suggested data model:

```text
signatures
  id
  display_name
  affiliation_optional
  role_optional
  city_region_optional
  country_optional
  website_optional
  statement_optional
  visibility_public
  status: pending | approved | rejected
  created_at
  approved_at
```

Important:

- Do not display submissions immediately.
- Moderation is required to prevent spam and hostile signatures.
- Signature feature should be a later phase, after static site launch.

---

## 13. Community Discussion

Do not add native comments at launch. They create moderation burden and technical complexity.

Future options:

- LinkedIn discussion.
- Email newsletter.
- Substack comments.
- Discord.
- Reddit.
- X hashtag.

Recommended first step:

- Use LinkedIn and possibly email capture.
- Avoid Discord/Reddit until there is enough demand to justify moderation overhead.

---

## 14. Design Direction

The user referenced **Kento Kawazoe’s site** as a north star: editorial Japanese restraint, real typographic hierarchy, and layouts that feel architected rather than dumped.

Desired design synthesis:

- Japanese editorial restraint.
- Strong typographic hierarchy.
- Business-school seriousness.
- Manifesto energy.
- Clean structure from the Human Question formatted pages.
- One coherent design direction, not three separate visual languages.
- Jakob Nielsen usability principles.

Design rules:

- Off-white / ivory background.
- Restrained palette.
- Strong typography.
- Minimal animation.
- No SaaS-confetti aesthetic.
- Fast render over flourish.
- Mobile-first.
- Clear navigation.
- Semantic HTML.
- Cards only where they add structure.
- CTAs should feel editorial, not salesy.
- Charts/media should be lazy-loaded or separated if heavy.

Potential palette inheritance:

- Ivory / cream background.
- Navy / slate for seriousness.
- Gold/amber accent.
- Black/dark gray body text.
- Muted gray secondary text.

The Human Question example currently uses:
- Libre Baskerville.
- DM Sans.
- Courier Prime.
- Navy, slate, gold, ivory.
- Verdict labels with green/navy/speculative/contested colors.

This design language can inform the broader site, but should be unified and simplified.

---

## 15. Performance and SEO Requirements

Performance is a top priority. Slow pages are punished by search engines and hurt reader engagement.

Requirements:

- Static-first rendering.
- Minimal JavaScript by default.
- No heavy animation.
- Lazy-load charts, images, and noncritical media.
- Optimize images.
- Avoid huge monolithic pages when content can be split.
- Use semantic HTML: one h1 per page, proper h2/h3 hierarchy, article/main/nav/footer landmarks.
- Real anchor links for outbound references.
- Descriptive meta titles and descriptions.
- Open Graph tags.
- Mobile rendering is required.
- Cross-browser support required for Chrome, Safari, and Edge.
- Nice-to-have support for Firefox, Opera, and Perplexity browser.

---

## 16. Analytics

Analytics should be included.

Options:

- Google Analytics.
- Plausible.
- Fathom.
- Umami.

Recommended tracked events:

- Page views.
- Read manifesto CTA.
- Read case study CTA.
- Explore Human Question CTA.
- Sign manifesto CTA.
- Download PDF.
- Outbound reference clicks.
- Scroll depth for manifesto and case pages.
- Human Question topic engagement.
- Signature submissions.

GitHub Pages does not provide a full analytics platform comparable to GA.

---

## 17. Technical Recommendation

Recommended stack:

- **Astro** static site.
- Hosted on GitHub Pages.
- Developed in VS Code using WSL/Ubuntu.
- CSS via global tokens and component-scoped styles.
- Markdown/MDX for essays and manifesto content.
- Structured content collections for Human Question pages.
- Supabase integration later for signatures.

Why Astro:

- Fast static output.
- Component model.
- Minimal JavaScript by default.
- Good for content-heavy sites.
- Better long-term maintainability than hand-written standalone HTML pages.
- Reusable components for Human Question topic pages.
- GitHub Pages deployment works well.

Alternative:

- Jekyll, if maximum GitHub Pages simplicity is desired.
- Plain HTML/CSS/JS, only if the site remains very small.
- Do not build the full site as a giant standalone HTML file.

---

## 18. Recommended Repository Structure

Suggested Astro project structure:

```text
nosmanifesto-site/
  public/
    assets/
      images/
      pdf/
      downloads/
  src/
    components/
      Header.astro
      Footer.astro
      PageHero.astro
      CTABox.astro
      ArticleLayout.astro
      ManifestoBody.astro
      HumanQuestionHero.astro
      HumanQuestionTopicNav.astro
      VerdictLegend.astro
      QuestionCard.astro
      VerdictBadge.astro
      SidebarBlock.astro
      SourceBlock.astro
      Callout.astro
      AcronymTooltip.astro
      SignForm.astro
      SignatoryRollcall.astro
    content/
      manifesto/
        nos-manifesto.md
      essays/
        million-dollar-keystroke.md
      human-question/
        ethics-society-human-impact.md
        economics-labor-industry.md
        education-human-development.md
    layouts/
      BaseLayout.astro
      ArticleLayout.astro
      ManifestoLayout.astro
      HumanQuestionLayout.astro
    pages/
      index.astro
      manifesto.astro
      case-study.astro
      human-question/
        index.astro
        [slug].astro
      essays/
        index.astro
        [slug].astro
      about.astro
      sign.astro
      signatories.astro
      references.astro
    styles/
      global.css
      tokens.css
  astro.config.mjs
  package.json
  README.md
```

---

## 19. Build Phases

Do not build everything at once.

### Phase 1 — Static Shell
- Astro setup.
- Global design tokens.
- Header/footer.
- Homepage.
- Manifesto page.
- About page.
- Basic Essays index placeholder.
- Basic Human Question index placeholder.
- GitHub Pages deploy.

### Phase 2 — Core Content
- Import final nOS Manifesto.
- Import business case page or PDF/download route.
- Add Case Study page.
- Add first Human Question topic page using the existing Ethics, Society & Human Impact example.

### Phase 3 — Human Question System
- Convert Q&A example into reusable components.
- Create topic landing page.
- Add remaining topic clusters.
- Implement local topic nav and evidence labels.

### Phase 4 — Signature System
- Create Supabase project.
- Add signature form.
- Add rollcall page.
- Add moderation workflow.
- Add spam protections.

### Phase 5 — Analytics and Refinement
- Add analytics.
- Track CTA events.
- Add SEO metadata.
- Add sitemap.
- Add RSS if desired.
- Cross-browser and mobile QA.
- Performance testing.

---

## 20. Initial Coding Agent Prompt

Use this as the first prompt in VS Code/Cline/Claude Code:

```text
We are building the official website for The nOS Manifesto at nosmanifesto.org.

Create a fast static Astro site deployable to GitHub Pages. The site has three major pillars:

1. The nOS thesis:
   - The nOS Manifesto
   - The companion business case, When the Tenant Becomes the Landlord
   - Signatures and rollcall

2. The Human Question:
   - A deep question-led public inquiry into what AI means for modern society
   - Not FAQ content
   - Topic pages contain long-form questions, evidence labels, sidebars, source blocks, and callouts

3. Author platform:
   - Essays, papers, possible videos, and About page

Design direction:
- Editorial Japanese restraint
- Strong typographic hierarchy
- Off-white background
- Navy/slate/gold accent system
- Serious, clean, fast, mobile-first
- No heavy animation
- Minimal JavaScript
- Semantic accessible HTML
- Shared layouts and reusable components

Initial routes:
- /
- /manifesto/
- /case-study/
- /human-question/
- /human-question/[slug]/
- /essays/
- /essays/[slug]/
- /about/
- /sign/
- /signatories/
- /references/

Create shared components:
- Header
- Footer
- PageHero
- CTABox
- ArticleLayout
- ManifestoLayout
- HumanQuestionLayout
- HumanQuestionHero
- VerdictLegend
- QuestionCard
- VerdictBadge
- SidebarBlock
- SourceBlock
- Callout
- SignForm placeholder
- SignatoryRollcall placeholder

Do not implement Supabase yet. Create placeholders and document where Supabase integration will go.

Performance requirements:
- Static-first
- Minimal JavaScript
- Lazy-load heavy media
- Mobile-first responsive layout
- SEO metadata per page
- Accessible semantic HTML
- GitHub Pages deployment instructions in README

Generate the Astro project structure, starter pages, CSS tokens, global styles, and README.
```

---

## 21. Immediate Questions for the New Project

These should be answered early:

1. Should the homepage lead with the manifesto or the broader AI public-intelligence platform?
2. Should the top nav use `nOS` or `Manifesto`?
3. Should The Human Question have its own visual identity within the shared site system?
4. Should the business case be a full HTML page, PDF download, or both?
5. Should references be centralized or kept per article?
6. Should signatures be public by default after approval, or should signers choose public/private?
7. Should email capture be included at launch?
8. Should analytics be Google Analytics or privacy-first analytics?
9. Should Human Question pages be Markdown/MDX or structured JSON/data files?
10. Should the initial site launch before all 75 questions are migrated?

---

## 22. Recommended First Launch Scope

Launch with:

- Homepage.
- Manifesto page.
- Case Study page or Case Study download page.
- Human Question landing page.
- One Human Question topic page: Ethics, Society & Human Impact.
- Essays landing page placeholder.
- About page.
- Sign page placeholder.
- Signatories placeholder.
- References placeholder.

Do not wait for all 75 questions to be migrated before publishing.

---

## 23. Working Principle

The website should feel like an architected public-intelligence platform, not a pile of documents.

The manifesto is the flag.
The case study is the evidence.
The Human Question is the inquiry engine.
The essays are the ongoing signal.
The signature rollcall is the movement layer.
