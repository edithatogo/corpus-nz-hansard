"""Validate the ParlaMint-NZ public endpoint release boundary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/parlamint_nz_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/parlamint_nz_validation_manifest.json"
SAMPLE_README_PATH = ROOT / "samples/parlamint-nz/README.md"
SAMPLE_XML_PATH = ROOT / "samples/parlamint-nz/ParlaMint-NZ.sample.xml"
SAMPLE_METADATA_PATH = ROOT / "samples/parlamint-nz/ParlaMint-NZ.metadata.xml"
DOC_PATH = ROOT / "docs/parlamint-nz-public-endpoint-release.md"
MAPPING_DOC_PATH = ROOT / "docs/parlamint-nz-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
TRACK_PATH = ROOT / "conductor/tracks/parlamint_nz_public_endpoint_release_20260610/index.md"
SCHEMA_PATH = ROOT / "schemas/parlamint_nz_public_endpoint_validation.schema.json"

REQUIRED_FIELDS = (
    "endpoint",
    "artifact_name",
    "artifact_version",
    "release_series_id",
    "release_level",
    "release_status",
    "publication_target",
    "validation_manifest",
    "input_release_versions",
    "known_exclusions",
    "dependency_groups",
    "dependency_validation",
    "validation_command",
    "output_artifacts",
    "validation_results",
    "traceability",
    "manifest_sha256",
)


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
        SAMPLE_README_PATH,
        SAMPLE_XML_PATH,
        SAMPLE_METADATA_PATH,
        DOC_PATH,
        MAPPING_DOC_PATH,
        ENDPOINT_DOC_PATH,
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

    if manifest["artifact_name"] != "ParlaMint-NZ public endpoint release":
        failures.append("artifact_name must be ParlaMint-NZ public endpoint release.")
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
    if sample_manifest["release_status"] != "sample-not-release":
        failures.append("sample manifest must remain sample-not-release.")
    if (
        sample_manifest["validation_results"]["readiness_status"]
        != "blocked-pending-validated-components"
    ):
        failures.append("sample readiness must remain blocked-pending-validated-components.")
    if sample_manifest["validation_results"]["component_metadata_validated"]:
        failures.append("sample must not claim validated component metadata yet.")

    if len(manifest["output_artifacts"]) != 3:
        failures.append("public endpoint release should still point to the three sample outputs.")
    if manifest["input_release_versions"]["document_level"] != "0.1.0":
        failures.append("document_level input version must be 0.1.0.")
    if manifest["validation_command"] != "python scripts/check_parlamint_nz_public_endpoint.py":
        failures.append("validation command must point to the public endpoint checker.")

    failures.extend(
        _doc_terms(
            DOC_PATH,
            (
                "blocked",
                "validated member identity",
                "validated party attribution",
                "validated speech-turn",
                "sample-only",
                "public endpoint release",
            ),
        )
    )
    failures.extend(
        _doc_terms(
            TRACK_PATH,
            (
                "blocked",
                "validated member identity",
                "validated party attribution",
                "validated speech-turn",
                "sample-only",
            ),
        )
    )
    failures.extend(
        _doc_terms(
            MAPPING_DOC_PATH,
            ("blocked-pending-validated-components", "sample-not-release", "ParlaMint-NZ"),
        )
    )
    failures.extend(
        _doc_terms(
            ENDPOINT_DOC_PATH,
            ("ParlaMint-NZ / TEI", "blocked-pending-validated-components", "sample-not-release"),
        )
    )
    failures.extend(
        _doc_terms(
            SAMPLE_README_PATH,
            (
                "sample-not-release",
                "blocked-pending-validated-components",
                "ParlaMint-NZ.sample.xml",
            ),
        )
    )

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLAMINT-NZ-PUBLIC: {failure}")
        return 1
    print("ParlaMint-NZ public endpoint release boundary is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
