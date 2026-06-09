"""Validate generated SOTA metadata packages and their manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/metadata_packages_manifest.json"
SCHEMA_PATH = ROOT / "schemas/metadata_packages_manifest.schema.json"
DOC_PATH = ROOT / "docs/sota-metadata-packages.md"
TRACK_PATH = ROOT / "conductor/tracks/sota_metadata_packages_20260609/evidence.md"
RELEASE_MANIFEST_PATH = ROOT / "manifests/public_dataset_release_manifest.json"
GENERATED_DIR = ROOT / "generated/metadata"

REQUIRED_PACKAGE_IDS = {"croissant", "ro-crate", "frictionless", "dcat", "prov-o"}
REQUIRED_SOURCE_MANIFESTS = {
    "manifests/public_dataset_release_manifest.json",
    "manifests/public_surface_audit.json",
    ".zenodo.json",
    "CITATION.cff",
    "DATASET_CARD.md",
    "schemas/hansard_record.schema.json",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_json_package(path: Path, package_id: str) -> list[str]:
    failures: list[str] = []
    try:
        payload = _json(path)
    except json.JSONDecodeError as error:
        return [f"{path.relative_to(ROOT).as_posix()} is invalid JSON: {error}"]

    if package_id == "croissant":
        for key in ("@context", "@type", "name", "description", "distribution", "recordSet"):
            if key not in payload:
                failures.append(f"croissant metadata is missing {key}.")
        if not payload.get("distribution"):
            failures.append("croissant metadata must include at least one distribution.")
    elif package_id == "ro-crate":
        if payload.get("@context") != "https://w3id.org/ro/crate/1.1/context":
            failures.append("ro-crate metadata must use the RO-Crate 1.1 context.")
        graph = payload.get("@graph", [])
        if not isinstance(graph, list) or not any(item.get("@id") == "./" for item in graph):
            failures.append("ro-crate metadata must include the root dataset graph node.")
    elif package_id == "frictionless":
        if payload.get("profile") != "data-package":
            failures.append("frictionless metadata must use profile=data-package.")
        resources = payload.get("resources", [])
        if not isinstance(resources, list) or not resources:
            failures.append("frictionless metadata must include resources.")
    return failures


def _validate_turtle_package(path: Path, package_id: str) -> list[str]:
    text = _read(path)
    required_by_id = {
        "dcat": ("@prefix dcat:", "dcat:Dataset", "dcat:Distribution"),
        "prov-o": ("@prefix prov:", "prov:Entity", "prov:Activity"),
    }
    return [
        f"{path.relative_to(ROOT).as_posix()} is missing {snippet}."
        for snippet in required_by_id[package_id]
        if snippet not in text
    ]


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, TRACK_PATH, RELEASE_MANIFEST_PATH):
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

    package_ids = {package.get("id") for package in manifest.get("packages", [])}
    if package_ids != REQUIRED_PACKAGE_IDS:
        failures.append(
            "metadata_packages_manifest.json must include exactly: "
            + ", ".join(sorted(REQUIRED_PACKAGE_IDS))
        )

    source_manifests = set(manifest.get("source_manifests", []))
    missing_sources = REQUIRED_SOURCE_MANIFESTS - source_manifests
    if missing_sources:
        failures.append(
            "metadata package source manifests missing: " + ", ".join(sorted(missing_sources))
        )

    for source_manifest in source_manifests:
        if not (ROOT / source_manifest).exists():
            failures.append(f"source manifest does not exist: {source_manifest}")

    release_manifest = _json(RELEASE_MANIFEST_PATH)
    publication = release_manifest["publication"]
    expected_surfaces = {
        "github": publication["github_repository"],
        "huggingface": publication["huggingface_dataset"],
        "zenodo": publication["zenodo_record"],
    }
    for surface_id, expected_url in expected_surfaces.items():
        if manifest["publication_surfaces"].get(surface_id) != expected_url:
            failures.append(f"{surface_id} metadata surface must match public release manifest.")

    if manifest.get("publication_surfaces", {}).get("osf") is not None:
        failures.append("OSF metadata surface must remain null until the optional mirror lands.")

    package_by_id = {package["id"]: package for package in manifest.get("packages", [])}
    for package_id, package in package_by_id.items():
        if package["output_path"].endswith((".json", ".jsonld")) and package["format"] == "turtle":
            failures.append(f"{package_id} turtle package must not use a JSON output path.")
        if package["output_path"].endswith(".ttl") and package["format"] != "turtle":
            failures.append(f"{package_id} TTL package must use turtle format.")
        if package["status"] != "generated":
            failures.append(f"{package_id} must be generated before this track can complete.")
        if not package["checksum"]:
            failures.append(f"{package_id} must have a checksum.")
            continue
        output_path = ROOT / package["output_path"]
        if not output_path.exists():
            failures.append(f"{package_id} output does not exist: {package['output_path']}")
            continue
        actual_checksum = _sha256(output_path)
        if package["checksum"] != actual_checksum:
            failures.append(
                f"{package_id} checksum mismatch: manifest has {package['checksum']}, "
                f"file has {actual_checksum}."
            )
        if package["format"] in {"json", "json-ld"}:
            failures.extend(_validate_json_package(output_path, package_id))
        if package["format"] == "turtle":
            failures.extend(_validate_turtle_package(output_path, package_id))
        if (
            package["status"] == "published"
            and manifest.get("publication_claims_allowed") is not True
        ):
            failures.append(f"{package_id} is published but publication claims are disabled.")
        unknown_sources = set(package["source_manifests"]) - source_manifests
        if unknown_sources:
            failures.append(
                f"{package_id} uses unknown source manifests: {', '.join(sorted(unknown_sources))}"
            )
        if package["validation_command"] != "python scripts/check_metadata_packages.py":
            failures.append(
                f"{package_id} validation command must use scripts/check_metadata_packages.py."
            )
        if package["generator"] != "python scripts/build_metadata_packages.py":
            failures.append(f"{package_id} generator must use scripts/build_metadata_packages.py.")

    if not GENERATED_DIR.exists():
        failures.append("generated/metadata must exist.")

    doc = _read(DOC_PATH)
    track = _read(TRACK_PATH)
    for required in (
        "build_metadata_packages.py",
        "Croissant",
        "RO-Crate",
        "Frictionless",
        "DCAT",
        "PROV-O",
        "corpus-nz-legislation",
        "metadata_packages_manifest.json",
        "ZENODO",
    ):
        if required not in doc and required.lower() not in doc.lower():
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")
    for required in (
        "Current State",
        "Target State",
        "Public Surface Implications",
        "Remaining Blockers",
        "Focused Validation",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"METADATA-PACKAGES: {failure}")
        return 1
    print("Metadata package contract is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
