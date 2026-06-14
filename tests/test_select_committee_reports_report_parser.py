"""Tests for enhanced select committee report parsing (Track 8, Phase 2)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.select_committee_reports.report_parser import (
    ParsedReport,
    extract_committee_name,
    extract_report_title,
    extract_report_date,
    extract_recommendations,
    extract_findings,
    extract_referenced_legislation,
    extract_referenced_bills,
    extract_witnesses_submitters,
    parse_report_text,
    WitnessSubmitter,
    LegislationRef,
    BillRef,
)

_MOCK_REPORT = """\
Report of the Justice Committee

Inquiry into the Criminal Procedure (Reform) Bill

June 2024

The Justice Committee has conducted an inquiry into the Criminal Procedure (Reform) Bill
and presents this report to the House of Representatives.

Contents
Introduction 3
Recommendations 5
Findings 7
Appendix 12

Recommendations
The committee recommends that the bill be passed with amendments.
The committee also recommends that the Ministry of Justice review
the implementation timeline within 12 months.

Findings
The committee finds that the current criminal procedure framework
is outdated and requires significant reform.
The committee further finds that there is broad support among
submitters for the proposed changes.

Legislation Referred To
This report references the Criminal Procedure Act 2011,
the Evidence Act 2006, and the Sentencing Act 2002.
Related bills include the Courts (Remote Participation) Bill
and the Criminal Procedure (Reform) Bill (2024/45).

Submissions
The committee received 87 submissions from the following:
John Smith (New Zealand Law Society)
Jane Doe (Auckland District Law Society)
Professor Alan Greensmith (University of Auckland)
Te Hunga Roia Maori o Aotearoa (Maori Law Society)
Dr Sarah Williams (Otago University)
Waitangi Tribunal
"""


class ExtractCommitteeNameTest(unittest.TestCase):

    def test_extracts_committee_name(self):
        name = extract_committee_name(_MOCK_REPORT)
        self.assertEqual(name, "Justice Committee")

    def test_returns_none_when_not_found(self):
        self.assertIsNone(extract_committee_name("Some random document."))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_committee_name(""))
        self.assertIsNone(extract_committee_name(None))

    def test_extracts_education_committee(self):
        text = "Report of the Education and Workforce Committee\n\nInquiry into..."
        name = extract_committee_name(text)
        self.assertEqual(name, "Education and Workforce Committee")

    def test_extracts_maori_committee(self):
        text = "Report of the Maori Affairs Committee\n\nInquiry into..."
        name = extract_committee_name(text)
        self.assertEqual(name, "Maori Affairs Committee")


class ExtractReportTitleTest(unittest.TestCase):

    def test_extracts_title(self):
        title = extract_report_title(_MOCK_REPORT)
        self.assertIsNotNone(title)
        self.assertIn("Criminal Procedure (Reform) Bill", title)

    def test_returns_none_when_not_found(self):
        self.assertIsNone(extract_report_title("Some random text."))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_report_title(""))

    def test_extracts_inquiry_title(self):
        text = "Report\n\nInquiry into the Mental Health Bill\n\nSome content"
        title = extract_report_title(text)
        self.assertIsNotNone(title)
        self.assertIn("Mental Health Bill", title)

    def test_extracts_petition_title(self):
        text = "Report\n\nPetition of John Smith\n\nContent follows"
        title = extract_report_title(text)
        self.assertIsNotNone(title)
        self.assertIn("Petition", title)


class ExtractReportDateTest(unittest.TestCase):

    def test_extracts_date_with_month_year(self):
        date = extract_report_date(_MOCK_REPORT)
        self.assertEqual(date, "2024-06")

    def test_extracts_iso_date(self):
        text = "Date: 2024-06-30\nSome text"
        date = extract_report_date(text)
        self.assertEqual(date, "2024-06-30")

    def test_extracts_nz_format_date(self):
        text = "30 June 2024\nReport content"
        date = extract_report_date(text)
        self.assertEqual(date, "2024-06-30")

    def test_returns_none_when_no_date(self):
        self.assertIsNone(extract_report_date("No date here"))

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(extract_report_date(""))
        self.assertIsNone(extract_report_date(None))


class ExtractRecommendationsTest(unittest.TestCase):

    def test_extracts_recommendations(self):
        recs = extract_recommendations(_MOCK_REPORT)
        self.assertGreaterEqual(len(recs), 2)
        self.assertTrue(any("passed with amendments" in r for r in recs))
        self.assertTrue(any("implementation timeline" in r for r in recs))

    def test_returns_empty_when_no_recommendations(self):
        text = "Report with no recommendations section."
        self.assertEqual(extract_recommendations(text), [])

    def test_returns_empty_for_empty_text(self):
        self.assertEqual(extract_recommendations(""), [])
        self.assertEqual(extract_recommendations(None), [])

    def test_recommendations_with_numbered_list(self):
        text = """\
