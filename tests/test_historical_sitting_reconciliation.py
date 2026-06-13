import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_historical_sitting_reconciliation import (  # noqa: E402
    MANIFEST_PATH,
    _failures,
    _json,
)


class HistoricalSittingReconciliationTest(unittest.TestCase):
    def test_reconciliation_contract_shape(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(manifest["artifact_name"], "historical_sitting_reconciliation")
        self.assertEqual(manifest["comparison_status"], "comparison-ready")
        self.assertEqual(manifest["current_state"]["status"], "comparison-ready")
        self.assertGreaterEqual(len(manifest["official_inventory"]["source_ids"]), 8)
        self.assertGreaterEqual(len(manifest["comparison_keys"]), 4)
        self.assertGreaterEqual(len(manifest["tolerance_rules"]), 4)

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
