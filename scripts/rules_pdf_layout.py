"""Identify source PDF text regions without moving artwork or table rules."""

from pathlib import Path
import re
import pymupdf
from bs4 import BeautifulSoup
import markdown

pymupdf.TOOLS.set_small_glyph_heights(True)
CJK = re.compile(r"[\u3400-\u9fff]")


def extract(name, root):
    ROOT = Path(root)
    doc = pymupdf.open(ROOT / "source" / f"{name}-zh.pdf")
    md = (ROOT / f"{name}.md").read_text()
    pages = re.split(r"<!-- p\.(\d+) -->", md)
    refs = {int(pages[i]): pages[i + 1] for i in range(1, len(pages), 2)}
    headings = {
        m[1]: m[1] + " " + m[2]
        for m in re.finditer(r"^#+ (\d+(?:\.\d+)*) (.+)$", md, re.M)
    }
    captions = {}
    for m in re.finditer(r"^\*{1,2}(Table|Figure) ([\d-]+) (.+?)\*{1,2}$", md, re.M):
        captions.setdefault((m[1], m[2]), m[1] + " " + m[2] + " " + m[3])
    front = {
        "知识产权声明": "Intellectual Property Statement",
        "阅读提示": "Reading Notes",
        "版本号说明": "Version Number Description",
        "场地图纸图例说明": "Field Drawing Legend",
        "修改日志": "Revision Log",
        "目录": "Contents",
        "表目录": "List of Tables",
        "图目录": "List of Figures",
        "预检录": "Pre-Inspection",
        "场地道具训练": "Field Prop Training",
        "适应性训练": "Adaptation Training",
        "附录1 赛前流程说明": "Appendix 1 Pre-Match Procedure Description",
        "附录2 未来规则规划": "Appendix 2 Future Rules Planning",
        "附录 赛前流程说明": "Appendix Pre-Match Procedure Description",
    }
    output = []
    for pi, page in enumerate(doc, 1):
        raw = []
        for b in page.get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                spans = [s for s in line["spans"] if s["text"].strip()]
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans).strip()
                bbox = pymupdf.Rect(line["bbox"])
                raw.append(
                    {
                        "text": text,
                        "bbox": list(bbox),
                        "size": max(s["size"] for s in spans),
                        "color": max(spans, key=lambda s: len(s["text"]))["color"],
                        "origin": list(spans[0]["origin"]),
                        "block": b["number"],
                    }
                )
        tables = []
        for t in page.find_tables().tables:
            r = pymupdf.Rect(t.bbox)
            if (
                r.width < 120
                or r.height < 30
                or t.row_count < 2
                or r.y0 < 65
                or r.y1 > 766
            ):
                continue
            rows = []
            data = t.extract()
            for ri, row in enumerate(t.rows):
                cells = []
                for ci, cell in enumerate(row.cells):
                    val = data[ri][ci]
                    if cell and val and val.strip():
                        cells.append(
                            {
                                "text": val.strip(),
                                "bbox": list(cell),
                                "size": 10.56,
                                "color": 0,
                                "table": len(tables),
                                "row": ri,
                                "col": ci,
                            }
                        )
                if cells:
                    rows.append(cells)
            tables.append({"bbox": list(r), "rows": rows})
        units = []
        for tab in tables:
            for row in tab["rows"]:
                units.extend(row)
        unmatched = []
        for line in raw:
            center = pymupdf.Point(
                (line["bbox"][0] + line["bbox"][2]) / 2,
                (line["bbox"][1] + line["bbox"][3]) / 2,
            )
            if any(pymupdf.Rect(t["bbox"]).contains(center) for t in tables):
                continue
            unmatched.append(line)
        groups = []
        for line in unmatched:
            if groups:
                last = groups[-1]
                lr = pymupdf.Rect(last["bbox"])
                r = pymupdf.Rect(line["bbox"])
                if (
                    abs(last["size"] - line["size"]) < 0.3
                    and line["color"] == last["color"]
                    and last["size"] < 12
                    and abs(r.x0 - lr.x0) < 30
                    and 8 < line["origin"][1] - last["last_origin"][1] < 23
                    and not re.search(r"[。；：！？.!?:;]$", last["text"])
                    and not re.match(
                        r"^(?:[\uf06c•]|R\d+\b|\d+[\.、]|\[\d+\])", line["text"]
                    )
                    and last["bbox"][3] < 766
                ):
                    last["text"] += line["text"]
                    last["bbox"] = list(lr | r)
                    last["last_origin"] = line["origin"]
                    continue
            line = dict(line)
            line["last_origin"] = line["origin"]
            groups.append(line)
        for g in groups:
            units.append(g)
        units.sort(key=lambda u: (round(u["bbox"][1], 1), u["bbox"][0]))
        for ui, u in enumerate(units):
            u["id"] = f"p{pi:03d}-u{ui:03d}"
            u["en"] = None
            text = u["text"]
            clean = " ".join(text.split())
            if not CJK.search(text):
                u["en"] = text
            elif u["bbox"][1] > 765:
                numbers = re.findall(r"\d+", text)
                u["en"] = numbers[-1] if text.startswith("©") else numbers[0]
                u["kind"] = "footer"
            elif clean in front:
                u["en"] = front[clean]
                u["kind"] = "heading"
            elif (
                (m := re.match(r"^(\d+(?:\.\d+)*)(?=[\u3400-\u9fff\s])\s*(.+)$", clean))
                and m[1] in headings
                and (u["size"] >= 12 or re.search(r"\.{3,}", clean))
            ):
                u["en"] = headings[m[1]]
                u["kind"] = "heading"
                if re.search(r"\.{3,}", clean):
                    u["en"] += " " + re.search(r"(\d+)\s*$", clean)[1]
                    u["kind"] = "toc"
            elif m := re.match(r"^(图|表)\s*(\d+-\d+)\s*(.+)$", clean):
                key = ("Figure" if m[1] == "图" else "Table", m[2])
                if key in captions:
                    u["en"] = captions[key]
                    u["kind"] = "caption"
                    if re.search(r"\.{3,}", clean):
                        u["en"] += " " + re.search(r"(\d+)\s*$", clean)[1]
                        u["kind"] = "toc"
        # Match intact table rows with checked English table rows where unambiguous.
        reference = re.sub(
            r"(?<=[0-9A-Za-z)])\*(?=[0-9A-Za-z(])", " × ", refs.get(pi, "")
        )
        soup = BeautifulSoup(
            markdown.markdown(reference, extensions=["tables"]), "html.parser"
        )
        engtables = soup.find_all("table")
        if len(engtables) == len(tables):
            for tab, eng in zip(tables, engtables):
                erows = [
                    [
                        c.get_text(" ", strip=True)
                        for c in r.find_all(["td", "th"], recursive=False)
                    ]
                    for r in eng.find_all("tr")
                ]
                if len(erows) != len(tab["rows"]):
                    continue
                for sr, er in zip(tab["rows"], erows):
                    if len(sr) != len(er):
                        continue
                    for su, en in zip(sr, er):
                        if CJK.search(su["text"]) and en:
                            su["en"] = en
                            su["auto_table"] = True
        # Some source tables have missing border segments: find_tables omits cells.
        # Append separate IDs so recovered text never renumbers the maintained maps.
        extras = []
        for line in raw:
            r = pymupdf.Rect(line["bbox"])
            center = (r.tl + r.br) / 2
            if (
                not CJK.search(line["text"])
                or not any(pymupdf.Rect(t["bbox"]).contains(center) for t in tables)
                or any(pymupdf.Rect(u["bbox"]).contains(center) for u in units)
            ):
                continue
            extra = dict(line)
            extra.update(id=f"p{pi:03d}-x{len(extras):03d}", en=None)
            for tab in tables:
                if not pymupdf.Rect(tab["bbox"]).contains(center):
                    continue
                columns = [
                    pymupdf.Rect(c["bbox"])
                    for row in tab["rows"]
                    for c in row
                    if c["bbox"][0] <= center.x <= c["bbox"][2]
                ]
                if columns:
                    col = min(columns, key=lambda c: abs(c.y0 - r.y0))
                    extra.update(bbox=[col.x0, r.y0 - 10, col.x1, r.y1 + 6], table=-1)
            if (
                extras
                and abs(extra["bbox"][0] - extras[-1]["bbox"][0]) < 3
                and 0 < extra["origin"][1] - extras[-1]["origin"][1] < 27
            ):
                previous = extras[-1]
                previous["text"] += " " + extra["text"]
                previous["bbox"] = list(
                    pymupdf.Rect(previous["bbox"]) | pymupdf.Rect(extra["bbox"])
                )
                previous["origin"] = extra["origin"]
            else:
                extras.append(extra)
        units.extend(extras)
        output.append({"page": pi, "reference": refs.get(pi, ""), "units": units})
    doc.close()
    return output


def extract_all(root):
    import collections

    data = {
        p.stem: extract(p.stem, root)
        for p in Path(root).glob("*.md")
        if p.name != "README.md"
    }
    cache = collections.defaultdict(set)
    for pages in data.values():
        for page in pages:
            for unit in page["units"]:
                if (
                    unit["en"]
                    and unit.get("kind") not in ["toc", "footer"]
                    and CJK.search(unit["text"])
                ):
                    cache[re.sub(r"\s+", "", unit["text"])].add(unit["en"])
    for pages in data.values():
        for page in pages:
            for unit in page["units"]:
                if unit["en"] is None:
                    values = cache.get(re.sub(r"\s+", "", unit["text"]), set())
                    if len(values) == 1:
                        unit["en"] = next(iter(values))
                        unit["cached"] = True
    return data
