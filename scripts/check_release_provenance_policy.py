"""Validate release provenance policy wiring."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_LEDGER_FIELDS = (
    "commit_sha",
    "workflow",
    "huggingface",
    "zenodo",
    "manifests",
    "artifacts",
    "provenance_policy",
)

REQUIRED_DOC_SNIPPETS = (
    "commit SHA",
    "workflow run",
    "Hugging Face revision",
    "Zenodo DOI",
    "concept DOI",
    "manifest hash",
    "record count",
    "coverage statement",
    "zenodraft",
)

REQUIRED_ZENODO_SNIPPETS = (
    "attestations: write",
    "id-token: write",
    "actions/attest-build-provenance@a2bbfa25375fe432b6a289bc6b6cd05ecd0c4c32",
    "generated/zenodo/*.tar.gz",
    "generated/zenodo/*.manifest.json",
)

REQUIRED_PUBLICATION_WORKFLOWS = (
    ".github/workflows/huggingface_publish.yml",
    ".github/workflows/zenodo_archive.yml",
    ".github/workflows/zenodo_metadata.yml",
    ".github/workflows/zenodo_publish.yml",
)


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _failures() -> list[str]:
    failures: list[str] = []

    schema = json.loads(_read("schemas/release_evidence_ledger.schema.json"))
    required = set(schema.get("required", []))
    for field in REQUIRED_LEDGER_FIELDS:
        if field not in required:
            failures.append(f"Release evidence ledger schema does not require {field}.")

    builder = _read("scripts/build_release_evidence_ledger.py")
    for strategy in (
        "github_artifact_attestation",
        "revision_and_manifest_hash",
        "signed_checksum",
        "documented_deferral",
    ):
        if strategy not in builder:
            failures.append(f"Release evidence builder is missing strategy {strategy}.")

    docs = _read("docs/release-evidence-ledger.md")
    for snippet in REQUIRED_DOC_SNIPPETS:
        if snippet not in docs:
            failures.append(f"docs/release-evidence-ledger.md is missing: {snippet}")

    zenodo_workflow = _read(".github/workflows/zenodo_archive.yml")
    for snippet in REQUIRED_ZENODO_SNIPPETS:
        if snippet not in zenodo_workflow:
            failures.append(f"Zenodo workflow is missing provenance snippet: {snippet}")

    if not re.search(
        r"actions/attest-build-provenance@[0-9a-f]{40}",
        zenodo_workflow,
    ):
        failures.append("Zenodo attestation action must stay pinned to a full commit SHA.")

    workflow_paths = sorted(
        path.relative_to(ROOT).as_posix() for path in (ROOT / ".github/workflows").glob("*.yml")
    )
    workflow_texts = {path: _read(path) for path in workflow_paths}
    for workflow_path in REQUIRED_PUBLICATION_WORKFLOWS:
        workflow_text = workflow_texts[workflow_path]
        if "workflow_dispatch:" not in workflow_text:
            failures.append(f"{workflow_path} must stay manually dispatched.")
        if re.search(r"^\s+pull_request\s*:", workflow_text, flags=re.MULTILINE):
            failures.append(f"{workflow_path} must not publish from pull_request.")
        if re.search(r"^\s+push\s*:", workflow_text, flags=re.MULTILINE):
            failures.append(f"{workflow_path} must not publish from push.")

    quality_workflow = _read(".github/workflows/quality.yml")
    if "python scripts\\check_release_provenance_policy.py" not in quality_workflow:
        failures.append("Quality workflow must run release provenance policy checks.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PROVENANCE-POLICY: {failure}")
        return 1
    print("Release provenance policy is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
