#!/usr/bin/env python3
"""Render the maintained English rules translations with their source artwork."""

import argparse
import hashlib
import html
from pathlib import Path
import re
import tempfile
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import markdown
from weasyprint import HTML

from rules_pdf_assets import extract_figures


DOCUMENTS = (
    'rmul-rules-manual',
    'rmul-participant-manual',
    'rmuc-rules-manual',
    'rmuc-participant-manual',
    'robot-building-specifications',
    'rule-change-preview',
)

STYLE = '''
@page {
  size: A4;
  margin: 17mm 16mm 18mm;
  @bottom-left { content: string(source); color: #566173; font-size: 8pt; }
  @bottom-right { content: counter(page); color: #566173; font-size: 8pt; }
}
@page wide { size: A4 landscape; }
html { font-family: sans-serif; font-size: 10pt; color: #172438; line-height: 1.35; }
h1 { font-size: 25pt; color: #123f70; line-height: 1.15; }
h2 { font-size: 18pt; color: #123f70; }
h3 { font-size: 14pt; color: #123f70; }
h4, h5, h6 { font-size: 11pt; color: #123f70; }
h1, h2, h3, h4, h5, h6 { break-after: avoid; }
p { margin: 0.6em 0; }
a { color: #145b96; text-decoration: none; overflow-wrap: anywhere; }
li { margin-bottom: 0.3em; }
blockquote { margin: 1em 0; padding: 0.1em 0.8em; border-left: 3px solid #6294ba;
  background: #f0f5f9; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: 1em 0;
  table-layout: fixed; }
thead { display: table-header-group; }
th { background: #e6edf5; text-align: left; }
th, td { padding: 5px; border: 0.6px solid #aab7c7; vertical-align: top;
  overflow-wrap: anywhere; }
tr { break-inside: avoid; }
table.wide { page: wide; font-size: 8pt; }
table.dense { font-size: 8pt; }
.source-marker { break-before: page; break-after: avoid; string-set: source content();
  font-size: 8pt; color: #65758a; margin-bottom: 1em; }
figure { margin: 1em 0 0; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; max-height: 205mm; object-fit: contain; }
figcaption { font-size: 8pt; color: #65758a; margin: 0.5em 0; }
.figure-caption { font-weight: bold; }
.edition { font-size: 10pt; padding: 1em; background: #f0f5f9; }
code { font-family: monospace; font-size: 8pt; overflow-wrap: anywhere; }
'''


def render_document(root, name, work):
    """Keep source page markers and inject figure artwork beside English keys."""
    source = root / 'source' / f'{name}-zh.pdf'
    text = (root / f'{name}.md').read_text()
    title = text.splitlines()[0].removeprefix('# ')
    text = re.sub(r'(?<=[0-9A-Za-z)])\*(?=[0-9A-Za-z(])', ' × ', text)
    text = re.sub(r'^# .+\n', '', text, count=1)
    text = re.sub(r'^`<!-- p.N -->` markers give the physical PDF page\.\n', '', text,
                  flags=re.MULTILINE)
    text = re.sub(
        r'<!-- p\.(\d+)(?:: contents list omitted)? -->',
        lambda m: f'\n<div class="source-marker">Source PDF page {m[1]}</div>\n',
        text,
    )
    body = markdown.markdown(text, extensions=['tables', 'sane_lists', 'toc'])
    soup = BeautifulSoup(body, 'html.parser')
    for link in soup.find_all('a', href=True):
        if not link['href'].startswith('#'):
            link['href'] = urljoin(
                'https://github.com/Thornbots/thornbots_workspace/blob/nightly/'
                'docs/rules/rm2027/', link['href'])
    figures = extract_figures(source, work / name / 'figures')
    english = root / 'figures' / 'english'
    inserted = []
    for paragraph in soup.find_all('p'):
        caption = re.match(r'^Figure (\d+-\d+)\b', paragraph.get_text())
        if not caption:
            continue
        number = caption[1]
        paragraph['class'] = ['figure-caption']
        translated = english / f'{name}-figure-{number}.svg'
        paths = [translated] if translated.exists() else figures.get("Figure " + number, [])
        if not paths:
            continue
        figure = soup.new_tag('figure')
        for path in paths:
            image = soup.new_tag('img', src=path.resolve().as_uri())
            image['alt'] = paragraph.get_text()
            image['style'] = f'max-height: {min(205, 195 / len(paths)):.1f}mm'
            figure.append(image)
        note = soup.new_tag('figcaption')
        note.string = ('English diagram; source values and branches retained.'
                       if translated.exists() else
                       'Source artwork. English caption and key follow.')
        figure.append(note)
        caption_tag = soup.new_tag('figcaption')
        caption_tag['class'] = ['figure-caption']
        caption_tag.string = paragraph.get_text()
        figure.append(caption_tag)
        paragraph.replace_with(figure)
        inserted.append(number)
    for table in soup.find_all('table'):
        columns = max((len(row.find_all(['th', 'td'], recursive=False))
                       for row in table.find_all('tr')), default=0)
        headings = [cell.get_text().strip().lower() for cell in table.find_all('th')]
        if headings == ['entry', 'printed page']:
            for row in table.find_all('tr'):
                cells = row.find_all(['th', 'td'], recursive=False)
                if len(cells) == 2:
                    cells[0]['style'] = 'width: 85%'
                    cells[1]['style'] = 'width: 15%'
        if columns >= 7:
            table['class'] = ['wide']
            previous = table.find_previous_sibling()
            if previous and previous.name == 'p' and previous.get_text().startswith('Table '):
                previous['style'] = 'page: wide'
                previous = previous.find_previous_sibling()
            if previous and 'source-marker' in previous.get('class', []):
                previous['style'] = 'page: wide'
        elif columns >= 5:
            table['class'] = ['dense']
    digest = hashlib.md5(source.read_bytes()).hexdigest()
    edition = (
        f'<h1>{html.escape(title)}</h1><div class="edition">'
        '<p><strong>English reference edition</strong></p>'
        '<p>The Chinese source is authoritative. English prose, tables, captions '
        'and figure keys follow the maintained Markdown translation. Original '
        'technical artwork is retained; English flowcharts replace selected '
        'Chinese diagrams. Any embedded source annotations are explained by '
        'the English keys.</p>'
        '<p>Source page markers refer to physical pages of the Chinese PDF. '
        'English pagination differs because translated text is reflowed. '
        'The contents lists retain the source printed page numbers.</p>'
        f'<p>Source MD5: <code>{digest}</code></p></div>'
    )
    output = root / 'pdf' / f'{name}-en.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    document = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                f'<title>{html.escape(title)}</title><style>{STYLE}</style>'
                f'</head><body>{edition}{soup}</body></html>')
    html_path = work / f'{name}.html'
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(document)
    HTML(filename=str(html_path)).write_pdf(str(output), presentational_hints=True)
    print(f'{output.name}: {len(inserted)} illustrated figures; '
          f'{output.stat().st_size / 1024 / 1024:.1f} MiB')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('documents', nargs='*', choices=DOCUMENTS)
    parser.add_argument('--root', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'docs/rules/rm2027')
    parser.add_argument('--work-dir', type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='rules-pdf-') as temporary:
        work = args.work_dir or Path(temporary)
        for name in args.documents or DOCUMENTS:
            render_document(args.root, name, work)


if __name__ == '__main__':
    main()
