from __future__ import annotations

import unittest

import scripts.check_ud_conllu_endpoint as ud_check


class UdConlluEndpointTests(unittest.TestCase):
    def test_sample_package_files_exist(self) -> None:
        self.assertTrue(ud_check.CONLLU_PATH.exists())
        self.assertTrue(ud_check.ALIGNMENT_PATH.exists())
        self.assertTrue(ud_check.README_PATH.exists())

    def test_manifest_boundary(self) -> None:
        manifest = ud_check._json(ud_check.MANIFEST_PATH)
        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertEqual(manifest["release_level"], "upstream-contribution")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )
        self.assertEqual(set(manifest["dependency_groups"]), ud_check.REQUIRED_DEPENDENCY_GROUPS)

    def test_checker_passes(self) -> None:
        self.assertEqual(ud_check._failures(), [])


if __name__ == "__main__":
    unittest.main()
