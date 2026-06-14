"""Tests for Regulations Review Committee PDF/HTML document parsing."""

from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.regulations_review_committee.pdf_parser import (
    extract_proceeding_text,
    extract_proceeding_metadata,
    extract_agenda_items,
    extract_committee_members,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()
_SAMPLE = TEST_TMP / "sample_proceeding.pdf"

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

_PROCEEDING_TEXT = (
    "Regulations Review Committee\n"
    "Meeting Date: 15 March 2024\n"
    "Present: Hon John Smith (Chair), Dr Jane Doe, Mr Bob Brown\n"
    "\n"
    "Agenda:\n"
    "1. Review of Subordinate Legislation (2024/01)\n"
    "2. Complaint re: ABC Regulations (Complaint 2023/42)\n"
    "3. Regulatory Standards - Proposed Amendments\n"
    "\n"
    "The committee considered complaint 2023/42 regarding the ABC Regulations 2023.\n"
    "The regulation reference is SR 2023/150.\n"
)


def setUpModule():
    _SAMPLE.write_bytes(_MINIMAL_PDF)


def tearDownModule():
    _SAMPLE.unlink(missing_ok=True)



class ExtractProceedingTextTest(unittest.TestCase):

    def test_extract_text_from_valid_pdf(self):
        text = extract_proceeding_text(_SAMPLE)
        self.assertIsInstance(text, str)
        self.assertIn("Hello World", text)

    def test_extract_text_returns_empty_for_missing_file(self):
        text = extract_proceeding_text(TEST_TMP / "nonexistent.pdf")
        self.assertEqual(text, "")

    def test_extract_text_handles_empty_pdf(self):
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
            text = extract_proceeding_text(empty)
            self.assertEqual(text, "")
        finally:
            empty.unlink(missing_ok=True)

    def test_extract_text_with_hash(self):
        result = extract_proceeding_text(_SAMPLE, compute_hash=True)
        self.assertIsInstance(result, dict)
        self.assertIn("Hello World", result["text"])
        expected = hashlib.sha256(result["text"].encode("utf-8")).hexdigest()
        self.assertEqual(result["sha256"], expected)


class ExtractProceedingMetadataTest(unittest.TestCase):

    def test_extract_metadata_from_pdf(self):
        meta = extract_proceeding_metadata(_SAMPLE)
        self.assertIsInstance(meta, dict)
        self.assertIn("page_count", meta)
        self.assertGreaterEqual(meta["page_count"], 1)

    def test_extract_metadata_for_missing_file(self):
        meta = extract_proceeding_metadata(TEST_TMP / "missing_meta.pdf")
        self.assertEqual(meta, {"page_count": 0, "error": "file_not_found"})


class ExtractAgendaItemsTest(unittest.TestCase):

    def test_extract_agenda_items_from_text(self):
        items = extract_agenda_items(_PROCEEDING_TEXT)
        self.assertGreaterEqual(len(items), 3)
        self.assertTrue(any("Review of Subordinate Legislation" in i for i in items))
        self.assertTrue(any("Complaint re: ABC Regulations" in i for i in items))

    def test_extract_agenda_items_empty_text(self):
        self.assertEqual(extract_agenda_items(""), [])

    def test_extract_agenda_items_no_agenda(self):
        text = "This is just a narrative with no agenda section."
        self.assertEqual(extract_agenda_items(text), [])


class ExtractCommitteeMembersTest(unittest.TestCase):

    def test_extract_members_from_text(self):
        members = extract_committee_members(_PROCEEDING_TEXT)
        self.assertGreaterEqual(len(members), 3)
        self.assertIn("Hon John Smith", members)

    def test_extract_members_empty_text(self):
        self.assertEqual(extract_committee_members(""), [])

    def test_extract_members_no_members_found(self):
        text = "Meeting considered various regulations."
        self.assertEqual(extract_committee_members(text), [])

    def test_extract_members_variant_formats(self):
        text = "Members Present: Alice, Bob, Charlie\n"
        members = extract_committee_members(text)
        self.assertGreaterEqual(len(members), 1)


if __name__ == "__main__":
    unittest.main()
