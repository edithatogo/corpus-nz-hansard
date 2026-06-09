import json
import sys
import unittest
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.segment_speech_turns import extract_turns_from_content, run_segmentation
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class SegmentSpeechTurnsTest(unittest.TestCase):
    def test_extract_turns_from_content_detects_colon_markers(self):
        content = "Heading\tAlice Smith\t:\t First speech text.\tBob Jones\t:\t Second speech text."

        turns = extract_turns_from_content(content)

        self.assertEqual(len(turns), 2)
        self.assertEqual(turns[0]["speaker_candidate"], "Alice Smith")
        self.assertEqual(turns[0]["speech_text"], "First speech text.")
        self.assertEqual(turns[0]["confidence"], "medium")
        self.assertEqual(turns[1]["speaker_candidate"], "Bob Jones")

    def test_extract_turns_from_content_returns_empty_without_markers(self):
        turns = extract_turns_from_content("Heading only\tNo colon marker")
        self.assertEqual(turns, [])

    def test_run_segmentation_writes_parquet_and_validation(self):
        case_dir = TEST_TMP / "speech_turns"
        case_dir.mkdir(parents=True, exist_ok=True)
        input_path = case_dir / "hansard.parquet"
        output_path = case_dir / "turns.parquet"
        validation_path = case_dir / "validation.json"

        table = pa.Table.from_pydict(
            {
                "parliament_document_id": ["doc-1", "doc-2"],
                "parliament_number": [47, 47],
                "document_type": ["Hansard - question", "Hansard - speech"],
                "title": ["Title 1", "Title 2"],
                "source_file": ["Hansard-47.csv", "Hansard-47.csv"],
                "source_row_number": [1, 2],
                "content": [
                    "Alice\t:\t Hello.\tBob\t:\t Reply.",
                    "No turn markers here",
                ],
            }
        )
        pq.write_table(table, input_path)

        result = run_segmentation(
            input_path=input_path,
            output_path=output_path,
            validation_path=validation_path,
            batch_size=1,
        )

        self.assertEqual(result["summary"]["documents_read"], 2)
        self.assertEqual(result["summary"]["turns_written"], 2)
        self.assertEqual(result["summary"]["documents_without_turns"], 1)
        self.assertTrue(output_path.exists())

        output = pq.read_table(output_path)
        self.assertEqual(output.num_rows, 2)
        self.assertEqual(output.column("speaker_candidate").to_pylist(), ["Alice", "Bob"])

        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        self.assertEqual(validation["summary"]["turns_written"], 2)


if __name__ == "__main__":
    unittest.main()
