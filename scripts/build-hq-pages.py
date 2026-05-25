#!/usr/bin/env python3
"""
Build Human Question public pages from source HTML files.
Applies: three-layer nav, width overrides, header cleanup, link fixes,
bottom nav, legacy footer link removal, and scroll-tracking JS.
Source files are never modified — output goes to public/human-question/[slug]/index.html.
"""
import re, os

SOURCE_DIR = "/home/mocha/projects/nosmanifesto-site/source-material/human-question"
PUBLIC_DIR = "/home/mocha/projects/nosmanifesto-site/public/human-question"

INJECTED_CSS = """/* === INJECTED: Global nav (Layer 1) === */
#nos-snav{background:var(--navy);border-bottom:2px solid var(--gold);position:sticky;top:0;z-index:300;padding:0 40px;}
#nos-snav-inner{margin:0 auto;display:flex;align-items:center;gap:0;overflow-x:auto;scrollbar-width:none;}
#nos-snav-inner::-webkit-scrollbar{display:none;}
.snav-wordmark{font-family:'Libre Baskerville',serif;font-size:16px;font-weight:700;color:var(--gold);text-decoration:none;padding:9px 18px 9px 0;border-right:1px solid rgba(201,146,42,.3);margin-right:10px;white-space:nowrap;flex-shrink:0;}
.snav-link{font-family:'DM Sans',system-ui,sans-serif;font-size:20px;font-weight:400;color:rgba(245,240,232,.7);text-decoration:none;padding:9px 12px;white-space:nowrap;border-bottom:2px solid transparent;margin-bottom:-2px;transition:color .2s,border-color .2s;flex-shrink:0;}
.snav-link:hover{color:var(--ivory);border-bottom-color:var(--amber);}
.snav-link.snav-active{color:var(--gold) !important;border-bottom-color:var(--gold);}
.snav-sign{font-family:'DM Sans',system-ui,sans-serif;font-size:20px;font-weight:400;color:rgba(245,240,232,.7);text-decoration:none;padding:9px 12px;white-space:nowrap;border-bottom:2px solid transparent;margin-bottom:-2px;transition:color .2s;flex-shrink:0;margin-left:auto;}
.snav-sign:hover{color:var(--ivory);}
/* === INJECTED: Topic nav (Layer 2) === */
#nos-topicnav{background:var(--slate);border-bottom:1px solid rgba(201,146,42,.35);position:sticky;top:40px;z-index:200;padding:0 40px;height:33px;overflow:hidden;}
#nos-topicnav-inner{margin:0 auto;display:flex;align-items:center;gap:0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;}
#nos-topicnav-inner::-webkit-scrollbar{display:none;}
.tnav-link{font-family:'DM Sans',system-ui,sans-serif;font-size:18px;font-weight:400;letter-spacing:.03em;text-transform:uppercase;color:rgba(245,240,232,.45);text-decoration:none;padding:7px 10px;white-space:nowrap;transition:color .2s;flex-shrink:0;}
.tnav-link:hover{color:rgba(245,240,232,.8);}
.tnav-link.tnav-active{color:var(--gold) !important;}
/* === INJECTED: Layer 3 — hide brand label, active question === */
.page-nav{top:73px !important;z-index:100 !important;}
.page-nav-brand{display:none !important;}
.page-nav-inner a.q-active{color:var(--gold) !important;border-color:var(--gold) !important;}
/* === INJECTED: Scroll margin === */
.qa-card{scroll-margin-top:125px !important;}
/* === INJECTED: Responsive width strategy === */
.header-inner,.page-body,.page-nav-inner,#nos-snav-inner,#nos-topicnav-inner{width:min(88vw,1500px) !important;max-width:none !important;margin-left:auto !important;margin-right:auto !important;}
@media(max-width:900px){.header-inner,.page-body,.page-nav-inner,#nos-snav-inner,#nos-topicnav-inner{width:calc(100vw - 40px) !important;}}
@media(max-width:480px){.header-inner,.page-body,.page-nav-inner,#nos-snav-inner,#nos-topicnav-inner{width:calc(100vw - 24px) !important;}}
/* === INJECTED: Unlock constrained inner content === */
.header-desc,.section-intro p{max-width:none !important;}
/* === INJECTED: Bottom nav === */
.page-nav-btm{background:var(--slate);border-top:2px solid var(--gold);padding:0 40px;}
.page-nav-btm .page-nav-inner a{border-bottom:none;margin-bottom:0;border-top:2px solid transparent;margin-top:-2px;}
.page-nav-btm .page-nav-inner a:hover{border-top-color:var(--amber);border-bottom:none;}
/* === INJECTED: Mobile === */
@media(max-width:680px){#nos-snav,#nos-topicnav,.page-nav-btm{padding:0 20px;}.snav-link,.snav-sign{padding:9px 8px;font-size:16px;}.tnav-link{padding:7px 7px;font-size:14px;}}
"""

