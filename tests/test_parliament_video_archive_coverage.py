from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "parliament_video_archive_coverage.json"
DOC = ROOT / "docs" / "parliament-video-archive-coverage.md"
SCHEMA = ROOT / "schemas" / "parliament_video_archive_coverage.schema.json"


def run_script(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def test_parliament_video_archive_coverage_builds_and_validates() -> None:
    run_script("scripts/build_parliament_video_archive_coverage.py")
    run_script("scripts/check_parliament_video_archive_coverage.py")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["coverage_status"] == "not-complete"
    assert manifest["policy"]["metadata_first"] is True
    assert manifest["policy"]["no_video_file_download"] is True
    assert manifest["summary"]["surface_count"] >= 4
    assert "sm-govt-nz" in {repo["repo"] for repo in manifest["adjacent_repo_findings"]}
    assert DOC.exists()
    assert SCHEMA.exists()
