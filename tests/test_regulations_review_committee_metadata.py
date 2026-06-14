"""Tests for metadata extraction from Regulations Review Committee proceedings."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.regulations_review_committee.metadata import (
    extract_meeting_date,
    extract_agenda_items,
    extract_committee_members,
    extract_complaint_subjects,
    extract_regulation_references,
    extract_all_metadata,
    ProceedingMetadata,
)

_SAMPLE_TEXT = (
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


class ExtractMeetingDateTest(unittest.TestCase):

    def test_extracts_iso_date(self):
        text = "Meeting Date: 2024-03-15\n"
        date = extract_meeting_date(text)
        self.assertEqual(date, "2024-03-15")

    def test_extracts_nz_date_format(self):
        date = extract_meeting_date(_SAMPLE_TEXT)
        self.assertIsNotNone(date)
        self.assertEqual(date, "2024-03-15")

    def test_extracts_date_variant(self):
        text = "Date of meeting: 15/03/2024\n"
        date = extract_meeting_date(text)
        self.assertIsNotNone(date)
        self.assertEqual(date, "2024-03-15")

    def test_returns_none_when_no_date(self):
        text = "Meeting minutes without any date..."
        self.assertIsNone(extract_meeting_date(text))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_meeting_date(""))


class ExtractAgendaItemsTest(unittest.TestCase):

    def test_extracts_agenda_items(self):
        items = extract_agenda_items(_SAMPLE_TEXT)
        self.assertGreaterEqual(len(items), 3)
        self.assertTrue(any("Review of Subordinate Legislation" in i for i in items))
        self.assertTrue(any("Complaint re: ABC Regulations" in i for i in items))

    def test_extracts_empty_when_no_agenda(self):
        items = extract_agenda_items("")
        self.assertEqual(items, [])

    def test_extracts_agenda_numbered_variants(self):
        text = "Agenda Items:\n1) Item A\n2) Item B\n"
        items = extract_agenda_items(text)
        self.assertIn("Item A", items)
        self.assertIn("Item B", items)


class ExtractCommitteeMembersTest(unittest.TestCase):

    def test_extracts_members(self):
        members = extract_committee_members(_SAMPLE_TEXT)
        self.assertGreaterEqual(len(members), 3)
        self.assertIn("Hon John Smith", members)
        self.assertIn("Dr Jane Doe", members)

    def test_extracts_members_variant(self):
        text = "Committee Members: Alice (Chair), Bob, Charlie\n"
        members = extract_committee_members(text)
        self.assertGreaterEqual(len(members), 3)

    def test_returns_empty_when_no_members(self):
        self.assertEqual(extract_committee_members(""), [])


class ExtractComplaintSubjectsTest(unittest.TestCase):

    def test_extracts_complaint_subjects(self):
        subjects = extract_complaint_subjects(_SAMPLE_TEXT)
        self.assertGreaterEqual(len(subjects), 1)
        self.assertIn("Complaint 2023/42", subjects)

    def test_extracts_multiple_complaints(self):
        text = "Considered complaint 2024/01 and complaint 2024/02.\n"
        subjects = extract_complaint_subjects(text)
        self.assertGreaterEqual(len(subjects), 2)

    def test_returns_empty_when_no_complaints(self):
        self.assertEqual(extract_complaint_subjects(""), [])

    def test_returns_empty_text_without_complaints(self):
        text = "Meeting discussed general regulatory standards."
        self.assertEqual(extract_complaint_subjects(text), [])


class ExtractRegulationReferencesTest(unittest.TestCase):

    def test_extracts_regulation_references(self):
        refs = extract_regulation_references(_SAMPLE_TEXT)
        self.assertGreaterEqual(len(refs), 1)
        self.assertIn("SR 2023/150", refs)

    def test_extracts_multiple_references(self):
        text = "Reviewed SR 2023/100, SR 2023/101, and LI 2024/5.\n"
        refs = extract_regulation_references(text)
        self.assertGreaterEqual(len(refs), 3)

    def test_returns_empty_when_no_references(self):
        self.assertEqual(extract_regulation_references(""), [])


class ExtractAllMetadataTest(unittest.TestCase):

    def test_extract_all_returns_proceeding_metadata(self):
        meta = extract_all_metadata(_SAMPLE_TEXT)
        self.assertIsInstance(meta, ProceedingMetadata)
        self.assertEqual(meta.meeting_date, "2024-03-15")
        self.assertGreaterEqual(len(meta.agenda_items), 3)
        self.assertGreaterEqual(len(meta.committee_members), 3)
        self.assertGreaterEqual(len(meta.complaint_subjects), 1)
        self.assertGreaterEqual(len(meta.regulation_references), 1)

    def test_extract_all_with_empty_text(self):
        meta = extract_all_metadata("")
        self.assertIsInstance(meta, ProceedingMetadata)
        self.assertIsNone(meta.meeting_date)
        self.assertEqual(meta.agenda_items, [])
        self.assertEqual(meta.committee_members, [])
        self.assertEqual(meta.complaint_subjects, [])
        self.assertEqual(meta.regulation_references, [])

    def test_to_dict(self):
        meta = ProceedingMetadata(
            meeting_date="2024-03-15",
            agenda_items=["Item A"],
            committee_members=["Member X"],
            complaint_subjects=["Complaint 1"],
            regulation_references=["SR 2024/1"],
        )
        d = meta.to_dict()
        self.assertEqual(d["meeting_date"], "2024-03-15")
        self.assertIn("Item A", d["agenda_items"])


if __name__ == "__main__":
    unittest.main()

