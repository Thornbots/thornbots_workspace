# RoboMaster 2027 rules (English translation)

Unofficial English translations of the RoboMaster 2027 University League
(RMUL) and University Championship (RMUC) rule documents, released
2026-10-15. ARCC treats itself as an RMUL
event, so these are the closest published base for ARCC 2027 until ARC
releases its own rules. The [game context](../../ARCC_2026_SENTRY_CONTEXT.md#robomaster-2027-rmul-base-rules)
summarizes the Sentry and CV deltas.

The Chinese PDFs govern; these translations are for team reference only.

| Translation | English PDF | Chinese source | Source pages | Source MD5 |
| --- | --- | --- | --- | --- |
| [RMUL Rules Manual V1.0.0](rmul-rules-manual.md) | [English](pdf/rmul-rules-manual-en.pdf) | [Chinese](source/rmul-rules-manual-zh.pdf) | 68 | `d75e932a7d69dd2fa53906dfc67512be` |
| [RMUL Participant Manual V1.0.0](rmul-participant-manual.md) | [English](pdf/rmul-participant-manual-en.pdf) | [Chinese](source/rmul-participant-manual-zh.pdf) | 28 | `b51b4a5839401dbc334531d0409b3d15` |
| [RMUC Rules Manual V1.0.0](rmuc-rules-manual.md) | [English](pdf/rmuc-rules-manual-en.pdf) | [Chinese](source/rmuc-rules-manual-zh.pdf) | 144 | `4ff71c2945d578c444ae5b9620e43dfb` |
| [RMUC Participant Manual V1.0.0](rmuc-participant-manual.md) | [English](pdf/rmuc-participant-manual-en.pdf) | [Chinese](source/rmuc-participant-manual-zh.pdf) | 37 | `5ef9fcc4938723ce3db7aed3fe4501c6` |
| [Robot Building Specifications Manual V1.0.0](robot-building-specifications.md) | [English](pdf/robot-building-specifications-en.pdf) | [Chinese](source/robot-building-specifications-zh.pdf) | 91 | `39175fdc1c263b10ec44727c5689c329` |
| [Rule-Change Preview](rule-change-preview.md) | [English](pdf/rule-change-preview-en.pdf) | [Chinese](source/rule-change-preview-zh.pdf) | 19 | `87c15791e3dbabab9dde749bc8cadf8b` |

RMUC is included for comparison; ARCC follows RMUL. The Building
Specifications Manual is shared by RMUC and RMUL; RMUL-only exemptions are
marked in its tables. The preview predates V1.0.0; where they
differ, the manuals win.

## Sources

- [RMUL 2027 Competition Rules](https://bbs.robomaster.com/wiki/20204847/1969150)
  (Rules, Participant and Building Specifications manuals).
- [RMUC 2027 Competition Rules](https://bbs.robomaster.com/wiki/20204847/1969149)
  (same Building Specifications Manual, plus the Rule-Change Preview).

The wiki pages render client-side. Their attachment URLs come from
`POST https://bbs.robomaster.com/developers-server/rest/posts/info/<post id>`
with body `{}`; the PDFs are in `data.attachments[].src` (URL-quote the
filename).

## Conventions

- `<!-- p.N -->` marks the start of physical PDF page N; running headers
  and footers are dropped. Each manual includes translated contents,
  table and figure lists where present, with the source's printed page numbers.
  Table rows split across pages are joined on the page where the row begins.
- Rule IDs, section, table and figure numbers, values and units are copied
  as printed, including apparent source typos.
- Markdown describes figures with translated captions, labels and dimensions.
  The English PDFs preserve the source page count, page sizes, section and
  figure positions, table geometry and page breaks. Split table rows stay on
  their original pages in the PDFs. English text is fitted into the original
  text areas; font sizes can differ to fit longer translations. Source artwork
  is retained, with English text and a translated talent-development pyramid.
  Contents, figure-list and table-list entries link to their destination pages.
- Terms follow the [game context](../../ARCC_2026_SENTRY_CONTEXT.md)
  (for example Infantry Robot for 步兵机器人, Bumpy Road for 起伏路段).

Translated from the extracted text and checked against a render of every
page. A second reviewer then compared every page with its render for the
RMUL and RMUC manuals, the Building Specifications Manual and the preview.

## PDF generation

The Markdown files maintain the readable translations. The page-specific
[layout maps](layout) maintain English text for source regions that cannot be
matched automatically to Markdown headings, captions or table cells. Region
IDs identify a physical page and text region in the pinned source PDFs; change
the maps if the source changes. The source hashes above identify that edition.

[build_rules_pdfs.py](../../../scripts/build_rules_pdfs.py) uses the original
PDFs as templates, replaces their Chinese text, and adds PDF contents links.
[rules_pdf_layout.py](../../../scripts/rules_pdf_layout.py) extracts the source
geometry and matches the checked Markdown. The renderer fails on untranslated
regions or unresolved contents destinations.

Install the pinned [Python dependencies](pdf-requirements.txt), then run
`python scripts/build_rules_pdfs.py` from the workspace root. It writes all six
English editions into `pdf/`; pass a manual basename to rebuild one edition.
Use `--report /tmp/rules-pdf-report.json` to record fitted text regions and
contents destinations for review. Temporary incomplete previews require both
`--allow-missing` and an explicit `--output-dir`; they never replace the
checked-in editions by default.

Run `python -m unittest discover -s scripts/tests -v` in the PDF environment
for navigation regressions (English-only contents entries, numbered titles,
and manuals whose printed numbering includes the cover).

The [layout validation](../../audits/rules-pdf-layout-2026-10-15.md) records
page counts, contents-link checks and visual review.
