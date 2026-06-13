"""Validate the Popolo/Open Civic Data public endpoint release boundary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/popolo_opencivicdata_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/popolo_opencivicdata_validation_manifest.json"
SAMPLE_README_PATH = ROOT / "samples/popolo-opencivicdata/README.md"
SAMPLE_FILES = [
    ROOT / "samples/popolo-opencivicdata/people.json",
    ROOT / "samples/popolo-opencivicdata/organizations.json",
    ROOT / "samples/popolo-opencivicdata/memberships.json",
    ROOT / "samples/popolo-opencivicdata/motions.json",
    ROOT / "samples/popolo-opencivicdata/vote-events.json",
    ROOT / "samples/popolo-opencivicdata/votes.jsonl",
    ROOT / "samples/popolo-opencivicdata/speeches.jsonl",
]
DOC_PATH = ROOT / "docs/popolo-opencivicdata-public-endpoint-release.md"
MAPPING_DOC_PATH = ROOT / "docs/popolo-opencivicdata-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
TRACK_PATH = (
    ROOT / "conductor/tracks/popolo_opencivicdata_public_endpoint_release_20260610/index.md"
)
SCHEMA_PATH = ROOT / "schemas/popolo_opencivicdata_public_endpoint_validation.schema.json"

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
        *SAMPLE_FILES,
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

    if manifest["artifact_name"] != "Popolo / Open Civic Data public endpoint release":
        failures.append("artifact_name must be Popolo / Open Civic Data public endpoint release.")
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
    if len(manifest["output_artifacts"]) != 8:
        failures.append("public endpoint release should still point to the eight sample outputs.")
    if (
        manifest["validation_command"]
        != "python scripts/check_popolo_opencivicdata_public_endpoint.py"
    ):
        failures.append("validation command must point to the public endpoint checker.")

    failures.extend(
        _doc_terms(
            DOC_PATH,
            (
                "blocked",
                "sample-only",
                "validated member identity",
                "validated party attribution",
                "validated vote/motion extraction",
                "validated speech-turn",
                "public endpoint release",
            ),
        )
    )
    failures.extend(
        _doc_terms(
            TRACK_PATH,
            (
                "blocked",
                "sample-only",
                "validated member identity",
                "validated party attribution",
                "validated vote/motion extraction",
                "validated speech-turn",
            ),
        )
    )
    failures.extend(
        _doc_terms(
            MAPPING_DOC_PATH,
            (
                "sample-not-release",
                "blocked-pending-validated-components",
                "Popolo / Open Civic Data",
            ),
        )
    )
    failures.extend(
        _doc_terms(
            ENDPOINT_DOC_PATH,
            (
                "Popolo / Open Civic Data",
                "blocked-pending-validated-components",
                "sample-not-release",
            ),
        )
    )
    failures.extend(
        _doc_terms(
            SAMPLE_README_PATH,
            (
                "sample-not-release",
                "blocked-pending-validated-components",
                "Popolo / Open Civic Data",
            ),
        )
    )

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"POPOLO-OCD-PUBLIC: {failure}")
        return 1
    print("Popolo/Open Civic Data public endpoint release boundary is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
