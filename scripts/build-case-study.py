#!/usr/bin/env python3
"""
Build case study HTML from markdown source.
Output: public/case-study/index.html
Source: source-material/case-study/when_tenant_becomes_landlord_paper.md
Assets: public/case-study/paper_assets/ (must be copied separately)
"""
import re, os, sys

MD_PATH = "/home/mocha/projects/nosmanifesto-site/source-material/case-study/when_tenant_becomes_landlord_paper.md"
OUT_PATH = "/home/mocha/projects/nosmanifesto-site/public/case-study/index.html"

# ── Inline markdown converter ──────────────────────────────────────────────

def inline(text):
    """Convert inline markdown to HTML."""
    text = text.replace(r'\$', '$').replace(r'\|', '|')
    # Bold+italic (***) before bold or italic alone
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # En/em dashes
    text = text.replace('---', '&mdash;').replace('--', '&ndash;')
    return text


def blocks_to_html(text):
    """Convert a markdown chunk to HTML. Returns HTML string."""
    text = text.strip()
    if not text:
        return ''

    # Split into block-level units separated by blank lines
    raw_blocks = re.split(r'\n{2,}', text)
    out = []

    i = 0
    while i < len(raw_blocks):
        blk = raw_blocks[i].strip()
        if not blk:
            i += 1
            continue

        # Raw HTML block — pass through
        if blk.startswith('<'):
            # Collect until closing tag if multiline split occurred
            out.append(blk)
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^-{3,}$', blk):
            out.append('<hr class="divider">')
            i += 1
            continue

        # Blockquote — accumulate consecutive > lines
        if blk.startswith('>'):
            lines = blk.split('\n')
            # Strip leading > and space
            content_lines = [re.sub(r'^>\s?', '', l) for l in lines]
            combined = ' '.join(l for l in content_lines if l.strip())
            # Extract strong title if first token is **...**
            title_m = re.match(r'\*\*(.+?)\*\*[.:]\s*(.*)', combined, re.DOTALL)
            if title_m:
                title = title_m.group(1)
                body = title_m.group(2).strip()
                out.append(
                    f'<div class="case-prompt">'
                    f'<div class="label">{inline(title)}</div>'
                    f'{("<p>" + inline(body) + "</p>") if body else ""}'
                    f'</div>'
                )
            else:
                out.append(f'<blockquote><p>{inline(combined)}</p></blockquote>')
            i += 1
            continue

        # Section headings
        m4 = re.match(r'^#### (.+)$', blk)
        m3 = re.match(r'^### (\d+\..+)$', blk)  # top-level sections 6/7/8 use ###
        m3sub = re.match(r'^### (.+)$', blk)
        m2 = re.match(r'^## (.+)$', blk)

        if m4:
            out.append(f'<h4 class="subsubsection-heading">{inline(m4.group(1))}</h4>')
        elif m2:
            title = m2.group(1)
            # Strip leading number for display? No, keep it.
            out.append(f'<h2 class="section-heading">{inline(title)}</h2>')
        elif m3 and re.match(r'^\d+\.', m3.group(1)):
            # Section-level heading masquerading as h3
            out.append(f'<h2 class="section-heading">{inline(m3.group(1))}</h2>')
        elif m3sub:
            out.append(f'<h3 class="subsection-heading">{inline(m3sub.group(1))}</h3>')
        else:
            # Ordered/unordered list
            if re.match(r'^\d+\.\s', blk) or blk.startswith('- ') or blk.startswith('* '):
                items = blk.split('\n')
                tag = 'ol' if re.match(r'^\d+\.', blk) else 'ul'
                li_html = ''.join(
                    f'<li>{inline(re.sub(r"^(\d+\.\s|-\s|\*\s)", "", it.strip()))}</li>'
                    for it in items if it.strip()
                )
                out.append(f'<{tag}>{li_html}</{tag}>')
            else:
                # Regular paragraph — join any soft-wrapped lines
                para = ' '.join(blk.split('\n'))
                out.append(f'<p>{inline(para)}</p>')

        i += 1

    return '\n'.join(out)


# ── HTML fragments ──────────────────────────────────────────────────────────

NAV_HTML = """<nav id="nos-snav" aria-label="Site navigation">
  <div id="nos-snav-inner">
    <a class="snav-wordmark" href="/">nOS</a>
    <a class="snav-link" href="/human-question/">The Human Question</a>
    <a class="snav-link snav-active" href="/case-study/">Case Study</a>
    <a class="snav-link" href="/essays/">Essays</a>
    <a class="snav-link" href="/about/">About</a>
    <a class="snav-sign" href="/sign/">Sign the Manifesto</a>
  </div>
</nav>"""

FOOTER_LEGEND = """  <div class="page-footer">
    <div class="footer-legend">
      <span class="footer-item"><span class="footer-mark aip"></span><span class="footer-letter">AIP</span> <span class="footer-name">Productivity</span></span>
      <span class="footer-item"><span class="footer-mark aio"></span><span class="footer-letter">AIO</span> <span class="footer-name">Orchestration</span></span>
      <span class="footer-item"><span class="footer-mark aia"></span><span class="footer-letter">AIA</span> <span class="footer-name">Agency</span></span>
    </div>
    <span class="footer-page">When the Tenant Becomes the Landlord &middot; {page}</span>
  </div>"""


