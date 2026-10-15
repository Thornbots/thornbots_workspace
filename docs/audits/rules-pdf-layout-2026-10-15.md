# RoboMaster English PDF layout check — 2026-10-15

The six English editions use the checked-in Chinese PDFs as page templates.
Their [translation index](../rules/rm2027/README.md) owns the source hashes,
files and generation instructions.

| Edition | Source / English physical pages | Linked contents entries |
| --- | --- | --- |
| RMUL Rules | 68 / 68 | 114 |
| RMUL Participant | 28 / 28 | 44 |
| RMUC Rules | 144 / 144 | 222 |
| RMUC Participant | 37 / 37 | 59 |
| Robot Building Specifications | 91 / 91 | 137 |
| Rule-Change Preview | 19 / 19 | 36 |
| Total | 387 / 387 | 612 |

## Validation

- Reopened the saved editions and compared every page size with its source.
  All source MD5 hashes still match the translation index.
- Counted source contents rows independently from extracted source text, then
  checked every saved PDF internal contents link: its source page, destination
  page, valid page range and English destination heading/caption. All 612
  entries resolve. This includes the already-English RM Award entry.
- No untranslated source text regions remain, and no extractable Chinese text
  remains in the English editions. Original branded artwork is retained.
- Reviewed contact sheets covering all 387 pages against the sources and
  inspected crowded tables, figure keys, covers, pyramids and flowcharts at
  full size. Corrected overlapping flowchart paragraphs and diagram legends,
  missing cells caused by incomplete source table borders, and cover fragments.
- Navigation regression tests cover English-only contents rows, digits at the
  start of titles (Figure 3-1 versus Figure 3-13, and 3V3), printed page numbers
  that include the cover, unchanged source bytes and atomic PDF publication.
- Workspace quality checks and actionlint pass. The document relocation also
  passed these checks in all nine affected package repositories. Link checks
  found only existing unavailable targets in the optional, uninitialized
  `firmware/MCBV3` submodule.

## Layout limits

English text is fitted into the source regions, with smaller fonts where
needed. Font metrics and line wrapping can differ from the Chinese edition;
physical pages, source artwork positions, table borders and content page
breaks stay fixed. The two talent-development pyramids use English vector
artwork within the source figure boxes.
