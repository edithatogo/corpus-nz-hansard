"""Validate the vote, motion, bill, and question extraction release surface."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/vote_motion_bill_question_extraction_validation.json"
SCHEMA_PATH = ROOT / "schemas/vote_motion_bill_question_extraction_validation.schema.json"
DOC_PATH = ROOT / "docs/vote-motion-bill-question-extraction-release.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
PROCEDURE_DOC_PATH = ROOT / "docs/nz-parliamentary-procedure-model.md"
TRACK_PATH = (
    ROOT / "conductor/tracks/vote_motion_bill_question_extraction_release_20260610/index.md"
)
OUTPUT_COVERAGE_PATH = (
    ROOT / "derived/vote_motion_bill_question_extraction/extraction_coverage.json"
)
OUTPUT_REVIEW_PATH = ROOT / "derived/vote_motion_bill_question_extraction/extraction_review.csv"

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


def _review_rows() -> list[dict[str, str]]:
    with OUTPUT_REVIEW_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        COMPONENT_DOC_PATH,
        ENDPOINT_DOC_PATH,
        PROCEDURE_DOC_PATH,
        TRACK_PATH,
        OUTPUT_COVERAGE_PATH,
        OUTPUT_REVIEW_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    failures.extend(_validate_schema(manifest))

    if manifest["artifact_name"] != "vote_motion_bill_question_extraction_validation":
        failures.append("artifact_name must be vote_motion_bill_question_extraction_validation.")
    if manifest["validation_status"] != "blocked":
        failures.append("validation_status must be blocked.")
    if manifest["release_gate_status"] != "blocked-pending-validated-components":
        failures.append("release_gate_status must be blocked-pending-validated-components.")
    if manifest["ok"] is not False:
        failures.append("ok must be false.")

    counts = manifest["counts"]
    if counts.get("procedure_samples_reviewed") != 6:
        failures.append("procedure_samples_reviewed must be 6.")
    if counts.get("vote_samples") != 2:
        failures.append("vote_samples must be 2.")
    if counts.get("question_samples") != 1:
        failures.append("question_samples must be 1.")
    if counts.get("procedural_decision_samples") != 2:
        failures.append("procedural_decision_samples must be 2.")
    if counts.get("boundary_samples") != 1:
        failures.append("boundary_samples must be 1.")
    if counts.get("validated_rows") != 0:
        failures.append("validated_rows must be 0.")
    if counts.get("review_rows") != 6:
        failures.append("review_rows must be 6.")
    if counts.get("blocked_rows") != 5:
        failures.append("blocked_rows must be 5.")
    if counts.get("excluded_rows") != 1:
        failures.append("excluded_rows must be 1.")

    review_rows = _review_rows()
    if len(review_rows) != 6:
        failures.append("review queue must contain six rows.")
    categories = {row["category"] for row in review_rows}
    if categories != {"party_vote", "personal_vote", "question", "stage", "ruling", "interjection"}:
        failures.append("review queue must cover the expected procedure categories.")
    if any(row["review_status"] == "" for row in review_rows):
        failures.append("review queue rows must preserve review status.")
    if review_rows[-1]["extraction_status"] != "excluded-by-design":
        failures.append("interjection boundary row must be excluded-by-design.")

    coverage = _json(OUTPUT_COVERAGE_PATH)
    if coverage.get("status") != "blocked":
        failures.append("coverage report must remain blocked.")
    if coverage.get("sample_counts", {}).get("procedure_samples_reviewed") != 6:
        failures.append("coverage report procedure sample count must be 6.")
    if coverage.get("gold_vote_domain", {}).get("sample_total") != 5:
        failures.append("coverage report must preserve five reviewed vote gold samples.")

    failures.extend(
        _doc_terms(
            DOC_PATH,
            (
                "blocked",
                "validated member identity",
                "validated party attribution",
                "validated sitting/proceeding",
                "review queue",
            ),
        )
    )
    failures.extend(
        _doc_terms(
            TRACK_PATH,
            (
                "blocked",
                "validated member identity",
                "validated party attribution",
                "validated sitting/proceeding",
            ),
        )
    )

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"VOTE-MOTION-BILL-QUESTION: {failure}")
        return 1
    print("Vote motion bill question extraction gate is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
