#!/usr/bin/env python3
import os
import re
import shutil
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content'
STATIC = ROOT / 'static'
ASSET_VERSION = '20260410g'

SITE = {
    'title': 'Wenjian Hao',
    'tagline': 'Ph.D. candidate, Purdue University AAE',
    'intro_text': (
        'I am a Ph.D. candidate in the School of Aeronautics and Astronautics at Purdue University, advised by Dr. '
        'Shaoshuai Mou. My research focuses on learning-based control for autonomous robots; data-driven modeling '
        'of nonlinear dynamics using globally linear representations; data-efficient reinforcement learning; '
        'optimal, safety-critical, and sampling-based control; and multi-agent systems.'
    ),
    'bio': (
        'I am a Ph.D. candidate in the School of Aeronautics and Astronautics at Purdue University, advised by Dr. '
        'Shaoshuai Mou. My research focuses on learning-based control for autonomous robots; data-driven modeling '
        'of nonlinear dynamics using globally linear representations; data-efficient reinforcement learning; '
        'optimal, safety-critical, and sampling-based control; and multi-agent systems.'
    ),
    'portrait': '/wenjian-hao.jpg',
    'email': 'mailto:haowjz@gmail.com',
    'scholar': 'https://scholar.google.com/citations?user=SQ2BSVsAAAAJ&hl=en',
    'github': 'https://github.com/wenjianhao',
    'nav': [
        ('Papers', '/#papers'),
        ('Projects', '/#projects'),
        ('Blog', '/#blog'),
        ('Miscellaneous', '/#miscellaneous'),
    ],
}

PAPER_GROUPS = [
    'Learning-Based Control for Robotics',
    'Dynamics Learning for Complex Systems',
    'Distributed Learning and Multi-Agent Systems',
]
PROJECT_GROUPS = [
    'Personal Projects',
    'Funded Projects',
]

MATHJAX = """
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    tags: 'all'
  },
  svg: { fontCache: 'global' }
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
""".strip()


def read_file(path):
    return path.read_text(encoding='utf-8')


