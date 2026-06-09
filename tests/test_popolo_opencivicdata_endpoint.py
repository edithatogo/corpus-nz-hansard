import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_popolo_opencivicdata_endpoint import (
    JSON_OUTPUTS,
    JSONL_OUTPUTS,
    MANIFEST_PATH,
    _failures,
    _json,
    _jsonl,
)


class PopoloOpenCivicDataEndpointTest(unittest.TestCase):
    def test_sample_outputs_parse(self):
        for path in JSON_OUTPUTS.values():
            self.assertTrue(_json(path))
        for path in JSONL_OUTPUTS.values():
            self.assertTrue(_jsonl(path))

    def test_manifest_keeps_sample_not_release_boundary(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )

    def test_party_vote_is_distinguished_from_individual_vote(self):
        votes = _jsonl(JSONL_OUTPUTS["votes"])

        self.assertEqual(votes[0]["voter_type"], "organization")

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
