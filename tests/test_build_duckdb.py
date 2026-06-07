import json
import sys
import unittest
import uuid
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_duckdb import build_duckdb_database

TEST_TMP = ROOT / ".tmp" / "tests"


class BuildDuckdbTest(unittest.TestCase):
    def test_build_duckdb_database_loads_parquet_and_writes_validation(self):
        case_dir = TEST_TMP / f"duckdb_build_{uuid.uuid4().hex}"
        case_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = case_dir / "hansard.parquet"
        database_path = case_dir / "hansard.duckdb"
        validation_path = case_dir / "duckdb_validation.json"

        table = pa.Table.from_pydict(
            {
                "source_file": ["Hansard-47.csv", "Hansard-48.csv"],
                "source_row_number": [1, 1],
                "parliament_number": [47, 48],
                "parliament_document_id": ["id-1", "id-2"],
                "document_type": ["question", "debate"],
                "title": ["Title 1", "Title 2"],
                "abbreviated_title": ["T1", "T2"],
                "status": ["Final", "Final"],
                "content": ["Text one", "Text two"],
                "member_of_parliament_raw": ["Alice", "Bob"],
                "member_of_parliament_count": [1, 1],
                "portfolio_raw": ["Health", None],
                "last_modified": ["2024-01-01T00:00:00", "2024-01-02T00:00:00"],
                "document_content_date": [
                    "2024-01-01T00:00:00",
                    "2024-01-02T00:00:00",
                ],
            }
        )
        pq.write_table(table, parquet_path)

        result = build_duckdb_database(
            parquet_path=parquet_path,
            database_path=database_path,
            validation_path=validation_path,
            expected_rows=2,
        )

        self.assertEqual(result["summary"]["row_count"], 2)
        self.assertEqual(result["summary"]["expected_rows"], 2)
        self.assertTrue(database_path.exists())
        self.assertTrue(validation_path.exists())

        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        self.assertEqual(validation["summary"]["row_count"], 2)
        self.assertEqual(validation["rows_by_parliament_number"]["47"], 1)

        with duckdb.connect(str(database_path), read_only=True) as connection:
            count = connection.execute("select count(*) from hansard").fetchone()[0]
            self.assertEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
