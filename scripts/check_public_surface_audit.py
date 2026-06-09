"""Validate public-surface audit evidence and documentation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "manifests/public_surface_audit.json"
SCHEMA_PATH = ROOT / "schemas/public_surface_audit.schema.json"
DOC_PATH = ROOT / "docs/public-surface-audit.md"
TRACK_PATH = ROOT / "conductor/tracks/public_surface_audit_evidence_20260609/evidence.md"

REQUIRED_SURFACE_IDS = {
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


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (AUDIT_PATH, SCHEMA_PATH, DOC_PATH, TRACK_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    audit = _json(AUDIT_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(audit), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{AUDIT_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    surface_ids = {surface.get("id") for surface in audit.get("surfaces", [])}
    if surface_ids != REQUIRED_SURFACE_IDS:
        failures.append(
            "public_surface_audit.json must include exactly: "
            + ", ".join(sorted(REQUIRED_SURFACE_IDS))
        )

    surface_by_id = {surface["id"]: surface for surface in audit.get("surfaces", [])}
    for active_surface in ("github", "huggingface", "zenodo"):
        surface = surface_by_id.get(active_surface, {})
        if surface.get("status") != "active":
            failures.append(f"{active_surface} must be active.")
        if not surface.get("url"):
            failures.append(f"{active_surface} must have a URL.")
        if surface.get("claims_allowed") is not True:
            failures.append(f"{active_surface} must allow public claims.")

    for inactive_surface in ("osf_optional", "future_metadata"):
        surface = surface_by_id.get(inactive_surface, {})
        if surface.get("claims_allowed") is not False:
            failures.append(f"{inactive_surface} must not allow public publication claims.")
        if not surface.get("follow_up_track"):
            failures.append(f"{inactive_surface} must name a follow-up track.")

    release_manifest = _json(ROOT / audit["release_manifest"])
    publication = release_manifest["publication"]
    expected_urls = {
        "github": publication["github_repository"],
        "huggingface": publication["huggingface_dataset"],
        "zenodo": publication["zenodo_record"],
    }
    for surface_id, expected_url in expected_urls.items():
        if surface_by_id.get(surface_id, {}).get("url") != expected_url:
            failures.append(f"{surface_id} URL must match the public release manifest.")

    doc = _read(DOC_PATH)
    track = _read(TRACK_PATH)
    for required in (
        "GitHub",
        "Hugging Face",
        "Zenodo",
        "OSF",
        "future metadata",
        "zenodraft",
        "public_surface_audit.json",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")
    for required in ("GitHub Surface", "Hugging Face Surface", "Zenodo Surface", "OSF Surface"):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PUBLIC-SURFACE-AUDIT: {failure}")
        return 1
    print("Public-surface audit evidence is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
