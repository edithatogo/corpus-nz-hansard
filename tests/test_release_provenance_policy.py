import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_release_provenance_policy import _failures


class ReleaseProvenancePolicyTest(unittest.TestCase):
    def test_repository_provenance_policy_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