SNAV_HTML = """<nav id="nos-snav" aria-label="Site navigation">
  <div id="nos-snav-inner">
    <a class="snav-wordmark" href="/">nOS</a>
    <a class="snav-link snav-active" href="/human-question/">The Human Question</a>
    <a class="snav-link" href="/case-study/">Case Study</a>
    <a class="snav-link" href="/essays/">Essays</a>
    <a class="snav-link" href="/about/">About</a>
    <a class="snav-sign" href="/sign/">Sign the Manifesto</a>
  </div>
</nav>
"""

TOPIC_LINKS = [
    ('technical-demystification',           'Technical'),
    ('economics-labor-industry',            'Economics'),
    ('geopolitics-national-security',       'Geopolitics'),
    ('ethics-society-human-impact',         'Ethics'),
    ('existential-frontier',                'Existential'),
    ('regulatory-legal-governance',         'Regulatory'),
    ('safety-security-information-integrity','Safety &amp; Security'),
    ('infrastructure-environment',          'Infrastructure'),
    ('faith-identity-human-condition',      'Faith &amp; Identity'),
    ('science-knowledge-domains',           'Science &amp; Domains'),
]

BATCH_GRID_MAP = {
    'QA_Technical_Demystification.html':         '/human-question/technical-demystification/',
    'QA_Economics_Labor_Industry.html':          '/human-question/economics-labor-industry/',
    'QA_Geopolitics_National_Security.html':     '/human-question/geopolitics-national-security/',
    'QA_Ethics_Society_Human_Impact.html':       '/human-question/ethics-society-human-impact/',
    'QA_Existential_Frontier.html':              '/human-question/existential-frontier/',
    'QA_Regulatory_Legal_Governance.html':       '/human-question/regulatory-legal-governance/',
    'QA_Safety_Security_Information_Integrity.html': '/human-question/safety-security-information-integrity/',
    'QA_Infrastructure_Environment.html':        '/human-question/infrastructure-environment/',
    'QA_Science_Knowledge_Domains.html':         '/human-question/science-knowledge-domains/',
    'QA_Faith_Identity_Human_Condition.html':    '/human-question/faith-identity-human-condition/',
}

SCROLL_JS = """<script>
(function(){
  const navLinks=document.querySelectorAll('.page-nav-inner a[href^="#q"]');
  if(!navLinks.length)return;
  const cards=Array.from(document.querySelectorAll('.qa-card[id]'));
  if(!cards.length)return;
  const visible=new Set();
  function update(){
    const activeId=cards.find(c=>visible.has(c.id))?.id;
    navLinks.forEach(link=>{
      link.classList.toggle('q-active',!!activeId&&link.getAttribute('href')==='#'+activeId);
    });
  }
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(e=>{e.isIntersecting?visible.add(e.target.id):visible.delete(e.target.id);});
    update();
  },{rootMargin:'-130px 0px -40% 0px',threshold:0});
  cards.forEach(card=>observer.observe(card));
})();
</script>
"""

PAGES = [
    {'batch': 1, 'source': '1_QA_Technical_Demystification.html',          'slug': 'technical-demystification'},
    {'batch': 2, 'source': '2_QA_Economics_Labor_Industry.html',           'slug': 'economics-labor-industry'},
    {'batch': 3, 'source': '3_QA_Geopolitics_National_Security.html',      'slug': 'geopolitics-national-security'},
    {'batch': 4, 'source': '4_QA_Ethics_Society_Human_Impact.html',        'slug': 'ethics-society-human-impact'},
    {'batch': 5, 'source': '5_QA_Existential_Frontier.html',               'slug': 'existential-frontier'},
    {'batch': 6, 'source': '6_QA_Regulatory_Legal_Governance.html',        'slug': 'regulatory-legal-governance'},
    {'batch': 7, 'source': '7_QA_Safety_Security_Information_Integrity.html', 'slug': 'safety-security-information-integrity'},
    {'batch': 8, 'source': '8_QA_Infrastructure_Environment.html',         'slug': 'infrastructure-environment'},
    {'batch': 9, 'source': '9_QA_Science_Knowledge_Domains.html',          'slug': 'science-knowledge-domains'},
]