def page_card(body_html, page_num, card_type='body'):
    """Wrap body HTML in a page card div."""
    if card_type == 'cover':
        cls = 'case-page first'
        inner = f'<div class="case-front">\n{body_html}\n</div>\n'
        inner += FOOTER_LEGEND.format(page=page_num)
    elif card_type == 'figure':
        cls = 'case-page figure-page'
        inner = f'<div class="page-body-area">\n{body_html}\n</div>\n'
        inner += FOOTER_LEGEND.format(page=page_num)
    elif card_type == 'single':
        cls = 'case-page'
        inner = f'<div class="page-body-area single-col">\n{body_html}\n</div>\n'
        inner += FOOTER_LEGEND.format(page=page_num)
    else:
        cls = 'case-page'
        inner = f'<div class="page-body-area">\n{body_html}\n</div>\n'
        inner += FOOTER_LEGEND.format(page=page_num)

    return f'<div class="{cls}">\n{inner}</div>\n'


# ── CSS ─────────────────────────────────────────────────────────────────────

CSS = """
:root{--serif:'EB Garamond',Georgia,serif;--sans:Calibri,'Segoe UI',Arial,sans-serif;--ink:#151515;--muted:#5f6368;--rule:#d9d5cb;--paper:#fafaf7;--teal:#2a6f7a;--charcoal:#2f3436;--ochre:#b88a44;--crimson:#c44d5c}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#e8e8e4;color:var(--ink)}
body{font-family:var(--serif);font-size:11pt;line-height:1.45}

/* ── Site nav ── */
#nos-snav{background:#0d1b2a;border-bottom:2px solid #c9922a;position:relative;z-index:300;padding:0 40px;}
#nos-snav-inner{width:min(88vw,1500px);margin:0 auto;display:flex;align-items:center;gap:0;overflow-x:auto;scrollbar-width:none;}
#nos-snav-inner::-webkit-scrollbar{display:none;}
.snav-wordmark{font-family:'Libre Baskerville',Georgia,serif;font-size:16px;font-weight:700;color:#c9922a;text-decoration:none;border-bottom:none;padding:9px 18px 9px 0;border-right:1px solid rgba(201,146,42,.3);margin-right:10px;white-space:nowrap;flex-shrink:0;}
.snav-link{font-family:'DM Sans',system-ui,sans-serif;font-size:20px;font-weight:400;color:rgba(245,240,232,.7);text-decoration:none;border-bottom:2px solid transparent;padding:9px 12px;white-space:nowrap;margin-bottom:-2px;transition:color .2s,border-color .2s;flex-shrink:0;}
.snav-link:hover{color:#f5f0e8;border-bottom-color:#e8a93c;}
.snav-link.snav-active{color:#c9922a!important;border-bottom-color:#c9922a;}
.snav-sign{font-family:'DM Sans',system-ui,sans-serif;font-size:20px;font-weight:400;color:rgba(245,240,232,.7);text-decoration:none;padding:9px 12px;white-space:nowrap;margin-left:auto;border-bottom:2px solid transparent;margin-bottom:-2px;transition:color .2s;flex-shrink:0;}
.snav-sign:hover{color:#f5f0e8;}

/* ── Page cards ── */
.case-shell{max-width:9in;margin:0 auto;padding:18px 0 42px}
.case-page{width:8.5in;height:11in;margin:0 auto 24px;background:#fff;box-shadow:0 8px 24px rgba(0,0,0,.15);padding:.55in .62in;overflow:hidden;position:relative}
.case-page.first{padding-top:.44in}
.case-page.figure-page{height:auto;min-height:8in;overflow:visible}
.case-page.figure-page .page-body-area{column-count:1;height:auto;overflow:visible}

/* ── Cover ── */
.case-front .eyebrow{font-family:var(--sans);text-transform:uppercase;letter-spacing:.18em;font-weight:700;font-size:9pt;color:#6a6a66;margin-bottom:18pt}
h1{font-size:22pt;line-height:1.1;font-weight:500;margin:0 0 8pt}
.subtitle{font-style:italic;font-size:15pt;color:#3f3f3c;margin-bottom:8pt}
.seminar,.author,.companion{font-size:11pt;margin:0 0 6pt}
.companion{font-style:italic}
.divider{border:0;border-top:1.25pt solid var(--ink);margin:18pt 0}
.abstract-block{font-weight:600;letter-spacing:.02em;line-height:1.55;margin:0 0 18pt}
.abstract-label{font-family:var(--sans);font-weight:700;letter-spacing:.06em}

/* ── Body ── */
.page-body-area{height:calc(11in - 1.1in);column-count:2;column-gap:.34in;column-fill:auto;overflow:hidden}
.page-body-area.single-col{column-count:1}
.case-page.first .page-body-area{height:calc(11in - 5.1in)}
p,li{font-size:10.2pt;line-height:1.46;margin:0 0 8pt;text-align:justify;hyphens:auto}
a{color:#7b561d;text-decoration:none;border-bottom:1px solid rgba(184,138,68,.45)}
h2.section-heading{font-family:var(--sans);font-size:13.6pt;line-height:1.18;text-transform:uppercase;letter-spacing:.08em;margin:0 0 9pt;break-after:avoid;column-span:all}
h3.subsection-heading{font-family:var(--sans);font-size:11.6pt;line-height:1.24;margin:13pt 0 6pt;break-after:avoid}
h4.subsubsection-heading{font-family:var(--sans);font-size:10.2pt;margin:10pt 0 5pt;break-after:avoid}
hr.divider{border:0;border-top:1pt solid var(--ink);margin:14pt 0}

/* ── Callout blocks ── */
.case-prompt,.evidence-key,.committee-checkpoint,.teaching-use-note{border-left:3px solid var(--ochre);background:#f6f1e7;padding:9pt 11pt;margin:9pt 0 12pt;break-inside:avoid;column-span:all}
.label{font-family:var(--sans);text-transform:uppercase;letter-spacing:.08em;font-size:7.7pt;font-weight:700;color:#7b561d;margin-bottom:4pt}
blockquote{border-left:3px solid var(--ochre);background:#f6f1e7;padding:9pt 11pt;margin:9pt 0 12pt;column-span:all}
blockquote p{margin:0}

/* ── Figures ── */
.exhibit-figure{column-span:all;width:100%;break-inside:avoid;margin:10pt 0 13pt}
.exhibit-figure img{width:100%;height:auto;display:block;border:1px solid var(--rule);background:#fff}
figcaption,.fig-caption{font-family:var(--sans);font-size:8.3pt;line-height:1.35;color:#4b4b49;margin:5pt 0 0}
figure{column-span:all;margin:10pt 0 13pt;break-inside:avoid}
figure img{width:100%;height:auto;display:block;border:1px solid var(--rule)}

/* ── Discussion questions ── */
.question-block{border-left:3px solid var(--teal);padding-left:12pt;margin-bottom:13pt;break-inside:avoid}
.question-number{font-family:var(--sans);font-weight:700;margin-right:6pt}
.cluster-b,.cluster-c{margin-top:4pt}
.proposal{border:1px dashed #aaa;padding:10pt 12pt;margin:10pt 0;background:#fafaf7}
.proposal-tag{font-family:var(--sans);font-size:7.7pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#888;margin-bottom:6pt}

/* ── References ── */
.intro p{margin-bottom:8pt}
.category-number{font-family:var(--sans);font-weight:700;margin-right:4pt}

/* ── Page footer ── */
.page-footer{position:absolute;left:.62in;right:.62in;bottom:.25in;border-top:.5pt solid var(--rule);padding-top:5pt;display:flex;justify-content:space-between;gap:10pt;font-family:var(--sans);font-size:7.2pt;color:#777}
.footer-legend{display:flex;gap:12pt}
.footer-item{display:flex;align-items:center;gap:4pt}
.footer-mark{display:inline-block;width:5pt;height:5pt;border-radius:50%}
.footer-mark.aip{background:var(--teal)}
.footer-mark.aio{background:var(--charcoal)}
.footer-mark.aia{background:var(--ochre)}
.footer-letter{font-weight:700;color:var(--ink);letter-spacing:.04em}
.footer-name{font-style:italic;color:var(--muted)}
.footer-page{letter-spacing:.06em;flex-shrink:0}

/* ── Config legend (Section 1) ── */
.legend{background:#f6f4ee;margin:16pt 0 8pt;padding:14pt 18pt 12pt;border-top:.6pt solid var(--ink);border-bottom:.6pt solid var(--ink);column-span:all;break-inside:avoid}
.legend-eyebrow{font-family:var(--sans);font-size:9.5pt;font-weight:700;letter-spacing:.18em;text-transform:uppercase;margin:0 0 10pt;padding-bottom:6pt;border-bottom:.4pt solid var(--rule)}
.legend-row{display:grid;grid-template-columns:12pt 28pt 1fr;gap:8pt;align-items:baseline;margin:0 0 8pt;font-family:var(--sans);font-size:10pt}
.legend-mark{width:7pt;height:7pt;border-radius:50%;align-self:center}
.legend-letter{font-weight:700}
.legend-name{font-weight:700;letter-spacing:.02em}
.legend-note{margin-top:10pt;padding-top:8pt;border-top:.4pt solid var(--rule);font-family:var(--sans);font-style:italic;font-size:9pt;line-height:1.4;color:var(--muted)}

/* ── Firework iframe ── */
.firework-wrap{width:100%;margin:10pt 0}
.firework-wrap iframe{width:100%;height:660px;border:none;display:block}

/* ── Responsive ── */
@media screen and (max-width:900px){
  .case-shell{padding:0}
  .case-page,.case-page.first,.case-page.figure-page{width:100%;height:auto;min-height:0;overflow:visible;margin:0 0 18px;padding:24px 18px 48px;box-shadow:none}
  .page-body-area,.case-page.first .page-body-area{height:auto;column-count:1;overflow:visible}
  .page-footer{position:static;margin-top:20px}
  h2.section-heading{column-span:unset}
  figure,figcaption,.legend{column-span:unset}
}

/* ── Print ── */
@media print{
  @page{size:Letter;margin:0}
  html,body{background:#fff}
  #nos-snav{display:none!important}
  .case-shell{max-width:none;padding:0}
  .case-page{box-shadow:none;margin:0;break-after:page;overflow:hidden;height:11in}
  .case-page.figure-page{height:auto;break-after:page}
  .case-page:last-child{break-after:auto}
  a{color:inherit;border-bottom:none}
}
"""

