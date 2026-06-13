"""Validate exploratory entity-linking outputs."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.entity_linking_exploratory_outputs import (  # noqa: E402
    DOC_PATH,
    JSONL_PATH,
    MANIFEST_PATH,
    README_PATH,
    RECORD_SCHEMA_PATH,
    REVIEW_PATH,
    SCHEMA_PATH,
)

TRACK_PATH = ROOT / "conductor/tracks/entity_linking_exploratory_outputs_20260610/index.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _jsonl_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        RECORD_SCHEMA_PATH,
        JSONL_PATH,
        REVIEW_PATH,
        DOC_PATH,
        README_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    record_schema = _json(RECORD_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    rows = _jsonl_rows(JSONL_PATH)
    row_validator = Draft202012Validator(record_schema)
    for index, row in enumerate(rows):
        for error in sorted(row_validator.iter_errors(row), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(
                f"{JSONL_PATH.relative_to(ROOT).as_posix()}[{index}] {location}: {error.message}"
            )

    review_rows = _csv_rows(REVIEW_PATH)
    if len(rows) != manifest["validation_counts"]["record_count"]:
        failures.append("JSONL row count must match manifest record_count.")
    if len(review_rows) != manifest["validation_counts"]["review_row_count"]:
        failures.append("Review CSV row count must match manifest review_row_count.")

    required_entity_types = {
        "person",
        "organisation",
        "place",
        "legislation",
        "ministry",
        "portfolio",
        "committee",
    }
    if {row["entity_type"] for row in review_rows} != required_entity_types:
        failures.append("Review CSV must cover the seven required entity types.")

    required_classes = {"positive", "negative", "ambiguous", "unresolved", "excluded"}
    if not required_classes.issubset({row["example_class"] for row in review_rows}):
        failures.append("Review CSV must cover all required example classes.")

    if manifest["release_status"] != "sample-not-release":
        failures.append("Manifest release_status must remain sample-not-release.")
    if manifest["validation_results"]["non_authoritative"] is not True:
        failures.append("Manifest must stay non-authoritative.")
    if manifest["validation_results"]["human_validation_required"] is not True:
        failures.append("Manifest must require human validation.")

    doc = _read(DOC_PATH)
    for required in (
        "non-authoritative",
        "machine-assisted",
        "people, organisations, places, legislation, ministries, portfolios, and committees",
        "False-Positive Analysis",
        "search or RAG enrichment and RDF exploratory graphs",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    readme = _read(README_PATH)
    for required in (
        "sample-not-release",
        "entity_linking_exploratory.jsonl",
        "entity_linking_exploratory_review.csv",
        "human validation",
    ):
        if required not in readme:
            failures.append(f"{README_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    track = _read(TRACK_PATH)
    for required in ("Outputs", "Review Sample", "False-Positive Analysis", "Validation"):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    if manifest["validation_counts"]["record_count"] != 7:
        failures.append("Expected exactly seven exploratory entity-linking records.")
    if manifest["validation_counts"]["linked"] < 2:
        failures.append("Expected at least two linked examples.")
    if manifest["validation_counts"]["unresolved"] < 2:
        failures.append("Expected at least two unresolved examples.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"ENTITY-LINKING-EXPLORATORY: {failure}")
        return 1
    print("Entity linking exploratory outputs are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