def extract_question_links(html):
    """Extract #q* anchor links from the page-nav-inner div."""
    m = re.search(r'<div class="page-nav-inner">(.*?)</div>', html, re.DOTALL)
    if not m:
        return []
    return re.findall(r'<a href="(#q\d+)">([^<]+)</a>', m.group(1))


def make_topicnav_html(active_slug):
    lines = [
        '<nav id="nos-topicnav" aria-label="Human Question topics">',
        '  <div id="nos-topicnav-inner">',
    ]
    for slug, label in TOPIC_LINKS:
        cls = 'tnav-link tnav-active' if slug == active_slug else 'tnav-link'
        lines.append(f'    <a class="{cls}" href="/human-question/{slug}/">{label}</a>')
    lines += ['  </div>', '</nav>']
    return '\n'.join(lines) + '\n'


def make_bottom_nav_html(question_links):
    links = '\n'.join(f'    <a href="{href}">{label}</a>' for href, label in question_links)
    return (
        '\n<nav class="page-nav page-nav-btm" aria-label="Page navigation bottom">\n'
        '  <div class="page-nav-inner">\n'
        f'{links}\n'
        '    <a href="/glossary/">Glossary →</a>\n'
        '  </div>\n'
        '</nav>\n'
    )


def process_page(page):
    source_path = os.path.join(SOURCE_DIR, page['source'])
    slug = page['slug']
    out_dir = os.path.join(PUBLIC_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')

    with open(source_path, 'r', encoding='utf-8') as f:
        html = f.read()

    question_links = extract_question_links(html)

    # 1. Remove legacy footer nav block before any href rewrites
    #    Pattern: optional <br><br>, then the "← Main Report" link and everything after it to </footer>
    html = re.sub(
        r'(<br><br>)?\s*\n?\s*<a href="index\.html">.*?(?=</footer>)',
        '\n',
        html,
        flags=re.DOTALL
    )

    # 2. Append injected CSS before </style>
    html = html.replace('</style>', INJECTED_CSS + '</style>', 1)

    # 3. Remove site-brand block
    html = re.sub(r'\s*<a class="site-brand"[^>]*>.*?</a>', '', html, flags=re.DOTALL)

    # 4. Remove header-eyebrow
    html = re.sub(r'\s*<div class="header-eyebrow">[^<]*</div>', '', html)

    # 5. Inject Layer 1 + Layer 2 nav after <body>
    html = html.replace('<body>', '<body>\n' + SNAV_HTML + make_topicnav_html(slug), 1)

    # 6. Fix glossary links
    html = html.replace('href="glossary.html"', 'href="/glossary/"')

    # 7. Fix any remaining index.html refs
    html = html.replace('href="index.html"', 'href="/"')

    # 8. Fix batch grid links
    for old_href, new_href in BATCH_GRID_MAP.items():
        html = html.replace(f'href="{old_href}"', f'href="{new_href}"')

    # 9. Inject bottom nav after </main>
    if question_links:
        html = html.replace('</main>', '</main>' + make_bottom_nav_html(question_links), 1)

    # 10. Page-specific patches
    if slug == 'economics-labor-industry':
        # Source has a misclassed stat-num span (should be stat-label) causing text overflow
        html = html.replace(
            '<span class="stat-num" style="font-size:11px;padding-top:0;">',
            '<span class="stat-label" style="font-size:11px;">'
        )
    if slug == 'ethics-society-human-impact':
        # Q5 title has a hyperlink to Surgeon General report; same link exists in body — remove from title
        html = html.replace(
            '<a href="https://www.hhs.gov/sites/default/files/surgeon-general-social-connection-advisory.pdf" target="_blank">Surgeon General declared loneliness a public health epidemic</a>',
            'Surgeon General declared loneliness a public health epidemic'
        )

    # 11. Add scroll-tracking JS before </body>
    html = html.replace('</body>', SCROLL_JS + '</body>')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  Batch {page['batch']}: /{slug}/  ({len(question_links)} questions)")


if __name__ == '__main__':
    print("Building Human Question pages...")
    for page in PAGES:
        process_page(page)
    print("Done.")
