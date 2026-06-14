"""Tests for PDF text extraction from submission documents."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.parliament_submissions.pdf_parser import extract_pdf_text, extract_pdf_metadata
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()
_SAMPLE = TEST_TMP / "sample_submission.pdf"

_MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
    b"/Resources << /Font << /F1 4 0 R >> >>\n/Contents 5 0 R >>\nendobj\n"
    b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    b"5 0 obj\n<< /Length 44 >>\nstream\n"
    b"BT /F1 12 Tf 72 700 Td (Hello World) Tj ET\n"
    b"endstream\nendobj\n"
    b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n"
    b"0000000058 00000 n \n0000000115 00000 n \n0000000266 00000 n \n"
    b"0000000357 00000 n \n"
    b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n469\n%%EOF"
)


def setUpModule():
    _SAMPLE.write_bytes(_MINIMAL_PDF)


def tearDownModule():
    _SAMPLE.unlink(missing_ok=True)


class PdfParserTest(unittest.TestCase):

    def test_extract_text_from_valid_pdf(self):
        text = extract_pdf_text(_SAMPLE)
        self.assertIsInstance(text, str)
        self.assertIn("Hello World", text)

    def test_extract_text_returns_empty_for_missing_file(self):
        text = extract_pdf_text(TEST_TMP / "nonexistent.pdf")
        self.assertEqual(text, "")

    def test_extract_text_returns_empty_for_empty_pdf(self):
        empty = TEST_TMP / "empty.pdf"
        empty.write_bytes(
            b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
            b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
            b"/Contents 4 0 R >>\nendobj\n"
            b"4 0 obj\n<< /Length 0 >>\nstream\nendstream\nendobj\n"
            b"xref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n"
            b"0000000058 00000 n \n0000000115 00000 n \n0000000202 00000 n \n"
            b"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n285\n%%EOF"
        )
        try:
            text = extract_pdf_text(empty)
            self.assertEqual(text, "")
        finally:
            empty.unlink(missing_ok=True)

    def test_extract_text_handles_multiline_content(self):
        ml = TEST_TMP / "multiline.pdf"
        content = (b"BT /F1 12 Tf 72 700 Td (Line one) Tj\n"
                   b"0 -14 Td (Line two) Tj\n0 -14 Td (Line three) Tj ET")
        ml.write_bytes(_make_pdf(content))
        try:
            text = extract_pdf_text(ml)
            for s in ("Line one", "Line two", "Line three"):
                self.assertIn(s, text)
        finally:
            ml.unlink(missing_ok=True)

    def test_extract_pdf_metadata_returns_dict(self):
        meta = extract_pdf_metadata(_SAMPLE)
        self.assertIsInstance(meta, dict)
        self.assertIn("page_count", meta)
        self.assertGreaterEqual(meta["page_count"], 1)

    def test_extract_pdf_metadata_for_missing_file(self):
        meta = extract_pdf_metadata(TEST_TMP / "missing_meta.pdf")
        self.assertEqual(meta, {"page_count": 0, "error": "file_not_found"})

    def test_extract_text_preserves_unicode_characters(self):
        uni = TEST_TMP / "unicode.pdf"
        uni.write_bytes(_make_pdf(b"BT /F1 12 Tf 72 700 Td (\x74\xC4\x81mara) Tj ET"))
        try:
            text = extract_pdf_text(uni)
            self.assertIsInstance(text, str)
            self.assertGreater(len(text.strip()), 0)
        finally:
            uni.unlink(missing_ok=True)

    def test_extract_text_with_sha256(self):
        result = extract_pdf_text(_SAMPLE, compute_hash=True)
        self.assertIsInstance(result, dict)
        self.assertIn("Hello World", result["text"])
        expected = hashlib.sha256(result["text"].encode("utf-8")).hexdigest()
        self.assertEqual(result["sha256"], expected)

    def test_extract_text_no_hash_flag(self):
        text = extract_pdf_text(_SAMPLE, compute_hash=False)
        self.assertIsInstance(text, str)


def _make_pdf(stream_content: bytes) -> bytes:
    length = len(stream_content)
    offset = 357 + length + 20
    return (
        b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
        b"/Resources << /Font << /F1 4 0 R >> >>\n/Contents 5 0 R >>\nendobj\n"
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"5 0 obj\n<< /Length " + str(length).encode() + b" >>\nstream\n"
        + stream_content + b"\nendstream\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n"
        b"0000000058 00000 n \n0000000115 00000 n \n0000000266 00000 n \n"
        b"0000000357 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n"
        + str(offset).encode() + b"\n%%EOF"
    )


if __name__ == "__main__":
    unittest.main()

# placeholder
