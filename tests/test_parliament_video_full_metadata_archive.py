from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "parliament_video_full_metadata_archive.json"
DOC = ROOT / "docs" / "parliament-video-full-metadata-archive.md"
SCHEMA = ROOT / "schemas" / "parliament_video_full_metadata_archive.schema.json"
SNAPSHOT = (
    ROOT
    / "derived"
    / "parliament_video_full_metadata_archive"
    / "parliament_video_full_metadata_archive_snapshot.json"
)
GAP_REPORT = (
    ROOT
    / "derived"
    / "parliament_video_full_metadata_archive"
    / "parliament_video_full_metadata_archive_gap_report.json"
)


def run_script(script: str, *args: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script), *args], check=True, cwd=ROOT)


class ParliamentVideoFullMetadataArchiveTests(unittest.TestCase):
    def test_full_metadata_archive_builds_and_validates(self) -> None:
        run_script("scripts/build_parliament_video_full_metadata_archive.py")
        run_script("scripts/check_parliament_video_full_metadata_archive.py")

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["track_id"], "parliament_video_full_metadata_archive_20260705")
        self.assertEqual(manifest["refresh_policy"]["cadence"], "monthly")
        self.assertEqual(manifest["refresh_policy"]["snapshot_retention"], 12)
        self.assertTrue(manifest["policy"]["metadata_first"])
        self.assertTrue(manifest["policy"]["no_media_download"])
        self.assertTrue(manifest["policy"]["no_video_file_download"])
        self.assertTrue(manifest["policy"]["no_audio_file_download"])
        self.assertTrue(manifest["policy"]["fallbacks_are_validation_only"])
        self.assertGreaterEqual(manifest["summary"]["approved_source_count"], 9)
        self.assertGreaterEqual(manifest["summary"]["record_count"], 16)
        self.assertIn("gap_report_path", manifest["archive"])
        self.assertIn("records_path", manifest["archive"])
        self.assertTrue(DOC.exists())
        self.assertTrue(SCHEMA.exists())
        self.assertTrue(SNAPSHOT.exists())
        self.assertTrue(GAP_REPORT.exists())

    def test_snapshot_comparison_detects_new_deleted_and_changed_records(self) -> None:
        from scripts.build_parliament_video_full_metadata_archive import compare_snapshots

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
        from scripts.check_parliament_video_full_metadata_archive import (
            FullMetadataArchiveNotApprovedError,
            require_full_metadata_archive_metadata_only,
        )

        with self.assertRaises(FullMetadataArchiveNotApprovedError):
            require_full_metadata_archive_metadata_only()

    def test_checker_script_runs_successfully(self) -> None:
        run_script("scripts/build_parliament_video_full_metadata_archive.py")
        run_script("scripts/check_parliament_video_full_metadata_archive.py")


if __name__ == "__main__":
    unittest.main()
