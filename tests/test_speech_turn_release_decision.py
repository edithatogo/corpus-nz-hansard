from __future__ import annotations

import json
import unittest
from pathlib import Path

import scripts.check_speech_turn_release_decision as decision_check

ROOT = Path(__file__).resolve().parents[1]


class SpeechTurnReleaseDecisionTests(unittest.TestCase):
    def test_manifest_shape(self) -> None:
        manifest = decision_check.load_json(decision_check.DECISION_MANIFEST_PATH)
        self.assertEqual(decision_check.validate_manifest(manifest), [])

    def test_gold_fixture_covers_reviewed_speech_turn_cases(self) -> None:
        fixture = json.loads(
            (ROOT / "fixtures/gold_evaluation_samples.json").read_text(encoding="utf-8")
        )
        speech_turn_samples = [
            sample for sample in fixture["samples"] if sample["domain"] == "speech_turn"
        ]
        self.assertEqual(
            [sample["sample_id"] for sample in speech_turn_samples],
            [
                "gold-speech-turn-01",
                "gold-speech-turn-02",
                "gold-speech-turn-03",
                "gold-speech-turn-04",
                "gold-speech-turn-05",
            ],
        )
        self.assertEqual(
            [sample["example_class"] for sample in speech_turn_samples],
            [
                "positive",
                "negative",
                "ambiguous",
                "unresolved",
                "excluded",
            ],
        )

    def test_decision_checker_passes(self) -> None:
        self.assertEqual(decision_check._failures(), [])


if __name__ == "__main__":
    unittest.main()
