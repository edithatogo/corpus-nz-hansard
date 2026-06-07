import hashlib
import json
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.inventory_archive import build_inventory, write_inventory

TEST_TMP = ROOT / ".tmp" / "tests"


class InventoryArchiveTest(unittest.TestCase):
    def test_build_inventory_records_archive_and_member_hashes(self):
        with self.subTest("small zip fixture"):
            case_dir = TEST_TMP / "inventory_members"
            case_dir.mkdir(parents=True, exist_ok=True)
            archive_path = case_dir / "sample.zip"
            first = b"alpha\n"
            second = b"beta\n"

            with zipfile.ZipFile(
                archive_path, "w", compression=zipfile.ZIP_DEFLATED
            ) as archive:
                archive.writestr("folder/one.csv", first)
                archive.writestr("folder/two.csv", second)

            inventory = build_inventory(archive_path)

            self.assertEqual(inventory["source_archive"]["name"], "sample.zip")
            self.assertEqual(
                inventory["source_archive"]["sha256"],
                hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            )
            self.assertEqual(inventory["summary"]["member_count"], 2)
            self.assertEqual(
                inventory["summary"]["total_uncompressed_size"],
                len(first) + len(second),
            )

            members = {member["name"]: member for member in inventory["members"]}
            self.assertEqual(
                members["folder/one.csv"]["sha256"],
                hashlib.sha256(first).hexdigest(),
            )
            self.assertEqual(
                members["folder/two.csv"]["sha256"],
                hashlib.sha256(second).hexdigest(),
            )
            self.assertEqual(members["folder/one.csv"]["uncompressed_size"], len(first))
            self.assertGreater(members["folder/two.csv"]["compressed_size"], 0)

    def test_write_inventory_creates_json_parent_directories(self):
        root = TEST_TMP / "write_inventory"
        root.mkdir(parents=True, exist_ok=True)
        archive_path = root / "sample.zip"
        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            archive.writestr("sample.csv", "a,b\n1,2\n")

        output_path = root / "nested" / "source_inventory.json"
        inventory = build_inventory(archive_path)
        write_inventory(inventory, output_path)

        written = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(written["source_archive"]["path"], str(archive_path))
        self.assertEqual(written["members"][0]["name"], "sample.csv")


if __name__ == "__main__":
    unittest.main()
