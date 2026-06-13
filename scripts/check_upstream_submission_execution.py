"""Validate the upstream submission execution manifest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/upstream_submission_execution_manifest.json"
SCHEMA_PATH = ROOT / "schemas/upstream_submission_execution.schema.json"
DOC_PATH = ROOT / "docs/upstream-submission-execution.md"
TRACK_PATH = ROOT / "conductor/tracks/upstream_submission_execution_20260610/index.md"
UPSTREAM_PACKAGES_PATH = ROOT / "manifests/upstream_contribution_packages_validation_manifest.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, TRACK_PATH, UPSTREAM_PACKAGES_PATH):
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

    if manifest["submission_state"] != "not-submitted":
        failures.append("submission_state must remain not-submitted.")
    if manifest["validation_results"]["targets_catalogued"] is not True:
        failures.append("targets_catalogued must be true.")
    if manifest["validation_results"]["external_submission_links_recorded"] is not False:
        failures.append("external_submission_links_recorded must remain false.")
    if manifest["validation_results"]["readiness_boundary"] != "local-review-only":
        failures.append("readiness_boundary must remain local-review-only.")
    if manifest["validation_results"]["blocked_targets"] != 6:
        failures.append("blocked_targets must equal the six endpoint release tracks.")

    targets = {item["target"]: item for item in manifest["submission_targets"]}
    expected_targets = {
        "ParlaMint-NZ / TEI",
        "Popolo / Open Civic Data",
        "Akoma Ntoso",
        "CAP / ParlaCAP",
        "Universal Dependencies / CoNLL-U",
        "RDF / Linked Data",
    }
    if set(targets) != expected_targets:
        failures.append("submission_targets must list the six endpoint families.")
    for target, item in targets.items():
        if item["submission_status"] != "blocked":
            failures.append(f"{target} must remain blocked.")
        if item["submission_url"] is not None or item["submitted_at"] is not None:
            failures.append(f"{target} must not record external submission evidence yet.")
        if not item["blocker_reason"]:
            failures.append(f"{target} must record a blocker reason.")

    templates = {item["target"]: item for item in manifest["submission_templates"]}
    if set(templates) != expected_targets:
        failures.append("submission_templates must list the six endpoint families.")
    if not any(
        "maintainer-confirmed codebook intake" in item["review_gate"]
        for item in manifest["submission_templates"]
    ):
        failures.append("submission templates must mention maintainer review gates.")

    doc_text = _read(DOC_PATH)
    for required in (
        "ParlaMint-NZ / TEI",
        "Popolo / Open Civic Data",
        "Akoma Ntoso",
        "CAP / ParlaCAP",
        "Universal Dependencies / CoNLL-U",
        "RDF / Linked Data",
        "local-review-only",
        "No submission URLs are recorded yet",
    ):
        if required not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    track_text = _read(TRACK_PATH)
    for required in (
        "Eligibility",
        "Handoff",
        "Follow-Up",
        "Submission Log",
        "Blocked Targets",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    upstream_packages = _json(UPSTREAM_PACKAGES_PATH)
    if upstream_packages["validation_results"]["package_catalogued"] is not True:
        failures.append("Upstream contribution package catalog must remain validated.")
    if upstream_packages["validation_results"]["external_submission_links_recorded"] is not False:
        failures.append("Upstream contribution package catalog must not claim submission links.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"UPSTREAM-SUBMISSION-EXECUTION: {failure}")
        return 1
    print("Upstream submission execution manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
