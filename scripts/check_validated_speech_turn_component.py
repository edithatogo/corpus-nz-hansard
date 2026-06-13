"""Validate the validated speech-turn component release gate."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

try:
    from scripts.build_validated_speech_turn_component import (
        DEFAULT_MANIFEST,
        OUTPUT_COLUMNS,
        REVIEW_QUEUE_COLUMNS,
        SCHEMA_PATH,
    )
    from scripts.validate_derived_fields import validate_manifest
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_validated_speech_turn_component import (
        DEFAULT_MANIFEST,
        OUTPUT_COLUMNS,
        REVIEW_QUEUE_COLUMNS,
        SCHEMA_PATH,
    )
    from scripts.validate_derived_fields import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = DEFAULT_MANIFEST
DOC_PATH = ROOT / "docs/validated-speech-turn-component-release.md"
TRACK_DIR = ROOT / "conductor/tracks/validated_speech_turn_component_release_20260610"
INDEX_PATH = TRACK_DIR / "index.md"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
METADATA_PATH = TRACK_DIR / "metadata.json"
TRACKS_PATH = ROOT / "conductor/tracks.md"
OUTPUT_PATH = ROOT / "generated/derived/hansard_speech_turns_validated.parquet"
REVIEW_QUEUE_PATH = ROOT / "derived/validated_speech_turns/speech_turn_review_queue.csv"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _csv_header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return next(csv.reader(handle))


def _failures() -> list[str]:
    failures: list[str] = []
    required_paths = [
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        INDEX_PATH,
        PLAN_PATH,
        EVIDENCE_PATH,
        METADATA_PATH,
    ]
    for path in required_paths:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    failures.extend(validate_manifest(manifest))
    if manifest["artifact_name"] != "validated_speech_turn_component":
        failures.append("artifact_name must be validated_speech_turn_component.")
    if manifest["track_id"] != "validated_speech_turn_component_release_20260610":
        failures.append("Manifest must reference the validated speech-turn track.")
    if manifest["ok"] is not False:
        failures.append(
            "Validated speech-turn release must remain blocked in the current workspace."
        )
    if manifest["validation_status"] not in {"blocked", "ok"}:
        failures.append("Validation status must be blocked or ok.")
    if manifest["release_gate_status"] not in {
        "blocked-pending-candidate-artifact",
        "blocked-pending-validated-member-identity",
        "ready",
    }:
        failures.append("Unexpected release gate status for the validated speech-turn track.")
    for key in (
        "validated_rows",
        "review_queue_rows",
        "validated_speaker_identity",
        "blocked_speaker_identity",
    ):
        if key not in manifest["counts"]:
            failures.append(f"Manifest counts must include {key}.")
    if (
        "candidate_parquet" not in manifest.get("source_hashes", {})
        and manifest["release_gate_status"] != "blocked-pending-candidate-artifact"
    ):
        failures.append(
            "Manifest must record the candidate parquet source hash when the candidate artifact exists."
        )
    if manifest["release_decision"]["decision"] not in {"defer", "promote"}:
        failures.append("Release decision must be defer or promote.")

    schema = _json(SCHEMA_PATH)
    required_statuses = {
        "validated",
        "blocked-pending-validated-member-identity",
        "unresolved",
        "ambiguous",
        "excluded",
    }
    if set(schema["properties"]["speaker_identity_status"]["enum"]) != required_statuses:
        failures.append(
            "Schema must enumerate the validated and blocked speaker identity statuses."
        )

    if not REVIEW_QUEUE_PATH.exists() and manifest["counts"]["review_queue_rows"] != 0:
        failures.append("Review queue must exist when rows are reported.")
    if REVIEW_QUEUE_PATH.exists() and _csv_header(REVIEW_QUEUE_PATH) != REVIEW_QUEUE_COLUMNS:
        failures.append(
            "Review queue CSV header must match the validated speech-turn review contract."
        )
    if OUTPUT_PATH.exists():
        table = pq.read_table(OUTPUT_PATH)
        if table.num_rows != manifest["counts"]["validated_rows"]:
            failures.append("Validated output row count must match the manifest.")
        elif list(table.column_names) != OUTPUT_COLUMNS:
            failures.append("Validated output schema must match the contract.")

    doc_text = _read(DOC_PATH)
    for term in (
        "blocked-pending-validated-member-identity",
        "blocked-pending-candidate-artifact",
        "Validated member identity",
        "candidate speech-turn parquet",
    ):
        if term not in doc_text:
            failures.append(f"Validated speech-turn docs missing term: {term}")

    if "blocked" not in _read(TRACKS_PATH).lower():
        failures.append("Track registry must expose blocked state.")

    metadata = _json(METADATA_PATH)
    if metadata["status"] != "blocked":
        failures.append("Track metadata must be blocked until member identity validation exists.")
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"VALIDATED-SPEECH-TURN: {failure}")
        return 1
    print("Validated speech-turn component release gate is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
