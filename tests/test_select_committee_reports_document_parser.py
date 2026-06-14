"""Tests for select committee reports multi-format document parsing."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.select_committee_reports.document_parser import (
    detect_format,
    extract_text_from_pdf,
    extract_text_from_html,
    extract_text_from_docx,
    extract_text,
    SUPPORTED_FORMATS,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class DetectFormatTest(unittest.TestCase):

    def test_detect_pdf_by_extension(self):
        self.assertEqual(detect_format("report.pdf"), "pdf")

    def test_detect_html_by_extension(self):
        self.assertEqual(detect_format("report.html"), "html")

    def test_detect_docx_by_extension(self):
        self.assertEqual(detect_format("report.docx"), "docx")

    def test_detect_unknown_extension(self):
        self.assertIsNone(detect_format("report.xyz"))

    def test_detect_no_extension(self):
        self.assertIsNone(detect_format("report"))

    def test_detect_by_content_type(self):
        self.assertEqual(detect_format("report.pdf", content_type="application/pdf"), "pdf")

    def test_detect_html_by_content_type(self):
        self.assertEqual(detect_format("report.foo", content_type="text/html"), "html")

    def test_detect_docx_by_content_type(self):
        self.assertEqual(
            detect_format("report.foo", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            "docx",
        )

    def test_supported_formats_defined(self):
        self.assertIn("pdf", SUPPORTED_FORMATS)
        self.assertIn("html", SUPPORTED_FORMATS)
        self.assertIn("docx", SUPPORTED_FORMATS)


class ExtractTextFromPdfTest(unittest.TestCase):

    def test_extract_from_missing_file(self):
        result = extract_text_from_pdf(TEST_TMP / "nonexistent.pdf")
        self.assertEqual(result, "")

    def test_extract_with_hash(self):
        result = extract_text_from_pdf(TEST_TMP / "ghost.pdf", compute_hash=True)
        self.assertIn("text", result)
        self.assertIn("sha256", result)


class ExtractTextFromHtmlTest(unittest.TestCase):

    def test_extract_from_simple_html(self):
        html = "<html><body><h1>Report Title</h1><p>Report content here.</p></body></html>"
        text = extract_text_from_html(html)
        self.assertIn("Report Title", text)
        self.assertIn("Report content here", text)

    def test_extract_from_empty_html(self):
        self.assertEqual(extract_text_from_html(""), "")

    def test_extract_strips_tags(self):
        html = "<div><p>Para <b>one</b></p><p>Para two</p></div>"
        text = extract_text_from_html(html)
        self.assertIn("Para one", text)
        self.assertIn("Para two", text)
        self.assertNotIn("<p>", text)

    def test_extract_with_line_breaks(self):
        html = "Line1<br>Line2<br/>Line3"
        text = extract_text_from_html(html)
        self.assertIn("Line1", text)
        self.assertIn("Line2", text)


class ExtractTextFromDocxTest(unittest.TestCase):

    def test_extract_from_missing_file(self):
        result = extract_text_from_docx(TEST_TMP / "nonexistent.docx")
        self.assertEqual(result, "")

    def test_extract_with_hash(self):
        result = extract_text_from_docx(TEST_TMP / "ghost.docx", compute_hash=True)
        self.assertIn("text", result)
        self.assertIn("sha256", result)


class ExtractTextIntegrationTest(unittest.TestCase):

    def test_extract_html_dispatches_correctly(self):
        html = "<html><body><p>Hello World</p></body></html>"
        text = extract_text(html, fmt="html")
        self.assertIn("Hello World", text)

    def test_extract_pdf_missing_file(self):
        text = extract_text(TEST_TMP / "missing.pdf", fmt="pdf")
        self.assertEqual(text, "")

    def test_extract_docx_missing_file(self):
        text = extract_text(TEST_TMP / "missing.docx", fmt="docx")
        self.assertEqual(text, "")

    def test_extract_unknown_format_returns_empty(self):
        text = extract_text("some content", fmt="unknown")
        self.assertEqual(text, "")


if __name__ == "__main__":
    unittest.main()
