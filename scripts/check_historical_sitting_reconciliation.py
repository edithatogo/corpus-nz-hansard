"""Validate the historical sitting reconciliation contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/historical_sitting_reconciliation.json"
SCHEMA_PATH = ROOT / "schemas/historical_sitting_reconciliation.schema.json"
DOC_PATH = ROOT / "docs/historical-sitting-reconciliation.md"
TRACK_PATH = ROOT / "conductor/tracks/full_historical_sitting_reconciliation_20260610/evidence.md"
INVENTORY_PATH = ROOT / "manifests/historical_sitting_inventory.json"
HISTORICAL_COVERAGE_PATH = ROOT / "manifests/historical_coverage_audit.json"
LEDGER_PATH = ROOT / "derived/historical_sitting_reconciliation/historical_sitting_ledger.parquet"
SUMMARY_PATH = ROOT / "derived/historical_sitting_reconciliation/historical_sitting_ledger_summary.json"

EXPECTED_SOURCE_IDS = {
    "nz-parliament-parliamentary-business-hub",
    "nz-parliament-historic-journals-of-the-house",
    "nz-parliament-daily-progress",
    "nz-parliament-journals-indexes",
    "nz-parliament-order-paper",
    "nz-parliament-weekly-journals-archive",
    "nz-parliament-sessional-journals-archive",
    "nz-parliament-hansard-current",
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
        TRACK_PATH,
        INVENTORY_PATH,
        HISTORICAL_COVERAGE_PATH,
        LEDGER_PATH,
        SUMMARY_PATH,
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

    inventory = _json(INVENTORY_PATH)
    source_ids = {item["id"] for item in inventory["sources"]}
    if source_ids != EXPECTED_SOURCE_IDS:
        failures.append(
            "historical sitting inventory source ids must match the official Parliament inventory."
        )
    if manifest["official_inventory"]["source_count"] != len(source_ids):
        failures.append("official inventory source count must match the inventory manifest.")

    coverage = _json(HISTORICAL_COVERAGE_PATH)
    if coverage["authority_cross_check"]["status"] != "available-not-yet-reconciled":
        failures.append("historical coverage audit must remain unreconciled until comparison runs.")

    summary = _json(SUMMARY_PATH)
    if summary["row_count"] != manifest["current_state"]["corpus_archive_rows"]:
        failures.append("ledger row count must match the corpus archive row count.")
    if summary["source_row_count"] != manifest["current_state"]["corpus_archive_rows"]:
        failures.append("summary source row count must match the corpus archive row count.")
    if summary["sitting_date_extracted_rows"] <= 0:
        failures.append("ledger summary must record at least one extracted sitting date.")
    if summary["volume_page_extracted_rows"] <= 0:
        failures.append("ledger summary must record at least one extracted volume/page reference.")

    track = _read(TRACK_PATH)
    for required in (
        "comparison-ready",
        "official inventory",
        "ledger",
        "blocked on comparison execution",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    doc = _read(DOC_PATH)
    for required in (
        "comparison contract",
        "comparison keys",
        "tolerance rules",
        "gap taxonomy",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    if manifest["comparison_status"] != "comparison-ready":
        failures.append("comparison_status must be comparison-ready.")
    if manifest["current_state"]["status"] != "comparison-ready":
        failures.append("current_state.status must be comparison-ready.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"HISTORICAL-SITTING-RECONCILIATION: {failure}")
        return 1
    print("Historical sitting reconciliation contract is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
