"""Validate historical coverage audit claims and release-language guardrails."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/historical_coverage_audit.json"
SCHEMA_PATH = ROOT / "schemas/historical_coverage_audit.schema.json"
DOC_PATH = ROOT / "docs/historical-coverage-audit.md"
README_PATH = ROOT / "README.md"
DATASET_CARD_PATH = ROOT / "DATASET_CARD.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
TRACK_PATH = ROOT / "conductor/tracks/historical_coverage_audit_20260609/evidence.md"

EXPECTED_PARLIAMENTS = set(range(47, 55))
EXPECTED_ROW_COUNTS = {
    47: 24378,
    48: 19709,
    49: 23877,
    50: 39803,
    51: 34808,
    52: 21171,
    53: 23402,
    54: 6774,
}
REQUIRED_STATUSES = {"verified", "partial", "unknown", "excluded"}
REQUIRED_AUTHORITY_SOURCES = {
    "nz-parliament-hansard-current",
    "nz-parliament-order-paper",
    "nz-parliament-daily-progress",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        README_PATH,
        DATASET_CARD_PATH,
        ENDPOINT_DOC_PATH,
        TRACK_PATH,
    ):
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

    source_inventory = _json(ROOT / "manifests/source_inventory.json")
    normalization = _json(ROOT / "manifests/normalization_validation.json")

    if manifest["source_archive"]["sha256"] != source_inventory["source_archive"]["sha256"]:
        failures.append("coverage audit source archive hash must match source inventory.")
    if manifest["source_archive"]["member_count"] != source_inventory["summary"]["member_count"]:
        failures.append("coverage audit source member count must match source inventory.")
    if manifest["source_archive"]["total_rows"] != normalization["summary"]["output_rows"]:
        failures.append("coverage audit total rows must match normalization validation.")

    claim_statuses = {claim["status"] for claim in manifest["claim_boundaries"]}
    missing_statuses = REQUIRED_STATUSES - claim_statuses
    if missing_statuses:
        failures.append(
            "coverage claim boundaries must include statuses: "
            + ", ".join(sorted(missing_statuses))
        )

    full_history_claims = [
        claim
        for claim in manifest["claim_boundaries"]
        if claim["claim_id"] == "full-historical-hansard-completeness"
    ]
    if not full_history_claims or full_history_claims[0]["status"] != "unknown":
        failures.append("full historical Hansard completeness must remain unknown.")

    parliament_coverage = {
        item["parliament_number"]: item for item in manifest["parliament_coverage"]
    }
    if set(parliament_coverage) != EXPECTED_PARLIAMENTS:
        failures.append("parliament coverage must cover exactly Parliament 47 through 54.")
    for parliament_number, expected_rows in EXPECTED_ROW_COUNTS.items():
        item = parliament_coverage.get(parliament_number)
        if item is None:
            continue
        if item["rows"] != expected_rows:
            failures.append(f"Parliament {parliament_number} row count is not {expected_rows}.")
        if item["coverage_status"] != "partial":
            failures.append(f"Parliament {parliament_number} must remain partial, not complete.")

    authority_ids = set(manifest["authority_cross_check"]["source_ids"])
    missing_authority = REQUIRED_AUTHORITY_SOURCES - authority_ids
    if missing_authority:
        failures.append(
            "coverage audit authority cross-check missing: " + ", ".join(sorted(missing_authority))
        )

    for required_gap in (
        "Before Parliament 47",
        "Within Parliament 47-54",
        "After the supplied Parliament 54 extract snapshot",
    ):
        if not any(gap["range"] == required_gap for gap in manifest["known_gaps"]):
            failures.append(f"coverage audit missing known gap: {required_gap}")

    guarded_docs = {
        "README.md": _read(README_PATH),
        "DATASET_CARD.md": _read(DATASET_CARD_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "docs/historical-coverage-audit.md": _read(DOC_PATH),
    }
    for relative_path, text in guarded_docs.items():
        for required in (
            "supplied DocumentsDB extract",
            "full historical NZ Hansard",
            "manifests/historical_coverage_audit.json",
        ):
            if required not in text:
                failures.append(f"{relative_path} is missing coverage language: {required}")

    track = _read(TRACK_PATH)
    for required in (
        "Coverage Manifest",
        "Archive Versus Historical Claims",
        "Authority Cross-Check",
        "Focused Validation",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"HISTORICAL-COVERAGE: {failure}")
        return 1
    print("Historical coverage audit manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
