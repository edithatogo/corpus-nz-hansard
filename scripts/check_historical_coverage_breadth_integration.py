"""Validate the cross-repo historical coverage breadth integration bridge."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "historical_coverage_breadth_integration.json"
SCHEMA_PATH = ROOT / "schemas" / "historical_coverage_breadth_integration.schema.json"
DOC_PATH = ROOT / "docs" / "historical-coverage-breadth-integration.md"
EVIDENCE_PATH = (
    ROOT
    / "conductor"
    / "tracks"
    / "historical_coverage_breadth_integration_20260705"
    / "evidence.md"
)
TRACK_PATH = ROOT / "conductor" / "tracks" / "historical_coverage_breadth_integration_20260705"
HATHI_REPO = ROOT.parent / "hathi-nz"
LEGISLATION_REPO = ROOT.parent / "corpus-law-nz"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, EVIDENCE_PATH, TRACK_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    if manifest["bridge_status"] != "evidence-only":
        failures.append("bridge_status must remain evidence-only.")
    if manifest["policy"]["no_completeness_claim"] is not True:
        failures.append("no_completeness_claim must stay true.")
    if manifest["policy"]["no_bulk_acquisition"] is not True:
        failures.append("no_bulk_acquisition must stay true.")

    if not HATHI_REPO.exists():
        failures.append("adjacent hathi-nz repo path must exist.")
    if not LEGISLATION_REPO.exists():
        failures.append("adjacent corpus-law-nz repo path must exist.")

    repos = {item["repo"] for item in manifest["adjacent_repos"]}
    if repos != {"hathi-nz", "corpus-law-nz"}:
        failures.append("adjacent repos must include hathi-nz and corpus-law-nz only.")

    source_map = manifest["source_map"]
    postures = {item["posture"] for item in source_map}
    for posture in ("official", "fallback", "supporting", "evidence_only", "excluded"):
        if posture not in postures:
            failures.append(f"source_map must include posture {posture}.")

    source_ids = {item["source_id"] for item in source_map}
    for required in (
        "nz-parliament-hansard-current",
        "papers-past-hansard",
        "google-books-hansard-volumes",
        "library-catalogue-hansard-holdings",
        "data-govt-parliament-dataset-requests",
        "excluded-nz-legislation",
        "excluded-nz-gazette",
    ):
        if required not in source_ids:
            failures.append(f"source_map missing required source_id {required}.")

    for required_phrase in (
        "no completeness claim",
        "HathiTrust",
        "corpus-law-nz",
        "gap-detection evidence",
        "discovery evidence",
    ):
        if required_phrase not in _read(DOC_PATH):
            failures.append(
                f"docs/historical-coverage-breadth-integration.md is missing: {required_phrase}"
            )
        if required_phrase not in _read(EVIDENCE_PATH):
            failures.append(
                f"conductor/tracks/historical_coverage_breadth_integration_20260705/evidence.md is missing: {required_phrase}"
            )

    if manifest["historical_gap_model"]["statuses"] != ["open", "narrowed", "resolved", "excluded"]:
        failures.append("historical gap statuses must use the expected taxonomy.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"HISTORICAL-COVERAGE-BREADTH: {failure}")
        return 1
    print("Historical coverage breadth integration manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
