import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_historical_sitting_inventory import (
    EXPECTED_SOURCE_IDS,
    MANIFEST_PATH,
    _failures,
    _json,
)


class HistoricalSittingInventoryTest(unittest.TestCase):
    def test_inventory_contains_expected_official_sources(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual({item["id"] for item in manifest["sources"]}, EXPECTED_SOURCE_IDS)
        self.assertEqual(manifest["inventory_status"], "source-inventory-only")
        self.assertEqual(manifest["reconciliation_status"], "pending-comparison")
        self.assertGreaterEqual(len(manifest["sources"]), 8)

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
