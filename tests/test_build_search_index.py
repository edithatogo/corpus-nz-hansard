import json
import sqlite3
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_search_index import build_search_index, chunk_text
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class BuildSearchIndexTest(unittest.TestCase):
    def test_chunk_text_preserves_offsets_and_overlap(self):
        chunks = chunk_text("Alpha beta gamma delta epsilon", max_chars=16, overlap=5)

        self.assertEqual(chunks[0]["start_char"], 0)
        self.assertEqual(chunks[0]["text"], "Alpha beta gamma")
        self.assertGreater(chunks[1]["start_char"], chunks[0]["start_char"])
        self.assertLess(chunks[1]["start_char"], chunks[0]["end_char"])
        self.assertEqual(chunks[-1]["end_char"], len("Alpha beta gamma delta epsilon"))

    def test_build_search_index_creates_fts_chunks_and_validation(self):
        case_dir = TEST_TMP / f"search_index_{uuid.uuid4().hex}"
        case_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = case_dir / "hansard.parquet"
        database_path = case_dir / "hansard_search.sqlite"
        validation_path = case_dir / "search_validation.json"

        table = pa.Table.from_pydict(
            {
                "source_file": ["Hansard-47.csv", "Hansard-47.csv"],
                "source_row_number": [1, 2],
                "parliament_number": [47, 47],
                "parliament_document_id": ["doc-1", "doc-2"],
                "document_type": ["Hansard - debate", "Hansard - question"],
                "title": ["Budget debate", "Health question"],
                "abbreviated_title": ["Budget", "Health"],
                "status": ["Final", "Final"],
                "content": [
                    "The budget debate focused on hospitals and schools.",
                    "The health question focused on hospitals and waiting lists.",
                ],
                "member_of_parliament_raw": ["Alice", "Bob"],
                "member_of_parliament_count": [1, 1],
                "portfolio_raw": ["Finance", "Health"],
                "last_modified": ["2024-01-01T00:00:00", "2024-01-02T00:00:00"],
                "document_content_date": [
                    "2024-01-01T00:00:00",
                    "2024-01-02T00:00:00",
                ],
            }
        )
        pq.write_table(table, parquet_path)

        result = build_search_index(
            parquet_path=parquet_path,
            database_path=database_path,
            validation_path=validation_path,
            max_chars=40,
            overlap=10,
            sample_queries=["hospitals", "budget"],
        )

        self.assertTrue(database_path.exists())
        self.assertTrue(validation_path.exists())
        self.assertEqual(result["summary"]["source_rows"], 2)
        self.assertEqual(result["summary"]["indexed_documents"], 2)
        self.assertGreaterEqual(result["summary"]["indexed_chunks"], 2)
        self.assertGreater(result["sample_queries"]["hospitals"], 0)

        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        self.assertEqual(validation["config"]["max_chars"], 40)
        self.assertEqual(validation["config"]["overlap"], 10)

        with sqlite3.connect(database_path) as connection:
            hits = connection.execute(
                """
                select c.parliament_document_id, c.citation
                from chunks_fts f
                join chunks c on c.chunk_id = f.rowid
                where chunks_fts match ?
                order by bm25(chunks_fts)
                """,
                ("budget",),
            ).fetchall()

        self.assertEqual(hits[0][0], "doc-1")
        self.assertIn("doc-1", hits[0][1])


if __name__ == "__main__":
    unittest.main()
