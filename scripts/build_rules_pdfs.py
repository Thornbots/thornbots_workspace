#!/usr/bin/env python3
"""Replace source PDF text in place, preserving page geometry and navigation."""

import argparse
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pymupdf as fitz

from rules_pdf_layout import CJK, extract_all

DOCUMENTS = (
    "rmul-rules-manual",
    "rmul-participant-manual",
    "rmuc-rules-manual",
    "rmuc-participant-manual",
    "robot-building-specifications",
    "rule-change-preview",
)


def rgb(value):
    return f"#{value:06x}"


def overlaps_x(left, right):
    return min(left.x1, right.x1) - max(left.x0, right.x0) > 10


def placement(page, unit, units, drawings, images):
    """Use existing cells or available space without crossing artwork or text."""
    box = fitz.Rect(unit["bbox"])
    if "table" in unit:
        return fitz.Rect(box.x0 + 2, box.y0 + 2, box.x1 - 2, box.y1 - 2), "left"
    if unit.get("kind") == "footer":
        return box + (-1, -1, 1, 2), "right" if box.x0 > 300 else "left"
    if re.search(r"\.{3,}", unit["text"]):
        return fitz.Rect(box.x0, box.y0 - 1, 539, box.y1 + 3), "left"
    if unit.get("kind") == "caption":
        return fitz.Rect(56.6, box.y0 - 1, 538.6, box.y1 + 4), (
            "center" if unit["text"].lstrip().startswith("图") else "left"
        )
    if unit["size"] >= 12:
        return fitz.Rect(
            56.6 if box.x0 > 200 else box.x0, box.y0 - 1, 538.6, box.y1 + 5
        ), ("center" if box.x0 > 200 else "left")
    containers = [
        d
        for d in drawings
        if d.width > 28
        and d.height > 12
        and d.x0 <= box.x0 + 3
        and d.x1 >= box.x1 - 3
        and d.y0 <= box.y0 + 3
        and d.y1 >= box.y1 - 3
        and d.width < 450
        and d.height < 210
    ]
    if containers:
        target = min(containers, key=lambda d: d.get_area())
        return fitz.Rect(
            target.x0 + 2, target.y0 + 1, target.x1 - 2, target.y1 - 1
        ), "center"
    right = 538.6 if box.x0 < 140 else min(539, box.x1 + 8)
    neighbors = [
        other["bbox"][0] - 3
        for other in units
        if other["id"] != unit["id"]
        and abs(other["bbox"][1] - box.y0) < 3
        and other["bbox"][0] >= box.x1 - 1
    ]
    if neighbors:
        right = min(right, min(neighbors))
    target = fitz.Rect(box.x0, box.y0 - 1, right, box.y1 + 5)
    below = [
        fitz.Rect(other["bbox"]).y0
        for other in units
        if other["id"] != unit["id"]
        and fitz.Rect(other["bbox"]).y0 >= box.y1 - 1
        and overlaps_x(target, fitz.Rect(other["bbox"]))
    ]
    below += [
        image.y0
        for image in images
        if image.y0 >= box.y1 - 1 and overlaps_x(target, image)
    ]
    limit = min(below + [765]) - 2
    if limit > target.y1:
        target.y1 = min(limit, box.y1 + max(8, unit["size"] * 0.8))
    return target, "left"


def english_markup(text):
    text = re.sub(r"[（(][^()（）]*[\u3400-\u9fff][^()（）]*[)）]", "", text)
    text = re.sub(r"(?<=[0-9A-Za-z)])\*(?=[0-9A-Za-z(])", " × ", text)
    text = re.sub(r"(?<=\S) - (?=[A-Z])", "\n• ", text)
    return html.escape(text).replace("\n", "<br>")


def draw_text(page, box, text, size, color, align, bold=False):
    family = "sans-serif" if bold else "serif"
    css = (
        f"* {{ margin:0; padding:0; }} body {{ font-family:{family}; "
        f"font-size:{size}pt; line-height:1.1; color:{rgb(color)}; "
        f"text-align:{align}; font-weight:{'bold' if bold else 'normal'}; }}"
    )
    rotation = 90 if box.width < 28 and box.height > 27 else 0
    spare, scale = page.insert_htmlbox(
        box, english_markup(text), css=css, scale_low=0.4, rotate=rotation
    )
    if spare < 0:
        raise ValueError(f"Cannot fit English into {box}: {text[:100]}")
    return scale