NAV_CSS = """
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@700&family=DM+Sans:opsz,wght@9..40,400&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap">
"""

# ── Content section extraction ───────────────────────────────────────────────

def read_md():
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        return f.read()


def split_at(md, marker):
    """Split markdown at a regex marker. Returns (before, after)."""
    m = re.search(marker, md, re.MULTILINE)
    if not m:
        return md, ''
    return md[:m.start()], md[m.start():]


def section(md, start_re, end_re=None):
    """Extract section between start and end regex."""
    m = re.search(start_re, md, re.MULTILINE)
    if not m:
        return ''
    start = m.start()
    if end_re:
        m2 = re.search(end_re, md[start+1:], re.MULTILINE)
        if m2:
            return md[start:start+1+m2.start()]
    return md[start:]


# ── Exhibit fragments ────────────────────────────────────────────────────────

EXHIBIT_CONFIG_LADDER = """<figure class="exhibit-figure">
<img src="/case-study/paper_assets/configuration-ladder.png" alt="Exhibit 1. The Configuration Ladder." />
<figcaption>Exhibit 1. The Configuration Ladder. AIP, AIO, and AIA form the core analytical terrain of the case: AI inside the application, AI orchestrating across applications, and AI pursuing goals across surfaces.</figcaption>
</figure>"""

