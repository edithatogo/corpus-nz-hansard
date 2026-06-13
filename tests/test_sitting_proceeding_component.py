from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.build_sitting_proceeding_component import build_sitting_proceeding_component
from scripts.check_sitting_proceeding_component import MANIFEST_PATH, _failures, _json


class SittingProceedingComponentTests(unittest.TestCase):
    def test_builder_emits_blocked_manifest_and_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest_path = tmp_path / "manifest.json"
            coverage_path = tmp_path / "coverage.json"
            review_path = tmp_path / "review.csv"
            manifest = build_sitting_proceeding_component(
                manifest_path=manifest_path,
                coverage_path=coverage_path,
                review_path=review_path,
                generated_at="2026-06-10T00:00:00+10:00",
            )
            self.assertEqual(manifest["validation_status"], "blocked")
            self.assertEqual(
                manifest["release_gate_status"], "blocked-pending-official-reconciliation"
            )
            self.assertEqual(manifest["counts"]["fixture_sittings"], 1)
            self.assertEqual(manifest["counts"]["fixture_proceeding_items"], 1)
            self.assertTrue(manifest_path.exists())
            self.assertTrue(coverage_path.exists())
            self.assertTrue(review_path.exists())

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["artifact_name"], "sitting_proceeding_component_validation")
        self.assertEqual(manifest["validation_status"], "blocked")


if __name__ == "__main__":
    unittest.main()