def toc_key(text):
    text = re.split(r"\.{3,}", text)[0].strip()
    if match := re.match(r"^(\d+)3V3", text):
        return match[1]
    match = re.match(r"([图表]?\s*\d+(?:[.\-]\d+)*)", text)
    return re.sub(r"\s+", "", match[1] if match else text)


def draw_contents_entry(page, box, english, source, size, color):
    number = re.search(r"(\d+)\s*$", source)
    label = re.sub(r"[.\s]*\d+\s*$", "", english).strip() if number else english
    original_size = size
    size = min(size, 10.56)
    font = fitz.Font("tiro")
    while font.text_length(label, fontsize=size) > box.width - 30 and size > 7:
        size -= 0.2
    value = number[1] if number else ""
    baseline = box.y0 + size
    ink = tuple(((color >> shift) & 255) / 255 for shift in (16, 8, 0))
    page.insert_text(
        (box.x0, baseline), label, fontname="tiro", fontsize=size, color=ink
    )
    width = font.text_length(value, fontsize=size)
    page.insert_text(
        (box.x1 - width, baseline), value, fontname="tiro", fontsize=size, color=ink
    )
    start = box.x0 + font.text_length(label, fontsize=size) + 5
    end = box.x1 - width - 5
    if end > start:
        page.draw_line(
            (start, baseline - 2),
            (end, baseline - 2),
            color=ink,
            width=0.5,
            dashes="[1 2] 0",
        )
    return size / original_size


def draw_cover(page, name):
    participant = "participant" in name
    shift = -15 if name == "rmul-participant-manual" else 0
    # Keep the original cover artwork, logo and version banner.
    bands = [
        (248, 567 + shift, 574, 594 + shift),
        (295, 623 + shift, 574, 657 + shift),
        (
            220 if name.startswith("robot") else 260,
            (650 if name.startswith("robot") else 660) + shift,
            574,
            713 + shift,
        ),
        (420, 713 + shift, 574, 765 + shift),
    ]
    for band in bands:
        page.draw_rect(fitz.Rect(band), color=None, fill=(1, 1, 1))
    draw_text(
        page,
        fitz.Rect(bands[0]),
        "26th National University Student Robot Competition",
        12,
        0x58595B,
        "right",
        True,
    )
    league = (
        "University League"
        if name.startswith("rmul")
        else "University Championship"
        if name.startswith("rmuc")
        else "University Series"
    )
    draw_text(
        page, fitz.Rect(bands[1]), "RoboMaster " + league, 16, 0x58595B, "right", True
    )
    title = (
        "Participant Manual"
        if participant
        else "Robot Building Specifications Manual"
        if name.startswith("robot")
        else "Rule-Change Preview Manual"
        if name.startswith("rule-change")
        else "Competition Rules Manual"
    )
    draw_text(
        page,
        fitz.Rect(bands[2]),
        title,
        24,
        0x00AFD7 if participant else 0x58595B,
        "right",
        True,
    )
    draw_text(
        page,
        fitz.Rect(420, 716 + shift, 574, 738 + shift),
        "Compiled by the RoboMaster Organizing Committee",
        8,
        0x888888,
        "right",
    )
    draw_text(
        page,
        fitz.Rect(420, 744 + shift, 574, 764 + shift),
        "Published "
        + ("September" if name.startswith("rule-change") else "October")
        + " 2026",
        9,
        0x888888,
        "right",
    )


def replace_pyramid(page, root, name, physical_page):
    expected = {"rmul-rules-manual": 10, "rmuc-rules-manual": 13}
    if expected.get(name) != physical_page:
        return
    images = [
        r
        for image in page.get_images()
        for r in page.get_image_rects(image[0])
        if r.y0 > 150 and r.width > 200 and r.height > 100
    ]
    if len(images) != 1:
        raise ValueError(f"{name}: cannot identify talent-development pyramid")
    svg = root / "figures" / "english" / f"{name}-figure-1-1.svg"
    tree = ET.fromstring(svg.read_text())

    def inherit_text(element, inherited):
        attributes = {**inherited, **element.attrib}
        if element.tag.endswith("}text"):
            for key in (
                "text-anchor",
                "font-family",
                "font-size",
                "font-weight",
                "fill",
            ):
                if key in attributes:
                    element.set(key, attributes[key])
        for child in element:
            inherit_text(child, attributes)

    inherit_text(tree, {})
    art = fitz.open("svg", ET.tostring(tree))
    replacement = fitz.open("pdf", art.convert_to_pdf())
    page.draw_rect(images[0], color=None, fill=(1, 1, 1))
    page.show_pdf_page(images[0], replacement, 0)
    replacement.close()
    art.close()


