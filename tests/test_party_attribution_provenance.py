from __future__ import annotations

import unittest

import scripts.check_party_attribution_provenance as party_check


class PartyAttributionProvenanceTests(unittest.TestCase):
    def test_package_manifest_boundary(self) -> None:
        manifest = party_check._json(party_check.PACKAGE_MANIFEST_PATH)
        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertEqual(manifest["submission_status"], "not-submitted")
        self.assertEqual(manifest["readiness_status"], "blocked-pending-validated-components")

    def test_review_table_matches_gold_fixture(self) -> None:
        failures = party_check._failures()
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
