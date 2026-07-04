"""Validate Parliament dataset seed-fetcher outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/parliament_dataset_seed_fetchers.json"
SCHEMA_PATH = ROOT / "schemas/parliament_dataset_seed_fetchers.schema.json"
DOC_PATH = ROOT / "docs/parliament-dataset-seed-fetchers.md"
INVENTORY_PATH = ROOT / "manifests/parliament_dataset_inventory.json"

REQUIRED_DATASET_FAMILIES = {
    "hansard_debates",
    "daily_progress",
    "journals",
    "papers_presented_ajhr",
    "order_paper_questions_business_sitting_programme",
    "select_committees",
    "petitions",
    "members_parties_seating_contacts",
    "parliamentary_rules_procedure",
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
    source_inventory = _json(INVENTORY_PATH)
    inventory_sources = {source["id"]: source for source in source_inventory["sources"]}

    if manifest.get("summary", {}).get("total_target_count") != len(targets):
        failures.append("summary.total_target_count must match targets length.")

    approved_families = {
        target["dataset_family"] for target in targets if target.get("approved") is True
    }
    if approved_families != REQUIRED_DATASET_FAMILIES:
        failures.append(
            "approved targets must cover exactly the approved seed families: "
            + ", ".join(sorted(REQUIRED_DATASET_FAMILIES))
        )

    seen_families: dict[str, list[str]] = {}
    for target in targets:
        family = target["dataset_family"]
        source_id = target["source_id"]
        seen_families.setdefault(family, []).append(source_id)

        source = inventory_sources.get(source_id)
        if source is None:
            failures.append(f"{source_id} is not present in the inventory manifest.")
            continue
        if target["source_posture"] != source["source_posture"]:
            failures.append(f"{source_id} posture must match the inventory manifest.")
        if source["source_posture"] == "excluded":
            failures.append(f"{source_id} must not be selected because it is excluded.")
        if target["proof_status"] == "fetched":
            if not target.get("index_sha256") or not target.get("sample_sha256"):
                failures.append(f"{source_id} fetched proof must carry both hashes.")
        if target["proof_status"] == "blocked":
            if not target.get("blocked_reason"):
                failures.append(f"{source_id} blocked proof must declare a blocked_reason.")
        if len(target.get("request_urls", [])) > 2:
            failures.append(f"{source_id} must keep request_urls bounded.")

    for family in REQUIRED_DATASET_FAMILIES:
        if family not in seen_families:
            failures.append(f"{family} must have at least one seed target.")

    for family, _source_ids in seen_families.items():
        family_targets = [target for target in targets if target["dataset_family"] == family]
        first_fallback = next(
            (
                index
                for index, target in enumerate(family_targets)
                if target["source_posture"] == "fallback"
            ),
            len(family_targets),
        )
        if any(
            target["source_posture"] == "official" for target in family_targets[first_fallback:]
        ):
            failures.append(f"{family} must list official targets before fallback targets.")

    doc = _read(DOC_PATH)
    for required in (
        "bounded seed proofs",
        "full acquisition",
        "no bulk acquisition",
        "official Parliament sources are preferred",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, INVENTORY_PATH):
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
            print(f"PARLIAMENT-SEED-FETCHERS: {failure}")
        return 1
    print("Parliament seed fetcher manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
