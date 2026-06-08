import hashlib
import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.normalize_hansard import normalize_row
from scripts.validate_hansard_records import validate_hansard_records

TEST_TMP = Path(tempfile.gettempdir()) / "corpus-nz-hansard-tests"


class ValidateHansardRecordsTest(unittest.TestCase):
    def test_validate_hansard_records_accepts_normalized_record(self):
        case_dir = TEST_TMP / f"validate_hansard_{uuid.uuid4().hex}"
        case_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = case_dir / "hansard.parquet"
        report_path = case_dir / "validation.json"

        record, warnings = normalize_row(
            {
                "ParliamentNumber": "47",
                "ParliamentDocumentId": "47HansS_1",
                "DocumentType": "Hansard - question",
                "Title": "Question title",
                "AbbreviatedTitle": "",
                "Status": "Final",
                "Content": "Speech text",
                "MemberOfParliament": "Alice",
                "Portfolio": "Health",
                "LastModified": "2007-07-15 00:44:33.743000000",
                "DocumentContentDate": "2007-07-15 00:44:33.743000000",
            },
            "Hansard-47.csv",
            1,
            source_archive="source.zip",
        )
        self.assertEqual(warnings, [])
        pq.write_table(pa.Table.from_pylist([record]), parquet_path)

        report = validate_hansard_records(
            parquet_path=parquet_path,
            schema_path=ROOT / "schemas" / "hansard_record.schema.json",
            report_path=report_path,
        )

        self.assertTrue(report["ok"])
        self.assertEqual(report["record_count"], 1)
        self.assertTrue(report_path.exists())

    def test_validate_hansard_records_detects_hash_mismatch(self):
        case_dir = TEST_TMP / f"validate_hansard_bad_{uuid.uuid4().hex}"
        case_dir.mkdir(parents=True, exist_ok=True)
        parquet_path = case_dir / "hansard.parquet"

        record, _ = normalize_row(
            {
                "ParliamentNumber": "47",
                "ParliamentDocumentId": "47HansS_1",
                "DocumentType": "Hansard - question",
                "Title": "Question title",
                "AbbreviatedTitle": "",
                "Status": "Final",
                "Content": "Speech text",
                "MemberOfParliament": "Alice",
                "Portfolio": "Health",
                "LastModified": "2007-07-15 00:44:33.743000000",
                "DocumentContentDate": "2007-07-15 00:44:33.743000000",
            },
            "Hansard-47.csv",
            1,
            source_archive="source.zip",
        )
        record["text_sha256"] = hashlib.sha256(b"other").hexdigest()
        pq.write_table(pa.Table.from_pylist([record]), parquet_path)

        report = validate_hansard_records(
            parquet_path=parquet_path,
            schema_path=ROOT / "schemas" / "hansard_record.schema.json",
            report_path=None,
        )

        self.assertFalse(report["ok"])
        self.assertIn("text_hash_mismatch", {error["type"] for error in report["errors"]})


if __name__ == "__main__":
    unittest.main()
