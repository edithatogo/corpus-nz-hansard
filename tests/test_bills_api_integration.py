from __future__ import annotations

import unittest

from scripts.build_bills_api_integration import build_bills_api_integration
from scripts.check_bills_api_integration import MANIFEST_PATH, _failures, _json


class BillsApiIntegrationTests(unittest.TestCase):
    def test_builder_emits_metadata_ready_manifest(self) -> None:
        manifest = build_bills_api_integration(
            manifest_path=None,
            crossref_path=None,
            legacy_crossref_path=None,
            stage_metadata_path=None,
            generated_at="2026-06-23T09:02:54+00:00",
        )
        self.assertEqual(manifest["track_id"], "bills_api_integration_20260612")
        self.assertTrue(manifest["authority_source_registered"])
        self.assertGreaterEqual(manifest["extraction_run"]["bill_details_processed"], 3513)
        self.assertEqual(manifest["extraction_run"]["unique_member_names"], 351)
        self.assertEqual(manifest["corpus_metadata_integration"]["status"], "ready")
        self.assertEqual(
            manifest["release_gate_status"],
            "ready-for-corpus-metadata-integration",
        )

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["artifact_name"], "bills_api_integration_validation")
        self.assertEqual(manifest["validation_status"], "metadata-ready")
        self.assertEqual(
            manifest["release_gate_status"],
            "ready-for-corpus-metadata-integration",
        )


if __name__ == "__main__":
    unittest.main()
