from __future__ import annotations

import unittest

from scripts.build_sitting_proceeding_component import build_sitting_proceeding_component
from scripts.check_sitting_proceeding_component import MANIFEST_PATH, _failures, _json


class SittingProceedingComponentTests(unittest.TestCase):
    def test_builder_emits_blocked_manifest_and_outputs(self) -> None:
        manifest = build_sitting_proceeding_component(
            manifest_path=None,
            coverage_path=None,
            review_path=None,
            generated_at="2026-06-10T00:00:00+10:00",
        )
        self.assertEqual(manifest["validation_status"], "blocked")
        self.assertEqual(manifest["release_gate_status"], "blocked-pending-official-reconciliation")
        self.assertEqual(manifest["counts"]["fixture_sittings"], 1)
        self.assertEqual(manifest["counts"]["fixture_proceeding_items"], 1)

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["artifact_name"], "sitting_proceeding_component_validation")
        self.assertEqual(manifest["validation_status"], "blocked")


if __name__ == "__main__":
    unittest.main()
