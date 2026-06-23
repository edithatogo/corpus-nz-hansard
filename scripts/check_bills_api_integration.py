"""Validate the Bills API integration validation surface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/bills_api_integration_validation.json"
CROSSREF_PATH = ROOT / "derived/bills_api/member_hansard_cross_reference.json"
LEGACY_CROSSREF_PATH = ROOT / "derived/crossref_bills_api.json"
STAGE_METADATA_PATH = ROOT / "derived/bills_api/bill_stage_metadata.json"
DOC_PATH = ROOT / "docs/bills-api-integration.md"
PLAN_PATH = ROOT / "conductor/tracks/bills_api_integration_20260612/plan.md"
METADATA_PATH = ROOT / "conductor/tracks/bills_api_integration_20260612/metadata.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _doc_terms(path: Path, terms: tuple[str, ...]) -> list[str]:
    text = _read(path)
    return [
        f"{path.relative_to(ROOT).as_posix()} is missing: {term}"
        for term in terms
        if term not in text
    ]


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        CROSSREF_PATH,
        LEGACY_CROSSREF_PATH,
        STAGE_METADATA_PATH,
        DOC_PATH,
        PLAN_PATH,
        METADATA_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    crossref = _json(CROSSREF_PATH)
    legacy_crossref = _json(LEGACY_CROSSREF_PATH)
    stage_metadata = _json(STAGE_METADATA_PATH)
    metadata = _json(METADATA_PATH)
    if manifest["artifact_name"] != "bills_api_integration_validation":
        failures.append("artifact_name must be bills_api_integration_validation.")
    if manifest["track_id"] != "bills_api_integration_20260612":
        failures.append("track_id must match the Bills API integration track.")
    if manifest["validation_status"] != "metadata-ready":
        failures.append("Bills API validation status must be metadata-ready.")
    if manifest["release_gate_status"] != "ready-for-corpus-metadata-integration":
        failures.append("Bills API release gate must be ready for corpus metadata integration.")
    if manifest["authority_source_registered"] is not True:
        failures.append("nz-parliament-bills-api must be registered in authority_sources.")

    run = manifest["extraction_run"]
    if run["bill_summaries_fetched"] < 3513:
        failures.append("Bills API capture must preserve at least the original 3,513 summaries.")
    if run["bill_details_processed"] != run["bill_summaries_fetched"]:
        failures.append("Bills API detail count must match summary count.")
    if run["unique_member_names"] != 351:
        failures.append("Bills API member capture must preserve 351 unique member names.")
    if run["members_artifact_count"] != 351:
        failures.append("members artifact must preserve 351 unique member names.")

    artifacts = manifest["captured_artifacts"]
    for name in ("members", "summary", "details", "bill_stage_metadata"):
        if artifacts[name]["valid_json"] is not True:
            failures.append(f"{name} artifact must be valid JSON.")
        if artifacts[name]["truncated"] is not False:
            failures.append(f"{name} artifact must not be truncated.")
    if artifacts["summary"].get("record_count") != run["bill_summaries_fetched"]:
        failures.append("summary artifact record_count must match extraction count.")
    if artifacts["details"].get("record_count") != run["bill_details_processed"]:
        failures.append("details artifact record_count must match extraction count.")
    if manifest["corpus_metadata_integration"]["status"] != "ready":
        failures.append("corpus metadata integration must be ready after full capture.")
    if manifest["corpus_metadata_integration"]["bill_stage_source_available"] is not True:
        failures.append("bill stage metadata source must be marked available.")
    if manifest["corpus_metadata_integration"].get("metadata_artifact") != (
        "derived/bills_api/bill_stage_metadata.json"
    ):
        failures.append("corpus metadata integration must point at bill_stage_metadata.json.")

    if stage_metadata["status"] != "metadata-ready":
        failures.append("bill-stage metadata artifact must be metadata-ready.")
    if stage_metadata["counts"]["bills"] != run["bill_details_processed"]:
        failures.append("bill-stage metadata bill count must match detail count.")
    if stage_metadata["counts"]["stage_records"] <= run["bill_details_processed"]:
        failures.append("bill-stage metadata must include multiple stage records across bills.")

    counts = crossref["counts"]
    if counts["bills_api_members"] != 351:
        failures.append("cross-reference must cover 351 Bills API member names.")
    if counts["exact_or_honorific_normalized_matches"] <= 0:
        failures.append("cross-reference must find at least one Hansard name match.")
    if (
        counts["exact_or_honorific_normalized_matches"] + counts["unmatched_bills_api_members"]
        != counts["bills_api_members"]
    ):
        failures.append("cross-reference counts must add up to Bills API member count.")
    if legacy_crossref.get("bills_api_members_count") != 351:
        failures.append("legacy crossref summary must report 351 Bills API members.")
    if legacy_crossref.get("cross_reference_artifact") != (
        "derived/bills_api/member_hansard_cross_reference.json"
    ):
        failures.append("legacy crossref summary must point to the full cross-reference artifact.")

    failures.extend(
        _doc_terms(
            DOC_PATH,
            (
                "3,516",
                "351",
                "non-truncated",
                "metadata-ready",
                "bill_stage_metadata.json",
                "member_hansard_cross_reference.json",
            ),
        )
    )
    plan_text = _read(PLAN_PATH)
    if "[ ]" in plan_text or "[~]" in plan_text or "[!]" in plan_text:
        failures.append("Bills API integration plan must not contain open task markers.")
    if metadata.get("status") != "completed":
        failures.append("Bills API track metadata status must be completed.")
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"BILLS-API-INTEGRATION: {failure}")
        return 1
    print("Bills API integration validation surface is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