def legend_rows(page, units, overrides):
    """Keep numbered figure keys in their source columns as English wraps."""
    markers = []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            chars = [c for span in line["spans"] for c in span["chars"]]
            text = "".join(c["c"] for c in chars)
            for match in re.finditer(r"\[(\d+)\]", text):
                char = chars[match.start()]
                markers.append((char["bbox"][0], char["bbox"][1], match[1]))
    rows = []
    for y in sorted({round(marker[1], 1) for marker in markers}):
        row_markers = sorted([m for m in markers if abs(m[1] - y) < 0.2])
        if len(row_markers) < 2:
            continue
        row = sorted(
            [
                u
                for u in units
                if abs(u["bbox"][1] - y) < 3
                and "table" not in u
                and u["bbox"][3] - u["bbox"][1] < 16
            ],
            key=lambda u: u["bbox"][0],
        )
        if not row or not any(CJK.search(u["text"]) for u in row):
            continue
        text = " ".join(overrides.get(u["id"], u["en"]) or "" for u in row)
        entries = dict(re.findall(r"\[(\d+)\](.*?)(?=\[\d+\]|$)", text))
        if any(m[2] not in entries for m in row_markers):
            continue
        below = [u["bbox"][1] for u in units if u["bbox"][1] > y + 8]
        bottom = min(min(below or [y + 32]) - 2, y + 30)
        rows.append(
            (
                row,
                [
                    (
                        fitz.Rect(
                            x,
                            y - 1,
                            row_markers[i + 1][0] - 6
                            if i + 1 < len(row_markers)
                            else 538.6,
                            bottom,
                        ),
                        f"[{number}] " + entries[number].strip(),
                    )
                    for i, (x, _, number) in enumerate(row_markers)
                ],
            )
        )
    return rows


