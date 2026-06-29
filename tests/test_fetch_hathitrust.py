import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.fetch_hathitrust import (
    EXPECTED_VOLUMES,
    build_inventory_from_hathifile,
    build_inventory_validation,
    build_volume_inventory,
    write_json,
)
from test_support import repo_tmp_dir

TEST_TMP = repo_tmp_dir()


class FetchHathiTrustTest(unittest.TestCase):
    def test_seeded_inventory_is_deterministic_and_blocked(self):
        case_dir = TEST_TMP / "hathitrust_seeded_inventory"
        inventory_path = build_volume_inventory(
            case_dir,
            discovered_ids=[],
            live_probe_attempted=False,
        )

        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["enumerated_count"], 39)
        self.assertEqual(inventory["pending_count"], EXPECTED_VOLUMES - 39)
        self.assertEqual(
            inventory["acquisition_status"],
            "complete-deferred-hathifile-or-oauth-required",
        )
        self.assertIn("uc1.b2940052-81", inventory["enumerated_ids"])

        validation = build_inventory_validation(inventory_path)
        self.assertEqual(validation["release_gate_status"], "blocked")
        self.assertEqual(validation["checks"]["htid_format"]["status"], "pass")
        self.assertEqual(validation["checks"]["source_prefix"]["status"], "pass")
        blocker_ids = {blocker["blocker_id"] for blocker in validation["blockers"]}
        self.assertIn("hathitrust-data-api-oauth-required", blocker_ids)
        self.assertIn("hathifile-or-browser-enumeration-required", blocker_ids)

    def test_validation_records_format_and_prefix_failures(self):
        case_dir = TEST_TMP / "hathitrust_validation_failures"
        inventory_path = case_dir / "volume_inventory.json"
        write_json(
            {
                "collection_id": "71329709",
                "enumerated_ids": ["uc1.b2889853", "miun.invalid", "bad id"],
                "expected_volumes": EXPECTED_VOLUMES,
                "source": "test_fixture",
            },
            inventory_path,
        )

        validation = build_inventory_validation(inventory_path)
        self.assertEqual(validation["checks"]["htid_format"]["status"], "fail")
        self.assertEqual(validation["checks"]["source_prefix"]["status"], "fail")
        self.assertEqual(
            validation["checks"]["source_prefix"]["non_matching_ids"],
            ["bad id", "miun.invalid"],
        )

    def test_hathifile_inventory_filters_to_nz_parliamentary_debates(self):
        case_dir = TEST_TMP / "hathitrust_hathifile"
        hathifile_path = case_dir / "hathi_full_sample.txt"
        case_dir.mkdir(parents=True, exist_ok=True)
        hathifile_path.write_text(
            "\n".join(
                [
                    "\t".join(
                        [
                            "uc1.b2889853",
                            "allow",
                            "pd",
                            "100034544",
                            "vol 1",
                            "uc1",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "New Zealand parliamentary debates",
                            "Wellington",
                            "",
                            "",
                            "",
                            "",
                            "nz",
                            "eng",
                            "SE",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "New Zealand. Parliament.",
                        ],
                    ),
                    "\t".join(
                        [
                            "uc1.noise",
                            "allow",
                            "pd",
                            "1",
                            "",
                            "uc1",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "California parliamentary debates",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "cau",
                            "eng",
                            "BK",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "Other author",
                        ],
                    ),
                ],
            ),
            encoding="utf-8",
        )

        inventory_path = build_inventory_from_hathifile(hathifile_path, case_dir / "out")
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        self.assertEqual(inventory["enumerated_ids"], ["uc1.b2889853"])
        self.assertEqual(inventory["source"], "local_hathifile")

        validation = build_inventory_validation(
            inventory_path,
            access_key_present=False,
            hathifile_path=hathifile_path,
        )
        blocker_ids = {blocker["blocker_id"] for blocker in validation["blockers"]}
        self.assertIn("hathitrust-data-api-oauth-required", blocker_ids)
        self.assertNotIn("local-hathifile-evidence-missing", blocker_ids)


if __name__ == "__main__":
    unittest.main()
