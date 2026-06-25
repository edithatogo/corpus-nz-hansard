from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_nzhc_cli_lists_migrated_commands() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "nz_hansard_corpus.cli", "--list"],
        check=True,
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
    )

    assert "build-manifest" in result.stdout
    assert "validate" in result.stdout
    assert "metadata build" in result.stdout
    assert "hf stage" in result.stdout
    assert "zenodo draft" in result.stdout


def test_package_cli_migration_checker_passes() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_package_cli_migration_execution.py")],
        check=True,
        cwd=ROOT,
    )
