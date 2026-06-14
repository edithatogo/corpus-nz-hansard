"""Tests for cross-corpus indexing of select committee reports (Track 8, Phase 2).

Links reports to Hansard debates and legislation bills/acts, with Parquet schema.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.select_committee_reports.correlation_index import (
    HansardLink,
    LegislationLink,
    CorrelationEntry,
    build_hansard_links,
    build_legislation_links,
    build_correlation_index,
    CorrelationIndex,
    CORRELATION_INDEX_SCHEMA,
)


class HansardLinkTest(unittest.TestCase):

    def test_hansard_link_defaults(self):
        link = HansardLink(hansard_id="hans-001")
        self.assertEqual(link.hansard_id, "hans-001")
        self.assertIsNone(link.sitting_date)
        self.assertEqual(link.relevance, 1.0)

    def test_hansard_link_with_values(self):
        link = HansardLink(
            hansard_id="hans-2024-06-30",
            sitting_date="2024-06-30",
            debate_title="Criminal Procedure Bill - First Reading",
            relevance=0.95,
        )
        self.assertEqual(link.sitting_date, "2024-06-30")
        self.assertEqual(link.relevance, 0.95)

    def test_hansard_link_to_dict(self):
        link = HansardLink(
            hansard_id="hans-001",
            sitting_date="2024-06-30",
            relevance=0.85,
        )
        d = link.to_dict()
        self.assertEqual(d["hansard_id"], "hans-001")
        self.assertEqual(d["relevance"], 0.85)
        self.assertNotIn("debate_title", d)


class LegislationLinkTest(unittest.TestCase):

    def test_legislation_link_defaults(self):
        link = LegislationLink(legislation_id="leg-001")
        self.assertEqual(link.legislation_id, "leg-001")
        self.assertIsNone(link.legislation_type)

    def test_legislation_link_with_values(self):
        link = LegislationLink(
            legislation_id="Criminal Procedure Act 2011",
            legislation_type="act",
            legislation_url="https://www.legislation.govt.nz/act/2011/0081",
        )
        self.assertEqual(link.legislation_type, "act")

    def test_legislation_link_to_dict(self):
        link = LegislationLink(
            legislation_id="Evidence Act 2006",
            legislation_type="act",
        )
        d = link.to_dict()
        self.assertEqual(d["legislation_id"], "Evidence Act 2006")
        self.assertEqual(d["legislation_type"], "act")
        self.assertNotIn("legislation_url", d)


class CorrelationEntryTest(unittest.TestCase):

    def test_correlation_entry_defaults(self):
        entry = CorrelationEntry(report_id="rep-001")
        self.assertEqual(entry.report_id, "rep-001")
        self.assertEqual(entry.hansard_links, [])
        self.assertEqual(entry.legislation_links, [])

    def test_correlation_entry_with_links(self):
        entry = CorrelationEntry(
            report_id="rep-001",
            committee_name="Justice Committee",
            report_title="Criminal Procedure Report",
            report_date="2024-06-30",
            hansard_links=[HansardLink(hansard_id="hans-001", relevance=0.9)],
            legislation_links=[LegislationLink(legislation_id="CPA 2011", legislation_type="act")],
        )
        self.assertEqual(len(entry.hansard_links), 1)
        self.assertEqual(len(entry.legislation_links), 1)

    def test_correlation_entry_to_dict(self):
        entry = CorrelationEntry(
            report_id="rep-001",
            committee_name="Justice Committee",
            hansard_links=[HansardLink(hansard_id="hans-001")],
        )
        d = entry.to_dict()
        self.assertEqual(d["report_id"], "rep-001")
        self.assertEqual(d["committee_name"], "Justice Committee")
        self.assertEqual(len(d["hansard_links"]), 1)
        self.assertEqual(d["hansard_links"][0]["hansard_id"], "hans-001")


class BuildHansardLinksTest(unittest.TestCase):

    def test_build_from_report_title_matching_debate(self):
        links = build_hansard_links(
            report_title="Inquiry into the Criminal Procedure (Reform) Bill",
            committee_name="Justice Committee",
            report_date="2024-06",
            available_debates=[
                {"id": "hans-001", "title": "Criminal Procedure (Reform) Bill - First Reading", "date": "2024-05-15"},
                {"id": "hans-002", "title": "Budget Debate 2024", "date": "2024-06-01"},
            ],
        )
        self.assertGreaterEqual(len(links), 1)
        self.assertTrue(any(l.hansard_id == "hans-001" for l in links))

    def test_build_returns_empty_with_no_matches(self):
        links = build_hansard_links(
            report_title="Some unrelated topic",
            committee_name="Justice Committee",
            report_date="2024-06",
            available_debates=[
                {"id": "hans-001", "title": "Budget Debate", "date": "2024-06-01"},
            ],
        )
        self.assertEqual(len(links), 0)

    def test_build_with_default_debates(self):
        links = build_hansard_links(
            report_title="Inquiry into the Justice Reform Bill",
            committee_name="Justice Committee",
            report_date="2024-06",
        )
        self.assertIsInstance(links, list)

    def test_build_links_by_committee_name(self):
        links = build_hansard_links(
            report_title="Annual Report 2024",
            committee_name="Justice Committee",
            report_date="2024-06",
            available_debates=[
                {"id": "hans-003", "title": "Justice Committee - 2024 Annual Review", "date": "2024-06-15"},
            ],
        )
        self.assertGreaterEqual(len(links), 1)


class BuildLegislationLinksTest(unittest.TestCase):

    def test_build_from_legislation_refs(self):
        links = build_legislation_links(
            legislation_refs=["Criminal Procedure Act 2011", "Evidence Act 2006"],
        )
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0].legislation_id, "Criminal Procedure Act 2011")
        self.assertEqual(links[0].legislation_type, "act")

    def test_build_from_bill_refs(self):
        links = build_legislation_links(
            bill_refs=["Criminal Procedure (Reform) Bill"],
        )
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0].legislation_type, "bill")

    def test_build_from_empty_refs(self):
        links = build_legislation_links()
        self.assertEqual(links, [])

    def test_build_combined_refs(self):
        links = build_legislation_links(
            legislation_refs=["CPA 2011"],
            bill_refs=["Reform Bill"],
        )
        self.assertEqual(len(links), 2)
        types = [l.legislation_type for l in links]
        self.assertIn("act", types)
        self.assertIn("bill", types)


class BuildCorrelationIndexTest(unittest.TestCase):

    def test_build_index_from_parsed_reports(self):
        index = build_correlation_index(
            parsed_reports=[
                {
                    "report_id": "rep-001",
                    "committee_name": "Justice Committee",
                    "report_title": "Inquiry into the Reform Bill",
                    "report_date": "2024-06",
                    "referenced_legislation": ["Criminal Procedure Act 2011"],
                    "referenced_bills": ["Reform Bill"],
                },
            ],
        )
        self.assertIsInstance(index, CorrelationIndex)
        self.assertEqual(len(index.entries), 1)

    def test_build_index_returns_empty_for_empty_input(self):
        index = build_correlation_index(parsed_reports=[])
        self.assertEqual(len(index.entries), 0)

    def test_build_index_with_multiple_reports(self):
        index = build_correlation_index(
            parsed_reports=[
                {"report_id": "rep-001", "committee_name": "Justice", "report_title": "Report 1", "report_date": "2024-01"},
                {"report_id": "rep-002", "committee_name": "Health", "report_title": "Report 2", "report_date": "2024-02"},
            ],
        )
        self.assertEqual(len(index.entries), 2)


class CorrelationIndexTest(unittest.TestCase):

    def test_index_has_schema(self):
        self.assertIsNotNone(CORRELATION_INDEX_SCHEMA)

    def test_index_to_dicts(self):
        index = CorrelationIndex(entries=[
            CorrelationEntry(report_id="rep-001", committee_name="Justice"),
            CorrelationEntry(report_id="rep-002", committee_name="Health"),
        ])
        dicts = index.to_dicts()
        self.assertEqual(len(dicts), 2)
        self.assertEqual(dicts[0]["report_id"], "rep-001")

    def test_index_metadata(self):
        index = CorrelationIndex(entries=[])
        meta = index.metadata()
        self.assertIn("total_entries", meta)
        self.assertIn("corpus", meta)
        self.assertEqual(meta["total_entries"], 0)
        self.assertEqual(meta["corpus"], "corpus-nz-hansard")

    def test_index_metadata_with_entries(self):
        index = CorrelationIndex(entries=[
            CorrelationEntry(report_id="rep-001", committee_name="Justice"),
        ])
        meta = index.metadata()
        self.assertEqual(meta["total_entries"], 1)
        self.assertEqual(meta["committees"], ["Justice"])


class CorrelationEntryEqualityTest(unittest.TestCase):

    def test_entries_equal(self):
        e1 = CorrelationEntry(report_id="rep-001")
        e2 = CorrelationEntry(report_id="rep-001")
        self.assertEqual(e1, e2)

    def test_entries_not_equal(self):
        e1 = CorrelationEntry(report_id="rep-001")
        e2 = CorrelationEntry(report_id="rep-002")
        self.assertNotEqual(e1, e2)


if __name__ == "__main__":
    unittest.main()