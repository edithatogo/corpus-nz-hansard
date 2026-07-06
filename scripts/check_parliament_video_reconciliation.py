"""Validate the NZ Parliament video reconciliation contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_reconciliation.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_reconciliation.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-reconciliation.md"
LEDGER_PATH = (
    ROOT / "derived" / "parliament_video_reconciliation" / "parliament_video_reconciliation_ledger.json"
)
INVENTORY_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"
SEED_PATH = ROOT / "manifests" / "parliament_video_seed_fetchers.json"
ARCHIVE_PATH = ROOT / "manifests" / "parliament_video_archive_coverage.json"

EXPECTED_GAP_STATUSES = {
    "metadata-only",
    "rights-gated",
    "fallback-only",
    "evidence-only",
    "access-blocked",
    "migrated",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, LEDGER_PATH, INVENTORY_PATH, SEED_PATH, ARCHIVE_PATH):
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

    if manifest["reconciliation_status"] != "not-complete":
        failures.append("reconciliation_status must remain not-complete.")
    ledger = manifest["ledger"]
    summary = manifest["summary"]
    if summary["ledger_row_count"] != len(ledger):
        failures.append("summary.ledger_row_count must match the ledger length.")
    if summary["source_count"] != 19:
        failures.append("summary.source_count must remain 19.")
    for key in (
        "metadata_first",
        "no_video_file_download",
        "no_audio_file_download",
        "no_public_media_release",
        "no_completeness_claim",
        "rights_review_required_before_media_acquisition",
        "fallbacks_are_validation_only",
    ):
        if manifest["policy"].get(key) is not True:
            failures.append(f"policy.{key} must be true.")
    for key in (
        "retrospective_archive_complete",
        "ongoing_archive_complete",
        "complete_video_archive",
        "metadata_completeness_claim",
        "media_completeness_claim",
    ):
        if summary.get(key) is not False:
            failures.append(f"summary.{key} must remain false.")

    gap_statuses = {row["gap_status"] for row in ledger}
    missing_statuses = EXPECTED_GAP_STATUSES - gap_statuses
    if missing_statuses:
        failures.append("ledger must include gap statuses: " + ", ".join(sorted(missing_statuses)))

    if not any(row["gap_status"] == "migrated" for row in ledger):
        failures.append("ledger must record at least one migrated surface.")
    if not any(row["gap_status"] == "access-blocked" for row in ledger):
        failures.append("ledger must record at least one access-blocked surface.")
    if not any(row["source_id"] == "adjacent-sm-govt-nz" for row in ledger):
        failures.append("ledger must include adjacent-sm-govt-nz boundary evidence.")
    if not any(row["source_id"] == "memento-cdx-web-archives" for row in ledger):
        failures.append("ledger must include memento-cdx-web-archives evidence.")

    inventory = _json(INVENTORY_PATH)
    seed = _json(SEED_PATH)
    archive = _json(ARCHIVE_PATH)
    if manifest["summary"]["seed_target_count"] != seed["summary"]["target_count"]:
        failures.append("summary.seed_target_count must match the seed manifest target count.")
    if manifest["summary"]["official_source_count"] != len(inventory["source_summary"]["official_source_ids"]):
        failures.append("summary.official_source_count must match the inventory manifest.")
    if manifest["summary"]["fallback_source_count"] != len(inventory["source_summary"]["fallback_source_ids"]):
        failures.append("summary.fallback_source_count must match the inventory manifest.")
    if len(manifest["adjacent_repo_findings"]) != len(archive["adjacent_repo_findings"]):
        failures.append("adjacent repo findings must mirror the archive coverage manifest.")

    doc_text = _read(DOC_PATH)
    for required in (
        "metadata-first reconciliation ledger",
        "not a complete retrospective archive",
        "media-completeness claim",
        "Gap Taxonomy",
        "Source Priorities",
        "Exception Ledger",
        "Fallback sources are validation only",
    ):
        if required not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    ledger_payload = _json(LEDGER_PATH)
    if ledger_payload["track_id"] != manifest["track_id"]:
        failures.append("derived ledger track_id must match the manifest.")
    if ledger_payload["summary"]["ledger_row_count"] != manifest["summary"]["ledger_row_count"]:
        failures.append("derived ledger summary must mirror the manifest.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-RECONCILIATION: {failure}")
        return 1
    print("Parliament video reconciliation contract is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
