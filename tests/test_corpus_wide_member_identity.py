from __future__ import annotations

import csv
import re
import unittest
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from scripts.build_corpus_wide_member_identity import (
    OUTPUT_COLUMNS,
    build_corpus_wide_release,
)
from scripts.check_corpus_wide_member_identity import _failures
from scripts.expand_member_authority import (
    IGNORED_TOKENS,
    MIN_TOKEN_LENGTH,
    _detect_reversed_name,
    _generate_authority_url,
    _member_id,
    _merge_near_duplicates,
    _nfkd,
)
from test_support import test_tmp_dir


class DetectedReversedNameTests(unittest.TestCase):
    def test_reversed_name_detected(self) -> None:
        result = _detect_reversed_name("Foster-Bell Paul")
        self.assertEqual(result, "Paul Foster-Bell")

    def test_reversed_name_two_word_hyphenated(self) -> None:
        result = _detect_reversed_name("Smith-Jones John")
        self.assertEqual(result, "John Smith-Jones")

    def test_normal_name_not_reversed(self) -> None:
        result = _detect_reversed_name("John Smith")
        self.assertIsNone(result)

    def test_single_word_returns_none(self) -> None:
        result = _detect_reversed_name("Speaker")
        self.assertIsNone(result)

    def test_known_first_name_not_at_end(self) -> None:
        result = _detect_reversed_name("Paul Goldsmith")
        self.assertIsNone(result)


class GenerateAuthorityUrlTests(unittest.TestCase):
    def test_simple_name(self) -> None:
        url = _generate_authority_url("Clayton Cosgrove")
        self.assertIn("cosgrove-clayton", url)
        self.assertTrue(url.startswith("https://www3.parliament.nz"))

    def test_hyphenated_surname(self) -> None:
        url = _generate_authority_url("Iain Lees-Galloway")
        self.assertIn("lees-galloway-iain", url)

    def test_multi_word_name(self) -> None:
        url = _generate_authority_url("H V Ross Robertson")
        self.assertIn("robertson-h-v-ross", url)

    def test_reversed_name_after_correction(self) -> None:
        url = _generate_authority_url("Paul Foster-Bell")
        self.assertIn("foster-bell-paul", url)

    def test_empty_name_returns_empty(self) -> None:
        self.assertEqual(_generate_authority_url(""), "")


class MergeNearDuplicatesTests(unittest.TestCase):
    def _make_record(self, canonical_name: str) -> dict[str, Any]:
        local_key = re.sub(r"[^a-z0-9]+", "-", canonical_name.lower()).strip("-")
        mid = _member_id(local_key)
        return {
            "component_id": mid,
            "member_id": mid,
            "display_name": canonical_name,
            "canonical_name": canonical_name,
            "aliases": [],
            "authority_source_id": "nz-parliament-corpus-derived",
            "authority_url": "",
            "service_periods": [],
            "resolution_scope": "corpus-auto-derived",
        }

    def test_merge_hilary_calvert(self) -> None:
        records = [
            self._make_record("Hilary Jane Calvert"),
            self._make_record("Hilary Calvert"),
        ]
        merged = _merge_near_duplicates(records)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["canonical_name"], "Hilary Jane Calvert")
        self.assertIn("Hilary Calvert", merged[0]["aliases"])

    def test_no_merge_different_surname(self) -> None:
        records = [
            self._make_record("Hilary Calvert"),
            self._make_record("Hilary Clinton"),
        ]
        merged = _merge_near_duplicates(records)
        self.assertEqual(len(merged), 2)

    def test_merge_with_existing_aliases(self) -> None:
        long_rec = self._make_record("Hilary Jane Calvert")
        short_rec = self._make_record("Hilary Calvert")
        short_rec["aliases"] = ["Hon Hilary Calvert"]
        merged = _merge_near_duplicates([short_rec, long_rec])
        self.assertEqual(len(merged), 1)
        self.assertIn("Hilary Calvert", merged[0]["aliases"])
        self.assertIn("Hon Hilary Calvert", merged[0]["aliases"])

    def test_empty_list(self) -> None:
        self.assertEqual(_merge_near_duplicates([]), [])


