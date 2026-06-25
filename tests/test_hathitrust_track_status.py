from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "hathitrust_hansard_acquisition_20260612"
TRACK_DIR = ROOT / "conductor" / "tracks" / TRACK_ID


def test_hathitrust_track_metadata_matches_closed_deferred_bookkeeping() -> None:
    metadata = json.loads((TRACK_DIR / "metadata.json").read_text(encoding="utf-8"))
    tracks_index = (ROOT / "conductor" / "tracks.md").read_text(encoding="utf-8")

    assert metadata["status"] == "complete"
    assert metadata["release_status"] == "closed-deferred-external-access-required"
    assert "### [x] Track: HathiTrust Hansard Acquisition" in tracks_index
    assert "39 recovered sample IDs" in tracks_index


def test_hathitrust_track_docs_do_not_overclaim_acquisition() -> None:
    index = (TRACK_DIR / "index.md").read_text(encoding="utf-8")
    plan = (TRACK_DIR / "plan.md").read_text(encoding="utf-8")
    evidence = (TRACK_DIR / "evidence.md").read_text(encoding="utf-8")

    assert "complete-deferred" in index
    assert "does not claim full 510-volume enumeration" in index
    assert "39 sample IDs recovered" in plan
    assert "closed-deferred-external-access-required" in evidence
    assert "Reopen only with a local hathifile" in evidence
    assert "Unblock Acceptance Criteria" in evidence
    assert "enumerated_count == 510" in evidence
