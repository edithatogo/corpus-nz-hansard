from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def test_full_historical_sitting_reconciliation_builds_and_validates() -> None:
    run_script("scripts/build_full_historical_sitting_reconciliation.py")
    run_script("scripts/check_full_historical_sitting_reconciliation.py")

    sample = json.loads(
        (
            ROOT
            / "samples"
            / "full-historical-sitting-reconciliation"
            / "sitting-reconciliation.json"
        ).read_text(
            encoding="utf-8",
        ),
    )
    assert sample["public_claims"]["full_historical_coverage"] is False
    assert sample["coverage_contract"]["requires_agent_review_fallback"] is True
    assert sample["coverage_contract"]["requires_human_review"] is False
