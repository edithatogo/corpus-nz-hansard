import json
import sys
import unittest
import uuid
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_historical_sitting_reconciliation import build_historical_sitting_ledger
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class BuildHistoricalSittingReconciliationTest(unittest.TestCase):
    def test_build_historical_sitting_ledger_writes_parquet_and_summary(self):
        case_dir = TEST_TMP / f"historical_sitting_reconciliation_{uuid.uuid4().hex}"
        case_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = case_dir / "hansard.parquet"
        ledger_path = case_dir / "historical_sitting_ledger.parquet"
        summary_path = case_dir / "historical_sitting_ledger_summary.json"

        table = pa.Table.from_pydict(
            {
                "stable_id": ["row-1", "row-2"],
                "source_file": ["Hansard-47.csv", "Hansard-47.csv"],
                "source_row_number": [1, 2],
                "parliament_number": [47, 47],
                "document_type": ["Hansard - question", "Hansard - vote"],
                "title": ["Question title", "Vote title"],
                "content": [
                    "Intro text. Sitting date: 16 June 2004. [Volume:624;Page:19111]",
                    "Other text without a sitting date but with [Volume:606;Page:3763]",
                ],
            }
        )
        pq.write_table(table, parquet_path)

        result = build_historical_sitting_ledger(
            parquet_path=parquet_path,
            ledger_path=ledger_path,
            summary_path=summary_path,
        )

        self.assertTrue(ledger_path.exists())
        self.assertTrue(summary_path.exists())
        self.assertEqual(result["summary"]["row_count"], 2)
        self.assertEqual(result["summary"]["sitting_date_extracted_rows"], 1)
        self.assertEqual(result["summary"]["volume_page_extracted_rows"], 2)
        self.assertEqual(result["summary"]["parliament_counts"]["47"], 2)

        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        self.assertEqual(summary["row_count"], 2)
        self.assertEqual(summary["publication_surface_counts"]["Hansard"], 2)

        ledger = pq.read_table(ledger_path)
        rows = ledger.to_pylist()
        self.assertEqual(rows[0]["sitting_date"], "16 June 2004")
        self.assertEqual(rows[0]["volume"], "624")
        self.assertEqual(rows[0]["page"], "19111")
        self.assertEqual(rows[1]["extraction_status"], "partial")


if __name__ == "__main__":
    unittest.main()