def render_document(root, name, pages, output_dir, allow_missing):
    source = root / "source" / f"{name}-zh.pdf"
    overrides = json.loads((root / "layout" / f"{name}.json").read_text())
    missing = [
        u["id"]
        for p in pages
        for u in p["units"]
        if u["en"] is None and not overrides.get(u["id"])
    ]
    if missing and not allow_missing:
        raise ValueError(f"{name}: {len(missing)} missing text regions: {missing[:8]}")
    document = fitz.open(source)
    report = {
        "document": name,
        "source_pages": len(document),
        "missing": missing,
        "regions": [],
        "contents_links": [],
    }
    anchors = {}
    anchor_texts = {}
    outlines = []
    for p in pages:
        for unit in p["units"]:
            if not re.search(r"\.{3,}", unit["text"]) and (
                unit["size"] >= 12
                or unit.get("kind") in ("heading", "caption")
                or re.match(r"^[图表]\s*\d+-\d+", unit["text"])
            ):
                anchors.setdefault(
                    toc_key(unit["text"]), (p["page"] - 1, unit["bbox"][1])
                )
                anchor_texts.setdefault(
                    toc_key(unit["text"]),
                    overrides.get(unit["id"], unit["en"]) or unit["text"],
                )
    labels = {
        int(u["en"]): p["page"] - 1
        for p in pages
        for u in p["units"]
        if u.get("kind") == "footer" and u["en"].isdigit()
    }
    for item in pages:
        page = document[item["page"] - 1]
        drawings = [fitz.Rect(d["rect"]) for d in page.get_drawings()]
        images = [
            rect
            for image in page.get_images()
            for rect in page.get_image_rects(image[0])
            if rect.y0 > 65
        ]
        targets = []
        legends = legend_rows(page, item["units"], overrides)
        legend_ids = {u["id"] for row, entries in legends for u in row}
        for row, entries in legends:
            for u in row:
                page.add_redact_annot(
                    fitz.Rect(u["bbox"]) + (-0.2, -0.2, 0.2, 0.2), fill=False
                )
        for unit in item["units"]:
            if unit["id"] in legend_ids:
                continue
            if not CJK.search(unit["text"]) and not re.search(r"\.{3,}", unit["text"]):
                continue
            if item["page"] == 1 and unit.get("kind") != "footer":
                page.add_redact_annot(fitz.Rect(unit["bbox"]), fill=False)
                continue
            english = overrides.get(unit["id"], unit["en"])
            if english is None:
                continue
            targets.append((unit, english))
            page.add_redact_annot(
                fitz.Rect(unit["bbox"]) + (-0.2, -0.2, 0.2, 0.2),
                fill=(1, 1, 1) if "-x" in unit["id"] else False,
            )
        page.apply_redactions(images=0, graphics=0)
        for link in page.get_links():
            if link["kind"] == fitz.LINK_GOTO:
                page.delete_link(link)
        for row, entries in legends:
            for box, text in entries:
                scale = draw_text(page, box, text, 10.56, row[0]["color"], "left")
                report["regions"].append(
                    {
                        "id": row[0]["id"],
                        "region_ids": [u["id"] for u in row],
                        "box": list(box),
                        "font_size": 10.56 * scale,
                        "scale": scale,
                    }
                )
        grouped = {}
        for unit, english in targets:
            box, align = placement(page, unit, item["units"], drawings, images)
            key = tuple(round(v, 2) for v in box)
            if key in grouped:
                grouped[key][1] += "\n" + english
                grouped[key][4].append(unit["id"])
            else:
                grouped[key] = [unit, english, box, align, [unit["id"]]]
        for unit, english, box, align, region_ids in grouped.values():
            if "-x" in unit["id"]:
                page.draw_rect(fitz.Rect(unit["bbox"]), color=None, fill=(1, 1, 1))
            contents = bool(re.search(r"\.{3,}", unit["text"]))
            if contents:
                canonical = anchor_texts.get(toc_key(unit["text"]))
                if canonical and not CJK.search(canonical):
                    english = canonical + " " + re.search(r"(\d+)\s*$", unit["text"])[1]
                scale = draw_contents_entry(
                    page, box, english, unit["text"], unit["size"], unit["color"]
                )
                destination = anchors.get(toc_key(unit["text"]))
                if destination is None:
                    number = re.search(r"(\d+)\s*$", unit["text"])
                    destination = (
                        (labels[int(number[1])], 70)
                        if number and int(number[1]) in labels
                        else None
                    )
                if destination and 0 <= destination[0] < len(document):
                    page.insert_link(
                        {
                            "kind": fitz.LINK_GOTO,
                            "from": box,
                            "page": destination[0],
                            "to": fitz.Point(0, max(0, destination[1] - 10)),
                        }
                    )
                    report["contents_links"].append(
                        {
                            "region": unit["id"],
                            "page": destination[0] + 1,
                            "key": toc_key(unit["text"]),
                            "source_page": item["page"],
                            "label": re.sub(r"[.\s]*\d+\s*$", "", english).strip(),
                        }
                    )
                else:
                    raise ValueError(
                        f"Contents destination missing: {name} {unit['id']}"
                    )
                key = toc_key(unit["text"])
                if not key.startswith(("图", "表")):
                    level = min(3, key.count(".") + 1) if key[0].isdigit() else 1
                    if outlines:
                        level = min(level, outlines[-1][0] + 1)
                    else:
                        level = 1
                    outlines.append(
                        [
                            level,
                            report["contents_links"][-1]["label"],
                            destination[0] + 1,
                        ]
                    )
            else:
                scale = draw_text(
                    page,
                    box,
                    english,
                    unit["size"],
                    unit["color"],
                    align,
                    bold=unit["size"] >= 12,
                )
            report["regions"].append(
                {
                    "id": unit["id"],
                    "region_ids": region_ids,
                    "box": list(box),
                    "font_size": unit["size"] * scale,
                    "scale": scale,
                }
            )
        if item["page"] == 1:
            draw_cover(page, name)
        replace_pyramid(page, root, name, item["page"])
    title = (root / f"{name}.md").read_text().splitlines()[0].removeprefix("# ")
    document.set_toc(outlines)
    document.set_metadata({**document.metadata, "title": title + " — English"})
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{name}-en.pdf"
    temporary = output.with_suffix(".tmp.pdf")
    try:
        document.save(temporary, garbage=4, deflate=True)
        report["output_pages"] = len(document)
        temporary.replace(output)
    finally:
        document.close()
        temporary.unlink(missing_ok=True)
    print(
        f"{output.name}: {len(pages)} pages, {len(report['contents_links'])} contents links, "
        f"{len(missing)} missing regions"
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("documents", nargs="*", choices=DOCUMENTS)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "docs/rules/rm2027",
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()
    if args.allow_missing and not args.output_dir:
        parser.error("--allow-missing requires an explicit temporary --output-dir")
    data = extract_all(args.root)
    reports = [
        render_document(
            args.root,
            name,
            data[name],
            args.output_dir or args.root / "pdf",
            args.allow_missing,
        )
        for name in args.documents or DOCUMENTS
    ]
    if args.report:
        args.report.write_text(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
