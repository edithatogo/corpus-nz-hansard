import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_historical_coverage_audit import (
    EXPECTED_PARLIAMENTS,
    EXPECTED_ROW_COUNTS,
    MANIFEST_PATH,
    _failures,
    _json,
)


class HistoricalCoverageAuditTest(unittest.TestCase):
    def test_claim_boundaries_include_all_statuses(self):
        manifest = _json(MANIFEST_PATH)
        statuses = {claim["status"] for claim in manifest["claim_boundaries"]}

        self.assertEqual(statuses, {"verified", "partial", "unknown", "excluded"})

    def test_parliament_coverage_matches_source_extract(self):
        manifest = _json(MANIFEST_PATH)
        coverage = {item["parliament_number"]: item for item in manifest["parliament_coverage"]}

        self.assertEqual(set(coverage), EXPECTED_PARLIAMENTS)
        self.assertEqual(
            {number: item["rows"] for number, item in coverage.items()},
            EXPECTED_ROW_COUNTS,
        )
        self.assertEqual({item["coverage_status"] for item in coverage.values()}, {"partial"})

    def test_full_historical_completeness_is_not_claimed(self):
        manifest = _json(MANIFEST_PATH)
        full_history = [
            claim
            for claim in manifest["claim_boundaries"]
            if claim["claim_id"] == "full-historical-hansard-completeness"
        ]

        self.assertEqual(len(full_history), 1)
        self.assertEqual(full_history[0]["status"], "unknown")

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
