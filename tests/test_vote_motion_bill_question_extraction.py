from __future__ import annotations

import unittest

from scripts.build_vote_motion_bill_question_extraction import (
    build_vote_motion_bill_question_extraction,
)
from scripts.check_vote_motion_bill_question_extraction import MANIFEST_PATH, _failures, _json


class VoteMotionBillQuestionExtractionTests(unittest.TestCase):
    def test_builder_emits_blocked_manifest_and_outputs(self) -> None:
        manifest = build_vote_motion_bill_question_extraction(
            manifest_path=None,
            coverage_path=None,
            review_path=None,
            generated_at="2026-06-10T00:00:00+10:00",
        )
        self.assertEqual(manifest["validation_status"], "blocked")
        self.assertEqual(
            manifest["release_gate_status"], "blocked-pending-validated-components"
        )
        self.assertEqual(manifest["counts"]["procedure_samples_reviewed"], 6)

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(
            manifest["artifact_name"], "vote_motion_bill_question_extraction_validation"
        )
        self.assertEqual(manifest["validation_status"], "blocked")


if __name__ == "__main__":
    unittest.main()
