import json
import sys
import unittest
import zipfile
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.normalize_hansard import normalize_row, run_normalization
from test_support import test_tmp_dir

TEST_TMP = test_tmp_dir()


class NormalizeHansardTest(unittest.TestCase):
    def test_normalize_row_maps_contract_fields_and_counts_members(self):
        row = {
            "ParliamentNumber": "47",
            "ParliamentDocumentId": "47HansS_1",
            "DocumentType": "Hansard - question",
            "Title": "Question title",
            "AbbreviatedTitle": "",
            "Status": "Final",
            "Content": "Speech text",
            "MemberOfParliament": "Alice; Bob ; ",
            "Portfolio": "Health;",
            "LastModified": "2007-07-15 00:44:33.743000000",
            "DocumentContentDate": "2007-07-15 00:44:33.743000000",
        }

        normalized, warnings = normalize_row(row, "Hansard-47.csv", 12)

        self.assertEqual(warnings, [])
        self.assertEqual(normalized["stable_id"], "47HansS_1")
        self.assertEqual(normalized["jurisdiction"], "New Zealand")
        self.assertEqual(normalized["country"], "NZ")
        self.assertEqual(normalized["source_file"], "Hansard-47.csv")
        self.assertEqual(normalized["source_row_number"], 12)
        self.assertEqual(normalized["parliament_number"], 47)
        self.assertEqual(normalized["abbreviated_title"], None)
        self.assertEqual(normalized["member_of_parliament_count"], 2)
        self.assertEqual(len(normalized["text_sha256"]), 64)
        self.assertEqual(len(normalized["source_hash"]), 64)
        self.assertEqual(normalized["language"], "en")
        self.assertEqual(normalized["last_modified"], "2007-07-15T00:44:33.743000")
        self.assertEqual(normalized["document_content_date"], "2007-07-15T00:44:33.743000")

    def test_normalize_row_records_parse_warnings(self):
        row = {
            "ParliamentNumber": "not-a-number",
            "ParliamentDocumentId": "id",
            "DocumentType": "type",
            "Title": "title",
            "AbbreviatedTitle": "abbr",
            "Status": "Final",
            "Content": "",
            "MemberOfParliament": "",
            "Portfolio": "",
            "LastModified": "bad-date",
            "DocumentContentDate": "",
        }

        normalized, warnings = normalize_row(row, "Hansard.csv", 1)

        self.assertEqual(normalized["parliament_number"], None)
        self.assertIn("invalid_parliament_number", warnings)
        self.assertIn("missing_content", warnings)
        self.assertIn("invalid_last_modified", warnings)

    def test_run_normalization_writes_parquet_manifest_and_validation(self):
        case_dir = TEST_TMP / "normalize_pipeline"
        case_dir.mkdir(parents=True, exist_ok=True)
        archive_path = case_dir / "sample.zip"
        output_dir = case_dir / "generated"
        manifest_path = case_dir / "manifest.json"
        validation_path = case_dir / "validation.json"

        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(
                "Hansard-47.csv",
                "ParliamentNumber,ParliamentDocumentId,DocumentType,Title,"
                "AbbreviatedTitle,Status,Content,MemberOfParliament,Portfolio,"
                "LastModified,DocumentContentDate\n"
                "47,id-1,type,title,abbr,Final,Text,Alice,Health,"
                "2007-07-15 00:44:33.743000000,2007-07-15 00:44:33.743000000\n",
            )

        result = run_normalization(
            archive_path=archive_path,
            output_dir=output_dir,
            manifest_path=manifest_path,
            validation_path=validation_path,
            batch_size=1,
        )

        parquet_path = Path(result["outputs"]["parquet"])
        self.assertTrue(parquet_path.exists())
        self.assertTrue(manifest_path.exists())
        self.assertTrue(validation_path.exists())

        table = pq.read_table(parquet_path)
        self.assertEqual(table.num_rows, 1)
        self.assertEqual(table.column("stable_id").to_pylist(), ["id-1"])
        self.assertEqual(table.column("parliament_number").to_pylist(), [47])
        self.assertEqual(table.column("content").to_pylist(), ["Text"])

        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        self.assertEqual(validation["summary"]["input_rows"], 1)
        self.assertEqual(validation["summary"]["output_rows"], 1)
        self.assertEqual(validation["summary"]["warning_count"], 0)


if __name__ == "__main__":
    unittest.main()
