"""Validate corpus-family naming and publication-surface alignment."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT_PATH = ROOT / "manifests/corpus_family_publication_alignment.json"
SCHEMA_PATH = ROOT / "schemas/corpus_family_publication_alignment.schema.json"
DOC_PATH = ROOT / "docs/corpus-family-naming-publication-alignment.md"
TRACK_EVIDENCE = (
    ROOT / "conductor/tracks/corpus_family_naming_publication_alignment_20260609/evidence.md"
)

REQUIRED_ENVIRONMENT_IDS = {
    "github",
    "huggingface",
    "zenodo",
    "osf_optional",
    "future_metadata",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (ALIGNMENT_PATH, SCHEMA_PATH, DOC_PATH, TRACK_EVIDENCE):
        if not path.exists():
            failures.append(f"{_relative(path)} must exist.")
    if failures:
        return failures

    alignment = _json(ALIGNMENT_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(alignment), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{_relative(ALIGNMENT_PATH)} {location}: {error.message}")

    release_manifest_path = ROOT / alignment["release_manifest"]
    public_surface_audit_path = ROOT / alignment["public_surface_audit"]
    for path in (release_manifest_path, public_surface_audit_path):
        if not path.exists():
            failures.append(f"{_relative(path)} must exist.")
    if failures:
        return failures

    release_manifest = _json(release_manifest_path)
    public_surface_audit = _json(public_surface_audit_path)

    labels = set(alignment["family"]["preferred_labels"])
    for required_label in ("corpus-nz-hansard", "corpus-nz-legislation"):
        if required_label not in labels:
            failures.append(f"preferred_labels must include {required_label}.")

    if public_surface_audit.get("repository") != "corpus-nz-hansard":
        failures.append("public_surface_audit repository must remain corpus-nz-hansard.")
    if public_surface_audit.get("corpus_family_sibling") != "corpus-nz-legislation":
        failures.append("public_surface_audit sibling must remain corpus-nz-legislation.")

    environment_by_id = {item["id"]: item for item in alignment.get("environment_gates", [])}
    audit_by_id = {item["id"]: item for item in public_surface_audit.get("surfaces", [])}
    if set(environment_by_id) != REQUIRED_ENVIRONMENT_IDS:
        failures.append(
            "environment_gates must include exactly: " + ", ".join(sorted(REQUIRED_ENVIRONMENT_IDS))
        )
    if set(audit_by_id) != REQUIRED_ENVIRONMENT_IDS:
        failures.append(
            "public_surface_audit surfaces must include exactly: "
            + ", ".join(sorted(REQUIRED_ENVIRONMENT_IDS))
        )

    publication = release_manifest["publication"]
    expected_urls = {
        "github": publication["github_repository"],
        "huggingface": publication["huggingface_dataset"],
        "zenodo": publication["zenodo_record"],
        "osf_optional": None,
        "future_metadata": None,
    }
    for environment_id, expected_url in expected_urls.items():
        environment = environment_by_id.get(environment_id, {})
        audit = audit_by_id.get(environment_id, {})
        if environment.get("public_url") != expected_url:
            failures.append(f"{environment_id} public_url must match the release manifest.")
        if audit.get("url") != expected_url:
            failures.append(f"{environment_id} audit URL must match the release manifest.")
        if environment.get("claims_allowed") != audit.get("claims_allowed"):
            failures.append(f"{environment_id} claims_allowed must match public_surface_audit.")

    for active_id in ("github", "huggingface", "zenodo"):
        environment = environment_by_id.get(active_id, {})
        if environment.get("non_migration_decision") != "keep-existing-url":
            failures.append(f"{active_id} must keep existing public URL.")
        if environment.get("claims_allowed") is not True:
            failures.append(f"{active_id} must allow publication claims.")

    for inactive_id in ("osf_optional", "future_metadata"):
        environment = environment_by_id.get(inactive_id, {})
        if environment.get("non_migration_decision") != "not-yet-published":
            failures.append(f"{inactive_id} must remain not-yet-published.")
        if environment.get("claims_allowed") is not False:
            failures.append(f"{inactive_id} must not allow publication claims.")
        if not environment.get("follow_up_track"):
            failures.append(f"{inactive_id} must name a follow-up track.")

    for gate in alignment.get("documentation_gates", []):
        path = ROOT / gate["path"]
        if not path.exists():
            failures.append(f"{gate['path']} must exist.")
            continue
        text = _read(path)
        for term in gate["required_terms"]:
            if term not in text:
                failures.append(f"{gate['path']} is missing: {term}")

    doc = _read(DOC_PATH)
    evidence = _read(TRACK_EVIDENCE)
    for required in (
        "corpus-nz-hansard",
        "corpus-nz-legislation",
        "GitHub",
        "Hugging Face",
        "Zenodo",
        "OSF",
        "Croissant",
        "RO-Crate",
        "Frictionless",
        "DCAT",
        "PROV-O",
        "```mermaid",
        "keep-existing-url",
        "not-yet-published",
    ):
        if required not in doc:
            failures.append(f"{_relative(DOC_PATH)} is missing: {required}")
    for required in (
        "Focused validation",
        "corpus_family_publication_alignment.json",
        "check_corpus_family_alignment.py",
    ):
        if required not in evidence:
            failures.append(f"{_relative(TRACK_EVIDENCE)} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"CORPUS-FAMILY-ALIGNMENT: {failure}")
        return 1
    print("Corpus-family naming and publication alignment is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
