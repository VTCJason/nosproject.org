#!/usr/bin/env python3
"""
Preprocess case study markdown for pandoc → xelatex → PDF build.
Reads IMMUTABLE source; writes clean pandoc-compatible markdown to /tmp/case-study-pandoc.md.
"""
import re, sys

SRC = "/home/mocha/projects/nosmanifesto-site/source-material/case-study/when_tenant_becomes_landlord_paper.md"
OUT = "/tmp/case-study-pandoc.md"
IMG_BASE = "/home/mocha/projects/nosmanifesto-site/public/case-study"


def latex_escape(text):
    """Escape LaTeX special characters in plain text (not in already-escaped sequences)."""
    # Order matters: backslash first
    text = text.replace('\\|', '|')          # markdown-escaped pipe → plain pipe
    text = re.sub(r'\\([^$\\])', r'\1', text)  # remove other markdown escapes
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('#', r'\#')
    # Keep \$ as-is (already valid LaTeX)
    return text


def md_inline_to_latex(text):
    """Convert inline markdown to LaTeX for use inside raw LaTeX blocks."""
    # Bold+italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # Italic
    text = re.sub(r'\*([^*\n]+?)\*', r'\\textit{\1}', text)
    # Links — escape underscores in display text (LaTeX treats _ as subscript)
    def link_to_href(m):
        link_text = m.group(1).replace('_', r'\_').replace('%', r'\%')
        url = m.group(2)
        return f'\\href{{{url}}}{{{link_text}}}'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_to_href, text)
    # Escaped pipe → plain pipe
    text = text.replace(r'\|', r'|')
    # Escape special LaTeX chars (after inline conversion)
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    return text


def bq_block_to_raw_latex(bq_text):
    """Convert a blockquote block (consecutive > lines) to a raw LaTeX callout."""
    lines = bq_text.strip().split('\n')
    # Strip '> ' or '>' prefix from each line
    content_lines = [re.sub(r'^>\s?', '', l) for l in lines]
    content = '\n'.join(content_lines).strip()

    # Convert inline markdown in the content to LaTeX
    content = md_inline_to_latex(content)

    raw = f"```{{=latex}}\n\\begin{{figure*}}[t]\n\\begin{{callout}}\n{content}\n\\end{{callout}}\n\\end{{figure*}}\n```"
    return raw


def figure_to_pandoc(m):
    """Convert <figure>...</figure> HTML block to raw LaTeX figure* (full-width, spans both columns)."""
    block = m.group(0)
    img_m = re.search(r'<img src="([^"]+)"', block)
    cap_m = re.search(r'<figcaption[^>]*>(.*?)</figcaption>', block, re.DOTALL)
    if not img_m:
        return ''
    src = img_m.group(1)              # e.g. paper_assets/foo.png
    full_path = f"{IMG_BASE}/{src}"   # absolute path for xelatex to resolve
    caption = ''
    if cap_m:
        caption = re.sub(r'<[^>]+>', '', cap_m.group(1)).strip()
        caption = md_inline_to_latex(caption)
    latex = (
        f"\\begin{{figure*}}[t]\n"
        f"\\centering\n"
        f"\\includegraphics[width=0.9\\textwidth,keepaspectratio]{{{full_path}}}\n"
        f"\\caption{{{caption}}}\n"
        f"\\end{{figure*}}"
    )
    return f'\n\n```{{=latex}}\n{latex}\n```\n\n'


def main():
    with open(SRC) as f:
        raw = f.read()

    # ── 1. Extract abstract from <div class="abstract-block"> ─────────────────
    abs_m = re.search(r'<div class="abstract-block">\s*(.*?)\s*</div>', raw, re.DOTALL)
    abstract_lines = ''
    if abs_m:
        abs_raw = abs_m.group(1)
        # Strip <span class="abstract-label">ABSTRACT.</span> and trim
        abs_raw = re.sub(r'<span[^>]*>ABSTRACT\.</span>\s*', '', abs_raw)
        abs_raw = re.sub(r'<[^>]+>', '', abs_raw).strip()
        # Indent each line for YAML block scalar
        abstract_lines = '\n'.join('  ' + l for l in abs_raw.split('\n'))

    # ── 2. Remove title block (lines 1-8) and abstract block from body ────────
    # Find where the abstract div ends and body content begins
    after_abstract = raw
    if abs_m:
        end_pos = abs_m.end()
        after_abstract = raw[end_pos:].lstrip('\n')
    else:
        # Skip first paragraph block (title)
        after_abstract = re.sub(r'^.*?(?=\n\n\n)', '', raw, count=1, flags=re.DOTALL)

    body = after_abstract

    # ── 3. Upgrade ### 6. / ### 7. / ### 8. (top-level sections) to ## ────────
    body = re.sub(r'^### (6\.|7\.|8\.)', r'## \1', body, flags=re.MULTILINE)

    # ── 4. Upgrade #### 6.x and #### 7.x subsections to ### ──────────────────
    body = re.sub(r'^#### (6\.|7\.)', r'### \1', body, flags=re.MULTILINE)

    # ── 5. Transform <figure>...</figure> blocks → pandoc figure syntax ────────
    body = re.sub(r'<figure>.*?</figure>', figure_to_pandoc, body, flags=re.DOTALL)

    # ── 6. Transform blockquote callouts → raw LaTeX callout environment ───────
    # Match blockquote blocks: consecutive lines starting with > (including bare >)
    def bq_sub(m):
        return '\n\n' + bq_block_to_raw_latex(m.group(0)) + '\n\n'

    body = re.sub(r'(?m)((?:^>[ \t]?[^\n]*\n)+)', bq_sub, body)

    # ── 7. Strip HTML span tags (References section headings) ─────────────────
    body = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', body, flags=re.DOTALL)

    # ── 8. Remove any leftover <div> or </div> tags ───────────────────────────
    body = re.sub(r'</?div[^>]*>', '', body)

    # ── 9. Remove the horizontal rule after the title block ───────────────────
    # (already above the callouts, will be gone since we stripped the title block)

    # ── Build output ──────────────────────────────────────────────────────────
    frontmatter = f"""---
title: "When the Tenant Becomes the Landlord"
subtitle: "Value-Chain Inversion in the Post-2026 Productivity Stack"
author: "Jason Troxel"
date: "Drafted April 2026; revised May 2026"
abstract: |
{abstract_lines}
---
"""

    output = frontmatter + '\n' + body.strip() + '\n'

    # Replace Unicode curly quotes not supported by EB Garamond TTF (applied to full output)
    output = output.replace('\u2018', '`').replace('\u2019', "'")
    output = output.replace('\u2018', '`').replace('\u2019', "'")

    with open(OUT, 'w') as f:
        f.write(output)

    print(f"Preprocessed: {SRC}")
    print(f"Output:       {OUT}")
    print(f"Lines:        {len(output.splitlines())}")


if __name__ == '__main__':
    main()
