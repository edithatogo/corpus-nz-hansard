"""Validate monthly dynamic archive publication configuration and evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "monthly_dynamic_archive_publication.yml"
CONTRACT = ROOT / "manifests" / "monthly_dynamic_archive_publication_contract.json"
EVIDENCE = ROOT / "manifests" / "monthly_dynamic_archive_publication_evidence.json"

REQUIRED_EVIDENCE_FIELDS = (
    "manifest_version",
    "track_id",
    "generated_at",
    "run",
    "source",
    "archive",
    "huggingface",
    "zenodo",
    "validation",
    "rights_boundary",
)

REQUIRED_MODES = ("dry-run", "huggingface", "zenodo-draft", "full")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    return value if isinstance(value, dict) else {}


def _contains_all(text: str, snippets: tuple[str, ...], label: str) -> list[str]:
    return [f"{label} is missing: {snippet}" for snippet in snippets if snippet not in text]


def _workflow_failures(text: str) -> list[str]:
    failures: list[str] = []
    failures.extend(
        _contains_all(
            text,
            (
                'cron: "17 3 1 * *"',
                "workflow_dispatch:",
                "publication_mode:",
                "Resolve publication mode",
                "Build monthly release evidence",
                "Upload monthly publication result artifacts",
            ),
            "Monthly workflow",
        )
    )
    for mode in REQUIRED_MODES:
        if not re.search(rf"^\s+- {re.escape(mode)}\s*$", text, flags=re.MULTILINE):
            failures.append(f"Monthly workflow is missing publication mode {mode}.")
    for permission in ("attestations: write", "contents: read", "id-token: write"):
        if permission not in text:
            failures.append(f"Monthly workflow is missing least-privilege permission {permission}.")
    for secret in ("SOURCE_ARCHIVE_URL", "HF_TOKEN", "ZENODO_TOKEN", "ARCHIVE_CREATORS_JSON"):
        if secret not in text:
            failures.append(f"Monthly workflow does not check or use required secret {secret}.")
    if re.search(r"^\s+pull_request\s*:", text, flags=re.MULTILINE):
        failures.append("Monthly workflow must not publish from pull_request events.")
    if "dependabot" in text.lower():
        failures.append("Monthly workflow must not include dependency-update publication paths.")
    if "publish_zenodo_deposition.py" in text:
        failures.append("Monthly workflow must not directly publish Zenodo depositions.")
    if "zenodo-production-publish environment" not in text:
        failures.append("Monthly workflow must record the protected Zenodo publish handoff.")
    return failures


def _contract_failures(contract: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if contract.get("workflow") != ".github/workflows/monthly_dynamic_archive_publication.yml":
        failures.append("Monthly contract points at the wrong workflow.")
    if contract.get("cadence") != "monthly":
        failures.append("Monthly contract cadence must be monthly.")
    required = tuple(contract.get("evidence_required_fields", ()))
    if required != REQUIRED_EVIDENCE_FIELDS:
        failures.append("Monthly contract evidence_required_fields do not match checker policy.")
    zenodo = contract.get("zenodo", {})
    if not isinstance(zenodo, dict) or not zenodo.get("publish_requires_protected_environment"):
        failures.append("Monthly contract must require protected Zenodo publication.")
    if not isinstance(zenodo, dict) or not zenodo.get("zenodraft_required_or_formally_evaluated"):
        failures.append("Monthly contract must require or formally evaluate zenodraft.")
    return failures


def _file_evidence_failures(value: Any, label: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{label} evidence must be an object."]
    failures: list[str] = []
    for field in ("path", "exists", "size_bytes", "sha256"):
        if field not in value:
            failures.append(f"{label} evidence is missing {field}.")
    if value.get("exists") and not value.get("sha256"):
        failures.append(f"{label} evidence exists but does not record sha256.")
    return failures


def _evidence_failures(contract: dict[str, Any], evidence: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for field in REQUIRED_EVIDENCE_FIELDS:
        if field not in evidence:
            failures.append(f"Evidence manifest is missing {field}.")
    if evidence.get("track_id") != contract.get("track_id"):
        failures.append("Evidence manifest track_id does not match the publication contract.")
    run = evidence.get("run", {})
    if not isinstance(run, dict) or "commit_sha" not in run:
        failures.append("Evidence manifest run block must include commit_sha.")
    archive = evidence.get("archive", {})
    if isinstance(archive, dict):
        failures.extend(_file_evidence_failures(archive.get("tarball"), "Archive tarball"))
        failures.extend(_file_evidence_failures(archive.get("manifest"), "Archive manifest"))
    else:
        failures.append("Evidence manifest archive block must be an object.")
    validation = evidence.get("validation", {})
    if isinstance(validation, dict):
        failures.extend(
            _file_evidence_failures(validation.get("record_validation"), "Record validation")
        )
        if validation.get("record_count") in (None, 0):
            failures.append("Evidence manifest must record a non-zero row count.")
    else:
        failures.append("Evidence manifest validation block must be an object.")
    huggingface = evidence.get("huggingface", {})
    if not isinstance(huggingface, dict) or not huggingface.get("repo_id"):
        failures.append("Evidence manifest must record the Hugging Face repository id.")
    zenodo = evidence.get("zenodo", {})
    if isinstance(zenodo, dict):
        if zenodo.get("protected_publish_environment") != "zenodo-production-publish":
            failures.append("Evidence manifest must record the protected Zenodo environment.")
        if zenodo.get("publish_handoff_only") is not True:
            failures.append("Evidence manifest must record Zenodo publish handoff-only behavior.")
    else:
        failures.append("Evidence manifest Zenodo block must be an object.")
    rights = evidence.get("rights_boundary", {})
    if isinstance(rights, dict):
        if rights.get("source_zip_committed") is not False:
            failures.append("Evidence manifest must state that the source zip is not committed.")
        if rights.get("source_zip_publicly_published") is not False:
            failures.append("Evidence manifest must state that the source zip is not republished.")
        if rights.get("no_official_endorsement_claim") is not True:
            failures.append("Evidence manifest must avoid official endorsement claims.")
    else:
        failures.append("Evidence manifest rights_boundary block must be an object.")
    return failures


def _failures() -> list[str]:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    contract = _read_json(CONTRACT)
    evidence = _read_json(EVIDENCE)
    failures: list[str] = []
    failures.extend(_workflow_failures(workflow_text))
    failures.extend(_contract_failures(contract))
    failures.extend(_evidence_failures(contract, evidence))
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"MONTHLY-PUBLICATION: {failure}")
        return 1
    print("Monthly dynamic archive publication configuration is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