EXHIBIT_VENDOR_MATRIX = """<figure class="exhibit-figure">
<img src="/case-study/paper_assets/vendor-positioning-matrix.png" alt="Exhibit 3. Vendor Positioning Matrix." />
<figcaption>Exhibit 3. Vendor Positioning Matrix. Conceptual placement for discussion; not a market-share ranking.</figcaption>
</figure>"""

EXHIBIT_COST_TO_VALUE = """<figure class="exhibit-figure">
<img src="/case-study/paper_assets/cost-to-value-migration.png" alt="Exhibit 4. Cost-to-Value Migration." />
<figcaption>Exhibit 4. Cost-to-Value Migration. The marginal cost of intelligence falls while dependency-adjusted price rises as the AI layer captures workflow position. Curves are conceptual and directional, not audited price history.</figcaption>
</figure>"""

EXHIBIT_TRIFURCATION = """<figure class="exhibit-figure">
<img src="/case-study/paper_assets/microsoft-trifurcation.png" alt="Exhibit 5. Microsoft Trifurcation." />
<figcaption>Exhibit 5. Microsoft Trifurcation. Microsoft&rsquo;s AI posture differs by portfolio slice: defensive in Office productivity, competitive in developer tooling, and dominant in enterprise AI infrastructure.</figcaption>
</figure>"""

EXHIBIT_FIREWORK = """<div class="firework-wrap">
<iframe src="/case-study/paper_assets/firework-interactive.html" title="Exhibit 2. The Firework Chart — interactive vendor map" allowfullscreen loading="lazy"></iframe>
</div>"""

CONFIG_LEGEND = """<div class="legend">
<div class="legend-eyebrow">Configuration legend</div>
<div class="legend-row"><span class="legend-mark" style="background:#2a6f7a"></span><span class="legend-letter">AIP</span><span><span class="legend-name">AI Productivity.</span> AI lives inside a host application&rsquo;s bounded domain, performing assignment-based work the application was designed to support.</span></div>
<div class="legend-row"><span class="legend-mark" style="background:#2f3436"></span><span class="legend-letter">AIO</span><span><span class="legend-name">AI Orchestration.</span> AI becomes the primary surface, maintaining coherent state across applications that were never designed to share state directly.</span></div>
<div class="legend-row"><span class="legend-mark" style="background:#b88a44"></span><span class="legend-letter">AIA</span><span><span class="legend-name">AI Agency.</span> AI operates with proactive agency, initiating work and executing goals across surfaces without requiring task-level user direction.</span></div>
<div class="legend-note">The case uses the acronyms at section openings and transitions and the descriptive names in body prose where flow benefits. A compressed legend appears in the running footer of every page.</div>
</div>"""


# ── Main build ───────────────────────────────────────────────────────────────

