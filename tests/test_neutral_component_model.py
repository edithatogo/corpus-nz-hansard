import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_neutral_component_model import (
    FIXTURE_PATH,
    MANIFEST_PATH,
    REQUIRED_COMMON_FIELDS,
    REQUIRED_FAMILIES,
    _component_index,
    _failures,
    _json,
)


class NeutralComponentModelTest(unittest.TestCase):
    def test_manifest_defines_required_families(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(
            {family["family_id"] for family in manifest["component_families"]},
            REQUIRED_FAMILIES,
        )

    def test_common_fields_are_required(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(set(manifest["common_required_fields"]), REQUIRED_COMMON_FIELDS)

    def test_fixtures_cover_required_families(self):
        fixtures = _json(FIXTURE_PATH)

        self.assertEqual(set(fixtures["components"]), REQUIRED_FAMILIES)

    def test_fixture_references_resolve(self):
        manifest = _json(MANIFEST_PATH)
        fixtures = _json(FIXTURE_PATH)
        index = _component_index(fixtures)

        for rule in manifest["referential_integrity"]:
            for row in fixtures["components"][rule["source_family"]]:
                self.assertEqual(index[row[rule["field"]]], rule["target_family"])

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
