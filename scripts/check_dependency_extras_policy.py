"""Validate optional dependency-group policy and endpoint citations."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
SCHEMA_PATH = ROOT / "schemas/dependency_extras_policy.schema.json"
DOC_PATH = ROOT / "docs/dependency-policy.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
REQUIREMENTS_README_PATH = ROOT / "requirements/README.md"
TRACK_PATH = ROOT / "conductor/tracks/dependency_extras_policy_20260609/evidence.md"

REQUIRED_GROUPS = {
    "data",
    "schema",
    "xml",
    "rdf",
    "authority",
    "nlp",
    "ml",
    "metadata",
}
REQUIRED_ENDPOINT_TRACKS = {
    "parlamint_nz_endpoint_20260609",
    "popolo_opencivicdata_endpoint_20260609",
    "akoma_ntoso_endpoint_20260609",
    "cap_parlacap_topic_endpoint_20260609",
    "ud_conllu_endpoint_20260609",
    "rdf_linked_data_endpoint_20260609",
}
REQUIRED_VALIDATION_FIELDS = {
    "dependency_groups",
    "install_commands",
    "library_versions",
    "lock_or_constraints",
    "model_versions",
    "release_affecting_dependencies",
    "tool_versions",
    "validation_command",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _requirement_names(path: Path) -> set[str]:
    names: set[str] = set()
    for raw_line in _read(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("-r "):
            continue
        match = re.match(r"([A-Za-z0-9_.-]+)", line)
        if match:
            names.add(match.group(1).replace("_", "-").lower())
    return names


def _failures() -> list[str]:
    failures: list[str] = []
    required_paths = (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        ENDPOINT_DOC_PATH,
        REQUIREMENTS_README_PATH,
        TRACK_PATH,
        ROOT / "requirements.txt",
        ROOT / "requirements/requirements.txt",
    )
    for path in required_paths:
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

    groups = {group["group"]: group for group in manifest["optional_groups"]}
    if set(groups) != REQUIRED_GROUPS:
        failures.append("Dependency extras manifest must define every required optional group.")

    aggregate_requirements = _read(ROOT / "requirements/requirements.txt")
    base_names = _requirement_names(ROOT / manifest["base_runtime"]["requirements_file"])
    allowed_base = {
        dependency.replace("_", "-").lower()
        for dependency in manifest["base_runtime"]["allowed_dependencies"]
    }
    if not allowed_base.issubset(base_names):
        failures.append("Base runtime requirements do not match dependency policy manifest.")

    for dependency in manifest["prohibited_base_dependencies"]:
        if dependency.replace("_", "-").lower() in base_names:
            failures.append(f"Base runtime includes prohibited optional dependency: {dependency}")

    for group_name, group in groups.items():
        path = ROOT / group["requirements_file"]
        if not path.exists():
            failures.append(f"{group['requirements_file']} must exist.")
            continue
        requirement_names = _requirement_names(path)
        expected = {dependency.replace("_", "-").lower() for dependency in group["dependencies"]}
        if not expected.issubset(requirement_names):
            failures.append(
                f"{group['requirements_file']} is missing dependencies for {group_name}."
            )
        include_line = f"-r {Path(group['requirements_file']).name}"
        if include_line not in aggregate_requirements:
            failures.append(
                f"requirements/requirements.txt is missing aggregate include: {include_line}"
            )
        if group["install_check_status"] != "deferred-until-implementation":
            failures.append(f"{group_name} install checks must remain endpoint-deferred.")
        if group["pin_policy"] != "pin-before-release-artifact":
            failures.append(f"{group_name} must use the release-artifact pin policy.")
        if group["default_runtime_allowed"]:
            failures.append(f"{group_name} must not be allowed in the default runtime.")

    endpoints = {item["endpoint_track"]: item for item in manifest["endpoint_requirements"]}
    missing_endpoints = REQUIRED_ENDPOINT_TRACKS - set(endpoints)
    if missing_endpoints:
        failures.append(
            f"Endpoint dependency references are incomplete: {sorted(missing_endpoints)}"
        )
    for endpoint in endpoints.values():
        unknown_groups = set(endpoint["required_groups"]) - REQUIRED_GROUPS
        if unknown_groups:
            failures.append(
                f"{endpoint['endpoint_track']} cites unknown groups: {sorted(unknown_groups)}"
            )
        missing_fields = REQUIRED_VALIDATION_FIELDS - set(endpoint["validation_manifest_fields"])
        if missing_fields:
            failures.append(
                f"{endpoint['endpoint_track']} validation manifest fields are missing: "
                f"{sorted(missing_fields)}"
            )
        for group_name in endpoint["required_groups"]:
            expected_file = groups[group_name]["requirements_file"]
            if expected_file not in endpoint["install_check_command"]:
                failures.append(
                    f"{endpoint['endpoint_track']} install check omits {expected_file}."
                )
        if "Pin" not in endpoint["release_affecting_dependencies"]:
            failures.append(f"{endpoint['endpoint_track']} must state a pinning rule.")

    docs = {
        "docs/dependency-policy.md": _read(DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "requirements/README.md": _read(REQUIREMENTS_README_PATH),
    }
    required_terms = (
        "manifests/dependency_extras_policy.json",
        "scripts/check_dependency_extras_policy.py",
        "requirements.txt",
        "tool_versions",
        "library_versions",
        "model_versions",
        "pin-before-release-artifact",
        "deferred-until-implementation",
    )
    for relative_path, text in docs.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing dependency policy term: {term}")
        for group in sorted(REQUIRED_GROUPS):
            if f"requirements/{group}.txt" not in text:
                failures.append(
                    f"{relative_path} is missing optional group: requirements/{group}.txt"
                )

    track_text = _read(TRACK_PATH)
    for required in (
        "Dependency Extras Manifest",
        "Endpoint Validation Requirements",
        "Focused Validation",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"DEPENDENCY-EXTRAS: {failure}")
        return 1
    print("Dependency extras policy is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
