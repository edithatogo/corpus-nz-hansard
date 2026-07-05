from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_parliament_video_track_plan import (  # noqa: E402
    TRACK_IDS,
    _failures,
    _missing_fragments,
)


class ParliamentVideoTrackPlanTest(unittest.TestCase):
    def test_all_video_tracks_are_registered_and_ci_visible(self) -> None:
        self.assertEqual(_failures(), [])

    def test_track_ids_remain_complete(self) -> None:
        self.assertEqual(
            set(TRACK_IDS),
            {
                "parliament_video_source_inventory_20260705",
                "parliament_video_seed_fetchers_20260705",
                "parliament_video_full_metadata_archive_20260705",
                "parliament_video_reconciliation_20260705",
                "parliament_video_media_acquisition_decision_20260705",
                "parliament_video_ongoing_archive_20260705",
            },
        )

    def test_missing_fragments_are_case_insensitive(self) -> None:
        self.assertEqual(_missing_fragments("Git Notes and github actions", ("git notes",)), [])
        self.assertEqual(
            _missing_fragments("Git Notes and github actions", ("remote push",)),
            ["remote push"],
        )

    def test_checker_script_runs_successfully(self) -> None:
        subprocess.run(
            [sys.executable, "scripts/check_parliament_video_track_plan.py"],
            check=True,
            cwd=ROOT,
        )


if __name__ == "__main__":
    unittest.main()
