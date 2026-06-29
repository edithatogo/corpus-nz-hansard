from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_speech_act_procedure_classifiers import build_speech_act_procedure_classifiers
from scripts.check_speech_act_procedure_classifiers import (
    EVALUATION_PATH,
    MANIFEST_PATH,
    _failures,
    _json,
)


class SpeechActProcedureClassifiersTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_speech_act_procedure_classifiers(generated_at="2026-06-11T00:00:00+10:00")
        self.assertEqual(manifest["status"], "release-ready")
        self.assertEqual(manifest["release_status"], "release-ready-baseline-plan-human-validation")
        self.assertEqual(
            manifest["evaluation_artifacts"]["publication_status"],
            "fixture-evaluation-only-not-authoritative",
        )

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["validation_results"]["blocked_by_speech_turn_gate"], False)
        self.assertEqual(manifest["validation_results"]["selector_checks_passed"], True)
        self.assertGreaterEqual(len(manifest["label_families"]), 4)

    def test_fixture_evaluation_was_written(self) -> None:
        evaluation = _json(EVALUATION_PATH)
        self.assertEqual(
            evaluation["publication_status"], "fixture-evaluation-only-not-authoritative"
        )
        self.assertTrue(evaluation["metrics"]["selector_checks_passed"])
        self.assertGreaterEqual(evaluation["metrics"]["reviewed_fixture_count"], 1)


if __name__ == "__main__":
    unittest.main()
