import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_cap_parlacap_topic_endpoint import (  # noqa: E402
    MANIFEST_PATH,
    SAMPLE_PATH,
    _csv_rows,
    _failures,
    _json,
)


class CapParlaCapTopicEndpointTest(unittest.TestCase):
    def test_sample_csv_has_expected_rows(self):
        rows = _csv_rows(SAMPLE_PATH)

        self.assertEqual(len(rows), 3)
        self.assertEqual(
            {row["coding_method"] for row in rows},
            {"human-coded", "rule-coded", "model-coded"},
        )

    def test_manifest_records_sample_not_release_boundary(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