Recommendations
1. Pass the bill.
2. Amend clause 5.
3. Conduct further review.
"""
        recs = extract_recommendations(text)
        self.assertEqual(len(recs), 3)
        self.assertIn("Pass the bill", recs[0])

    def test_recommendations_with_indented_list(self):
        text = """\
The committee makes the following recommendations:
  1. That the bill be passed
  2. That the regulations be reviewed
"""
        recs = extract_recommendations(text)
        self.assertGreaterEqual(len(recs), 1)


class ExtractFindingsTest(unittest.TestCase):

    def test_extracts_findings(self):
        findings = extract_findings(_MOCK_REPORT)
        self.assertGreaterEqual(len(findings), 2)
        self.assertTrue(any("criminal procedure" in f.lower() for f in findings))
        self.assertTrue(any("broad support" in f.lower() for f in findings))

    def test_returns_empty_when_no_findings(self):
        text = "No findings section in this text."
        self.assertEqual(extract_findings(text), [])

    def test_returns_empty_for_empty_text(self):
        self.assertEqual(extract_findings(""), [])
        self.assertEqual(extract_findings(None), [])

    def test_findings_with_numbered_list(self):
        text = """\
Findings
1. The current law is inadequate.
2. There is widespread support for reform.
"""
        findings = extract_findings(text)
        self.assertEqual(len(findings), 2)


class ExtractReferencedLegislationTest(unittest.TestCase):

    def test_extracts_legislation_references(self):
        refs = extract_referenced_legislation(_MOCK_REPORT)
        self.assertGreaterEqual(len(refs), 3)
        self.assertIn("Criminal Procedure Act 2011", refs)
        self.assertIn("Evidence Act 2006", refs)
        self.assertIn("Sentencing Act 2002", refs)

    def test_returns_empty_when_none_found(self):
        text = "No legislation mentioned in this text."
        self.assertEqual(extract_referenced_legislation(text), [])

    def test_returns_empty_for_empty_text(self):
        self.assertEqual(extract_referenced_legislation(""), [])
        self.assertEqual(extract_referenced_legislation(None), [])

    def test_detects_act_year_pattern(self):
        text = "References the Health and Safety at Work Act 2015."
        refs = extract_referenced_legislation(text)
        self.assertEqual(len(refs), 1)
        self.assertIn("Health and Safety at Work Act 2015", refs)

    def test_detects_multiple_acts(self):
        text = "Acts include the Care of Children Act 2004, Oranga Tamariki Act 1989."
        refs = extract_referenced_legislation(text)
        self.assertGreaterEqual(len(refs), 2)

    def test_detects_regulations(self):
        text = "The Secondary Legislation Act 2021 and regulations."
        refs = extract_referenced_legislation(text)
        self.assertIn("Secondary Legislation Act 2021", refs)

    def test_legislation_ref_dataclass(self):
        ref = LegislationRef(name="Criminal Procedure Act 2011", year=2011, type="act")
        self.assertEqual(ref.name, "Criminal Procedure Act 2011")
        self.assertEqual(ref.year, 2011)
        self.assertEqual(ref.type, "act")

    def test_legislation_ref_to_dict(self):
        ref = LegislationRef(name="Evidence Act 2006", year=2006, type="act")
        d = ref.to_dict()
        self.assertEqual(d["name"], "Evidence Act 2006")
        self.assertEqual(d["year"], 2006)


class ExtractReferencedBillsTest(unittest.TestCase):

    def test_extracts_bill_references(self):
        bills = extract_referenced_bills(_MOCK_REPORT)
        self.assertGreaterEqual(len(bills), 2)
        self.assertTrue(any("Criminal Procedure (Reform) Bill" in b for b in bills))
        self.assertTrue(any("Courts (Remote Participation) Bill" in b for b in bills))

    def test_returns_empty_when_none_found(self):
        text = "No bills mentioned in this text."
        self.assertEqual(extract_referenced_bills(text), [])

    def test_returns_empty_for_empty_text(self):
        self.assertEqual(extract_referenced_bills(""), [])
        self.assertEqual(extract_referenced_bills(None), [])

    def test_detects_bill_pattern(self):
        text = "The committee considered the Taxation (Budget) Bill."
        bills = extract_referenced_bills(text)
        self.assertIn("Taxation (Budget) Bill", bills)

    def test_detects_multiple_bills(self):
        text = "Related: the Employment Relations Bill, Health and Safety Bill."
        bills = extract_referenced_bills(text)
        self.assertGreaterEqual(len(bills), 2)

    def test_bill_ref_dataclass(self):
        ref = BillRef(name="Criminal Procedure (Reform) Bill", bill_number="2024/45")
        self.assertIn("Criminal Procedure", ref.name)
        self.assertEqual(ref.bill_number, "2024/45")

    def test_bill_ref_to_dict(self):
        ref = BillRef(name="Courts (Remote Participation) Bill")
        d = ref.to_dict()
        self.assertEqual(d["name"], "Courts (Remote Participation) Bill")
        self.assertIsNone(d.get("bill_number"))


class ExtractWitnessesSubmittersTest(unittest.TestCase):

    def test_extracts_witnesses(self):
        witnesses = extract_witnesses_submitters(_MOCK_REPORT)
        self.assertGreaterEqual(len(witnesses), 6)
        self.assertTrue(any("John Smith" in w.name for w in witnesses))
        self.assertTrue(any("Waitangi Tribunal" in w.name for w in witnesses))

    def test_returns_empty_when_none_found(self):
        text = "No submission section."
        self.assertEqual(extract_witnesses_submitters(text), [])

    def test_returns_empty_for_empty_text(self):
        self.assertEqual(extract_witnesses_submitters(""), [])
        self.assertEqual(extract_witnesses_submitters(None), [])

    def test_parses_org_affiliation(self):
        text = """\
