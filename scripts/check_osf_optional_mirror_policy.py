"""Validate the OSF optional mirror policy files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
POLICY_DOC = ROOT / "docs/osf-optional-mirror-policy.md"
POLICY_MANIFEST = ROOT / "manifests/osf_optional_mirror_policy.json"
POLICY_SCHEMA = ROOT / "schemas/osf_optional_mirror_policy.schema.json"
TRACK_EVIDENCE = ROOT / "conductor/tracks/osf_optional_mirror_policy_20260609/evidence.md"

REQUIRED_CANONICAL_URLS = {
    "https://github.com/edithatogo/corpus-nz-hansard",
    "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus",
    "https://doi.org/10.5281/zenodo.20595194",
}
REQUIRED_ACTIVATION_CONTROLS = {
    "osf_project_url",
    "release_version",
    "source_commit",
    "mirrored_artifacts",
    "sha256_checksums",
    "canonical_artifact_urls",
    "citation_wording",
    "maintenance_owner",
}


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (POLICY_DOC, POLICY_MANIFEST, POLICY_SCHEMA, TRACK_EVIDENCE):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(POLICY_MANIFEST)
    schema = _json(POLICY_SCHEMA)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(
            f"{POLICY_MANIFEST.relative_to(ROOT).as_posix()} {location}: {error.message}"
        )

    osf = manifest.get("osf", {})
    if osf.get("decision") != "optional_future_mirror":
        failures.append("OSF decision must be optional_future_mirror.")
    if osf.get("status") != "inactive":
        failures.append("OSF status must remain inactive until live OSF evidence exists.")
    if osf.get("claims_allowed") is not False:
        failures.append(
            "OSF public claims must remain disabled until activation controls are complete."
        )
    if osf.get("project_url") is not None:
        failures.append("OSF project_url must remain null until a live project is validated.")

    canonical_urls = set(manifest.get("canonical_surfaces", {}).values())
    if canonical_urls != REQUIRED_CANONICAL_URLS:
        failures.append("Canonical surfaces must be GitHub, Hugging Face, and the Zenodo DOI.")

    controls = set(manifest.get("mirror_controls", {}).get("required_before_activation", []))
    missing_controls = sorted(REQUIRED_ACTIVATION_CONTROLS - controls)
    if missing_controls:
        failures.append("OSF activation controls missing: " + ", ".join(missing_controls))
    if manifest.get("mirror_controls", {}).get("checksum_algorithm") != "sha256":
        failures.append("OSF mirror checksum algorithm must be sha256.")

    citation = manifest.get("citation", {})
    if citation.get("authoritative_target") != "zenodo":
        failures.append("OSF citation policy must keep Zenodo as the authoritative target.")
    if "10.5281/zenodo.20595194" not in str(citation.get("required_text", "")):
        failures.append("OSF citation text must include the canonical Zenodo DOI.")
    if "convenience mirror" not in str(citation.get("osf_note", "")):
        failures.append("OSF note must describe OSF as a convenience mirror.")

    doc = POLICY_DOC.read_text(encoding="utf-8")
    evidence = TRACK_EVIDENCE.read_text(encoding="utf-8")
    for required in (
        "optional future mirror",
        "GitHub",
        "Hugging Face",
        "Zenodo",
        "OSF",
        "SHA-256",
        "corpus-nz-hansard",
        "corpus-nz-legislation",
        "Future metadata",
        "Zenodo DOI",
    ):
        if required not in doc:
            failures.append(f"{POLICY_DOC.relative_to(ROOT).as_posix()} is missing: {required}")
    for required in (
        "Policy Decision",
        "Canonical Surfaces",
        "OSF Activation Controls",
        "Citation Boundary",
        "Focused Validation",
    ):
        if required not in evidence:
            failures.append(f"{TRACK_EVIDENCE.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"OSF-OPTIONAL-MIRROR-POLICY: {failure}")
        return 1
    print("OSF optional mirror policy is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
