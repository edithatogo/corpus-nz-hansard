from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "parliament_video_reconciliation.json"
DOC = ROOT / "docs" / "parliament-video-reconciliation.md"
SCHEMA = ROOT / "schemas" / "parliament_video_reconciliation.schema.json"
LEDGER = ROOT / "derived" / "parliament_video_reconciliation" / "parliament_video_reconciliation_ledger.json"


def run_script(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


class ParliamentVideoReconciliationTest(unittest.TestCase):
    def test_reconciliation_builds_and_validates(self) -> None:
        run_script("scripts/build_parliament_video_reconciliation.py")
        run_script("scripts/check_parliament_video_reconciliation.py")

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        assert manifest["track_id"] == "parliament_video_reconciliation_20260705"
        assert manifest["reconciliation_status"] == "not-complete"
        assert manifest["policy"]["metadata_first"] is True
        assert manifest["policy"]["no_video_file_download"] is True
        assert manifest["summary"]["retrospective_archive_complete"] is False
        assert manifest["summary"]["ongoing_archive_complete"] is False
        assert manifest["summary"]["metadata_completeness_claim"] is False
        assert manifest["summary"]["media_completeness_claim"] is False
        assert manifest["summary"]["source_count"] == 19
        assert manifest["summary"]["official_source_count"] == 9
        assert manifest["summary"]["fallback_source_count"] == 7
        assert manifest["summary"]["supporting_source_count"] == 3
        assert manifest["summary"]["gap_status_counts"]["metadata-only"] >= 1
        assert manifest["summary"]["gap_status_counts"]["access-blocked"] >= 1
        assert any(row["source_id"] == "official-youtube-nz-parliament" for row in manifest["ledger"])
        assert any(row["source_id"] == "memento-cdx-web-archives" for row in manifest["ledger"])
        assert any(row["source_id"] == "adjacent-sm-govt-nz" for row in manifest["ledger"])
        assert DOC.exists()
        assert SCHEMA.exists()
        assert LEDGER.exists()

    def test_checker_remains_clean(self) -> None:
        from scripts.check_parliament_video_reconciliation import _failures

        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
