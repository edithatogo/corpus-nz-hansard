from __future__ import annotations

import unittest

import scripts.check_upstream_contribution_packages as upstream_check


class UpstreamContributionPackagesTests(unittest.TestCase):
    def test_manifest_boundary(self) -> None:
        manifest = upstream_check._json(upstream_check.MANIFEST_PATH)
        self.assertEqual(manifest["release_status"], "local-review-only")
        self.assertEqual(manifest["submission_status"], "not-submitted")
        self.assertTrue(manifest["validation_results"]["package_catalogued"])

    def test_package_catalog(self) -> None:
        failures = upstream_check._failures()
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
