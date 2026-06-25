from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.check_hathitrust_acquisition import MANIFEST_PATH, _failures
from scripts.fetch_hathitrust import (
    EXPECTED_VOLUMES,
    KNOWN_WAYBACK_SAMPLE_IDS,
    build_volume_inventory,
)
from test_support import repo_tmp_dir

TEST_TMP = repo_tmp_dir()


class HathiTrustAcquisitionTests(unittest.TestCase):
    def test_inventory_uses_seed_when_live_probe_returns_no_ids(self) -> None:
        output_path = build_volume_inventory(
            TEST_TMP / "hathitrust_seeded_inventory",
            discovered_ids=[],
            live_probe_attempted=True,
        )
        inventory = json.loads(Path(output_path).read_text(encoding="utf-8"))

        self.assertEqual(
            inventory["artifact_name"],
            "hathitrust_hansard_acquisition_inventory",
        )
        self.assertEqual(inventory["expected_volumes"], EXPECTED_VOLUMES)
        self.assertEqual(inventory["live_wayback_discovered_count"], 0)
        self.assertEqual(inventory["seeded_wayback_sample_count"], len(KNOWN_WAYBACK_SAMPLE_IDS))
        self.assertEqual(inventory["enumerated_count"], len(KNOWN_WAYBACK_SAMPLE_IDS))
        self.assertEqual(
            inventory["pending_count"],
            EXPECTED_VOLUMES - len(KNOWN_WAYBACK_SAMPLE_IDS),
        )
        self.assertEqual(
            inventory["acquisition_status"], "complete-deferred-hathifile-or-oauth-required"
        )

    def test_inventory_merges_live_ids_with_seed(self) -> None:
        output_path = build_volume_inventory(
            TEST_TMP / "hathitrust_live_inventory_merge",
            discovered_ids=["uc1.zz999999", KNOWN_WAYBACK_SAMPLE_IDS[0]],
            live_probe_attempted=True,
        )
        inventory = json.loads(Path(output_path).read_text(encoding="utf-8"))

        self.assertIn("uc1.zz999999", inventory["enumerated_ids"])
        self.assertEqual(inventory["live_wayback_discovered_count"], 2)
        self.assertEqual(inventory["enumerated_count"], len(KNOWN_WAYBACK_SAMPLE_IDS) + 1)

    def test_repo_manifest_is_consistent(self) -> None:
        self.assertTrue(MANIFEST_PATH.exists())
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
