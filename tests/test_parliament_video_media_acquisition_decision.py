from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "parliament_video_media_acquisition_decision.json"
DOC = ROOT / "docs" / "parliament-video-media-acquisition-decision.md"
SCHEMA = ROOT / "schemas" / "parliament_video_media_acquisition_decision.schema.json"


def run_script(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def test_decision_builds_and_validates() -> None:
    run_script("scripts/build_parliament_video_media_acquisition_decision.py")
    run_script("scripts/check_parliament_video_media_acquisition_decision.py")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["track_id"] == "parliament_video_media_acquisition_decision_20260705"
    assert manifest["decision_state"] == "excluded"
    assert manifest["decision_scope"] == "media acquisition"
    assert manifest["policy"]["metadata_first"] is True
    assert manifest["policy"]["no_media_download"] is True
    assert manifest["policy"]["rights_review_required_before_media_acquisition"] is True
    assert manifest["media"]["video"] == "excluded"
    assert manifest["media"]["audio"] == "excluded"
    assert manifest["media"]["metadata"] == "allowed"
    assert len(manifest["rights_evidence"]) >= 8
    assert any(
        item["source_id"] == "parliament-copyright-and-video-terms"
        for item in manifest["rights_evidence"]
    )
    assert DOC.exists()
    assert SCHEMA.exists()


def test_media_download_gate_blocks_without_approval() -> None:
    from scripts.check_parliament_video_media_acquisition_decision import (
        MediaAcquisitionNotApprovedError,
        require_media_acquisition_approval,
    )

    with pytest.raises(MediaAcquisitionNotApprovedError):
        require_media_acquisition_approval()


def test_checker_script_runs_successfully() -> None:
    subprocess.run(
        [sys.executable, "scripts/check_parliament_video_media_acquisition_decision.py"],
        check=True,
        cwd=ROOT,
    )
