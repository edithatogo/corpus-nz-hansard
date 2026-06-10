from __future__ import annotations

import unittest

import scripts.check_akoma_ntoso_endpoint as akoma_check


class AkomaNtosoEndpointTests(unittest.TestCase):
    def test_sample_package_files_exist(self) -> None:
        self.assertTrue(akoma_check.SAMPLE_XML_PATH.exists())
        self.assertTrue(akoma_check.METADATA_XML_PATH.exists())
        self.assertTrue(akoma_check.SAMPLE_README_PATH.exists())

    def test_manifest_boundary(self) -> None:
        manifest = akoma_check._json(akoma_check.MANIFEST_PATH)
        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertEqual(manifest["release_level"], "upstream-contribution")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )
        self.assertEqual(set(manifest["dependency_groups"]), akoma_check.REQUIRED_DEPENDENCY_GROUPS)

    def test_checker_passes(self) -> None:
        self.assertEqual(akoma_check._failures(), [])


if __name__ == "__main__":
    unittest.main()
