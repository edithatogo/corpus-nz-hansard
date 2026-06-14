"""Tests for metadata extraction from select committee reports."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.select_committee_reports.metadata import (
    extract_report_date,
    extract_committee_name,
    extract_bill_reference,
    extract_report_subject,
    extract_member_recommendations,
    extract_all_metadata,
    ReportMetadata,
)

_SAMPLE_TEXT = """\
Justice Committee
Report Date: 30 June 2024

Inquiry into the Justice Reform Bill

The committee recommends that the bill be passed with amendments.
Committee members: Hon John Smith (Chair), Dr Jane Doe

Subject: Justice Reform and Access to Legal Aid
Bill referred: Justice Reform Bill (2024/123)
"""


class ExtractReportDateTest(unittest.TestCase):

    def test_extracts_iso_date(self):
        text = "Report Date: 2024-06-30\n"
        date = extract_report_date(text)
        self.assertEqual(date, "2024-06-30")

    def test_extracts_nz_date_format(self):
        date = extract_report_date(_SAMPLE_TEXT)
        self.assertIsNotNone(date)
        self.assertEqual(date, "2024-06-30")

    def test_extracts_date_variant(self):
        text = "Date of report: 30/06/2024\n"
        date = extract_report_date(text)
        self.assertEqual(date, "2024-06-30")

    def test_returns_none_when_no_date(self):
        text = "Report without any date..."
        self.assertIsNone(extract_report_date(text))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_report_date(""))


class ExtractCommitteeNameTest(unittest.TestCase):

    def test_extracts_name_from_text(self):
        name = extract_committee_name(_SAMPLE_TEXT)
        self.assertEqual(name, "Justice Committee")

    def test_extracts_committee_variant(self):
        text = "Report of the Health Committee\n"
        name = extract_committee_name(text)
        self.assertEqual(name, "Health Committee")

    def test_returns_none_when_not_found(self):
        self.assertIsNone(extract_committee_name("No committee here."))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_committee_name(""))


class ExtractBillReferenceTest(unittest.TestCase):

    def test_extracts_bill_reference(self):
        ref = extract_bill_reference(_SAMPLE_TEXT)
        self.assertEqual(ref, "Justice Reform Bill")

    def test_extracts_bill_variant(self):
        text = "Inquiry into the Mental Health (Compulsory Assessment) Bill\n"
        ref = extract_bill_reference(text)
        self.assertIn("Mental Health", ref)

    def test_returns_none_when_not_found(self):
        text = "General committee business without a bill reference."
        self.assertIsNone(extract_bill_reference(text))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_bill_reference(""))


class ExtractReportSubjectTest(unittest.TestCase):

    def test_extracts_subject(self):
        subject = extract_report_subject(_SAMPLE_TEXT)
        self.assertEqual(subject, "Justice Reform and Access to Legal Aid")

    def test_returns_none_when_not_found(self):
        self.assertIsNone(extract_report_subject("No subject line here."))


class ExtractMemberRecommendationsTest(unittest.TestCase):

    def test_extracts_recommendations(self):
        recs = extract_member_recommendations(_SAMPLE_TEXT)
        self.assertGreaterEqual(len(recs), 1)
        self.assertTrue(any("passed with amendments" in r for r in recs))

    def test_returns_empty_when_no_recommendations(self):
        self.assertEqual(extract_member_recommendations(""), [])


class ExtractAllMetadataTest(unittest.TestCase):

    def test_extract_all_returns_report_metadata(self):
        meta = extract_all_metadata(_SAMPLE_TEXT)
        self.assertIsInstance(meta, ReportMetadata)
        self.assertEqual(meta.report_date, "2024-06-30")
        self.assertEqual(meta.committee_name, "Justice Committee")
        self.assertEqual(meta.bill_reference, "Justice Reform Bill")

    def test_extract_all_with_empty_text(self):
        meta = extract_all_metadata("")
        self.assertIsInstance(meta, ReportMetadata)
        self.assertIsNone(meta.report_date)
        self.assertIsNone(meta.committee_name)
        self.assertEqual(meta.recommendations, [])

    def test_to_dict(self):
        meta = ReportMetadata(
            report_date="2024-06-30",
            committee_name="Justice Committee",
            bill_reference="Justice Reform Bill",
            subject="Justice Reform",
            recommendations=["Pass the bill"],
        )
        d = meta.to_dict()
        self.assertEqual(d["report_date"], "2024-06-30")
        self.assertIn("Pass the bill", d["recommendations"])


if __name__ == "__main__":
    unittest.main()
