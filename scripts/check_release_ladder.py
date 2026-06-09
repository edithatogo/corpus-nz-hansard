"""Validate release ladder policy, mappings, and publication guardrails."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/release_ladder.json"
SCHEMA_PATH = ROOT / "schemas/release_ladder.schema.json"
DOC_PATH = ROOT / "docs/release-ladder.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
PUBLIC_CHECKLIST_PATH = ROOT / "docs/public-release-checklist.md"
PUBLICATION_STATUS_PATH = ROOT / "docs/publication-status.md"
TRACK_PATH = ROOT / "conductor/tracks/release_ladder_20260609/evidence.md"

REQUIRED_LEVELS = {
    "document-level",
    "authority-source",
    "neutral-component",
    "endpoint",
    "upstream-contribution",
}
REQUIRED_FIELDS = {
    "release_series_id",
    "release_level",
    "artifact_name",
    "artifact_version",
    "input_release_versions",
    "validation_manifest",
    "publication_target",
    "known_exclusions",
    "release_status",
    "manifest_sha256",
}
REQUIRED_ARTIFACTS = {
    "public dataset release manifest": "document-level",
    "authority source discovery": "authority-source",
    "component contracts": "neutral-component",
    "endpoint contracts": "endpoint",
    "upstream contribution packages": "upstream-contribution",
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
        COMPONENT_DOC_PATH,
        ENDPOINT_DOC_PATH,
        PUBLIC_CHECKLIST_PATH,
        PUBLICATION_STATUS_PATH,
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

    release_levels = {level["id"]: level for level in manifest["release_levels"]}
    if set(release_levels) != REQUIRED_LEVELS:
        failures.append("release ladder must define exactly the five required release levels.")

    if manifest["current_public_release"]["version"] != "0.1.0":
        failures.append("current public release must remain v0.1.0.")
    if manifest["current_public_release"]["release_level"] != "document-level":
        failures.append("current public release must remain document-level.")
    if "immutable" not in manifest["current_public_release"]["immutable_policy"].lower():
        failures.append("current public release must state an immutable policy.")

    artifacts = {item["artifact"]: item for item in manifest["artifact_map"]}
    for artifact, required_level in REQUIRED_ARTIFACTS.items():
        if artifact not in artifacts:
            failures.append(f"release ladder missing artifact mapping: {artifact}")
        elif artifacts[artifact]["release_level"] != required_level:
            failures.append(f"{artifact} must map to release level {required_level}.")

    if artifacts.get("public dataset release manifest", {}).get("status") != "published":
        failures.append("public dataset release manifest must remain published.")
    if artifacts.get("speech-turn candidates", {}).get("status") != "excluded":
        failures.append("speech-turn candidates must remain excluded until validated.")

    fields = set(manifest["manifest_field_requirements"])
    missing_fields = REQUIRED_FIELDS - fields
    if missing_fields:
        failures.append(
            "release ladder missing manifest fields: " + ", ".join(sorted(missing_fields))
        )

    surfaces = {item["surface"] for item in manifest["surface_relationships"]}
    if surfaces != {"github", "huggingface", "zenodo", "osf", "upstream"}:
        failures.append("release ladder surface relationships are incomplete.")

    public_manifest = _json(ROOT / "manifests/public_dataset_release_manifest.json")
    if public_manifest["publication"]["github_release"].rsplit("/", maxsplit=1)[-1] != "v0.1.0":
        failures.append("public dataset release manifest must keep GitHub release v0.1.0.")
    if public_manifest["publication_status"] != "published":
        failures.append("public dataset release manifest must remain published.")

    required_doc_terms = (
        "document-level",
        "authority-source",
        "neutral-component",
        "endpoint",
        "upstream-contribution",
        "v0.1.0",
        "immutable",
        "manifests/release_ladder.json",
    )
    for relative_path, text in {
        "docs/release-ladder.md": _read(DOC_PATH),
        "docs/component-contracts.md": _read(COMPONENT_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "docs/public-release-checklist.md": _read(PUBLIC_CHECKLIST_PATH),
        "docs/publication-status.md": _read(PUBLICATION_STATUS_PATH),
    }.items():
        for term in required_doc_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing release ladder term: {term}")

    track = _read(TRACK_PATH)
    for required in (
        "Release Levels",
        "Artifact Map",
        "Manifest Fields",
        "Focused Validation",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"RELEASE-LADDER: {failure}")
        return 1
    print("Release ladder manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
