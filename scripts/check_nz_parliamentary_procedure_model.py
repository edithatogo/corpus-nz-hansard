"""Validate NZ parliamentary procedure model, fixtures, and endpoint mappings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/nz_parliamentary_procedure_model.json"
MANIFEST_SCHEMA_PATH = ROOT / "schemas/nz_parliamentary_procedure_model.schema.json"
FIXTURE_PATH = ROOT / "fixtures/nz_parliamentary_procedure_samples.json"
FIXTURE_SCHEMA_PATH = ROOT / "schemas/nz_parliamentary_procedure_samples.schema.json"
DOC_PATH = ROOT / "docs/nz-parliamentary-procedure-model.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
AUTHORITY_MANIFEST_PATH = ROOT / "manifests/authority_sources.json"
TRACK_PATH = ROOT / "conductor/tracks/nz_parliamentary_procedure_model_20260609/evidence.md"

REQUIRED_CATEGORIES = {
    "party_vote",
    "personal_vote",
    "question",
    "supplementary_question",
    "stage",
    "ruling",
    "interjection",
    "procedural_unit",
}
REQUIRED_LINKS = {"document", "sitting", "member", "party", "motion", "bill", "vote"}
REQUIRED_AUTHORITY_IDS = {
    "nz-parliament-parliamentary-rules",
    "nz-parliament-order-paper",
    "nz-parliament-hansard-current",
    "nz-parliament-daily-progress",
    "nz-parliament-bills-current",
    "nz-parliament-written-questions",
    "nz-parliament-oral-questions",
}
REQUIRED_ENDPOINTS = {
    "parlamint_nz_endpoint_20260609",
    "popolo_opencivicdata_endpoint_20260609",
    "akoma_ntoso_endpoint_20260609",
    "cap_parlacap_topic_endpoint_20260609",
}
REQUIRED_FIXTURE_CATEGORIES = {
    "party_vote",
    "personal_vote",
    "question",
    "stage",
    "ruling",
    "interjection",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _validate_json(data_path: Path, schema_path: Path, failures: list[str], label: str) -> None:
    data = _json(data_path)
    schema = _json(schema_path)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{label} {location}: {error.message}")


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        MANIFEST_SCHEMA_PATH,
        FIXTURE_PATH,
        FIXTURE_SCHEMA_PATH,
        DOC_PATH,
        COMPONENT_DOC_PATH,
        ENDPOINT_DOC_PATH,
        AUTHORITY_MANIFEST_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    _validate_json(MANIFEST_PATH, MANIFEST_SCHEMA_PATH, failures, "procedure manifest")
    _validate_json(FIXTURE_PATH, FIXTURE_SCHEMA_PATH, failures, "procedure fixtures")

    manifest = _json(MANIFEST_PATH)
    fixtures = _json(FIXTURE_PATH)
    authority_ids = {source["id"] for source in _json(AUTHORITY_MANIFEST_PATH)["sources"]}

    if set(manifest["authority_source_ids"]) != REQUIRED_AUTHORITY_IDS:
        failures.append("Procedure model must cite the required authority sources.")
    if not set(manifest["authority_source_ids"]).issubset(authority_ids):
        failures.append(
            "Procedure model cites authority sources not present in authority_sources.json."
        )

    categories = {item["category"]: item for item in manifest["procedural_categories"]}
    if set(categories) != REQUIRED_CATEGORIES:
        failures.append("Procedure model must define every required procedural category.")
    if set(manifest["component_links"]) != REQUIRED_LINKS:
        failures.append(
            "Procedure model component links must cover document/sitting/member/party/motion/bill/vote."
        )

    for category_name, category in categories.items():
        if not set(category["authority_source_ids"]).issubset(authority_ids):
            failures.append(f"{category_name} cites unknown authority source IDs.")
        if not set(category["required_links"]).issubset(REQUIRED_LINKS | {"proceeding_item"}):
            failures.append(f"{category_name} cites unknown component links.")
        if "uncertainty" not in " ".join(category["uncertainty_fields"]):
            failures.append(f"{category_name} must record uncertainty/status fields.")

    if "candidate evidence" not in manifest["uncertainty_policy"]["rule"]:
        failures.append(
            "Uncertainty policy must state that surface text is only candidate evidence."
        )

    endpoint_tracks = {item["track_id"] for item in manifest["endpoint_mappings"]}
    if endpoint_tracks != REQUIRED_ENDPOINTS:
        failures.append("Procedure endpoint mappings are incomplete.")
    for mapping in manifest["endpoint_mappings"]:
        unknown_categories = set(mapping["mapped_categories"]) - REQUIRED_CATEGORIES
        if unknown_categories:
            failures.append(
                f"{mapping['track_id']} maps unknown categories: {sorted(unknown_categories)}"
            )
        if "validation" not in " ".join(mapping["required_validation"]):
            failures.append(f"{mapping['track_id']} must include endpoint validation requirements.")

    fixture_categories = {sample["category"] for sample in fixtures["samples"]}
    missing_fixture_categories = REQUIRED_FIXTURE_CATEGORIES - fixture_categories
    if missing_fixture_categories:
        failures.append(
            f"Procedure fixtures are missing categories: {sorted(missing_fixture_categories)}"
        )
    fixture_document_types = {sample["document_type"] for sample in fixtures["samples"]}
    for required_document_type in ("Hansard - vote", "Hansard - question"):
        if required_document_type not in fixture_document_types:
            failures.append(f"Procedure fixtures must include {required_document_type}.")
    for sample in fixtures["samples"]:
        if sample["category"] not in REQUIRED_CATEGORIES:
            failures.append(f"{sample['sample_id']} uses an unknown category.")
        if not set(sample["authority_source_ids"]).issubset(authority_ids):
            failures.append(f"{sample['sample_id']} cites unknown authority source IDs.")
        if sample["review"]["model_generated_label"]:
            failures.append(f"{sample['sample_id']} must not be model-generated gold.")

    required_terms = (
        "manifests/nz_parliamentary_procedure_model.json",
        "fixtures/nz_parliamentary_procedure_samples.json",
        "party_vote",
        "personal_vote",
        "question",
        "supplementary_question",
        "stage",
        "ruling",
        "interjection",
        "procedural_unit",
        "authority_source_ids",
        "uncertainty_status",
        "not_speech_turn_by_default",
    )
    for relative_path, text in {
        "docs/nz-parliamentary-procedure-model.md": _read(DOC_PATH),
        "docs/component-contracts.md": _read(COMPONENT_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
    }.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing procedure model term: {term}")

    track_text = _read(TRACK_PATH)
    for required in (
        "Procedural Taxonomy",
        "Procedure Fixtures",
        "Endpoint Mappings",
        "Focused Validation",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"NZ-PROCEDURE: {failure}")
        return 1
    print("NZ parliamentary procedure model is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