def write_file(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def slugify(value):
    value = value.strip().lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-')


def parse_date(value):
    value = value.strip().strip('"')
    for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return datetime(1970, 1, 1)


def format_date(dt):
    return dt.strftime('%B %Y')


def format_year(dt):
    return dt.strftime('%Y')


def parse_front_matter(raw):
    if not raw.startswith('---\n'):
        return {}, raw
    parts = raw.split('\n---\n', 1)
    if len(parts) != 2:
        return {}, raw
    fm_raw = parts[0].split('\n', 1)[1]
    body = parts[1]
    data = {}
    for line in fm_raw.splitlines():
        if not line.strip() or line.strip().startswith('#'):
            continue
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.strip()
        val = val.strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
        elif val in ('true', 'false'):
            val = val == 'true'
        data[key] = val
    return data, body.lstrip('\n')


def inline_markdown(text):
    math_spans = []

    def stash_math(match):
        math_spans.append(match.group(0))
        return f"__MATH_{len(math_spans) - 1}__"

    text = re.sub(r'\$[^$]+\$', stash_math, text)
    text = escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    for idx, span in enumerate(math_spans):
        text = text.replace(f"__MATH_{idx}__", span)
    return text


def display_title(title):
    title = title.strip()
    if not title:
        return title
    return title[0].upper() + title[1:].lower()


def emphasize_author_names(author_text):
    text = escape(author_text)
    patterns = [
        r'\bW Hao\b',
        r'\bWenjian Hao\b',
        r'\bHao,\s*Wenjian\b',
    ]
    for pattern in patterns:
        text = re.sub(pattern, lambda m: f'<strong>{m.group(0)}</strong>', text)
    return text


def youtube_embed(video_id):
    return (
        '<div class="video-wrap">'
        f'<iframe src="https://www.youtube.com/embed/{video_id}" title="YouTube video" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
        'allowfullscreen loading="lazy"></iframe></div>'
    )


def render_markdown(body):
    body = body.replace('<!--more-->', '')
    lines = body.splitlines()
    out = []
    paragraph = []
    in_ul = False
    in_ol = False
    in_code = False
    code_lang = ''
    code_lines = []
    in_math_block = False
    math_end = ''
    math_lines = []

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            text = ' '.join(x.strip() for x in paragraph).strip()
            if text:
                out.append(f'<p>{inline_markdown(text)}</p>')
            paragraph = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append('</ul>')
            in_ul = False
        if in_ol:
            out.append('</ol>')
            in_ol = False

    def flush_math_block():
        nonlocal in_math_block, math_end, math_lines
        if math_lines:
            out.append('\n'.join(math_lines))
        in_math_block = False
        math_end = ''
        math_lines = []

    for raw in lines:
        line = raw.rstrip('\n')
        stripped = line.strip()

        if in_code:
            if stripped.startswith('```'):
                code = escape('\n'.join(code_lines))
                klass = f' class="language-{code_lang}"' if code_lang else ''
                out.append(f'<pre><code{klass}>{code}</code></pre>')
                in_code = False
                code_lang = ''
                code_lines = []
            else:
                code_lines.append(line)
            continue

        if in_math_block:
            math_lines.append(line)
            if stripped == math_end or stripped.startswith(math_end):
                flush_math_block()
            continue

        if stripped.startswith('```'):
            flush_paragraph()
            close_lists()
            in_code = True
            code_lang = stripped[3:].strip()
            code_lines = []
            continue

        if stripped == '$$':
            flush_paragraph()
            close_lists()
            in_math_block = True
            math_end = '$$'
            math_lines = [line]
            continue

        if stripped.startswith(r'\begin{equation'):
            flush_paragraph()
            close_lists()
            in_math_block = True
            math_end = r'\end{equation}'
            math_lines = [line]
            continue

        if stripped.startswith(r'\begin{align'):
            flush_paragraph()
            close_lists()
            in_math_block = True
            math_end = r'\end{align}'
            math_lines = [line]
            continue

        if not stripped:
            flush_paragraph()
            close_lists()
            continue

        if stripped == '---':
            flush_paragraph()
            close_lists()
            out.append('<hr>')
            continue

        yt = re.match(r'\{\{<\s*youtube\s+([A-Za-z0-9_-]+)\s*>\}\}', stripped)
        if yt:
            flush_paragraph()
            close_lists()
            out.append(youtube_embed(yt.group(1)))
            continue

        if stripped.startswith('<'):
            flush_paragraph()
            close_lists()
            out.append(line)
            continue

        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            flush_paragraph()
            close_lists()
            level = len(m.group(1))
            text = inline_markdown(m.group(2).strip())
            anchor = slugify(re.sub(r'<[^>]+>', '', m.group(2)))
            out.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            continue

        m = re.match(r'^\d+\.\s+(.*)$', stripped)
        if m:
            flush_paragraph()
            if in_ul:
                out.append('</ul>')
                in_ul = False
            if not in_ol:
                out.append('<ol>')
                in_ol = True
            out.append(f'<li>{inline_markdown(m.group(1).strip())}</li>')
            continue

        if stripped.startswith('- '):
            flush_paragraph()
            if in_ol:
                out.append('</ol>')
                in_ol = False
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{inline_markdown(stripped[2:].strip())}</li>')
            continue

        paragraph.append(line)

    flush_paragraph()
    close_lists()
    return '\n'.join(out)


def excerpt_from_body(body):
    body = re.sub(r'---', ' ', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\{\{<[^>]+>\}\}', ' ', body)
    body = re.sub(r'`[^`]+`', ' ', body)
    body = re.sub(r'\$[^$]+\$', ' ', body)
    text = ' '.join(body.split())
    return text[:220].rsplit(' ', 1)[0] + '...' if len(text) > 220 else text


def extract_resource_links(body):
    pdf_url = ''
    code_url = ''
    for label, url in re.findall(r'-\s+\[([^\]]+)\]\(([^)]+)\)', body):
        norm = label.strip().lower()
        if not pdf_url and norm == 'paper':
            pdf_url = url
        if not code_url and ('code' in norm):
            code_url = url
    return pdf_url, code_url


def load_entries(section):
    entries = []
    for path in sorted((CONTENT / section).glob('*.md')):
        if path.name == '_index.md' or path.name.startswith('.'):
            continue
        raw = read_file(path)
        front, body = parse_front_matter(raw)
        rendered = render_markdown(body)
        pdf_url, code_url = extract_resource_links(body)
        dt = parse_date(str(front.get('date', '1970-01-01')))
        slug = slugify(path.stem)
        if section == 'blog' and path.stem:
            slug = slugify(path.stem)
        summary = front.get('summary') or excerpt_from_body(body)
        entries.append({
            'title': front.get('title', path.stem),
            'date': dt,
            'date_label': format_date(dt),
            'year': format_year(dt),
            'author': front.get('author', ''),
            'summary': summary,
            'body_html': rendered,
            'slug': slug,
            'section': section,
            'group': front.get('paper_group') or front.get('project_group') or '',
            'venue': front.get('venue', ''),
            'math': bool(front.get('math')),
            'pdf_url': pdf_url,
            'code_url': code_url,
        })
    entries.sort(key=lambda x: x['date'], reverse=True)
    return entries


def page_shell(title, content, description='', include_math=False):
    nav = ''.join(f'<a href="{href}">{label}</a>' for label, href in SITE['nav'])
    math = MATHJAX if include_math else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{escape(title)} | {escape(SITE['title'])}</title>
  <meta name="description" content="{escape(description or title)}">
  <link rel="icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <link href="/css/bootstrap.min.css?v={ASSET_VERSION}" rel="stylesheet">
  <link href="/css/site.css?v={ASSET_VERSION}" rel="stylesheet">
  {math}
</head>
<body>
  <div class="site-nav-wrap">
    <div class="container">
      <div class="site-nav">
        <div class="site-title"><a href="/">{escape(SITE['title'])}</a></div>
        <div class="site-menu">{nav}</div>
      </div>
    </div>
  </div>
  {content}
</body>
</html>
'''


def home_shell(title, content, description=''):
    nav = ''.join(f'<a href="{href}">{label}</a>' for label, href in SITE['nav'])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{escape(title)} | {escape(SITE['title'])}</title>
  <meta name="description" content="{escape(description or title)}">
  <link rel="icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <link href="/css/bootstrap.min.css?v={ASSET_VERSION}" rel="stylesheet">
  <link href="/css/site.css?v={ASSET_VERSION}" rel="stylesheet">
</head>
<body>
  <div class="container home-top">
    <div class="row">
      <div class="col-12">
        <div class="home-masthead">
          <div class="home-identity">
            <div class="home-name">{escape(SITE['title'])}</div>
            <div class="home-role">{escape(SITE['tagline'])}</div>
          </div>
          <div class="site-menu home-menu">{nav}</div>
        </div>
      </div>
    </div>
  </div>
  {content}
</body>
</html>
'''


def hero_block():
    return f'''
<div class="container">
  <div class="row">
    <div class="col-12">
      <div class="hero-intro">
        <div class="hero-copy">
          <p class="hero-text">{escape(SITE['intro_text'])}</p>
          <div class="hero-buttons">
            <a class="hero-button" href="{SITE['email']}"><i class="bi bi-envelope" aria-hidden="true"></i><span>Email</span></a>
            <a class="hero-button" href="{SITE['scholar']}"><i class="bi bi-mortarboard" aria-hidden="true"></i><span>Scholar</span></a>
            <a class="hero-button" href="{SITE['github']}"><i class="bi bi-github" aria-hidden="true"></i><span>GitHub</span></a>
          </div>
        </div>
        <div class="hero-visual">
          <img src="{SITE['portrait']}" class="img-fluid" id="portrait" alt="Wenjian Hao portrait">
        </div>
      </div>
    </div>
  </div>
</div>
'''


def render_home_section(section_id, title, items, kind):
    cards = []
    for item in items:
        meta = ''
        if kind == 'papers':
            authors = emphasize_author_names(item['author'])
            venue_parts = []
            if item['venue']:
                venue_parts.append(escape(item['venue']))
            if not item['venue'] or not re.search(r'\b(19|20)\d{2}\b', item['venue']):
                venue_parts.append(item['year'])
            resources = []
            if item.get('pdf_url'):
                resources.append(f"<a href='{escape(item['pdf_url'])}'>[PDF]</a>")
            if item.get('code_url'):
                resources.append(f"<a href='{escape(item['code_url'])}'>[Code]</a>")
            venue_line = ' · '.join(venue_parts)
            if resources:
                venue_line = f"{venue_line} · {' / '.join(resources)}" if venue_line else ' / '.join(resources)
            venue_html = f"<div class='entry-venue'>{venue_line}</div>" if venue_line else ''
            meta = f"<div class='entry-authors'>{authors}</div>{venue_html}"
        else:
            meta = f"<div class='entry-year'>{item['date_label']}</div>"
        cards.append(
            f"<div class='content-entry'>"
            f"<div class='content-entry-main'><div class='entry-title'><a href='/{kind}/{item['slug']}/'>{escape(display_title(item['title']) if kind in ('papers', 'blog') else item['title'])}</a></div>"
            f"<div class='entry-summary'>{escape(item['summary'])}</div>{meta}</div></div>"
        )
    return f"<section id='{section_id}' class='content-section'><h1>{escape(title)}</h1>{''.join(cards)}</section>"


def render_grouped_list(title, grouped_html):
    return f"<div class='container subpage'><div class='row'><div class='col-12'><h1 class='section-page-title'>{escape(title)}</h1>{grouped_html}</div></div></div>"


def paper_list_entry(item):
    venue_parts = []
    if item['venue']:
        venue_parts.append(escape(item['venue']))
    if not item['venue'] or not re.search(r'\b(19|20)\d{2}\b', item['venue']):
        venue_parts.append(item['year'])
    resources = []
    if item.get('pdf_url'):
        resources.append(f"<a href='{escape(item['pdf_url'])}'>[PDF]</a>")
    if item.get('code_url'):
        resources.append(f"<a href='{escape(item['code_url'])}'>[Code]</a>")
    venue_line = ' · '.join(venue_parts)
    if resources:
        venue_line = f"{venue_line} · {' / '.join(resources)}" if venue_line else ' / '.join(resources)
    venue_html = f"<div class='entry-venue'>{venue_line}</div>" if venue_line else ''
    return (
        "<div class='content-entry'><div class='content-entry-main'>"
        f"<div class='entry-title'><a href='/papers/{item['slug']}/'>{escape(display_title(item['title']))}</a></div>"
        f"<div class='entry-summary'>{escape(item['summary'])}</div>"
        f"<div class='entry-authors'>{emphasize_author_names(item['author'])}</div>"
        f"{venue_html}</div></div>"
    )


def render_detail(entry):
    title = display_title(entry['title']) if entry['section'] in ('papers', 'blog') else entry['title']
    meta_parts = [entry['date_label']]
    if entry['author']:
        meta_parts.append(entry['author'])
    if entry['venue']:
        meta_parts.append(entry['venue'])
    meta = ' · '.join(escape(x) for x in meta_parts if x)
    body = f'''
<div class="container subpage article-page">
  <div class="row">
    <div class="col-12">
      <div class="article-meta"><a href="/">Home</a> / <a href="/{entry['section']}/">{entry['section'].title()}</a></div>
      <h1 class="section-page-title">{escape(title)}</h1>
      <div class="article-submeta">{meta}</div>
      <div class="article-content">{entry['body_html']}</div>
    </div>
  </div>
</div>
'''
    return page_shell(title, body, entry['summary'], include_math=entry['math'])


def render_home(papers, projects, blogs, misc):
    content = hero_block() + f'''
<div class="container">
  <div class="row">
    <div class="col-12">
      {render_home_section('papers', 'Highlighted Work', papers, 'papers')}
      {render_home_section('projects', 'Projects', projects, 'projects')}
      {render_home_section('blog', 'Blog', blogs, 'blog')}
      {render_home_section('miscellaneous', 'Miscellaneous', misc, 'miscellaneous')}
    </div>
  </div>
</div>
'''
    return home_shell(SITE['title'], content, SITE['bio'])


def build_list_pages(papers, projects, blogs, misc):
    paper_groups = []
    for group in PAPER_GROUPS:
        items = [p for p in papers if p['group'] == group]
        if not items:
            continue
        entries = ''.join(paper_list_entry(i) for i in items)
        paper_groups.append(f"<section class='content-section grouped-section'><h2>{escape(group)}</h2>{entries}</section>")
    write_file(ROOT / 'papers' / 'index.html', page_shell('Papers', render_grouped_list('Papers', ''.join(paper_groups)), 'Papers and publications'))

    grouped_projects = []
    for group in PROJECT_GROUPS:
        source_group = group if group != 'Funded Projects' else 'Funded Research Projects'
        items = [p for p in projects if p['group'] in (group, source_group)]
        if not items:
            continue
        entries = ''.join(
            f"<div class='content-entry'><div class='content-entry-main'><div class='entry-title'><a href='/projects/{i['slug']}/'>{escape(i['title'])}</a></div><div class='entry-summary'>{escape(i['summary'])}</div><div class='entry-year'>{i['date_label']}</div></div></div>"
            for i in items
        )
        grouped_projects.append(f"<section class='content-section grouped-section'><h2>{escape(group)}</h2>{entries}</section>")
    write_file(ROOT / 'projects' / 'index.html', page_shell('Projects', render_grouped_list('Projects', ''.join(grouped_projects)), 'Projects'))

    blog_entries = ''.join(
        f"<div class='content-entry'><div class='content-entry-main'><div class='entry-title'><a href='/blog/{i['slug']}/'>{escape(display_title(i['title']))}</a></div><div class='entry-summary'>{escape(i['summary'])}</div><div class='entry-year'>{i['date_label']}</div></div></div>"
        for i in blogs
    )
    write_file(ROOT / 'blog' / 'index.html', page_shell('Blog', render_grouped_list('Blog', blog_entries), 'Blog posts'))

    misc_entries = ''.join(
        f"<div class='content-entry'><div class='content-entry-main'><div class='entry-title'><a href='/miscellaneous/{i['slug']}/'>{escape(i['title'])}</a></div><div class='entry-summary'>{escape(i['summary'])}</div><div class='entry-year'>{i['date_label']}</div></div></div>"
        for i in misc
    )
    write_file(ROOT / 'miscellaneous' / 'index.html', page_shell('Miscellaneous', render_grouped_list('Miscellaneous', misc_entries), 'Miscellaneous'))


def copy_static_assets():
    if STATIC.exists():
        for path in STATIC.rglob('*'):
            if path.is_dir():
                continue
            rel = path.relative_to(STATIC)
            dest = ROOT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                dest.chmod(0o644)
            shutil.copy2(path, dest)


def clean_old_outputs():
    for path in [ROOT / 'index.html', ROOT / '404.html']:
        if path.exists():
            path.unlink()
    for directory in ['papers', 'projects', 'blog', 'miscellaneous']:
        target = ROOT / directory
        if target.exists():
            for item in target.iterdir():
                if item.name == 'index.html':
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)


def main():
    clean_old_outputs()
    copy_static_assets()
    papers = load_entries('papers')
    projects = load_entries('projects')
    blogs = load_entries('blog')
    misc = load_entries('miscellaneous')

    write_file(ROOT / 'index.html', render_home(papers, projects, blogs, misc))
    build_list_pages(papers, projects, blogs, misc)

    for entry in papers + projects + blogs + misc:
        write_file(ROOT / entry['section'] / entry['slug'] / 'index.html', render_detail(entry))

    write_file(ROOT / '404.html', page_shell('404', '<div class="container subpage"><div class="row"><div class="col-12"><h1 class="section-page-title">404</h1><p>Page not found.</p></div></div></div>', 'Page not found'))


if __name__ == '__main__':
    main()
