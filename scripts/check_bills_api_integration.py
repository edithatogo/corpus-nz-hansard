"""Validate the Bills API integration validation surface."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/bills_api_integration_validation.json"
CROSSREF_PATH = ROOT / "derived/bills_api/member_hansard_cross_reference.json"
LEGACY_CROSSREF_PATH = ROOT / "derived/crossref_bills_api.json"
DOC_PATH = ROOT / "docs/bills-api-integration.md"
PLAN_PATH = ROOT / "conductor/tracks/bills_api_integration_20260612/plan.md"


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
    for path in (MANIFEST_PATH, CROSSREF_PATH, LEGACY_CROSSREF_PATH, DOC_PATH, PLAN_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    crossref = _json(CROSSREF_PATH)
    legacy_crossref = _json(LEGACY_CROSSREF_PATH)
    if manifest["artifact_name"] != "bills_api_integration_validation":
        failures.append("artifact_name must be bills_api_integration_validation.")
    if manifest["track_id"] != "bills_api_integration_20260612":
        failures.append("track_id must match the Bills API integration track.")
    if manifest["authority_source_registered"] is not True:
        failures.append("nz-parliament-bills-api must be registered in authority_sources.")
    run = manifest["extraction_run"]
    if run["bill_summaries_fetched"] != 3513:
        failures.append("run log must preserve 3,513 fetched bill summaries.")
    if run["bill_details_processed"] != 3513:
        failures.append("run log must preserve 3,513 processed bill details.")
    if run["unique_member_names"] != 351:
        failures.append("run log must preserve 351 unique member names.")
    if run["members_artifact_count"] != 351:
        failures.append("members artifact must preserve 351 unique member names.")

    artifacts = manifest["captured_artifacts"]
    if artifacts["members"]["valid_json"] is not True:
        failures.append("members artifact must remain valid JSON.")
    if artifacts["summary"]["truncated"] is not True:
        failures.append("summary artifact must be declared as truncated.")
    if artifacts["details"]["truncated"] is not True:
        failures.append("details artifact must be declared as truncated.")
    if manifest["corpus_metadata_integration"]["status"] != "deferred":
        failures.append("corpus metadata integration must remain deferred.")
    if manifest["corpus_metadata_integration"]["bill_stage_source_available"] is not True:
        failures.append("bill stage metadata source must be marked available.")

    counts = crossref["counts"]
    if counts["bills_api_members"] != 351:
        failures.append("cross-reference must cover 351 Bills API member names.")
    if counts["exact_or_honorific_normalized_matches"] <= 0:
        failures.append("cross-reference must find at least one Hansard name match.")
    if (
        counts["exact_or_honorific_normalized_matches"]
        + counts["unmatched_bills_api_members"]
        != counts["bills_api_members"]
    ):
        failures.append("cross-reference counts must add up to Bills API member count.")
    if legacy_crossref.get("bills_api_members_count") != 351:
        failures.append("legacy crossref summary must no longer report zero Bills API members.")
    if legacy_crossref.get("cross_reference_artifact") != (
        "derived/bills_api/member_hansard_cross_reference.json"
    ):
        failures.append("legacy crossref summary must point to the full cross-reference artifact.")

    failures.extend(
        _doc_terms(
            DOC_PATH,
            (
                "3,513",
                "351",
                "truncated",
                "deferred",
                "member_hansard_cross_reference.json",
            ),
        )
    )
    plan_text = _read(PLAN_PATH)
    if "[ ]" in plan_text or "[!]" in plan_text or "[~]" in plan_text:
        failures.append("Bills API integration plan must not contain open task markers.")
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
