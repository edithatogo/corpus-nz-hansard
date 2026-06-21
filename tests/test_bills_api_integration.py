from __future__ import annotations

import unittest

from scripts.build_bills_api_integration import build_bills_api_integration
from scripts.check_bills_api_integration import MANIFEST_PATH, _failures, _json


class BillsApiIntegrationTests(unittest.TestCase):
    def test_builder_emits_review_evidence_manifest(self) -> None:
        manifest = build_bills_api_integration(
            manifest_path=None,
            crossref_path=None,
            legacy_crossref_path=None,
            generated_at="2026-06-12T00:00:00+10:00",
        )
        self.assertEqual(manifest["track_id"], "bills_api_integration_20260612")
        self.assertTrue(manifest["authority_source_registered"])
        self.assertEqual(manifest["extraction_run"]["bill_details_processed"], 3513)
        self.assertEqual(manifest["extraction_run"]["unique_member_names"], 351)
        self.assertEqual(manifest["corpus_metadata_integration"]["status"], "deferred")

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["artifact_name"], "bills_api_integration_validation")
        self.assertEqual(
            manifest["release_gate_status"],
            "deferred-pending-full-stage-record-capture",
        )


if __name__ == "__main__":
    unittest.main()
