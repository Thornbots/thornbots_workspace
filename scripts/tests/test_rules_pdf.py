"""Regression checks for PDF contents links and source-page preservation."""

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

import pymupdf as fitz

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_rules_pdfs import render_document, toc_key


class NavigationTests(unittest.TestCase):
    def build(self, source_label, english_label, heading, printed_page):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        (root / "source").mkdir()
        (root / "layout").mkdir()
        (root / "fixture.md").write_text("# Fixture\n")
        (root / "layout/fixture.json").write_text(json.dumps({}))
        source = root / "source/fixture-zh.pdf"
        doc = fitz.open()
        for text in ("Cover", source_label, heading):
            page = doc.new_page()
            page.insert_text((60, 112), text, fontname="china-s", fontsize=10)
        doc.save(source)
        doc.close()
        original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        pages = [
            {
                "page": 2,
                "units": [
                    {
                        "id": "p002-u000",
                        "text": source_label,
                        "en": english_label,
                        "bbox": [60, 100, 539, 116],
                        "size": 10,
                        "color": 0,
                    }
                ],
            },
            {
                "page": 3,
                "units": [
                    {
                        "id": "p003-u000",
                        "text": heading,
                        "en": heading,
                        "bbox": [60, 100, 300, 116],
                        "size": 16,
                        "color": 0,
                    },
                    {
                        "id": "p003-u001",
                        "text": str(printed_page),
                        "en": str(printed_page),
                        "kind": "footer",
                        "bbox": [60, 780, 80, 792],
                        "size": 10,
                        "color": 0,
                    },
                ],
            },
        ]
        pages.insert(0, {"page": 1, "units": []})
        report = render_document(root, "fixture", pages, root / "out", False)
        with fitz.open(root / "out/fixture-en.pdf") as result:
            self.assertEqual(len(result), 3)
            links = result[1].get_links()
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0]["page"], 2)
            self.assertEqual(report["contents_links"][0]["page"], 3)
            self.assertTrue(result.get_toc())
            self.assertEqual(result[0].rect, fitz.Rect(0, 0, 595, 842))
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), original_hash)
        self.assertFalse(list((root / "out").glob("*.tmp.pdf")))

    def test_numbers_in_titles_do_not_change_figure_or_section_ids(self):
        self.assertEqual(toc_key("图 3-1 3V3 场地 ........ 22"), "图3-1")
        self.assertEqual(toc_key("图 3-13 功率检测 ........ 33"), "图3-13")
        self.assertEqual(toc_key("3 3V3 对抗赛 ........ 16"), "3")
        self.assertEqual(toc_key("33V3 对抗赛"), "3")

    def test_already_english_contents_entry_still_gets_link(self):
        self.build(
            "5.8 RM Award ................ 1", "5.8 RM Award 1", "5.8 RM Award", 1
        )

    def test_printed_page_fallback_does_not_assume_cover_offset(self):
        self.build(
            "声明 ................ 3",
            "Statement 3",
            "Intellectual Property Statement",
            3,
        )


if __name__ == "__main__":
    unittest.main()
