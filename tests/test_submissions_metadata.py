"""Tests for metadata extraction from submission documents."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.parliament_submissions.metadata import (
    extract_submitter_name,
    extract_date,
    extract_committee_reference,
    extract_bill_reference,
    extract_all_metadata,
    SubmissionMetadata,
)


class ExtractSubmitterNameTest(unittest.TestCase):

    def test_extracts_name_from_top_of_document(self):
        text = "Submission by Jane Citizen\n\nI support this bill..."
        name = extract_submitter_name(text)
        self.assertEqual(name, "Jane Citizen")

    def test_extracts_name_with_organisation(self):
        text = "Submission from the New Zealand Law Society\n\nWe write..."
        name = extract_submitter_name(text)
        self.assertIsNotNone(name)
        self.assertIn("Law", name)

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_submitter_name(""))

    def test_returns_none_when_no_name_found(self):
        text = "The committee should consider..."
        self.assertIsNone(extract_submitter_name(text))

    def test_extracts_name_with_preposition_variants(self):
        text = "Submission by: John Smith\n\nIntroduction..."
        name = extract_submitter_name(text)
        self.assertEqual(name, "John Smith")

    def test_extracts_name_with_iwi_affiliation(self):
        text = "Ngati Whatua Orakei submit the following..."
        name = extract_submitter_name(text)
        self.assertIsNotNone(name)


class ExtractDateTest(unittest.TestCase):

    def test_extracts_iso_date(self):
        text = "Date: 2024-03-15\n\nSubmission body..."
        date = extract_date(text)
        self.assertEqual(date, "2024-03-15")

    def test_extracts_nz_date_format(self):
        text = "Submitted on 15 March 2024\n\nBody text..."
        date = extract_date(text)
        self.assertIsNotNone(date)

    def test_extracts_date_from_many_formats(self):
        text = "15/03/2024\n\nSubmission..."
        date = extract_date(text)
        self.assertIsNotNone(date)

    def test_returns_none_when_no_date(self):
        text = "Submission text without any date..."
        self.assertIsNone(extract_date(text))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_date(""))


class ExtractCommitteeReferenceTest(unittest.TestCase):

    def test_extracts_committee_name(self):
        text = "Submitted to the Justice Committee\n\nBody..."
        committee = extract_committee_reference(text)
        self.assertIsNotNone(committee)
        self.assertIn("Justice", committee)

    def test_extracts_select_committee(self):
        text = "To the Health Select Committee\n\nSubmission..."
        committee = extract_committee_reference(text)
        self.assertIsNotNone(committee)
        self.assertIn("Health", committee)

    def test_returns_none_when_no_committee(self):
        text = "Submission content without committee reference..."
        self.assertIsNone(extract_committee_reference(text))

    def test_returns_none_for_empty(self):
        self.assertIsNone(extract_committee_reference(""))


class ExtractBillReferenceTest(unittest.TestCase):

    def test_extracts_bill_name(self):
        text = "Submission on the ABC Amendment Bill\n\nBody..."
        bill = extract_bill_reference(text)
        self.assertIsNotNone(bill)
        self.assertIn("ABC", bill)

    def test_extracts_bill_reference_from_submission(self):
        text = "Submission on Climate Change Response Bill\n\nDetails..."
        bill = extract_bill_reference(text)
        self.assertIsNotNone(bill)
        self.assertIn("Climate Change", bill)

    def test_returns_none_when_no_bill(self):
        text = "General submission about policy..."
        self.assertIsNone(extract_bill_reference(text))

    def test_returns_none_for_empty(self):
        self.assertIsNone(extract_bill_reference(""))


class ExtractAllMetadataTest(unittest.TestCase):

    _SAMPLE_TEXT = (
        "Submission by Jane Citizen\n\n"
        "Submitted to the Justice Select Committee\n\n"
        "Re: ABC Amendment Bill\n\n"
        "Date: 2024-03-15\n\n"
        "Body of submission..."
    )

    def test_extract_all_returns_submission_metadata(self):
        meta = extract_all_metadata(self._SAMPLE_TEXT)
        self.assertIsInstance(meta, SubmissionMetadata)
        self.assertEqual(meta.submitter, "Jane Citizen")
        self.assertEqual(meta.date, "2024-03-15")
        self.assertIsNotNone(meta.committee)
        self.assertIsNotNone(meta.bill_reference)

    def test_extract_all_with_empty_text(self):
        meta = extract_all_metadata("")
        self.assertIsInstance(meta, SubmissionMetadata)
        self.assertIsNone(meta.submitter)
        self.assertIsNone(meta.date)

    def test_to_dict(self):
        meta = SubmissionMetadata(
            submitter="Jane", date="2024-01-01",
            committee="Justice", bill_reference="ABC Bill",
        )
        d = meta.to_dict()
        self.assertEqual(d["submitter"], "Jane")
        self.assertEqual(d["date"], "2024-01-01")


if __name__ == "__main__":
    unittest.main()

