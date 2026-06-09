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
        self.assertTrue(manifest["publication_claims_allowed"])

        packages = {package["id"]: package for package in manifest["packages"]}
        self.assertEqual(
            set(packages),
            {"croissant", "ro-crate", "frictionless", "dcat", "prov-o"},
        )
        self.assertEqual(packages["croissant"]["format"], "json-ld")
        self.assertEqual(packages["frictionless"]["format"], "json")
        self.assertEqual(packages["dcat"]["format"], "turtle")
        self.assertEqual(packages["prov-o"]["format"], "turtle")
        self.assertEqual({package["status"] for package in packages.values()}, {"generated"})
        self.assertTrue(all(package["checksum"] for package in packages.values()))

    def test_metadata_package_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])

    def test_generated_package_files_have_expected_shapes(self):
        manifest = _json(MANIFEST_PATH)
        packages = {package["id"]: package for package in manifest["packages"]}

        croissant = _json(ROOT / packages["croissant"]["output_path"])
        self.assertEqual(croissant["@type"], "sc:Dataset")
        self.assertTrue(croissant["recordSet"][0]["field"])

        ro_crate = _json(ROOT / packages["ro-crate"]["output_path"])
        self.assertEqual(ro_crate["@context"], "https://w3id.org/ro/crate/1.1/context")

        datapackage = _json(ROOT / packages["frictionless"]["output_path"])
        self.assertEqual(datapackage["profile"], "data-package")

        dcat = (ROOT / packages["dcat"]["output_path"]).read_text(encoding="utf-8")
        self.assertIn("dcat:Dataset", dcat)

        prov = (ROOT / packages["prov-o"]["output_path"]).read_text(encoding="utf-8")
        self.assertIn("prov:Activity", prov)


if __name__ == "__main__":
    unittest.main()
