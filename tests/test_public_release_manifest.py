import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_public_release_manifest import build_release_manifest, write_manifest

TEST_TMP = ROOT / ".tmp" / "tests"


class PublicReleaseManifestTest(unittest.TestCase):
    def test_build_release_manifest_combines_existing_pipeline_evidence(self):
        case_dir = TEST_TMP / "public_release_manifest"
        case_dir.mkdir(parents=True, exist_ok=True)
        source_inventory = case_dir / "source.json"
        schema_discovery = case_dir / "schema.json"
        normalization_validation = case_dir / "normalization.json"
        record_schema_validation = case_dir / "record_schema.json"
        duckdb_validation = case_dir / "duckdb.json"

        source_inventory.write_text(
            json.dumps(
                {
                    "source_archive": {"sha256": "abc", "name": "source.zip"},
                    "summary": {"member_count": 8},
                }
            ),
            encoding="utf-8",
        )
        schema_discovery.write_text(
            json.dumps({"summary": {"file_count": 8, "total_rows": 10}}),
            encoding="utf-8",
        )
        normalization_validation.write_text(
            json.dumps(
                {
                    "summary": {
                        "input_rows": 10,
                        "output_rows": 10,
                        "warning_count": 0,
                    }
                }
            ),
            encoding="utf-8",
        )
        record_schema_validation.write_text(
            json.dumps(
                {
                    "record_count": 10,
                    "ok": True,
                    "errors": [],
                    "warnings": [],
                }
            ),
            encoding="utf-8",
        )
        duckdb_validation.write_text(
            json.dumps(
                {
                    "summary": {
                        "row_count": 10,
                        "row_count_matches_expected": True,
                    }
                }
            ),
            encoding="utf-8",
        )

        manifest = build_release_manifest(
            source_inventory_path=source_inventory,
            schema_discovery_path=schema_discovery,
            normalization_validation_path=normalization_validation,
            record_schema_validation_path=record_schema_validation,
            duckdb_validation_path=duckdb_validation,
        )

        self.assertEqual(manifest["source"]["sha256"], "abc")
        self.assertEqual(manifest["counts"]["normalized_rows"], 10)
        self.assertEqual(manifest["counts"]["schema_validated_rows"], 10)
        self.assertEqual(manifest["quality"]["normalization_warnings"], 0)
        self.assertTrue(manifest["quality"]["record_schema_valid"])
        self.assertEqual(manifest["publication_status"], "prepared_for_review")
        self.assertFalse(manifest["published"])

    def test_write_manifest_creates_parent_directory(self):
        output_path = TEST_TMP / "public_release_write" / "manifest.json"
        write_manifest({"ok": True}, output_path)
        self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