Submissions received from:
John Smith (New Zealand Law Society)
Jane Doe (Auckland Council)
"""
        witnesses = extract_witnesses_submitters(text)
        self.assertEqual(len(witnesses), 2)
        self.assertEqual(witnesses[0].name, "John Smith")
        self.assertEqual(witnesses[0].affiliation, "New Zealand Law Society")

    def test_witness_submitter_dataclass(self):
        ws = WitnessSubmitter(name="John Smith", affiliation="NZ Law Society")
        self.assertEqual(ws.name, "John Smith")
        self.assertEqual(ws.affiliation, "NZ Law Society")

    def test_witness_submitter_to_dict(self):
        ws = WitnessSubmitter(name="Jane Doe")
        d = ws.to_dict()
        self.assertEqual(d["name"], "Jane Doe")


class ParsedReportDataClassTest(unittest.TestCase):

    def test_parsed_report_defaults(self):
        report = ParsedReport()
        self.assertIsNone(report.committee_name)
        self.assertIsNone(report.report_title)
        self.assertIsNone(report.report_date)
        self.assertEqual(report.recommendations, [])
        self.assertEqual(report.findings, [])
        self.assertEqual(report.referenced_legislation, [])
        self.assertEqual(report.referenced_bills, [])
        self.assertEqual(report.witnesses_submitters, [])

    def test_parsed_report_with_values(self):
        report = ParsedReport(
            committee_name="Justice Committee",
            report_title="Inquiry into the Reform Bill",
            report_date="2024-06",
            recommendations=["Pass the bill"],
            findings=["Current law is outdated"],
            referenced_legislation=[LegislationRef(name="CPA 2011", year=2011, type="act")],
            referenced_bills=[BillRef(name="Reform Bill")],
            witnesses_submitters=[WitnessSubmitter(name="John Smith")],
        )
        self.assertEqual(report.committee_name, "Justice Committee")
        self.assertEqual(len(report.recommendations), 1)

    def test_parsed_report_to_dict(self):
        report = ParsedReport(
            committee_name="Justice Committee",
            recommendations=["Pass the bill"],
            referenced_legislation=[LegislationRef(name="CPA 2011", year=2011, type="act")],
        )
        d = report.to_dict()
        self.assertEqual(d["committee_name"], "Justice Committee")
        self.assertIn("recommendations", d)
        self.assertIn("referenced_legislation", d)
        self.assertNotIn("findings", d)

    def test_parsed_report_empty_to_dict(self):
        report = ParsedReport()
        d = report.to_dict()
        self.assertEqual(d, {})


class ParseReportTextIntegrationTest(unittest.TestCase):

    def test_parse_full_report(self):
        parsed = parse_report_text(_MOCK_REPORT)
        self.assertIsInstance(parsed, ParsedReport)
        self.assertEqual(parsed.committee_name, "Justice Committee")
        self.assertIsNotNone(parsed.report_title)
        self.assertIn("Criminal Procedure (Reform) Bill", parsed.report_title)
        self.assertEqual(parsed.report_date, "2024-06")
        self.assertGreaterEqual(len(parsed.recommendations), 2)
        self.assertGreaterEqual(len(parsed.findings), 2)
        self.assertGreaterEqual(len(parsed.referenced_legislation), 3)
        self.assertGreaterEqual(len(parsed.referenced_bills), 2)
        self.assertGreaterEqual(len(parsed.witnesses_submitters), 6)

    def test_parse_empty_text(self):
        parsed = parse_report_text("")
        self.assertIsInstance(parsed, ParsedReport)
        self.assertIsNone(parsed.committee_name)

    def test_parse_minimal_text(self):
        text = "Some basic report text without structure."
        parsed = parse_report_text(text)
        self.assertIsInstance(parsed, ParsedReport)

    def test_committee_with_hyphen_and_ampersand(self):
        text = """\
Report of the Social Services and Community Committee

Inquiry into the Social Security Bill

The committee makes the following recommendations:
1. That the bill proceed.

Findings
The committee finds this bill beneficial.
"""
        parsed = parse_report_text(text)
        self.assertEqual(parsed.committee_name, "Social Services and Community Committee")
        self.assertGreaterEqual(len(parsed.recommendations), 1)


if __name__ == "__main__":
    unittest.main()