from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests/nzlii_historical_acquisition_status.json"


def test_nzlii_status_manifest_records_current_blocker() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["acquisition_status"] == "complete-deferred-cloudflare-challenge"
    assert manifest["release_status"] == "closed-deferred-external-access-required"
    assert manifest["authority_source_id"] == "nzlii-historical-bills"
    assert manifest["authority_source_registered"] is True
    blocked_targets = [
        target
        for target in manifest["targets"]
        if target["status"] == "blocked-403-cloudflare-challenge"
    ]
    assert len(blocked_targets) >= 4
    assert manifest["robots"]["reachable"] is False
    assert manifest["robots"]["status"] == "blocked-403-cloudflare-challenge"
    assert manifest["robots"]["previous_content_signal"]["search_content_signal"] == "yes"
    assert manifest["robots"]["previous_content_signal"]["ai_train_content_signal"] == "no"


def test_nzlii_checker_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_nzlii_historical_acquisition.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
