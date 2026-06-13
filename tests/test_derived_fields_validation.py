from __future__ import annotations

import unittest

import scripts.validate_derived_fields as derived_validation


class DerivedFieldsValidationTests(unittest.TestCase):
    def test_member_manifest_shape(self) -> None:
        manifest = derived_validation.load_json(
            derived_validation.ROOT / "manifests/member_identity_resolution_validation.json"
        )
        self.assertEqual(derived_validation.validate_manifest(manifest), [])

    def test_party_manifest_shape(self) -> None:
        manifest = derived_validation.load_json(
            derived_validation.ROOT / "manifests/party_attribution_validation.json"
        )
        self.assertEqual(derived_validation.validate_manifest(manifest), [])

    def test_sitting_proceeding_manifest_shape(self) -> None:
        manifest = derived_validation.load_json(
            derived_validation.ROOT / "manifests/sitting_proceeding_component_validation.json"
        )
        self.assertEqual(derived_validation.validate_manifest(manifest), [])

    def test_vote_motion_bill_question_manifest_shape(self) -> None:
        manifest = derived_validation.load_json(
            derived_validation.ROOT
            / "manifests/vote_motion_bill_question_extraction_validation.json"
        )
        self.assertEqual(derived_validation.validate_manifest(manifest), [])

    def test_speech_turn_manifest_shape(self) -> None:
        manifest = derived_validation.load_json(
            derived_validation.ROOT / "manifests/speech_turn_validated_artifact_validation.json"
        )
        self.assertEqual(derived_validation.validate_manifest(manifest), [])

    def test_gold_sample_counts(self) -> None:
        counts = derived_validation.gold_sample_counts("member_resolution")
        self.assertEqual(counts["sample_total"], 5)
        self.assertEqual(counts["positive"], 1)
        self.assertEqual(counts["negative"], 1)
        self.assertEqual(counts["ambiguous"], 1)
        self.assertEqual(counts["unresolved"], 1)
        self.assertEqual(counts["excluded"], 1)

    def test_segmentation_counts(self) -> None:
        counts = derived_validation.segmentation_counts()
        self.assertEqual(counts["turns_written"], 439)
        self.assertEqual(counts["medium_confidence"], 439)


if __name__ == "__main__":
    unittest.main()
