"""Validate neutral parliamentary component model schemas, fixtures, and gates."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/neutral_component_model.json"
MANIFEST_SCHEMA_PATH = ROOT / "schemas/neutral_component_model.schema.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
FIXTURE_SCHEMA_PATH = ROOT / "schemas/neutral_component_fixtures.schema.json"
VALIDATION_MANIFEST_PATH = ROOT / "manifests/neutral_component_validation_manifest.json"
DOC_PATH = ROOT / "docs/neutral-component-model.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
INTEROP_DOC_PATH = ROOT / "docs/interoperability-design.md"
README_PATH = ROOT / "README.md"
AUTHORITY_MANIFEST_PATH = ROOT / "manifests/authority_sources.json"
TRACK_PATH = ROOT / "conductor/tracks/neutral_component_model_20260609/evidence.md"

ID_PATTERN = re.compile(r"^nzhc-component-[a-f0-9]{16}$")
REQUIRED_FAMILIES = {
    "sittings",
    "proceeding_items",
    "speech_turns",
    "members",
    "parties",
    "motions",
    "votes",
    "bills",
    "topics",
    "linguistic_annotations",
}
REQUIRED_COMMON_FIELDS = {
    "component_id",
    "component_type",
    "derived_from",
    "derivation_method",
    "derivation_version",
    "validation_status",
    "provenance",
    "authority_source_ids",
}
REQUIRED_VALIDATION_FIELDS = {
    "artifact_name",
    "artifact_version",
    "component_families",
    "input_release_versions",
    "schema_paths",
    "fixture_paths",
    "validation_command",
    "referential_integrity_status",
    "blocking_errors",
    "publication_status",
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


def _component_index(fixtures: dict[str, Any]) -> dict[str, str]:
    index: dict[str, str] = {}
    for family, rows in fixtures["components"].items():
        for row in rows:
            index[row["component_id"]] = family
    return index


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        MANIFEST_SCHEMA_PATH,
        FIXTURE_PATH,
        FIXTURE_SCHEMA_PATH,
        VALIDATION_MANIFEST_PATH,
        DOC_PATH,
        COMPONENT_DOC_PATH,
        ENDPOINT_DOC_PATH,
        INTEROP_DOC_PATH,
        README_PATH,
        AUTHORITY_MANIFEST_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    _validate_json(MANIFEST_PATH, MANIFEST_SCHEMA_PATH, failures, "neutral component model")
    _validate_json(FIXTURE_PATH, FIXTURE_SCHEMA_PATH, failures, "neutral component fixtures")

    manifest = _json(MANIFEST_PATH)
    fixtures = _json(FIXTURE_PATH)
    validation_manifest = _json(VALIDATION_MANIFEST_PATH)
    authority_ids = {source["id"] for source in _json(AUTHORITY_MANIFEST_PATH)["sources"]}

    families = {family["family_id"]: family for family in manifest["component_families"]}
    if set(families) != REQUIRED_FAMILIES:
        failures.append("Neutral component model must define every required family.")
    if set(fixtures["components"]) != REQUIRED_FAMILIES:
        failures.append("Neutral component fixtures must include every required family.")
    if set(manifest["common_required_fields"]) != REQUIRED_COMMON_FIELDS:
        failures.append("Neutral component model common required fields are incomplete.")
    if set(manifest["validation_manifest_requirements"]) != REQUIRED_VALIDATION_FIELDS:
        failures.append("Neutral component validation manifest requirements are incomplete.")

    fixture_index = _component_index(fixtures)
    for family_name, family in families.items():
        if not ID_PATTERN.fullmatch(family["id_pattern"].removeprefix("^").removesuffix("$")):
            if family["id_pattern"] != "^nzhc-component-[a-f0-9]{16}$":
                failures.append(f"{family_name} has an invalid ID pattern.")
        rows = fixtures["components"].get(family_name, [])
        if not rows:
            failures.append(f"{family_name} must have at least one fixture row.")
        for row in rows:
            missing_common = REQUIRED_COMMON_FIELDS - set(row)
            if missing_common:
                failures.append(
                    f"{family_name} fixture missing common fields: {sorted(missing_common)}"
                )
            missing_specific = set(family["required_fields"]) - set(row)
            if missing_specific:
                failures.append(
                    f"{family_name} fixture missing required fields: {sorted(missing_specific)}"
                )
            if row.get("component_type") != family["component_type"]:
                failures.append(f"{family_name} fixture component_type does not match manifest.")
            id_value = row.get(family["id_field"])
            if id_value != row.get("component_id"):
                failures.append(f"{family_name} fixture id field must equal component_id.")
            if not ID_PATTERN.fullmatch(row.get("component_id", "")):
                failures.append(f"{family_name} fixture component_id is not stable-patterned.")
            unknown_authority_ids = set(row.get("authority_source_ids", [])) - authority_ids
            if unknown_authority_ids:
                failures.append(
                    f"{family_name} fixture cites unknown authority IDs: {sorted(unknown_authority_ids)}"
                )
            if row.get("validation_status") == "validated":
                failures.append(
                    f"{family_name} fixture must not publish validated derived data yet."
                )

    for rule in manifest["referential_integrity"]:
        rows = fixtures["components"].get(rule["source_family"], [])
        for row in rows:
            value = row.get(rule["field"])
            if value is None:
                failures.append(
                    f"{rule['source_family']} fixture missing RI field {rule['field']}."
                )
                continue
            if fixture_index.get(value) != rule["target_family"]:
                failures.append(
                    f"{rule['source_family']}.{rule['field']} must reference {rule['target_family']}."
                )

    for field in REQUIRED_VALIDATION_FIELDS:
        if field not in validation_manifest:
            failures.append(f"Neutral component validation manifest missing {field}.")
    if validation_manifest.get("blocking_errors") != 0:
        failures.append(
            "Neutral component validation manifest must have zero blocking fixture errors."
        )
    if validation_manifest.get("publication_status") != "not-published-derived-fixtures-only":
        failures.append(
            "Neutral component validation manifest must keep derived fixtures unpublished."
        )
    for path_value in validation_manifest.get("schema_paths", []) + validation_manifest.get(
        "fixture_paths", []
    ):
        if not (ROOT / path_value).exists():
            failures.append(
                f"Neutral component validation manifest path does not exist: {path_value}"
            )

    required_terms = (
        "manifests/neutral_component_model.json",
        "fixtures/neutral_components.json",
        "manifests/neutral_component_validation_manifest.json",
        "sittings",
        "proceeding_items",
        "speech_turns",
        "members",
        "parties",
        "motions",
        "votes",
        "bills",
        "topics",
        "linguistic_annotations",
        "derivation_method",
        "derivation_version",
        "validation_status",
        "provenance",
        "referential integrity",
        "not-published-derived-fixtures-only",
    )
    for relative_path, text in {
        "docs/neutral-component-model.md": _read(DOC_PATH),
        "docs/component-contracts.md": _read(COMPONENT_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "docs/interoperability-design.md": _read(INTEROP_DOC_PATH),
        "README.md": _read(README_PATH),
    }.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing neutral component term: {term}")

    track_text = _read(TRACK_PATH)
    for required in (
        "Machine-Readable Schemas",
        "Fixtures And Referential Integrity",
        "Validation Manifest",
        "Focused Validation",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"NEUTRAL-COMPONENT: {failure}")
        return 1
    print("Neutral parliamentary component model is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
