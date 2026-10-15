# RoboMaster 2027 rules (English translation)

Unofficial English translations of the RoboMaster 2027 University League
(RMUL) and University Championship (RMUC) rule documents, released
2026-10-15. ARCC treats itself as an RMUL
event, so these are the closest published base for ARCC 2027 until ARC
releases its own rules. The [game context](../../../ARCC_2026_SENTRY_CONTEXT.md#robomaster-2027-rmul-base-rules)
summarizes the Sentry and CV deltas.

The Chinese PDFs govern. Copyright in the source documents belongs to DJI;
these translations are for team reference only.

| Translation | Source PDF | Pages | MD5 |
| --- | --- | --- | --- |
| [RMUL Rules Manual V1.0.0](rmul-rules-manual.md) | RoboMaster 2027 机甲大师高校联盟赛比赛规则手册 V1.0.0（20261015）.pdf | 68 | `d75e932a7d69dd2fa53906dfc67512be` |
| [RMUL Participant Manual V1.0.0](rmul-participant-manual.md) | RoboMaster 2027 机甲大师高校联盟赛参赛手册V1.0.0（20261015）.pdf | 28 | `b51b4a5839401dbc334531d0409b3d15` |
| [RMUC Rules Manual V1.0.0](rmuc-rules-manual.md) | RoboMaster 2027 机甲大师超级对抗赛比赛规则手册V1.0.0（20261015）.pdf | 144 | `4ff71c2945d578c444ae5b9620e43dfb` |
| [RMUC Participant Manual V1.0.0](rmuc-participant-manual.md) | RoboMaster 2027 机甲大师超级对抗赛参赛手册V1.0.0（20261015）.pdf | 37 | `5ef9fcc4938723ce3db7aed3fe4501c6` |
| [Robot Building Specifications Manual V1.0.0](robot-building-specifications.md) | RoboMaster 2027 机甲大师高校系列赛机器人制作规范手册V1.0.0（20261015）.pdf | 91 | `39175fdc1c263b10ec44727c5689c329` |
| [Rule-Change Preview](rule-change-preview.md) | RoboMaster 2027 高校系列赛规则变更前瞻手册（20260909）.pdf | 19 | `87c15791e3dbabab9dde749bc8cadf8b` |

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

- `<!-- p.N -->` marks the start of physical PDF page N; running headers,
  footers and contents pages are dropped. Table rows split across pages are
  joined on the page where the row begins.
- Rule IDs, section, table and figure numbers, values and units are copied
  as printed, including apparent source typos.
- Figures are not reproduced: each has its caption plus a list of the labels
  and dimensions it carries. Read the PDF page for geometry.
- Terms follow the [game context](../../../ARCC_2026_SENTRY_CONTEXT.md)
  (for example Infantry Robot for 步兵机器人, Bumpy Road for 起伏路段).

Translated from the extracted text and checked against a render of every
page. A second reviewer then compared every page with its render for the
RMUL manuals, the Building Specifications Manual, the preview and RMUC Rules
pp.37-54; the rest of the RMUC documents had only the translator's check.
