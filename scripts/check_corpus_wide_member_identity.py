"""Validate the corpus-wide member identity release gate."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.build_corpus_wide_member_identity import (
        OUTPUT_COLUMNS,
        REVIEW_QUEUE_COLUMNS,
        REVIEW_QUEUE_CSV,
        SCHEMA_PATH,
        VALIDATION_MANIFEST_PATH,
    )
    from scripts.validate_derived_fields import validate_manifest
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_corpus_wide_member_identity import (
        OUTPUT_COLUMNS,
        REVIEW_QUEUE_COLUMNS,
        REVIEW_QUEUE_CSV,
        SCHEMA_PATH,
        VALIDATION_MANIFEST_PATH,
    )
    from scripts.validate_derived_fields import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs/corpus-wide-member-identity-release.md"
TRACK_DIR = ROOT / "conductor/tracks/corpus_wide_member_identity_release_20260610"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
METADATA_PATH = TRACK_DIR / "metadata.json"
TRACKS_PATH = ROOT / "conductor/tracks.md"


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
        REVIEW_QUEUE_CSV,
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
    if manifest["artifact_name"] != "corpus_wide_member_identity":
        failures.append("Manifest artifact_name must be corpus_wide_member_identity.")
    if manifest["track_id"] != "corpus_wide_member_identity_release_20260610":
        failures.append("Manifest must reference the corpus-wide member identity track.")
    if manifest["ok"] is not False:
        failures.append(
            "Corpus-wide member identity must remain blocked until authority coverage review passes."
        )
    if manifest["validation_status"] != "blocked":
        failures.append("Validation status must remain blocked for the current release gate.")
    if not manifest["release_gate_status"].startswith("blocked-"):
        failures.append("Release gate status must be blocked for the current implementation.")
    if manifest["counts"]["source_rows_from_schema_discovery"] <= 0:
        failures.append("Manifest must inventory source rows from schema discovery.")
    if manifest["counts"]["source_files_from_schema_discovery"] <= 0:
        failures.append("Manifest must inventory source files from schema discovery.")
    for status in ("exact", "alias", "multi-person", "unresolved", "ambiguous", "conflict"):
        if status not in manifest["counts"]:
            failures.append(f"Manifest counts must include status: {status}")
    for field in ("source_summary", "release_decision", "source_hashes", "source_manifests"):
        if field not in manifest:
            failures.append(f"Manifest must include {field}.")
    if manifest["release_decision"]["decision"] != "defer":
        failures.append("Release decision must defer until validation gates pass.")
    if (
        "No corpus-wide member identity release is published"
        not in manifest["release_decision"]["public_claim"]
        and "not a validated public member identity release"
        not in manifest["release_decision"]["public_claim"]
    ):
        failures.append("Release decision must avoid public-release overclaiming.")

    review_header = _csv_header(REVIEW_QUEUE_CSV)
    if review_header != REVIEW_QUEUE_COLUMNS:
        failures.append("Review queue CSV header must match the corpus-wide review queue contract.")
    if "member_resolution_status" not in _read(SCHEMA_PATH):
        failures.append("Schema must define member_resolution_status.")
    schema = _json(SCHEMA_PATH)
    schema_statuses = set(schema["properties"]["member_resolution_status"]["enum"])
    expected_statuses = {"exact", "alias", "multi-person", "unresolved", "ambiguous", "conflict"}
    if schema_statuses != expected_statuses:
        failures.append(
            "Schema must enumerate exact, alias, multi-person, unresolved, ambiguous, and conflict statuses."
        )

    outputs = manifest.get("outputs", {})
    output_csv = outputs.get("member_identity_csv")
    if output_csv:
        output_path = ROOT / output_csv
        if not output_path.exists():
            failures.append(f"Declared member identity output does not exist: {output_csv}")
        elif _csv_header(output_path) != OUTPUT_COLUMNS:
            failures.append(
                "Member identity CSV header must match the corpus-wide output contract."
            )
        else:
            rows = _csv_rows(output_path)
            if len(rows) != manifest["counts"]["derived_rows"]:
                failures.append("Derived row count must match member identity CSV rows.")
            statuses = {row["member_resolution_status"] for row in rows}
            if not statuses.issubset(expected_statuses):
                failures.append("Member identity CSV contains an unsupported resolution status.")

    doc_text = _read(DOC_PATH)
    for term in (
        "blocked-pending-corpus-artifact",
        "blocked-pending-authority-coverage-review",
        "review overrides",
        "must not be published as a validated component",
    ):
        if term not in doc_text:
            failures.append(f"Corpus-wide member identity docs missing term: {term}")

    plan_text = _read(PLAN_PATH)
    if "[!]" not in plan_text and "blocked" not in plan_text.lower():
        failures.append("Track plan must record the current release blocker.")
    if "blocked" not in _read(TRACKS_PATH).lower():
        failures.append("Track registry must expose blocked state.")

    metadata = _json(METADATA_PATH)
    if metadata["status"] != "blocked":
        failures.append(
            "Track metadata must be blocked until corpus input and authority coverage gates pass."
        )
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"CORPUS-WIDE-MEMBER-IDENTITY: {failure}")
        return 1
    print("Corpus-wide member identity release gate is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
