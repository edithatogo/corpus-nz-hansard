from __future__ import annotations

import csv
import unittest

import pyarrow as pa
import pyarrow.parquet as pq

from scripts.build_validated_speech_turn_component import (
    OUTPUT_COLUMNS,
    REVIEW_QUEUE_COLUMNS,
    build_validated_speech_turn_component,
)
from scripts.check_validated_speech_turn_component import _failures
from test_support import test_tmp_dir


class ValidatedSpeechTurnComponentTests(unittest.TestCase):
    def test_checker_passes_for_repo_gate(self) -> None:
        self.assertEqual(_failures(), [])

    def test_builder_emits_blocked_rows_for_candidate_artifact(self) -> None:
        tmp = test_tmp_dir() / "validated-speech-turn"
        tmp.mkdir(parents=True, exist_ok=True)
        candidate_path = tmp / "hansard_speech_turns.parquet"
        output_path = tmp / "hansard_speech_turns_validated.parquet"
        review_queue_path = tmp / "speech_turn_review_queue.csv"
        overrides_path = tmp / "speech_turn_review_overrides.csv"
        manifest_path = tmp / "manifest.json"
        table = pa.Table.from_pylist(
            [
                {
                    "parliament_document_id": "47HansS_20050217_00000759",
                    "parliament_number": 47,
                    "document_type": "Hansard - speech",
                    "title": "Example Speech",
                    "source_file": "Hansard-test.csv",
                    "source_row_number": 1,
                    "turn_index": 1,
                    "speaker_candidate": "RODNEY HIDE",
                    "speech_text": "Yes.",
                    "confidence": "medium",
                    "method": "tab_colon_marker_v1",
                },
                {
                    "parliament_document_id": "47HansS_20031210_00001051",
                    "parliament_number": 47,
                    "document_type": "Hansard - speech",
                    "title": "Example Speech 2",
                    "source_file": "Hansard-test.csv",
                    "source_row_number": 2,
                    "turn_index": 1,
                    "speaker_candidate": "Hon Roger Sowry",
                    "speech_text": "I raise a point of order Mr Speaker.",
                    "confidence": "medium",
                    "method": "tab_colon_marker_v1",
                },
            ]
        )
        pq.write_table(table, candidate_path)

        manifest = build_validated_speech_turn_component(
            candidate_parquet=candidate_path,
            output_parquet=output_path,
            review_queue_csv=review_queue_path,
            overrides_csv=overrides_path,
            manifest_path=manifest_path,
            generated_at="2026-06-10T00:00:00+00:00",
        )

        self.assertEqual(
            manifest["release_gate_status"], "blocked-pending-validated-member-identity"
        )
        self.assertEqual(manifest["counts"]["validated_rows"], 2)
        self.assertEqual(manifest["counts"]["review_queue_rows"], 2)
        with output_path.open("rb") as handle:
            table = pq.read_table(handle)
        self.assertEqual(list(table.column_names), OUTPUT_COLUMNS)
        self.assertEqual(table.num_rows, 2)
        with review_queue_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(list(rows[0]), REVIEW_QUEUE_COLUMNS)
        self.assertEqual(
            rows[0]["speaker_identity_status"], "blocked-pending-validated-member-identity"
        )


if __name__ == "__main__":
    unittest.main()
