import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.canonical_ids import canonical_id, canonical_uri, component_payload
from scripts.check_canonical_id_uri_policy import MANIFEST_PATH, _failures, _json


class CanonicalIdUriPolicyTest(unittest.TestCase):
    def test_component_id_generation_is_deterministic(self):
        payload = component_payload(
            release_version="0.1.0",
            component_type="speech-turn",
            source_stable_id="47HansS_20050217_00000759",
            local_key="turn-0001",
            validation_manifest="manifests/speech_turn_validated_artifact_validation.json",
        )

        self.assertEqual(
            canonical_id("neutral-component", payload), "nzhc-component-0dc17fbde51c939f"
        )

    def test_uri_generation_is_deterministic(self):
        identifier = "nzhc-document-8e93abc58c9b722f"

        self.assertEqual(
            canonical_uri("document", identifier),
            "https://w3id.org/nz-hansard/document/nzhc-document-8e93abc58c9b722f",
        )

    def test_manifest_examples_match_helpers(self):
        manifest = _json(MANIFEST_PATH)

        for example in manifest["examples"]:
            self.assertEqual(
                canonical_id(example["artifact_class"], example["payload"]), example["expected_id"]
            )

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
