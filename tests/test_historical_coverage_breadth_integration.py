from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "historical_coverage_breadth_integration.json"
DOC = ROOT / "docs" / "historical-coverage-breadth-integration.md"
SCHEMA = ROOT / "schemas" / "historical_coverage_breadth_integration.schema.json"


def run_script(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def test_historical_coverage_breadth_integration_builds_and_validates() -> None:
    run_script("scripts/build_historical_coverage_breadth_integration.py")
    run_script("scripts/check_historical_coverage_breadth_integration.py")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["bridge_status"] == "evidence-only"
    assert manifest["policy"]["no_completeness_claim"] is True
    assert "hathi-nz" in manifest["adjacent_repos"][0]["repo"]
    assert "corpus-law-nz" in manifest["boundary_rules"][0]
    assert DOC.exists()
    assert SCHEMA.exists()
