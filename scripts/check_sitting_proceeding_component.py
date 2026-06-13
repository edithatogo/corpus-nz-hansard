"""Validate the sitting and proceeding component release surface."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/sitting_proceeding_component_validation.json"
SCHEMA_PATH = ROOT / "schemas/sitting_proceeding_component_validation.schema.json"
DOC_PATH = ROOT / "docs/sitting-proceeding-component-release.md"
NEUTRAL_DOC_PATH = ROOT / "docs/neutral-component-model.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
RELEASE_LADDER_DOC_PATH = ROOT / "docs/release-ladder.md"
TRACK_PATH = ROOT / "conductor/tracks/sitting_proceeding_component_release_20260610/index.md"
HISTORICAL_COVERAGE_PATH = ROOT / "manifests/historical_coverage_audit.json"
OUTPUT_COVERAGE_PATH = (
    ROOT / "derived/sitting_proceeding_components/sitting_proceeding_coverage.json"
)
OUTPUT_REVIEW_PATH = ROOT / "derived/sitting_proceeding_components/sitting_proceeding_review.csv"

REQUIRED_FIELDS = (
    "artifact_name",
    "artifact_version",
    "generated_at",
    "ok",
    "validation_status",
    "release_gate_status",
    "counts",
    "errors",
    "warnings",
    "source_hashes",
    "source_manifests",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _validate_schema(manifest: dict[str, Any]) -> list[str]:
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{location}: {error.message}")
    return failures


def _doc_terms(path: Path, terms: tuple[str, ...]) -> list[str]:
    text = _read(path)
    return [
        f"{path.relative_to(ROOT).as_posix()} is missing: {term}"
        for term in terms
        if term not in text
    ]


def _review_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        NEUTRAL_DOC_PATH,
        COMPONENT_DOC_PATH,
        ENDPOINT_DOC_PATH,
        RELEASE_LADDER_DOC_PATH,
        TRACK_PATH,
        HISTORICAL_COVERAGE_PATH,
        OUTPUT_COVERAGE_PATH,
        OUTPUT_REVIEW_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    failures.extend(_validate_schema(manifest))

    if manifest["artifact_name"] != "sitting_proceeding_component_validation":
        failures.append("artifact_name must be sitting_proceeding_component_validation.")
    if manifest["validation_status"] != "blocked":
        failures.append("validation_status must be blocked.")
    if manifest["release_gate_status"] != "blocked-pending-official-reconciliation":
        failures.append("release_gate_status must be blocked-pending-official-reconciliation.")
    if manifest["ok"] is not False:
        failures.append("ok must be false.")

    counts = manifest["counts"]
    if counts.get("fixture_sittings") != 1:
        failures.append("fixture_sittings must be 1.")
    if counts.get("fixture_proceeding_items") != 1:
        failures.append("fixture_proceeding_items must be 1.")
    if counts.get("validated_rows") != 0:
        failures.append("validated_rows must be 0.")
    if counts.get("review_rows") != 2:
        failures.append("review_rows must be 2.")
    if _review_row_count(OUTPUT_REVIEW_PATH) != 2:
        failures.append("review queue must contain two rows.")

    coverage = _json(OUTPUT_COVERAGE_PATH)
    if coverage.get("status") != "blocked":
        failures.append("coverage report must remain blocked.")
    if coverage.get("fixture_counts", {}).get("sittings") != 1:
        failures.append("coverage report fixture sitting count must be 1.")
    if coverage.get("fixture_counts", {}).get("proceeding_items") != 1:
        failures.append("coverage report fixture proceeding count must be 1.")
    if coverage.get("coverage_counts", {}).get("reconciled_sittings") != 0:
        failures.append("coverage report reconciled sitting count must be 0.")
    if coverage.get("coverage_counts", {}).get("reconciled_proceedings") != 0:
        failures.append("coverage report reconciled proceeding count must be 0.")

    doc_terms = (
        "blocked",
        "official sitting and proceeding reconciliation",
        "Future Validation Requirements",
        "review queue",
        "coverage",
    )
    failures.extend(_doc_terms(DOC_PATH, doc_terms))

    track_terms = (
        "Repo-side builder/checker are implemented",
        "blocked",
        "official sitting and proceeding evidence",
    )
    failures.extend(_doc_terms(TRACK_PATH, track_terms))

    failures.extend(_doc_terms(COMPONENT_DOC_PATH, ("sittings", "proceeding_items")))
    failures.extend(_doc_terms(ENDPOINT_DOC_PATH, ("sittings", "proceeding_items")))
    failures.extend(_doc_terms(NEUTRAL_DOC_PATH, ("sittings", "proceeding_items")))
    failures.extend(
        _doc_terms(RELEASE_LADDER_DOC_PATH, ("neutral-component", "sittings", "proceedings"))
    )

    historical = _json(HISTORICAL_COVERAGE_PATH)
    if historical["authority_cross_check"]["status"] != "available-not-yet-reconciled":
        failures.append("historical coverage audit must stay unreconciled.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"SITTING-PROCEEDING: {failure}")
        return 1
    print("Sitting and proceeding component release gate is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
