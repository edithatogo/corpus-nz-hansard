"""Validate the static documentation portal."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_static_documentation_portal import (  # noqa: E402
    HTML_PATH,
    MANIFEST_PATH,
    build_static_documentation_portal,
)

SCHEMA_PATH = ROOT / "schemas/static_documentation_portal.schema.json"
SOURCE_DOC_PATH = ROOT / "docs/static-documentation-portal.md"
TRACK_PATH = ROOT / "conductor/tracks/static_documentation_portal_20260610/index.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
PUBLIC_RELEASE_PATH = ROOT / "manifests/public_dataset_release_manifest.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, HTML_PATH, SOURCE_DOC_PATH, TRACK_PATH):
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

    if manifest["validation_results"]["portal_built"] is not True:
        failures.append("portal_built must remain true.")
    if manifest["validation_results"]["current_public_release_version"] != "0.1.0":
        failures.append("current_public_release_version must stay on v0.1.0.")

    html_text = _read(HTML_PATH)
    for required in (
        "Static Documentation Portal",
        "Current Public Release",
        "Release Ladder",
        "Artifact Map",
        "Track Status",
        "Citation Guidance",
        "Data Dictionaries",
        "Claim Boundary",
        "GitHub release",
        "Hugging Face dataset",
        "Zenodo record",
    ):
        if required not in html_text:
            failures.append(f"{HTML_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    doc_text = _read(SOURCE_DOC_PATH)
    for required in (
        "Static Documentation Portal",
        "release ladder",
        "validation status",
        "citation patterns",
        "endpoint readiness",
    ):
        if required.lower() not in doc_text.lower():
            failures.append(
                f"{SOURCE_DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}"
            )

    track_text = _read(TRACK_PATH)
    for required in ("Release Ladder", "Track Status", "Citation Guidance", "Data Dictionaries"):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    release_ladder = _json(RELEASE_LADDER_PATH)
    public_release = _json(PUBLIC_RELEASE_PATH)
    if (
        manifest["current_public_release"]["github_release"]
        != public_release["publication"]["github_release"]
    ):
        failures.append("GitHub release URL must match the public dataset release manifest.")
    if manifest["release_ladder_snapshot"]["artifact_map_count"] != len(
        release_ladder["artifact_map"]
    ):
        failures.append("Artifact map count must match the release ladder manifest.")
    if manifest["track_snapshot"]["summary_counts"]["complete"] < 1:
        failures.append("Track status summary should include completed tracks.")

    if not build_static_documentation_portal(manifest_path=MANIFEST_PATH):
        failures.append("Portal build helper returned no manifest.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"STATIC-DOCUMENTATION-PORTAL: {failure}")
        return 1
    print("Static documentation portal is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
