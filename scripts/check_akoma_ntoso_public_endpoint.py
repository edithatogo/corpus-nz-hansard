"""Validate the Akoma Ntoso public endpoint release boundary."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/akoma_ntoso_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/akoma_ntoso_validation_manifest.json"
SAMPLE_XML_PATH = ROOT / "samples/akoma-ntoso/Akoma-Ntoso.sample.xml"
SAMPLE_METADATA_PATH = ROOT / "samples/akoma-ntoso/Akoma-Ntoso.metadata.xml"
SAMPLE_README_PATH = ROOT / "samples/akoma-ntoso/README.md"
MAPPING_DOC_PATH = ROOT / "docs/akoma-ntoso-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/akoma-ntoso-public-endpoint-release.md"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/akoma_ntoso_public_endpoint_release_20260610/index.md"
SCHEMA_PATH = ROOT / "schemas/akoma_ntoso_public_endpoint_validation.schema.json"

AKN_NS = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
REQUIRED_DEPENDENCY_GROUPS = {"xml", "schema", "authority"}
REQUIRED_OUTPUTS = {
    "samples/akoma-ntoso/Akoma-Ntoso.sample.xml",
    "samples/akoma-ntoso/Akoma-Ntoso.metadata.xml",
    "samples/akoma-ntoso/README.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _validate_schema(manifest: dict[str, Any]) -> list[str]:
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{location}: {error.message}")
    return failures


def _strip_ref(value: str | None) -> str | None:
    if value is None:
        return None
    return value[1:] if value.startswith("#") else value


def _parse_xml(path: Path, failures: list[str]) -> ET.Element[str] | None:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        failures.append(f"{path.relative_to(ROOT).as_posix()} is not well-formed XML: {exc}")
        return None


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
        SAMPLE_MANIFEST_PATH,
        SAMPLE_XML_PATH,
        SAMPLE_METADATA_PATH,
        SAMPLE_README_PATH,
        MAPPING_DOC_PATH,
        ENDPOINT_DOC_PATH,
        DOC_PATH,
        DEPENDENCY_MANIFEST_PATH,
        RELEASE_LADDER_PATH,
        TRACK_PATH,
        SCHEMA_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    sample_manifest = _json(SAMPLE_MANIFEST_PATH)
    failures.extend(_validate_schema(manifest))

    sample_root = _parse_xml(SAMPLE_XML_PATH, failures)
    metadata_root = _parse_xml(SAMPLE_METADATA_PATH, failures)
    if sample_root is None or metadata_root is None:
        return failures

    if sample_root.tag != f"{{{AKN_NS}}}akomaNtoso":
        failures.append("Akoma Ntoso sample XML must use akomaNtoso root namespace.")
    if metadata_root.tag != f"{{{AKN_NS}}}akomaNtoso":
        failures.append("Akoma Ntoso metadata XML must use akomaNtoso root namespace.")

    if manifest["artifact_name"] != "Akoma Ntoso public endpoint release":
        failures.append("artifact_name must be Akoma Ntoso public endpoint release.")
    if manifest["release_level"] != "endpoint":
        failures.append("release_level must be endpoint.")
    if manifest["release_status"] != "blocked-pending-validated-components":
        failures.append("release_status must be blocked-pending-validated-components.")
    if manifest["validation_results"]["readiness_status"] != "blocked-pending-validated-components":
        failures.append("readiness_status must remain blocked-pending-validated-components.")
    if manifest["validation_results"]["component_metadata_validated"]:
        failures.append("component_metadata_validated must remain false.")
    if manifest["public_claim"]["sample_only"] is not True:
        failures.append("public_claim.sample_only must be true.")
    if manifest["profile"]["selection_status"] != "blocked-pending-validated-components":
        failures.append(
            "profile selection_status must remain blocked-pending-validated-components."
        )
    if set(manifest["dependency_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("dependency groups must match xml/schema/authority.")
    if set(manifest["output_artifacts"]) != REQUIRED_OUTPUTS:
        failures.append("output artifacts must remain the sample package outputs.")
    if sample_manifest["release_status"] != "sample-not-release":
        failures.append("sample manifest must remain sample-not-release.")
    if (
        sample_manifest["validation_results"]["readiness_status"]
        != "blocked-pending-validated-components"
    ):
        failures.append("sample readiness must remain blocked-pending-validated-components.")
    if sample_manifest["validation_results"]["component_metadata_validated"]:
        failures.append("sample must not claim validated component metadata yet.")

    if manifest["traceability"] != sample_manifest["traceability"]:
        failures.append("traceability must match the sample manifest traceability.")

    dependency_manifest = _json(DEPENDENCY_MANIFEST_PATH)
    akn_entry = next(
        item
        for item in dependency_manifest["endpoint_requirements"]
        if item["endpoint_track"] == "akoma_ntoso_endpoint_20260609"
    )
    if set(akn_entry["required_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("dependency extras policy and Akoma Ntoso manifest disagree.")

    release_ladder = _json(RELEASE_LADDER_PATH)
    artifacts = {item["artifact"]: item for item in release_ladder["artifact_map"]}
    if "Akoma Ntoso sample package" not in artifacts:
        failures.append("release ladder missing Akoma Ntoso sample package mapping.")

    for relative_path, terms in {
        "docs/akoma-ntoso-public-endpoint-release.md": (
            "sample-only",
            "validated member identity",
            "validated party attribution",
            "validated speech-turn",
            "validated motion",
            "validated vote",
            "public endpoint release",
        ),
        "conductor/tracks/akoma_ntoso_public_endpoint_release_20260610/index.md": (
            "sample-only",
            "validated member identity",
            "validated party attribution",
            "validated speech-turn",
            "validated motion",
            "validated vote",
        ),
        "docs/akoma-ntoso-mapping.md": (
            "sample-not-release",
            "blocked-pending-validated-components",
            "Akoma Ntoso",
        ),
        "docs/endpoint-contracts.md": (
            "Akoma Ntoso",
            "sample-not-release",
            "blocked-pending-validated-components",
        ),
        "samples/akoma-ntoso/README.md": (
            "sample-not-release",
            "blocked-pending-validated-components",
            "Akoma Ntoso",
        ),
    }.items():
        path = ROOT / relative_path
        failures.extend(_doc_terms(path, terms))

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"AKOMA-NTOSO-PUBLIC: {failure}")
        return 1
    print("Akoma Ntoso public endpoint release boundary is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
