from __future__ import annotations

import csv
import unittest

import pyarrow as pa
import pyarrow.parquet as pq

from scripts.build_corpus_wide_party_attribution import (
    OUTPUT_COLUMNS,
    REVIEW_QUEUE_COLUMNS,
    _extract_vote_labels,
    build_corpus_wide_release,
)
from scripts.check_corpus_wide_party_attribution import _failures
from test_support import test_tmp_dir


class CorpusWidePartyAttributionTests(unittest.TestCase):
    def test_checker_passes_for_repo_gate(self) -> None:
        self.assertEqual(_failures(), [])

    def test_extract_vote_labels(self) -> None:
        labels = _extract_vote_labels(
            "A party vote was called for on the question That the bill be now read a second time. "
            "Ayes 68 New Zealand National 49; ACT New Zealand 11; New Zealand First 8. "
            "Noes 48 New Zealand Labour 34; Green Party of Aotearoa New Zealand 14."
        )
        self.assertEqual(
            [
                (item["party_vote_side"], item["party_label_raw"], item["party_vote_count"])
                for item in labels
            ],
            [
                ("Ayes", "New Zealand National", 49),
                ("Ayes", "ACT New Zealand", 11),
                ("Ayes", "New Zealand First", 8),
                ("Noes", "New Zealand Labour", 34),
                ("Noes", "Green Party of Aotearoa New Zealand", 14),
            ],
        )

    def test_builder_emits_party_vote_rows_and_review_queue(self) -> None:
        tmp = test_tmp_dir() / "corpus-wide-party-attribution"
        tmp.mkdir(parents=True, exist_ok=True)
        parquet_path = tmp / "hansard.parquet"
        output_csv = tmp / "party_attribution.csv"
        review_queue_csv = tmp / "party_attribution_review_queue.csv"
        overrides_csv = tmp / "party_attribution_review_overrides.csv"
        manifest_path = tmp / "manifest.json"
        table = pa.Table.from_pylist(
            [
                {
                    "stable_id": "vote-1",
                    "source_file": "Hansard-test.csv",
                    "source_row_number": 1,
                    "parliament_number": 54,
                    "parliament_document_id": "vote-1",
                    "document_type": "Hansard - vote",
                    "document_content_date": "2024-06-25T00:00:00",
                    "content": "A party vote was called for on the question That the bill be now read a second time. "
                    "Ayes 68 New Zealand National 49; ACT New Zealand 11; New Zealand First 8. "
                    "Noes 48 New Zealand Labour 34; Green Party of Aotearoa New Zealand 14.",
                    "member_of_parliament_raw": "",
                    "source_hash": "source-hash-1",
                },
                {
                    "stable_id": "speech-1",
                    "source_file": "Hansard-test.csv",
                    "source_row_number": 2,
                    "parliament_number": 47,
                    "parliament_document_id": "speech-1",
                    "document_type": "Hansard - speech",
                    "document_content_date": "2004-01-01T00:00:00",
                    "content": "CLAYTON COSGROVE: The second is a certificate of incorporation...",
                    "member_of_parliament_raw": "CLAYTON COSGROVE",
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

        self.assertEqual(
            manifest["release_gate_status"], "blocked-pending-validated-member-identity"
        )
        self.assertEqual(manifest["counts"]["derived_rows"], 5)
        self.assertEqual(manifest["counts"]["review_queue_rows"], 1)
        with output_csv.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(list(rows[0]), OUTPUT_COLUMNS)
        self.assertEqual(rows[0]["party_label_raw"], "New Zealand National")
        self.assertEqual(rows[0]["party_vote_side"], "Ayes")
        with review_queue_csv.open(encoding="utf-8", newline="") as handle:
            review_rows = list(csv.DictReader(handle))
        self.assertEqual(list(review_rows[0]), REVIEW_QUEUE_COLUMNS)
        self.assertEqual(review_rows[0]["document_type"], "Hansard - speech")
        self.assertEqual(review_rows[0]["review_status"], "needs-review")


if __name__ == "__main__":
    unittest.main()
