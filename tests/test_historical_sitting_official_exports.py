import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_historical_sitting_official_exports import (  # noqa: E402
    DOC_PATH,
    MANIFEST_PATH,
    _failures,
    _json,
)


class HistoricalSittingOfficialExportsTest(unittest.TestCase):
    def test_official_export_manifest_shape(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(manifest["artifact_name"], "historical_sitting_official_exports")
        self.assertEqual(manifest["publication_stages"], ["draft", "weekly", "sessional"])
        self.assertGreaterEqual(len(manifest["sources"]), 3)
        self.assertGreaterEqual(len(manifest["authoritative_statements"]), 2)
        self.assertTrue(DOC_PATH.exists())

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
