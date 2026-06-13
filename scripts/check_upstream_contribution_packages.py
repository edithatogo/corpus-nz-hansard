"""Validate the upstream contribution package catalog."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/upstream_contribution_packages_validation_manifest.json"
DOC_PATH = ROOT / "docs/upstream-contribution-packages.md"
TRACK_PATH = ROOT / "conductor/tracks/upstream_contribution_packages_20260609/evidence.md"

REQUIRED_TARGETS = {
    "ParlaMint-NZ / TEI": "fork-plus-data-branch-pull-request",
    "Popolo / Open Civic Data": "github-issues-or-pull-requests",
    "CAP / ParlaCAP": "unconfirmed-maintainer-path",
}

REQUIRED_DOC_TERMS = (
    "ParlaMint-NZ / TEI",
    "fork-based pull requests",
    "mysociety/parlparse",
    "issues and pull requests",
    "CAP / ParlaCAP",
    "locally blocked",
    "No upstream submission links are recorded",
)

REQUIRED_TRACK_TERMS = (
    "Current Mechanism Checks",
    "Package Contents",
    "Readiness Boundary",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, DOC_PATH, TRACK_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    if manifest["release_status"] != "local-review-only":
        failures.append("Upstream contribution package manifest must remain local-review-only.")
    if manifest["submission_status"] != "not-submitted":
        failures.append(
            "Upstream contribution package manifest must not claim external submission."
        )
    if manifest["validation_results"]["package_catalogued"] is not True:
        failures.append(
            "Upstream contribution package manifest must mark the catalogued package as true."
        )
    if manifest["validation_results"]["mechanisms_checked"] is not True:
        failures.append("Upstream contribution package manifest must mark mechanisms_checked true.")

    targets = {item["target"]: item for item in manifest["package_contents"]}
    if set(targets) != set(REQUIRED_TARGETS):
        failures.append("Upstream contribution package manifest must list the expected targets.")
    for target, mechanism in REQUIRED_TARGETS.items():
        item = targets.get(target)
        if item is None:
            continue
        if item["contribution_mechanism"] != mechanism:
            failures.append(f"{target} must record contribution mechanism {mechanism}.")
        if not item["local_artifacts"]:
            failures.append(f"{target} must list local artifacts.")

    doc_text = _read(DOC_PATH)
    for term in REQUIRED_DOC_TERMS:
        if term not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing term: {term}")

    track_text = _read(TRACK_PATH)
    for term in REQUIRED_TRACK_TERMS:
        if term not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing term: {term}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"UPSTREAM-CONTRIBUTION-PACKAGES: {failure}")
        return 1
    print("Upstream contribution packages are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
