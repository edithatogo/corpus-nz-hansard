from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "parliament_video_ongoing_archive.json"
DOC = ROOT / "docs" / "parliament-video-ongoing-archive.md"
SCHEMA = ROOT / "schemas" / "parliament_video_ongoing_archive.schema.json"
SNAPSHOT = (
    ROOT
    / "derived"
    / "parliament_video_ongoing_archive"
    / "parliament_video_ongoing_archive_snapshot.json"
)
CHANGES = (
    ROOT
    / "derived"
    / "parliament_video_ongoing_archive"
    / "parliament_video_ongoing_archive_changes.json"
)


def run_script(script: str, *args: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script), *args], check=True, cwd=ROOT)


class ParliamentVideoOngoingArchiveTests(unittest.TestCase):
    def test_ongoing_archive_builds_and_validates(self) -> None:
        run_script("scripts/build_parliament_video_ongoing_archive.py")
        run_script("scripts/check_parliament_video_ongoing_archive.py")

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["track_id"], "parliament_video_ongoing_archive_20260705")
        self.assertEqual(manifest["refresh_policy"]["cadence"], "weekly")
        self.assertEqual(manifest["refresh_policy"]["snapshot_retention"], 12)
        self.assertEqual(manifest["policy"]["no_media_download"], True)
        self.assertEqual(manifest["policy"]["no_video_file_download"], True)
        self.assertEqual(manifest["policy"]["no_audio_file_download"], True)
        self.assertEqual(
            manifest["policy"]["rights_review_required_before_media_acquisition"], True
        )
        self.assertGreaterEqual(manifest["summary"]["monitored_surface_count"], 7)
        self.assertIn("parliament-video-ongoing-archive.yml", manifest["workflow"]["path"])
        self.assertIn("new_deletions", manifest["change_policy"])
        self.assertTrue(DOC.exists())
        self.assertTrue(SCHEMA.exists())
        self.assertTrue(SNAPSHOT.exists())
        self.assertTrue(CHANGES.exists())

    def test_snapshot_comparison_detects_new_deleted_and_changed_records(self) -> None:
        from scripts.build_parliament_video_ongoing_archive import compare_snapshots

        previous = {
            "records": [
                {"source_id": "a", "digest": "1", "status": "unchanged"},
                {"source_id": "b", "digest": "2", "status": "unchanged"},
            ]
        }
        current = {
            "records": [
                {"source_id": "a", "digest": "9", "status": "changed"},
                {"source_id": "c", "digest": "3", "status": "new"},
            ]
        }

        diff = compare_snapshots(previous, current)

        self.assertEqual(diff["new_source_ids"], ["c"])
        self.assertEqual(diff["deleted_source_ids"], ["b"])
        self.assertEqual(diff["changed_source_ids"], ["a"])

    def test_no_media_guard_fails_closed_without_approval(self) -> None:
        from scripts.check_parliament_video_ongoing_archive import (
            OngoingArchiveNotApprovedError,
            require_ongoing_archive_metadata_only,
        )

        with self.assertRaises(OngoingArchiveNotApprovedError):
            require_ongoing_archive_metadata_only()

    def test_checker_script_runs_successfully(self) -> None:
        run_script("scripts/check_parliament_video_ongoing_archive.py")


if __name__ == "__main__":
    unittest.main()
