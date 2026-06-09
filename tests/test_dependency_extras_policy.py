import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_dependency_extras_policy import (
    MANIFEST_PATH,
    REQUIRED_GROUPS,
    REQUIRED_VALIDATION_FIELDS,
    _failures,
    _json,
    _requirement_names,
)


class DependencyExtrasPolicyTest(unittest.TestCase):
    def test_optional_groups_cover_required_domains(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual({group["group"] for group in manifest["optional_groups"]}, REQUIRED_GROUPS)

    def test_base_runtime_excludes_heavy_endpoint_stacks(self):
        manifest = _json(MANIFEST_PATH)
        base_names = _requirement_names(ROOT / manifest["base_runtime"]["requirements_file"])

        prohibited = {
            dependency.replace("_", "-").lower()
            for dependency in manifest["prohibited_base_dependencies"]
        }
        self.assertTrue(prohibited.isdisjoint(base_names))

    def test_endpoint_requirements_declare_groups_and_versions(self):
        manifest = _json(MANIFEST_PATH)

        for endpoint in manifest["endpoint_requirements"]:
            self.assertTrue(endpoint["required_groups"])
            self.assertTrue(
                REQUIRED_VALIDATION_FIELDS.issubset(endpoint["validation_manifest_fields"])
            )
            self.assertIn("Pin", endpoint["release_affecting_dependencies"])

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
