from __future__ import annotations

import unittest

import scripts.check_rdf_linked_data_endpoint as rdf_check


class RdfLinkedDataEndpointTests(unittest.TestCase):
    def test_sample_package_files_exist(self) -> None:
        self.assertTrue(rdf_check.TURTLE_PATH.exists())
        self.assertTrue(rdf_check.JSONLD_PATH.exists())
        self.assertTrue(rdf_check.SHAPES_PATH.exists())
        self.assertTrue(rdf_check.SPARQL_PATH.exists())
        self.assertTrue(rdf_check.README_PATH.exists())

    def test_manifest_boundary(self) -> None:
        manifest = rdf_check._json(rdf_check.MANIFEST_PATH)
        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertEqual(manifest["release_level"], "upstream-contribution")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )
        self.assertEqual(set(manifest["dependency_groups"]), rdf_check.REQUIRED_DEPENDENCY_GROUPS)

    def test_checker_passes(self) -> None:
        self.assertEqual(rdf_check._failures(), [])


if __name__ == "__main__":
    unittest.main()