class IgnoredTokensTests(unittest.TestCase):
    def test_presiding_officer_excluded(self) -> None:
        self.assertIn("Presiding Officer", IGNORED_TOKENS)

    def test_the_clerk_excluded(self) -> None:
        self.assertIn("The Clerk", IGNORED_TOKENS)

    def test_vacant_excluded(self) -> None:
        self.assertIn("Vacant", IGNORED_TOKENS)

    def test_speaker_variants_excluded(self) -> None:
        self.assertIn("Speaker", IGNORED_TOKENS)
        self.assertIn("Mr Speaker", IGNORED_TOKENS)
        self.assertIn("Madam Speaker", IGNORED_TOKENS)


class NfkdNormalizationTests(unittest.TestCase):
    def test_macron_normalized(self) -> None:
        self.assertEqual(_nfkd("Tāmati"), "Tamati")

    def test_macron_upper_normalized(self) -> None:
        self.assertEqual(_nfkd("TĀMATI"), "TAMATI")

    def test_no_macron_unchanged(self) -> None:
        self.assertEqual(_nfkd("Tamati"), "Tamati")

    def test_ascii_unchanged(self) -> None:
        self.assertEqual(_nfkd("A B C 1 2 3"), "A B C 1 2 3")

    def test_empty_string(self) -> None:
        self.assertEqual(_nfkd(""), "")

    def test_min_token_length(self) -> None:
        self.assertEqual(MIN_TOKEN_LENGTH, 3)


class CorpusWideMemberIdentityTests(unittest.TestCase):
    def test_checker_passes_for_repo_gate(self) -> None:
        self.assertEqual(_failures(), [])

    def test_builder_resolves_exact_alias_multi_and_unresolved_rows(self) -> None:
        tmp = test_tmp_dir() / "corpus-wide-member-identity"
        tmp.mkdir(parents=True, exist_ok=True)
        parquet_path = tmp / "hansard.parquet"
        output_csv = tmp / "member_identity.csv"
        review_queue_csv = tmp / "member_identity_review_queue.csv"
        overrides_csv = tmp / "member_identity_review_overrides.csv"
        manifest_path = tmp / "manifest.json"
        table = pa.Table.from_pylist(
            [
                {
                    "stable_id": "doc-1",
                    "source_file": "Hansard-test.csv",
                    "source_row_number": 1,
                    "parliament_number": 47,
                    "parliament_document_id": "doc-1",
                    "document_type": "Hansard - speech",
                    "document_content_date": "2004-01-01T00:00:00",
                    "member_of_parliament_raw": "Clayton Cosgrove",
                    "source_hash": "source-hash-1",
                },
                {
                    "stable_id": "doc-2",
                    "source_file": "Hansard-test.csv",
                    "source_row_number": 2,
                    "parliament_number": 47,
                    "parliament_document_id": "doc-2",
                    "document_type": "Hansard - question",
                    "document_content_date": "2004-01-02T00:00:00",
                    "member_of_parliament_raw": "CLAYTON COSGROVE; Hon Roger Sowry; Unknown Person",
                    "source_hash": "source-hash-2",
                },
            ]
        )
        pq.write_table(table, parquet_path)

        manifest = build_corpus_wide_release(
            parquet_path=parquet_path,
            output_csv=output_csv,
            review_queue_csv=review_queue_csv,
            overrides_csv=overrides_csv,
            manifest_path=manifest_path,
            generated_at="2026-06-10T00:00:00+00:00",
        )

        self.assertEqual(manifest["counts"]["derived_rows"], 4)
        self.assertEqual(manifest["counts"]["exact"], 1)
        self.assertEqual(manifest["counts"]["multi-person"], 2)
        self.assertEqual(manifest["counts"]["unresolved"], 1)
        with output_csv.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(list(rows[0]), OUTPUT_COLUMNS)
        self.assertEqual(rows[0]["member_resolution_status"], "exact")
        self.assertEqual(rows[1]["member_resolution_status"], "multi-person")
        self.assertEqual(rows[2]["member_resolution_status"], "multi-person")
        self.assertEqual(rows[3]["member_resolution_status"], "unresolved")
        with review_queue_csv.open(encoding="utf-8", newline="") as handle:
            review_rows = list(csv.DictReader(handle))
        self.assertEqual(len(review_rows), 1)
        self.assertEqual(review_rows[0]["member_raw_token"], "Unknown Person")


if __name__ == "__main__":
    unittest.main()
