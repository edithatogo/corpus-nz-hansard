import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_metadata_packages import MANIFEST_PATH, _failures, _json


class MetadataPackagesTest(unittest.TestCase):
    def test_manifest_names_all_required_package_targets(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(manifest["repository"], "corpus-nz-hansard")
        self.assertEqual(manifest["corpus_family_sibling"], "corpus-nz-legislation")
        self.assertFalse(manifest["publication_claims_allowed"])

        packages = {package["id"]: package for package in manifest["packages"]}
        self.assertEqual(
            set(packages),
            {"croissant", "ro-crate", "frictionless", "dcat", "prov-o"},
        )
        self.assertEqual(packages["croissant"]["format"], "json-ld")
        self.assertEqual(packages["frictionless"]["format"], "json")
        self.assertEqual(packages["dcat"]["format"], "turtle")
        self.assertEqual(packages["prov-o"]["format"], "turtle")

    def test_metadata_package_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
