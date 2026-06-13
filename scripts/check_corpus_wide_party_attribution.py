"""Validate the corpus-wide party attribution release gate."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.build_corpus_wide_party_attribution import (
        OUTPUT_COLUMNS,
        REVIEW_QUEUE_COLUMNS,
        SCHEMA_PATH,
        VALIDATION_MANIFEST_PATH,
    )
    from scripts.validate_derived_fields import validate_manifest
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_corpus_wide_party_attribution import (
        OUTPUT_COLUMNS,
        REVIEW_QUEUE_COLUMNS,
        SCHEMA_PATH,
        VALIDATION_MANIFEST_PATH,
    )
    from scripts.validate_derived_fields import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs/corpus-wide-party-attribution-release.md"
TRACK_DIR = ROOT / "conductor/tracks/corpus_wide_party_attribution_release_20260610"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
METADATA_PATH = TRACK_DIR / "metadata.json"
TRACKS_PATH = ROOT / "conductor/tracks.md"
OUTPUT_CSV = ROOT / "derived/corpus_wide_party_attribution/party_attribution.csv"
REVIEW_QUEUE_CSV = ROOT / "derived/corpus_wide_party_attribution/party_attribution_review_queue.csv"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _csv_header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return next(csv.reader(handle))


def _failures() -> list[str]:
    failures: list[str] = []
    required_paths = [
        VALIDATION_MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        PLAN_PATH,
        EVIDENCE_PATH,
        METADATA_PATH,
    ]
    for path in required_paths:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(VALIDATION_MANIFEST_PATH)
    failures.extend(validate_manifest(manifest))
    if manifest["artifact_name"] != "corpus_wide_party_attribution":
        failures.append("Manifest artifact_name must be corpus_wide_party_attribution.")
    if manifest["track_id"] != "corpus_wide_party_attribution_release_20260610":
        failures.append("Manifest must reference the corpus-wide party attribution track.")
    if manifest["ok"] is not False:
        failures.append(
            "Corpus-wide party attribution must remain blocked until validated member identity exists."
        )
    if manifest["validation_status"] != "blocked":
        failures.append("Validation status must remain blocked for the current release gate.")
    if manifest["release_gate_status"] != "blocked-pending-validated-member-identity":
        failures.append(
            "Release gate status must remain blocked-pending-validated-member-identity."
        )
    for key in (
        "explicit_party_labels",
        "unresolved_member_dependency",
        "authoritative",
        "blocked",
    ):
        if key not in manifest["counts"]:
            failures.append(f"Manifest counts must include {key}.")
    if manifest["counts"]["source_rows_from_schema_discovery"] <= 0:
        failures.append("Manifest must inventory source rows from schema discovery.")
    if manifest["counts"]["source_files_from_schema_discovery"] <= 0:
        failures.append("Manifest must inventory source files from schema discovery.")
    if "member_identity_validation" not in manifest.get("input_artifacts", {}):
        failures.append("Manifest must name the member identity validation input.")
    if manifest["release_decision"]["decision"] != "defer":
        failures.append("Release decision must defer until validated member identity exists.")

    schema = _json(SCHEMA_PATH)
    required_statuses = {"authoritative", "alias", "ambiguous", "unresolved", "blocked"}
    if set(schema["properties"]["party_attribution_status"]["enum"]) != required_statuses:
        failures.append(
            "Schema must enumerate authoritative, alias, ambiguous, unresolved, and blocked statuses."
        )

    if _csv_header(REVIEW_QUEUE_CSV) != REVIEW_QUEUE_COLUMNS:
        failures.append("Review queue CSV header must match the corpus-wide review queue contract.")
    if OUTPUT_CSV.exists() and _csv_header(OUTPUT_CSV) != OUTPUT_COLUMNS:
        failures.append("Party attribution CSV header must match the corpus-wide output contract.")

    doc_text = _read(DOC_PATH)
    for term in (
        "blocked-pending-validated-member-identity",
        "validated member identity",
        "Explicit party-vote labels can be extracted",
    ):
        if term not in doc_text:
            failures.append(f"Corpus-wide party attribution docs missing term: {term}")

    if "blocked" not in _read(TRACKS_PATH).lower():
        failures.append("Track registry must expose blocked state.")

    metadata = _json(METADATA_PATH)
    if metadata["status"] != "blocked":
        failures.append("Track metadata must be blocked until validated member identity exists.")
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"CORPUS-WIDE-PARTY-ATTRIBUTION: {failure}")
        return 1
    print("Corpus-wide party attribution release gate is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
