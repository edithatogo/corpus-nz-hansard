from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_speech_act_procedure_classifiers import build_speech_act_procedure_classifiers
from scripts.check_speech_act_procedure_classifiers import MANIFEST_PATH, _failures, _json


class SpeechActProcedureClassifiersTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_speech_act_procedure_classifiers(generated_at="2026-06-11T00:00:00+10:00")
        self.assertEqual(manifest["status"], "blocked")
        self.assertEqual(manifest["release_status"], "blocked-pending-validated-speech-turn")

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["validation_results"]["blocked_by_speech_turn_gate"], True)
        self.assertGreaterEqual(len(manifest["label_families"]), 4)


if __name__ == "__main__":
    unittest.main()
