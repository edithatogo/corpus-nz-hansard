"""Validate the Parliament dataset inventory manifest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/parliament_dataset_inventory.json"
SCHEMA_PATH = ROOT / "schemas/parliament_dataset_inventory.schema.json"
DOC_PATH = ROOT / "docs/parliament-dataset-inventory.md"
AUTHORITY_SOURCES_PATH = ROOT / "manifests/authority_sources.json"
HISTORICAL_SITTING_PATH = ROOT / "manifests/historical_sitting_inventory.json"
CROSS_REPO_DOC_PATH = ROOT / "docs/cross-repo-dataset-architecture.md"

REQUIRED_DATASET_FAMILIES = {
    "hansard_debates",
    "order_paper_questions_business_sitting_programme",
    "daily_progress",
    "journals",
    "papers_presented_ajhr",
    "select_committees",
    "petitions",
    "members_parties_seating_contacts",
    "parliamentary_rules_procedure",
    "video_audio_calendar",
}
VALID_POSTURES = {"official", "fallback", "supporting", "evidence_only", "excluded"}
OFFICIAL_PUBLISHER = "New Zealand Parliament"
EXCLUDED_IDS = {
    "excluded-nz-legislation",
    "excluded-nz-gazette",
    "excluded-hathitrust",
    "excluded-internet-archive",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _schema_failures(manifest: dict[str, Any]) -> list[str]:
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")
    return failures


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures = _schema_failures(manifest)
    families = set(manifest.get("dataset_families", []))
    if families != REQUIRED_DATASET_FAMILIES:
        failures.append(
            "dataset_families must exactly match required families: "
            + ", ".join(sorted(REQUIRED_DATASET_FAMILIES))
        )

    family_coverage = manifest.get("family_coverage", {})
    if set(family_coverage) != REQUIRED_DATASET_FAMILIES:
        failures.append("family_coverage must cover every required dataset family.")

    sources = manifest.get("sources", [])
    source_ids = [source.get("id") for source in sources]
    duplicate_ids = sorted(
        {source_id for source_id in source_ids if source_ids.count(source_id) > 1}
    )
    for source_id in duplicate_ids:
        failures.append(f"Duplicate source id: {source_id}")

    sources_by_id = {source["id"]: source for source in sources if "id" in source}
    for source in sources:
        source_id = source.get("id", "<missing>")
        posture = source.get("source_posture")
        if posture not in VALID_POSTURES:
            failures.append(f"{source_id} has unsupported source_posture: {posture}")
        unknown_families = set(source.get("dataset_families", [])) - REQUIRED_DATASET_FAMILIES
        if unknown_families:
            failures.append(
                f"{source_id} uses unknown families: {', '.join(sorted(unknown_families))}"
            )
        if posture == "fallback" and not source.get("fallback_for"):
            failures.append(f"{source_id} fallback source must declare fallback_for source IDs.")
        for fallback_target in source.get("fallback_for", []):
            if fallback_target not in sources_by_id:
                failures.append(
                    f"{source_id} fallback_for references missing source: {fallback_target}"
                )
        if posture == "official" and source.get("publisher") != OFFICIAL_PUBLISHER:
            failures.append(f"{source_id} is official but publisher is not New Zealand Parliament.")
        if posture == "excluded":
            if not source.get("excluded"):
                failures.append(f"{source_id} has excluded posture but excluded=false.")
            if source.get("acquisition_priority") != "excluded":
                failures.append(f"{source_id} exclusion must use acquisition_priority=excluded.")
        elif source.get("excluded"):
            failures.append(f"{source_id} is excluded=true without excluded posture.")
        if "complete" in source.get("coverage_period", "").lower():
            failures.append(f"{source_id} coverage_period must not claim completeness.")

    missing_exclusions = EXCLUDED_IDS - set(sources_by_id)
    if missing_exclusions:
        failures.append("missing explicit exclusions: " + ", ".join(sorted(missing_exclusions)))

    for source_id in EXCLUDED_IDS & set(sources_by_id):
        source = sources_by_id[source_id]
        if source["source_posture"] != "excluded":
            failures.append(f"{source_id} must use excluded posture.")

    for source in sources:
        if source.get("publisher") == "data.govt.nz":
            if source.get("source_posture") != "evidence_only":
                failures.append(f"{source['id']} data.govt.nz records must be evidence_only.")
            if source.get("acquisition_priority") != "evidence_only":
                failures.append(
                    f"{source['id']} data.govt.nz records must not be acquisition targets."
                )

    for family, coverage in family_coverage.items():
        primary_ids = coverage.get("primary_source_ids", [])
        if not primary_ids:
            failures.append(f"{family} must declare primary_source_ids.")
        for source_id in primary_ids + coverage.get("fallback_source_ids", []):
            if source_id not in sources_by_id:
                failures.append(f"{family} references missing source id: {source_id}")
            elif family not in sources_by_id[source_id]["dataset_families"]:
                failures.append(f"{family} references source without matching family: {source_id}")
        if not any(
            sources_by_id.get(source_id, {}).get("source_posture") == "official"
            for source_id in primary_ids
        ):
            failures.append(f"{family} must have an official primary source.")
        if coverage.get("completion_claim") != "inventory-only-no-completeness-claim":
            failures.append(f"{family} has unsupported completion claim.")

    for family in REQUIRED_DATASET_FAMILIES:
        family_sources = [
            source
            for source in sources
            if family in source.get("dataset_families", [])
            and source.get("source_posture") != "excluded"
        ]
        first_non_official = next(
            (
                index
                for index, source in enumerate(family_sources)
                if source.get("source_posture") != "official"
            ),
            len(family_sources),
        )
        for source in family_sources[first_non_official:]:
            if source.get("source_posture") == "official":
                failures.append(f"{family} does not list official sources before fallbacks.")

    policy = manifest.get("policy", {})
    for key in (
        "official_sources_first",
        "excludes_nz_legislation",
        "excludes_nz_gazette",
        "hathitrust_not_acquisition_dependency",
        "internet_archive_not_acquisition_dependency",
        "no_bulk_acquisition",
        "no_historical_completeness_claim",
        "data_govt_requests_evidence_only",
    ):
        if policy.get(key) is not True:
            failures.append(f"policy.{key} must be true.")

    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        AUTHORITY_SOURCES_PATH,
        HISTORICAL_SITTING_PATH,
        CROSS_REPO_DOC_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    failures.extend(_validate_manifest(manifest))

    authority_sources = _json(AUTHORITY_SOURCES_PATH)
    authority_ids = {source["id"] for source in authority_sources["sources"]}
    reused_ids = {
        "nz-parliament-hansard-current",
        "nz-parliament-order-paper",
        "nz-parliament-daily-progress",
        "nz-parliament-weekly-journals-archive",
        "nz-parliament-written-questions",
        "nz-parliament-oral-questions",
        "nz-parliament-parliamentary-rules",
        "nz-parliament-members-current",
    }
    missing_reused_ids = reused_ids - authority_ids
    if missing_reused_ids:
        failures.append(
            "authority_sources.json no longer contains expected source ids: "
            + ", ".join(sorted(missing_reused_ids))
        )

    doc = _read(DOC_PATH)
    cross_repo_doc = _read(CROSS_REPO_DOC_PATH)
    for required in (
        "NZ legislation and Gazette remain out of scope",
        "HathiTrust and Internet Archive are excluded acquisition dependencies",
        "Data.govt.nz requests are evidence only",
        "parliament_dataset_seed_fetchers_20260703",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")
    if "manifests/parliament_dataset_inventory.json" not in cross_repo_doc:
        failures.append(
            "cross-repo architecture doc must reference parliament_dataset_inventory.json."
        )

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-DATASET-INVENTORY: {failure}")
        return 1
    print("Parliament dataset inventory manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
