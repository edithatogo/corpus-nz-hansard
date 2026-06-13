from __future__ import annotations

import unittest

from scripts.build_upstream_submission_execution import build_upstream_submission_execution
from scripts.check_upstream_submission_execution import MANIFEST_PATH, _failures, _json


class UpstreamSubmissionExecutionTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_upstream_submission_execution(generated_at="2026-06-11T00:00:00+10:00")
        self.assertEqual(manifest["submission_state"], "not-submitted")

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["validation_results"]["readiness_boundary"], "local-review-only")
        self.assertEqual(manifest["validation_results"]["blocked_targets"], 6)


if __name__ == "__main__":
    unittest.main()
