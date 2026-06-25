from __future__ import annotations

import unittest

from scripts.check_parliament_website_stealth_access import _failures


class ParliamentWebsiteStealthAccessTests(unittest.TestCase):
    def test_saved_stealth_artifacts_and_track_status_are_consistent(self) -> None:
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