def build():
    md = read_md()

    # Helper: convert a markdown range to HTML
    def h(text):
        return blocks_to_html(text)

    # Extract key sections by splitting at heading markers
    def get(start_pat, end_pat):
        m1 = re.search(start_pat, md, re.MULTILINE)
        if not m1:
            return ''
        m2 = re.search(end_pat, md[m1.end():], re.MULTILINE)
        body = md[m1.end(): m1.end() + m2.start()] if m2 else md[m1.end():]
        return body.strip()

    # ── Cover and Abstract ──────────────────────────────────────────────────
    # Title page: title + abstract only. Callout blocks move to card 2 (column-span:all).
    cover_html = """
<h1 id="case-title">When the Tenant Becomes the Landlord</h1>
<div class="subtitle">Value-Chain Inversion in the Post-2026 Productivity Stack</div>
<div class="seminar">A Discussion Case for Graduate Strategy Seminars</div>
<div class="author">Jason Troxel &nbsp;|&nbsp; Drafted April 2026; revised May 2026</div>
<div class="companion">Companion to <em>The nOS Manifesto</em></div>
<hr class="divider">
<div class="abstract-block">
<p><span class="abstract-label">ABSTRACT.</span>&nbsp; Between October 2025 and April 2026, the leading frontier-model vendors and the hyperscaler platforms distributing them advanced positions that diverge across the architectural stack rather than competing for the same layer of it, in what may be the most consequential platform migration in computing since the decoupling of software from hardware that enabled cloud-native computing. Anthropic completed a six-month traversal of Microsoft Office through native Claude integrations and crossed $30 billion in annualized revenue run rate by April 2026, passing OpenAI for the first time. Google launched Workspace Intelligence, a cross-application semantic layer consolidating Gmail, Drive, Docs, Sheets, Slides, Chat, and Calendar under a Gemini-powered orchestration surface. OpenAI shipped Atlas (an AI-native browser) and Frontier (an enterprise semantic layer), announced a desktop superapp consolidating ChatGPT, Codex, and Atlas under a single platform, and reached $24 billion annualized revenue. Perplexity scaled Comet (an AI-native browser) and Computer (an autonomous agent platform) past 100 million monthly active users at a $20 billion valuation, expanding Personal Computer to all Mac users in May 2026. Meta acquired Manus (the autonomous AI agent built by Butterfly Effect) for approximately $2 billion in December 2025 and committed $115 to $135 billion in 2026 AI infrastructure. Amazon committed roughly $200 billion in 2026 AI infrastructure and up to $25 billion in cumulative Anthropic investment, positioning AWS Bedrock as the primary cloud-distribution channel for the frontier-model layer.</p>
<p>The velocity is not incidental. Frontier-model vendors compete simultaneously on capability advancement (DeepSeek V4&rsquo;s compressed sparse attention mechanisms continue to lower frontier-inference costs) and monetized engagement growth (daily active paying users and time-in-app per paid user have converged as operative measures of platform position ahead of public-market events). Read individually, the moves can be justified on conventional terms (market share capture, productivity feature improvement, distribution expansion). Read together, they make more analytical sense as positioning across three observable architectural states for the productivity and operating-system stack, here designated AIP (AI Productivity), AIO (AI Orchestration), and AIA (AI Agency), and as evidence that the migration toward a destination beyond those three states is already underway.</p>
<p>This case examines the empirical record from October 2025 through April 2026, places it in the context of prior platform migrations, and asks students to reason about which configuration captures the value, on what timeline, and which vendor is positioned to win. The case is the analytical companion to the author&rsquo;s nOS Manifesto, which signals the direction in which computing will transition over the next two decades: extending the trajectory that personal computing began, that connected computing scaled, and that cloud computing distilled into the present configuration. The case stress-tests that signaled trajectory against the empirical record.</p>
</div>
"""

    # Callout blocks — rendered column-span:all at top of card 2
    callout_html = """<div class="case-prompt">
<div class="label">Case decision frame</div>
<p>You are advising an enterprise strategy committee in April 2026. The organization must decide whether to consolidate around its incumbent productivity suite, preserve optionality across orchestration vendors, or begin piloting agency-layer systems before the market stabilizes. The decision is not which chatbot to buy. The decision is which configuration of work the institution is willing to depend on.</p>
</div>
<div class="case-prompt">
<div class="label">Evidence discipline used in this case</div>
<p><strong>Observed record</strong> means shipped products, disclosed metrics, and dated market events. <strong>Analytical thesis</strong> means the paper&rsquo;s interpretation of what the record means. <strong>Forward forecast</strong> means directional claims about where the configuration migration may go.</p>
</div>
"""

    # ── Section 1 ───────────────────────────────────────────────────────────
    s1 = get(r'^## 1\.', r'^## 2\.')

    # ── Section 2 ───────────────────────────────────────────────────────────
    s2_raw = get(r'^## 2\.', r'^## 3\.')
    # Split s2: intro + 2.1-2.4 text (figure tag already in md, remove it — we add manually)
    s2_no_fig = re.sub(r'<figure>.*?</figure>', '', s2_raw, flags=re.DOTALL)

    # ── Section 3 ───────────────────────────────────────────────────────────
    s3_raw = get(r'^## 3\.', r'^## 4\.')
    # Remove figure tags (we insert manually at correct positions)
    s3_no_figs = re.sub(r'<figure>.*?</figure>', '', s3_raw, flags=re.DOTALL)
    # Remove the blockquote firework reference
    s3_no_figs = re.sub(r'> \*\*Exhibit 2.*?(?=\n\n)', '', s3_no_figs, flags=re.DOTALL)

    # Split section 3 at subsection boundaries
    s31 = get(r'^### 3\.1\. AIP', r'^### 3\.2\. AIO')
    s32 = get(r'^### 3\.2\. AIO', r'^### 3\.3\. AIA')
    s33 = get(r'^### 3\.3\. AIA', r'^## 4\.')
    # Remove figures from subsections
    s31 = re.sub(r'<figure>.*?</figure>', '', s31, flags=re.DOTALL)
    s32 = re.sub(r'<figure>.*?</figure>', '', s32, flags=re.DOTALL)
    s33 = re.sub(r'<figure>.*?</figure>', '', s33, flags=re.DOTALL)
    # Remove firework callout
    s33 = re.sub(r'> \*\*Exhibit 2.*?(?=\n\n)', '', s33, flags=re.DOTALL)
    # Extract committee checkpoint from end of s33
    s33_cp = re.search(r'> \*\*Committee checkpoint.*', s33, re.DOTALL)
    s33_body = s33[:s33_cp.start()].strip() if s33_cp else s33

    # Split s31 at subsubsection level for pagination
    s31_intro = get(r'^### 3\.1\.', r'^#### The canonical case')
    s31_copilot = get(r'^#### The canonical case: Microsoft', r'^#### The second leg')
    s31_google = get(r'^#### The second leg', r'^#### The entry-point')
    s31_rest = get(r'^#### The entry-point', r'^### 3\.2\.')

    # Split s32
    s32_intro = get(r'^### 3\.2\. AIO', r'^#### The two-front')
    s32_twofront = get(r'^#### The two-front advance', r'^#### The developer-tooling slice is further')
    s32_devtools = get(r'^#### The developer-tooling slice is further', r'^#### OpenAI')
    s32_openai = get(r'^#### OpenAI.s parallel AIO', r'^#### The consumer-scale')
    s32_perp = get(r'^#### The consumer-scale AIO', r'^#### Microsoft.s structural')
    s32_msft = get(r'^#### Microsoft.s structural', r'^### 3\.3\.')

    # Split s33
    s33_narrow = get(r'^#### Narrow-domain', r'^#### The closest production')
    s33_perp = get(r'^#### The closest production', r'^#### The directional AIA')
    s33_openai = get(r'^#### The directional AIA', r'^#### The protocol-level')
    s33_anthropic = get(r'^#### The protocol-level AIA', r'^#### The acquired')
    s33_manus = get(r'^#### The acquired-AIA', r'^#### The hardware')
    s33_jony = get(r'^#### The hardware-directional', r'^#### The category-defining')
    s33_oss = get(r'^#### The category-defining', r'^#### What AIA looks like')
    s33_summary = get(r'^#### What AIA looks like in production', r'^> \*\*Committee checkpoint')
    s33_summary = re.sub(r'<figure>.*?</figure>', '', s33_summary, flags=re.DOTALL)

    # ── Section 4 ───────────────────────────────────────────────────────────
    s4 = get(r'^## 4\.', r'^## 5\.')

    # ── Section 5 ───────────────────────────────────────────────────────────
    s5 = get(r'^## 5\.', r'^### 6\.')  # 6 starts with ###

    # ── Section 6 ───────────────────────────────────────────────────────────
    s6_raw = get(r'^### 6\.', r'^### 7\.')
    s6_no_figs = re.sub(r'<figure>.*?</figure>', '', s6_raw, flags=re.DOTALL)
    s61 = get(r'^#### 6\.1\.', r'^#### 6\.2\.')
    s62 = get(r'^#### 6\.2\.', r'^#### 6\.3\.')
    s63 = get(r'^#### 6\.3\.', r'^#### 6\.4\.')
    s64 = get(r'^#### 6\.4\.', r'^#### 6\.5\.')
    s64 = re.sub(r'<figure>.*?</figure>', '', s64, flags=re.DOTALL)
    s61 = re.sub(r'<figure>.*?</figure>', '', s61, flags=re.DOTALL)
    s65 = get(r'^#### 6\.5\.', r'^### 7\.')
    s6_cp = get(r'^> \*\*Committee checkpoint: after the economics', r'^### 7\.')

    # ── Section 7 ───────────────────────────────────────────────────────────
    s7_raw = get(r'^### 7\.', r'^### 8\.')
    # Handle proposal block
    s71 = get(r'^#### 7\.1\.', r'^#### 7\.2\.')
    s72 = get(r'^#### 7\.2\.', r'^#### 7\.3\.')
    s73 = get(r'^#### 7\.3\.', r'^#### 7\.4\.')
    s74 = get(r'^#### 7\.4\.', r'^#### 7\.5\.')
    s75_raw = get(r'^#### 7\.5\.', r'^### 8\.')

    # ── Section 8 ───────────────────────────────────────────────────────────
    s8 = get(r'^### 8\.', r'^## 9\.')

    # ── Section 9 (Discussion Questions) ───────────────────────────────────
    s9 = get(r'^## 9\.', r'^## 10\.')

    # ── Section 10 (References) ─────────────────────────────────────────────
    s10 = md[md.find('## 10. References'):]

    # ── Assemble page cards ──────────────────────────────────────────────────
    cards = []
    p = 1

    # Card 1: Cover
    cards.append(page_card(cover_html, p, 'cover'))
    p += 1

    # Card 2: callouts + S1 + S2 intro paragraphs only (all of 2.1 moves to Card 3)
    s2_21 = get(r'^## 2\.', r'^### 2\.2\. AIO')
    s2_21_no_fig = re.sub(r'<figure>.*?</figure>', '', s2_21, flags=re.DOTALL)
    # Split before "### 2.1." so card 2 holds only the S2 intro text
    s21_split_marker = '### 2.1. AIP: AI Productivity'
    if s21_split_marker in s2_21_no_fig:
        split_idx = s2_21_no_fig.index(s21_split_marker)
        s2_intro_only = s2_21_no_fig[:split_idx].rstrip()
        s2_21_full = s2_21_no_fig[split_idx:]  # heading + all 4 paragraphs
    else:
        s2_intro_only = s2_21_no_fig
        s2_21_full = ''
    cards.append(page_card(
        callout_html + h(f'## 1. The Question the Case Examines\n\n{s1}\n\n## 2. The Three Configurations\n\n{s2_intro_only}'),
        p
    ))
    p += 1

    # Card 3: all of 2.1 AIP (heading + 4 paragraphs) + S2.2 AIO + S2.3 AIA + S2.4 (text only)
    s2_rest = get(r'^### 2\.2\. AIO', r'^## 3\.')
    s2_rest_no_fig = re.sub(r'<figure>.*?</figure>', '', s2_rest, flags=re.DOTALL)
    cards.append(page_card(
        h(f'{s2_21_full}\n\n### 2.2. AIO: AI Orchestration\n\n{s2_rest_no_fig}'),
        p
    ))
    p += 1

    # Card 4 (figure): Configuration legend + config ladder figure
    cards.append(page_card(CONFIG_LEGEND + '\n' + EXHIBIT_CONFIG_LADDER, p, 'figure'))
    p += 1

    # Card 5: Section 3 heading + 3.1 intro + Copilot
    s3_intro = get(r'^## 3\.', r'^### 3\.1\.')
    s3_intro_clean = re.sub(r'> \*\*Exhibit 2.*?(?=\n\n)', '', s3_intro, flags=re.DOTALL)
    cards.append(page_card(
        h(f'## 3. The Empirical Record, October 2025 to April 2026\n\n{s3_intro_clean}\n\n### 3.1. AIP in Production\n\n{s31_intro}\n\n#### The canonical case: Microsoft 365 Copilot\n\n{s31_copilot}'),
        p
    ))
    p += 1

    # Card 6: 3.1 Google + entry-point + devtools + summary + 3.2 intro + two-front advance
    cards.append(page_card(
        h(f'#### The second leg: Google Workspace AI features\n\n{s31_google}\n\n#### The entry-point case: Anthropic\'s original Office add-ins\n\n{s31_rest}\n\n### 3.2. AIO in Production\n\n{s32_intro}\n\n#### The two-front advance: Anthropic and Google, six weeks apart\n\n{s32_twofront}'),
        p
    ))
    p += 1

    # Card 7: 3.2 developer tooling + OpenAI AIO + Perplexity + Microsoft AIO + summary
    cards.append(page_card(
        h(f'#### The developer-tooling slice is further along than the office-productivity slice\n\n{s32_devtools}\n\n#### OpenAI\'s parallel AIO push: Atlas and Frontier\n\n{s32_openai}\n\n#### The consumer-scale AIO case: Perplexity\n\n{s32_perp}\n\n#### Microsoft\'s structural position in AIO\n\n{s32_msft}'),
        p
    ))
    p += 1

    # Card 8: 3.3 intro + narrow-domain + Perplexity Computer + OpenAI AIA + Anthropic MCP
    s33_intro = get(r'^### 3\.3\. AIA', r'^#### Narrow-domain')
    cards.append(page_card(
        h(f'### 3.3. AIA in Production\n\n{s33_intro}\n\n#### Narrow-domain proactive agency at consumer scale\n\n{s33_narrow}\n\n#### The closest production-mature general-purpose AIA case: Perplexity Computer with Personal Computer\n\n{s33_perp}\n\n#### The directional AIA case: OpenAI\'s superapp consolidation\n\n{s33_openai}\n\n#### The protocol-level AIA case: Anthropic and MCP\n\n{s33_anthropic}'),
        p
    ))
    p += 1

    # Card 9: Manus + Jony Ive + open-source + AIA summary (no vendor matrix or checkpoint)
    cards.append(page_card(
        h(f'#### The acquired-AIA case: Meta\'s Manus\n\n{s33_manus}\n\n#### The hardware-directional AIA case: the Jony Ive partnership\n\n{s33_jony}\n\n#### The category-defining open-source case: OpenClaw, Hermes, and OpenJarvis\n\n{s33_oss}\n\n#### What AIA looks like in production\n\n{s33_summary}'),
        p
    ))
    p += 1

    # Card 10 (figure): Vendor positioning matrix + empirical record committee checkpoint
    cp_html = h('> **Committee checkpoint: after the empirical record**\n\n> At this point the strategy committee has enough evidence to reject a single-product-category reading. The practical question becomes whether the enterprise should privilege the incumbent productivity suite, preserve optionality through external orchestration, or begin testing goal-directed agents before the procurement vocabulary catches up.')
    cards.append(page_card(EXHIBIT_VENDOR_MATRIX + '\n' + cp_html, p, 'figure'))
    p += 1

    # Card 11 (figure): Firework chart
    firework_html = f"""<h2 class="section-heading">Exhibit 2. The Firework Chart</h2>
<p>Interactive vendor map: AI vendors positioned across the three capability tiers. Select a vendor tab or click a vendor banner to open its detail view. Burst radius encodes relative position; tier color encodes configuration category.</p>
{EXHIBIT_FIREWORK}"""
    cards.append(page_card(firework_html, p, 'figure'))
    p += 1

    # Card 12: Section 4 complete
    cards.append(page_card(h(f'## 4. Change and Consequences: Two Strategic Frames\n\n{s4}'), p))
    p += 1

    # Card 13: Section 5 — 5.1 through 5.3 only (5.4 moves to Card 14)
    s5_54_split = re.search(r'\n### 5\.4\.', s5)
    if s5_54_split:
        s5_part1 = s5[:s5_54_split.start()].strip()
        s5_part2 = s5[s5_54_split.start():].strip()
    else:
        s5_part1 = s5
        s5_part2 = ''
    cards.append(page_card(h(f'## 5. The Demand-Side Force: Citizen Developers and the Knowledge-Management Problem\n\n{s5_part1}'), p))
    p += 1

    # Card 14: Section 5.4 + Section 6 intro + 6.1 (text only)
    s6_intro = get(r'^### 6\. The Economics', r'^#### 6\.1\.')
    cards.append(page_card(
        h(f'{s5_part2}\n\n### 6. The Economics of Each Configuration\n\n{s6_intro}\n\n#### 6.1. Unit cost falls, dependency cost rises\n\n{s61}'),
        p
    ))
    p += 1

    # Card 15 (figure): Cost-to-value figure + 6.2 + 6.3 + 6.4
    cards.append(page_card(
        EXHIBIT_COST_TO_VALUE + '\n' +
        h(f'#### 6.2. The infrastructure bill\n\n{s62}\n\n#### 6.3. AI priced against value, not compute cost\n\n{s63}\n\n#### 6.4. The cross-vendor consequences\n\n{s64}'),
        p, 'figure'
    ))
    p += 1

    # Card 16 (figure): Trifurcation figure + 6.5 + economics committee checkpoint
    s6cp_text = '> **Committee checkpoint: after the economics**\n\n> The pricing question is no longer the marginal cost of intelligence. It is whether the enterprise can adopt the AI layer without allowing dependency-adjusted price, workflow lock-in, and infrastructure-tethered commitments to outrun measurable value.'
    cards.append(page_card(
        EXHIBIT_TRIFURCATION + '\n' +
        h(f'#### 6.5. What the cost-to-value migration establishes\n\n{s65}\n\n{s6cp_text}'),
        p, 'figure'
    ))
    p += 1

    # Card 17: Section 7 intro + 7.1 + 7.2
    s7_intro = get(r'^### 7\. Implications', r'^#### 7\.1\.')
    cards.append(page_card(
        h(f'### 7. Implications for Decision Makers\n\n{s7_intro}\n\n#### 7.1. Will all incumbents please rise\n\n{s71}\n\n#### 7.2. Second stars to the right\n\n{s72}'),
        p
    ))
    p += 1

    # Card 18: 7.3 + 7.4 + 7.5
    cards.append(page_card(
        h(f'#### 7.3. Enterprise flex\n\n{s73}\n\n#### 7.4. For the workforce and the educators training it\n\n{s74}\n\n#### 7.5. For regulators and antitrust authorities\n\n{s75_raw}'),
        p
    ))
    p += 1

    # Card 19: Section 8 Conclusion
    cards.append(page_card(h(f'### 8. Conclusion\n\n{s8}'), p))
    p += 1

    # Card 20: Section 9 Discussion Questions (single column)
    cards.append(page_card(h(f'## 9. Discussion Questions\n\n{s9}'), p, 'single'))
    p += 1

    # Card 21: Section 10 References (single column)
    cards.append(page_card(h(s10), p, 'single'))

    # ── Final HTML assembly ──────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>When the Tenant Becomes the Landlord</title>
<meta name="description" content="A graduate strategy case on value-chain inversion in the post-2026 productivity stack.">
{NAV_CSS}
<style>
{CSS}
</style>
</head>
<body>
{NAV_HTML}
<div class="case-shell">
{''.join(cards)}
</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Built: {OUT_PATH}")
    print(f"Cards: {len(cards)}")
    print(f"File size: {len(html):,} bytes")


if __name__ == '__main__':
    build()
