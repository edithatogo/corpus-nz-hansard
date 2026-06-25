from __future__ import annotations

import unittest

from scripts.build_vote_motion_bill_question_extraction import (
    build_vote_motion_bill_question_extraction,
)
from scripts.check_vote_motion_bill_question_extraction import MANIFEST_PATH, _failures, _json


class VoteMotionBillQuestionExtractionTests(unittest.TestCase):
    def test_builder_emits_release_ready_manifest_and_outputs(self) -> None:
        manifest = build_vote_motion_bill_question_extraction(
            manifest_path=None,
            coverage_path=None,
            review_path=None,
            generated_at="2026-06-10T00:00:00+10:00",
        )
        self.assertEqual(manifest["validation_status"], "ok")
        self.assertEqual(
            manifest["release_gate_status"],
            "release-ready-fixture-reviewed-extraction-agent-review",
        )
        self.assertEqual(manifest["counts"]["procedure_samples_reviewed"], 6)
        self.assertEqual(manifest["counts"]["validated_rows"], 5)
        self.assertEqual(manifest["counts"]["blocked_rows"], 0)
        self.assertEqual(manifest["counts"]["excluded_rows"], 1)

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(
            manifest["artifact_name"], "vote_motion_bill_question_extraction_validation"
        )
        self.assertEqual(manifest["validation_status"], "ok")


if __name__ == "__main__":
    unittest.main()
