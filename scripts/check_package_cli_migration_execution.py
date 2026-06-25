"""Validate the package and CLI migration execution track."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "package_cli_migration_execution_20260610"
MANIFEST = ROOT / "manifests" / "package_cli_migration_execution.json"
DOC = ROOT / "docs" / "package-cli-migration-execution.md"
PYPROJECT = ROOT / "pyproject.toml"
TRACKS_MD = ROOT / "conductor" / "tracks.md"
PACKAGE = ROOT / "src" / "nz_hansard_corpus"

RELEASE_STATUS = "release-ready-package-cli-compatibility-layer"
REQUIRED_COMMANDS = {
    "nzhc build-manifest",
    "nzhc validate",
    "nzhc metadata build",
    "nzhc hf stage",
    "nzhc zenodo draft",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(_read(path))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    pyproject = tomllib.loads(_read(PYPROJECT))
    scripts = pyproject["project"]["scripts"]
    manifest = _json(MANIFEST)

    _require((PACKAGE / "__init__.py").is_file(), "package namespace is missing")
    _require((PACKAGE / "cli.py").is_file(), "package CLI is missing")
    _require(scripts["nzhc"] == "nz_hansard_corpus.cli:main", "nzhc entry point is missing")
    _require(
        scripts["corpus-nz-hansard"] == "nz_hansard_corpus.cli:main",
        "legacy console script must route through package CLI",
    )
    _require("uv" not in pyproject.get("tool", {}), "uv package=false boundary must be removed")

    _require(manifest["release_status"] == RELEASE_STATUS, "manifest release status is stale")
    _require(
        set(manifest["commands"]) == REQUIRED_COMMANDS, "manifest command inventory is incomplete"
    )
    _require(
        manifest["legacy_scripts_remain_supported"] is True, "legacy scripts must remain supported"
    )
    _require(
        manifest["publication_boundary_preserved"] is True, "publication boundary must be explicit"
    )

    completed_text = "\n".join(
        [
            _read(TRACK / "plan.md"),
            _read(TRACK / "evidence.md"),
            _read(TRACK / "index.md"),
            _read(DOC),
        ]
    )
    for phrase in (
        RELEASE_STATUS,
        "legacy scripts remain supported",
        "publication boundary is preserved",
        "nzhc metadata build",
    ):
        _require(phrase in completed_text, f"missing required documentation phrase: {phrase}")

    metadata = _json(TRACK / "metadata.json")
    _require(metadata.get("status") == "complete", "track metadata must be complete")
    _require(
        "### [x] Track: Package And CLI Migration Execution" in _read(TRACKS_MD),
        "conductor/tracks.md checkbox is not complete",
    )

    result = subprocess.run(
        [sys.executable, "-m", "nz_hansard_corpus.cli", "--list"],
        check=True,
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
    )
    for command in REQUIRED_COMMANDS:
        _require(command.replace("nzhc ", "") in result.stdout, f"CLI list missing {command}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
