"""Tests for submission schema normalization and Bill ID linkage."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.parliament_submissions.normalization import (
    NORMALIZED_SCHEMA,
    normalize_submitter_name,
    normalize_date,
    normalize_committee,
    normalize_bill_reference,
    normalize_text_content,
    normalize_submission_entry,
    write_normalized_parquet,
)
from scripts.parliament_submissions.bill_linkage import (
    BillLinkageIndex,
    parse_bill_reference_from_text,
    cross_reference_bills,
    build_linkage_index,
    _normalize_bill_title,
    DEFAULT_BILLS_CATALOG,
)
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


# ---------------------------------------------------------------------------
#  Schema Normalization Tests
# ---------------------------------------------------------------------------

class NormalizedSchemaTest(unittest.TestCase):
    """Verify the Parquet schema definition."""

    def test_schema_is_pyarrow_schema(self):
        import pyarrow as pa
        self.assertIsInstance(NORMALIZED_SCHEMA, pa.Schema)

    def test_schema_contains_expected_fields(self):
        expected = {
            "submission_id", "submitter_name", "submitter_normalized",
            "date", "date_normalized", "committee", "committee_normalized",
            "bill_reference", "bill_reference_normalized",
            "text_content", "text_sha256", "source_url",
            "parliament_number", "submission_year",
        }
        field_names = {f.name for f in NORMALIZED_SCHEMA}
        for field in expected:
            self.assertIn(field, field_names, f"Missing field: {field}")

    def test_schema_field_types(self):
        import pyarrow as pa
        type_map = {f.name: f.type for f in NORMALIZED_SCHEMA}
        # Key fields should be strings
        self.assertEqual(type_map["submission_id"], pa.string())
        self.assertEqual(type_map["submitter_name"], pa.string())
        self.assertEqual(type_map["date"], pa.string())
        self.assertEqual(type_map["text_content"], pa.string())
        self.assertEqual(type_map["submission_year"], pa.int32())


class NormalizeSubmitterNameTest(unittest.TestCase):

    def test_trims_whitespace(self):
        self.assertEqual(normalize_submitter_name("  Jane Citizen  "), "Jane Citizen")

    def test_removes_trailing_punctuation(self):
        self.assertEqual(normalize_submitter_name("Jane Citizen,"), "Jane Citizen")
        self.assertEqual(normalize_submitter_name("Jane Citizen."), "Jane Citizen")
        self.assertEqual(normalize_submitter_name("Jane Citizen;"), "Jane Citizen")

    def test_collapses_multiple_spaces(self):
        self.assertEqual(normalize_submitter_name("Jane   Citizen"), "Jane Citizen")

    def test_returns_none_for_empty(self):
        self.assertIsNone(normalize_submitter_name(""))
        self.assertIsNone(normalize_submitter_name("   "))
        self.assertIsNone(normalize_submitter_name(None))

    def test_preserves_organisation_names(self):
        self.assertEqual(
            normalize_submitter_name("New Zealand Law Society"),
            "New Zealand Law Society",
        )


class NormalizeDateTest(unittest.TestCase):

    def test_iso_date_preserved(self):
        self.assertEqual(normalize_date("2024-03-15"), "2024-03-15")

    def test_nz_date_converted(self):
        self.assertEqual(normalize_date("15 March 2024"), "2024-03-15")

    def test_dmy_slash_converted(self):
        self.assertEqual(normalize_date("15/03/2024"), "2024-03-15")

    def test_dmy_dash_converted(self):
        self.assertEqual(normalize_date("15-03-2024"), "2024-03-15")

    def test_returns_none_for_invalid(self):
        self.assertIsNone(normalize_date("not-a-date"))
        self.assertIsNone(normalize_date(""))
        self.assertIsNone(normalize_date(None))


class NormalizeCommitteeTest(unittest.TestCase):

    def test_trims_and_collapses(self):
        self.assertEqual(
            normalize_committee("  Justice   Committee "),
            "Justice Committee",
        )

    def test_removes_extra_whitespace(self):
        self.assertEqual(
            normalize_committee("Health    Select Committee"),
            "Health Select Committee",
        )

    def test_returns_none_for_empty(self):
        self.assertIsNone(normalize_committee(""))
        self.assertIsNone(normalize_committee(None))


class NormalizeBillReferenceTest(unittest.TestCase):

    def test_trims_and_strips_punctuation(self):
        self.assertEqual(
            normalize_bill_reference("  ABC Amendment Bill. "),
            "ABC Amendment Bill",
        )

    def test_preserves_multi_word_bill_name(self):
        self.assertEqual(
            normalize_bill_reference("Climate Change Response Amendment Bill"),
            "Climate Change Response Amendment Bill",
        )

    def test_returns_none_for_empty(self):
        self.assertIsNone(normalize_bill_reference(""))
        self.assertIsNone(normalize_bill_reference(None))


class NormalizeTextContentTest(unittest.TestCase):

    def test_strips_leading_trailing_whitespace(self):
        self.assertEqual(
            normalize_text_content("  \nHello World\n  "),
            "Hello World",
        )

    def test_normalizes_line_endings(self):
        self.assertEqual(
            normalize_text_content("Line one\r\nLine two\rLine three"),
            "Line one\nLine two\nLine three",
        )

    def test_collapses_excessive_blank_lines(self):
        result = normalize_text_content("Line one\n\n\n\nLine two")
        self.assertIn("Line one", result)
        self.assertIn("Line two", result)
        self.assertNotIn("\n\n\n", result)

    def test_returns_empty_string_for_none(self):
        self.assertEqual(normalize_text_content(None), "")

    def test_returns_empty_string_for_empty(self):
        self.assertEqual(normalize_text_content(""), "")


class NormalizeSubmissionEntryTest(unittest.TestCase):

    def test_normalizes_complete_record(self):
        entry = {
            "id": "sub-001",
            "submitter": "  Jane Citizen  ",
            "submission_date": "15 March 2024",
            "committee": "  Justice   Committee ",
            "bill_reference": "ABC Bill.",
            "text_content": "  Submission body text\r\n\r\n  ",
            "source_url": "https://example.com/sub.pdf",
        }
        result = normalize_submission_entry(entry)
        self.assertEqual(result["submitter_name"], "Jane Citizen")
        self.assertEqual(result["date_normalized"], "2024-03-15")
        self.assertEqual(result["committee_normalized"], "Justice Committee")
        self.assertEqual(result["bill_reference_normalized"], "ABC Bill")
        self.assertEqual(result["text_content"], "Submission body text")

    def test_handles_minimal_entry(self):
        entry = {"id": "sub-min"}
        result = normalize_submission_entry(entry)
        self.assertEqual(result["submission_id"], "sub-min")
        self.assertIsNone(result["submitter_name"])
        self.assertIsNone(result["date_normalized"])
        self.assertIsNone(result["committee_normalized"])
        self.assertIsNone(result["bill_reference_normalized"])

    def test_sets_submission_year_from_date(self):
        entry = {"id": "sub-002", "submission_date": "2024-03-15"}
        result = normalize_submission_entry(entry)
        self.assertEqual(result["submission_year"], 2024)

    def test_defaults_year_when_no_date(self):
        entry = {"id": "sub-003"}
        result = normalize_submission_entry(entry)
        self.assertIsNone(result["submission_year"])

    def test_computes_text_sha256(self):
        entry = {"id": "sub-004", "text_content": "Hello World"}
        import hashlib
        result = normalize_submission_entry(entry)
        expected = hashlib.sha256(b"Hello World").hexdigest()
        self.assertEqual(result["text_sha256"], expected)


class WriteNormalizedParquetTest(unittest.TestCase):

    def test_writes_parquet_file(self):
        records = [
            normalize_submission_entry({
                "id": "sub-001",
                "submitter": "Jane Citizen",
                "submission_date": "2024-03-15",
                "committee": "Justice Committee",
            }),
        ]
        out_path = TEST_TMP / "test_normalized.parquet"
        result_path = write_normalized_parquet(records, out_path)
        self.assertTrue(Path(result_path).exists())
        Path(result_path).unlink(missing_ok=True)

    def test_read_back_parquet_has_correct_columns(self):
        import pyarrow.parquet as pq
        records = [
            normalize_submission_entry({"id": "sub-001", "submitter": "Jane"}),
        ]
        out_path = TEST_TMP / "test_columns.parquet"
        write_normalized_parquet(records, out_path)
        table = pq.read_table(str(out_path))
        field_names = {f.name for f in table.schema}
        self.assertIn("submission_id", field_names)
        self.assertIn("submitter_name", field_names)
        self.assertIn("date_normalized", field_names)
        out_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
#  Bill ID Linkage Tests
# ---------------------------------------------------------------------------

class BillLinkageIndexTest(unittest.TestCase):

    def test_index_initializes_empty(self):
        idx = BillLinkageIndex()
        self.assertEqual(len(idx.bills_catalog), 0)
        self.assertEqual(len(idx.linkage_map), 0)

    def test_index_initializes_with_catalog(self):
        catalog = [
            {"id": "bill-001", "title": "ABC Amendment Bill"},
            {"id": "bill-002", "title": "XYZ Reform Bill"},
        ]
        idx = BillLinkageIndex(catalog)
        self.assertEqual(len(idx.bills_catalog), 2)

    def test_lookup_by_exact_title(self):
        catalog = [{"id": "bill-001", "title": "ABC Amendment Bill"}]
        idx = BillLinkageIndex(catalog)
        result = idx.lookup("ABC Amendment Bill")
        self.assertEqual(result, "bill-001")

    def test_lookup_returns_none_for_unknown(self):
        idx = BillLinkageIndex()
        self.assertIsNone(idx.lookup("Nonexistent Bill"))

    def test_lookup_by_normalized_title(self):
        catalog = [{"id": "bill-001", "title": "ABC Amendment Bill"}]
        idx = BillLinkageIndex(catalog)
        result = idx.lookup("ABC Amendment Bill.")
        self.assertEqual(result, "bill-001")

    def test_add_linkage(self):
        idx = BillLinkageIndex()
        idx.add_linkage("sub-001", "bill-001", confidence=0.95)
        self.assertIn("sub-001", idx.linkage_map)
        self.assertEqual(idx.linkage_map["sub-001"]["bill_id"], "bill-001")
        self.assertEqual(idx.linkage_map["sub-001"]["confidence"], 0.95)

    def test_add_linkage_multiple_submissions(self):
        idx = BillLinkageIndex()
        idx.add_linkage("sub-001", "bill-001")
        idx.add_linkage("sub-002", "bill-001")
        idx.add_linkage("sub-003", "bill-002")
        self.assertEqual(len(idx.linkage_map), 3)

    def test_export_linkage_index(self):
        idx = BillLinkageIndex()
        idx.add_linkage("sub-001", "bill-001", confidence=1.0)
        exported = idx.export_linkage_index()
        self.assertEqual(len(exported), 1)
        self.assertEqual(exported[0]["submission_id"], "sub-001")
        self.assertEqual(exported[0]["bill_id"], "bill-001")

    def test_str_representation(self):
        catalog = [{"id": "b1", "title": "Test Bill"}]
        idx = BillLinkageIndex(catalog)
        repr_str = repr(idx)
        self.assertIn("BillLinkageIndex", repr_str)
        self.assertIn("1 bills", repr_str)


class ParseBillReferenceFromTextTest(unittest.TestCase):

    def test_detects_bill_reference_in_text(self):
        text = "We submit on the ABC Amendment Bill 2024"
        result = parse_bill_reference_from_text(text)
        self.assertIsNotNone(result)
        self.assertIn("ABC", result)

    def test_returns_none_when_no_reference(self):
        text = "This is a general submission about policy matters"
        self.assertIsNone(parse_bill_reference_from_text(text))

    def test_detects_bill_with_standard_suffix(self):
        text = "Submission regarding the Climate Change Response Bill"
        result = parse_bill_reference_from_text(text)
        self.assertIsNotNone(result)
        self.assertIn("Climate Change", result)

    def test_returns_none_for_empty_text(self):
        self.assertIsNone(parse_bill_reference_from_text(""))
        self.assertIsNone(parse_bill_reference_from_text(None))


class CrossReferenceBillsTest(unittest.TestCase):

    def test_cross_reference_matches_exact(self):
        catalog = [
            {"id": "bill-001", "title": "ABC Amendment Bill"},
        ]
        submissions = [
            {
                "submission_id": "sub-001",
                "bill_reference": "ABC Amendment Bill",
                "bill_reference_normalized": "ABC Amendment Bill",
            },
        ]
        idx = cross_reference_bills(submissions, catalog)
        self.assertIn("sub-001", idx.linkage_map)
        self.assertEqual(idx.linkage_map["sub-001"]["bill_id"], "bill-001")

    def test_cross_reference_no_match(self):
        catalog = [
            {"id": "bill-001", "title": "ABC Amendment Bill"},
        ]
        submissions = [
            {
                "submission_id": "sub-001",
                "bill_reference": "XYZ Bill",
                "bill_reference_normalized": "XYZ Bill",
            },
        ]
        idx = cross_reference_bills(submissions, catalog)
        self.assertNotIn("sub-001", idx.linkage_map)

    def test_cross_reference_multiple_hits(self):
        catalog = [
            {"id": "bill-001", "title": "ABC Amendment Bill"},
            {"id": "bill-002", "title": "XYZ Reform Bill"},
        ]
        submissions = [
            {
                "submission_id": "sub-001",
                "bill_reference_normalized": "ABC Amendment Bill",
            },
            {
                "submission_id": "sub-002",
                "bill_reference_normalized": "XYZ Reform Bill",
            },
        ]
        idx = cross_reference_bills(submissions, catalog)
        self.assertEqual(len(idx.linkage_map), 2)

    def test_cross_reference_empty_catalog(self):
        submissions = [
            {
                "submission_id": "sub-001",
                "bill_reference_normalized": "ABC Amendment Bill",
            },
        ]
        idx = cross_reference_bills(submissions, [])
        self.assertEqual(len(idx.linkage_map), 0)

    def test_cross_reference_empty_submissions(self):
        idx = cross_reference_bills([], [{"id": "b1", "title": "Test"}])
        self.assertEqual(len(idx.linkage_map), 0)


class BuildLinkageIndexTest(unittest.TestCase):

    def test_integration_build_linkage(self):
        catalog = [
            {"id": "bill-001", "title": "ABC Amendment Bill"},
            {"id": "bill-002", "title": "XYZ Reform Bill"},
        ]
        raw_submissions = [
            {"id": "sub-001", "bill_reference": "ABC Amendment Bill",
             "submitter": "Jane", "submission_date": "2024-03-15"},
            {"id": "sub-002", "bill_reference": "XYZ Reform Bill",
             "submitter": "Bob", "submission_date": "2024-04-01"},
        ]
        normalized = [normalize_submission_entry(s) for s in raw_submissions]
        idx = build_linkage_index(normalized, catalog)
        self.assertEqual(len(idx.linkage_map), 2)
        self.assertEqual(idx.linkage_map["sub-001"]["bill_id"], "bill-001")
        self.assertEqual(idx.linkage_map["sub-002"]["bill_id"], "bill-002")

    def test_build_linkage_fallback_to_text_parsing(self):
        """When bill_reference is missing, fall back to text parsing."""
        catalog = [
            {"id": "bill-001", "title": "ABC Amendment Bill"},
        ]
        raw_submissions = [
            {
                "id": "sub-001",
                "text_content": "We submit on the ABC Amendment Bill 2024",
            },
        ]
        normalized = [normalize_submission_entry(s) for s in raw_submissions]
        idx = build_linkage_index(normalized, catalog)
        self.assertIn("sub-001", idx.linkage_map)
        self.assertEqual(idx.linkage_map["sub-001"]["bill_id"], "bill-001")


class NormalizeBillTitleTest(unittest.TestCase):

    def test_lowercases(self):
        result = _normalize_bill_title("ABC Amendment Bill")
        self.assertEqual(result, "abc amendment bill")

    def test_strips_punctuation(self):
        result = _normalize_bill_title("ABC Amendment Bill,")
        self.assertEqual(result, "abc amendment bill")

    def test_collapses_spaces(self):
        result = _normalize_bill_title("ABC   Amendment   Bill")
        self.assertEqual(result, "abc amendment bill")

    def test_strips_leading_trailing(self):
        result = _normalize_bill_title("  ABC Amendment Bill  ")
        self.assertEqual(result, "abc amendment bill")

    def test_returns_empty_for_none(self):
        self.assertEqual(_normalize_bill_title(None), "")
        self.assertEqual(_normalize_bill_title(""), "")


class DefaultBillsCatalogTest(unittest.TestCase):

    def test_default_catalog_is_list(self):
        catalog = DEFAULT_BILLS_CATALOG
        self.assertIsInstance(catalog, list)


if __name__ == "__main__":
    unittest.main()

