"""Validate Parliament dataset full-acquisition outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/parliament_dataset_full_acquisition.json"
SCHEMA_PATH = ROOT / "schemas/parliament_dataset_full_acquisition.schema.json"
DOC_PATH = ROOT / "docs/parliament-dataset-full-acquisition.md"
INVENTORY_PATH = ROOT / "manifests/parliament_dataset_inventory.json"
SEED_MANIFEST_PATH = ROOT / "manifests/parliament_dataset_seed_fetchers.json"

REQUIRED_DATASET_FAMILIES = {
    "journals",
    "papers_presented_ajhr",
    "order_paper_questions_business_sitting_programme",
    "select_committees",
    "petitions",
    "members_parties_seating_contacts",
    "video_audio_calendar",
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
    targets = manifest.get("targets", [])
    reconciliation = manifest.get("reconciliation", [])

    if manifest.get("publication_boundary") != "not-public-release-ready":
        failures.append("publication_boundary must remain not-public-release-ready.")

    policy = manifest.get("policy", {})
    for key in (
        "official_sources_first",
        "rights_safe",
        "no_bulk_acquisition",
        "no_public_release",
        "excludes_nz_legislation",
        "excludes_nz_gazette",
        "hathitrust_not_acquisition_dependency",
        "internet_archive_not_acquisition_dependency",
        "no_historical_completeness_claim",
    ):
        if policy.get(key) is not True:
            failures.append(f"policy.{key} must be true.")

    approved_families = {
        target["dataset_family"] for target in targets if target.get("approved") is True
    }
    if approved_families != REQUIRED_DATASET_FAMILIES:
        failures.append(
            "approved targets must cover exactly the approved acquisition families: "
            + ", ".join(sorted(REQUIRED_DATASET_FAMILIES))
        )

    if manifest.get("summary", {}).get("total_target_count") != len(targets):
        failures.append("summary.total_target_count must match targets length.")
    if manifest.get("summary", {}).get("family_count") != len(
        {target["dataset_family"] for target in targets}
    ):
        failures.append("summary.family_count must match target families.")
    if manifest.get("summary", {}).get("reconciled_family_count") != len(reconciliation):
        failures.append("summary.reconciled_family_count must match reconciliation rows.")

    seen_pairs: set[tuple[str, str]] = set()
    for target in targets:
        pair = (target["dataset_family"], target["source_id"])
        if pair in seen_pairs:
            failures.append(f"duplicate acquisition target: {pair[0]} / {pair[1]}")
        seen_pairs.add(pair)

        if target["rights_boundary"] != "not-public-release-ready":
            failures.append(f"{target['source_id']} rights boundary must remain gated.")
        if target["proof_status"] == "fetched":
            if not target.get("index_sha256") or not target.get("detail_sha256s"):
                failures.append(f"{target['source_id']} fetched target must carry hashes.")
            if not target.get("detail_paths"):
                failures.append(f"{target['source_id']} fetched target must record detail paths.")
        if target["proof_status"] == "blocked" and not target.get("blocked_reason"):
            failures.append(f"{target['source_id']} blocked target must record a reason.")
        if len(target.get("request_urls", [])) > 3:
            failures.append(f"{target['source_id']} must keep request_urls bounded.")
        if target["dataset_family"] not in REQUIRED_DATASET_FAMILIES:
            failures.append(f"{target['source_id']} uses an unsupported dataset family.")

    families = {target["dataset_family"] for target in targets}
    if families != REQUIRED_DATASET_FAMILIES:
        failures.append(
            "targets must cover exactly the approved acquisition families: "
            + ", ".join(sorted(REQUIRED_DATASET_FAMILIES))
        )

    doc = _read(DOC_PATH)
    for required in (
        "repeatable, resumable, hash-backed, rights-safe",
        "not-public-release-ready",
        "cache policy",
        "refresh cadence",
        "official Parliament sources are preferred",
        "no bulk acquisition",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    seed_manifest = _json(SEED_MANIFEST_PATH)
    if seed_manifest.get("summary", {}).get("approved_target_count", 0) < len(
        REQUIRED_DATASET_FAMILIES
    ):
        failures.append("seed manifest must retain the approved seed-proof baseline.")

    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, INVENTORY_PATH, SEED_MANIFEST_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures
    failures.extend(_validate_manifest(_json(MANIFEST_PATH)))
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-FULL-ACQUISITION: {failure}")
        return 1
    print("Parliament full-acquisition manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
