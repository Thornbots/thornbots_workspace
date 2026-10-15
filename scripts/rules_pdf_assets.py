"""Extract original figure artwork from the Chinese RoboMaster PDFs."""

from __future__ import annotations

import re
from pathlib import Path

import pymupdf as fitz


_CAPTION = re.compile(r"^图\s*(\d+)\s*[-－]\s*(\d+)(?:\s|$)")
_BODY_TOP = 65
_BODY_BOTTOM = 765
_MIN_WIDTH = 45
_MIN_HEIGHT = 25
_DPI = 180


def _captions(page: fitz.Page) -> list[tuple[float, float, str]]:
    found = []
    for block in page.get_text("blocks"):
        _, y0, _, y1, raw = block[:5]
        text = " ".join(raw.split())
        if re.search(r"(?:\.{3,}|…{2,})", text):
            continue
        match = _CAPTION.match(text)
        if match and y0 >= _BODY_TOP and y0 < _BODY_BOTTOM:
            found.append((y0, y1, f"Figure {match[1]}-{match[2]}"))
    return sorted(found)


def _image_rectangles(page: fitz.Page) -> list[fitz.Rect]:
    rectangles = {}
    for image in page.get_images(full=True):
        for rect in page.get_image_rects(image[0]):
            if (
                rect.width > _MIN_WIDTH
                and rect.height > _MIN_HEIGHT
                and rect.y0 >= _BODY_TOP
                and rect.y1 <= _BODY_BOTTOM
            ):
                key = tuple(round(value, 2) for value in rect)
                rectangles[key] = rect
    return sorted(rectangles.values(), key=lambda rect: (rect.y0, rect.x0))


def extract_figures(source_pdf: Path, output_dir: Path) -> dict[str, list[Path]]:
    """Render embedded artwork between each figure caption and the prior caption."""
    source_pdf = Path(source_pdf)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    figures: dict[str, list[Path]] = {}
    document = fitz.open(source_pdf)
    scale = _DPI / 72
    matrix = fitz.Matrix(scale, scale)

    for page in document:
        captions = _captions(page)
        if not captions:
            continue
        images = _image_rectangles(page)
        previous_caption_bottom = _BODY_TOP
        for top, bottom, name in captions:
            paths = figures.setdefault(name, [])
            candidates = [
                rect
                for rect in images
                if rect.y0 >= previous_caption_bottom and rect.y1 <= top
            ]
            for rect in candidates:
                occurrence = len(paths) + 1
                safe_name = name.lower().replace(" ", "_")
                path = output_dir / f"{safe_name}_{occurrence:02d}.png"
                pixmap = page.get_pixmap(matrix=matrix, clip=rect, alpha=False)
                pixmap.save(path)
                paths.append(path)
            previous_caption_bottom = bottom

    document.close()
    return figures
