import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_release_ladder import MANIFEST_PATH, REQUIRED_LEVELS, _failures, _json


class ReleaseLadderTest(unittest.TestCase):
    def test_defines_required_levels(self):
        manifest = _json(MANIFEST_PATH)
        levels = {level["id"] for level in manifest["release_levels"]}

        self.assertEqual(levels, REQUIRED_LEVELS)

    def test_current_release_remains_document_level(self):
        manifest = _json(MANIFEST_PATH)
        current = manifest["current_public_release"]

        self.assertEqual(current["version"], "0.1.0")
        self.assertEqual(current["release_level"], "document-level")
        self.assertIn("immutable", current["immutable_policy"])

    def test_artifact_map_separates_future_levels(self):
        manifest = _json(MANIFEST_PATH)
        artifacts = {item["artifact"]: item for item in manifest["artifact_map"]}

        self.assertEqual(
            artifacts["public dataset release manifest"]["release_level"], "document-level"
        )
        self.assertEqual(
            artifacts["authority source discovery"]["release_level"], "authority-source"
        )
        self.assertEqual(artifacts["component contracts"]["release_level"], "neutral-component")
        self.assertEqual(artifacts["endpoint contracts"]["release_level"], "endpoint")
        self.assertEqual(
            artifacts["upstream contribution packages"]["release_level"], "upstream-contribution"
        )

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
