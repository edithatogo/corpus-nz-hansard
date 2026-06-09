import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_nz_parliamentary_procedure_model import (
    FIXTURE_PATH,
    MANIFEST_PATH,
    REQUIRED_CATEGORIES,
    REQUIRED_FIXTURE_CATEGORIES,
    REQUIRED_LINKS,
    _failures,
    _json,
)


class NzParliamentaryProcedureModelTest(unittest.TestCase):
    def test_manifest_defines_required_categories(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(
            {item["category"] for item in manifest["procedural_categories"]},
            REQUIRED_CATEGORIES,
        )

    def test_component_links_cover_required_targets(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(set(manifest["component_links"]), REQUIRED_LINKS)

    def test_fixtures_cover_required_boundaries(self):
        fixtures = _json(FIXTURE_PATH)

        self.assertTrue(
            REQUIRED_FIXTURE_CATEGORIES.issubset(
                {sample["category"] for sample in fixtures["samples"]}
            )
        )

    def test_fixtures_are_reviewed_not_model_generated(self):
        fixtures = _json(FIXTURE_PATH)

        for sample in fixtures["samples"]:
            self.assertEqual(sample["review"]["review_status"], "reviewed")
            self.assertFalse(sample["review"]["model_generated_label"])

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
