"""Validate multi-git mirror workflow and OSF policy linkage."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

WORKFLOW_PATH = ROOT / ".github/workflows/mirror_sync.yml"
STATUS_MANIFEST_PATH = ROOT / "manifests/multi_git_archive_mirroring_status.json"
QUALITY_WORKFLOW_PATH = ROOT / ".github/workflows/quality.yml"
MAKEFILE_PATH = ROOT / "Makefile"
QUALITY_DOC_PATH = ROOT / "docs/quality-gate.md"

APPROVED_CHECKOUT_SHA = "93cb6efe18208431cddfb8368fd83d5badbf9bfd"

REQUIRED_MIRROR_WORKFLOW_SNIPPETS = (
    "push:",
    "branches: [ main, master ]",
    "workflow_dispatch:",
    "permissions:",
    "contents: read",
    "fetch-depth: 0",
    "persist-credentials: false",
    "GITHUB_REF_TO_PUSH: ${{ github.ref }}",
    "GIT_MIRROR_URL: ${{ secrets.GIT_MIRROR_URL }}",
    "GIT_MIRROR_SSH_PRIVATE_KEY: ${{ secrets.GIT_MIRROR_SSH_PRIVATE_KEY }}",
    'if [ -z "$GIT_MIRROR_URL" ]; then',
    "GIT_MIRROR_URL is not set, skipping mirror.",
    'if [ -z "$GIT_MIRROR_SSH_PRIVATE_KEY" ]; then',
    "GIT_MIRROR_SSH_PRIVATE_KEY is not set, skipping mirror.",
    'ssh-keyscan -t ed25519 "$HOST"',
    'git remote add mirror "$GIT_MIRROR_URL"',
    'git push --force --prune mirror "HEAD:${GITHUB_REF_TO_PUSH}"',
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _status_manifest_failures() -> list[str]:
    failures: list[str] = []
    manifest = _json(STATUS_MANIFEST_PATH)
    expected = {
        "artifact_name": "multi_git_archive_mirroring_status",
        "track_id": "multi_git_archive_mirroring_20260614",
        "repo_side_status": "implemented",
        "live_status": "deferred-to-future-roadmap",
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            failures.append(f"status manifest {key} must be {value}.")
    workflow = manifest.get("workflow", {})
    if workflow.get("checkout_ref") != APPROVED_CHECKOUT_SHA:
        failures.append("status manifest must record the approved checkout SHA.")
    if workflow.get("manual_trigger") is not True:
        failures.append("status manifest must record workflow_dispatch support.")
    if workflow.get("incomplete_secret_pair_behavior") != "skip-before-ssh-setup":
        failures.append("status manifest must record skip-before-ssh-setup secret handling.")
    for secret in ("GIT_MIRROR_URL", "GIT_MIRROR_SSH_PRIVATE_KEY"):
        if secret not in workflow.get("secrets_required", []):
            failures.append(f"status manifest missing required secret: {secret}")
    archives = manifest.get("archives", {})
    if archives.get("osf_status") != "inactive-until-policy-activation":
        failures.append("status manifest must record inactive OSF status.")
    if archives.get("osf_claims_allowed") is not False:
        failures.append("status manifest must not allow OSF publication claims yet.")
    blocked_on = " ".join(manifest.get("blocked_on", []))
    for required in ("edithatogo", "GIT_MIRROR_URL", "GIT_MIRROR_SSH_PRIVATE_KEY", "Mirror Sync"):
        if required not in blocked_on:
            failures.append(f"status manifest blocked_on must include: {required}")
    if manifest.get("future_roadmap_ref") != "conductor/improvement-backlog.md":
        failures.append("status manifest must point to the future roadmap backlog.")
    return failures


def _osf_policy_failures() -> list[str]:
    sys.path.insert(0, str(ROOT))
    from scripts.check_osf_optional_mirror_policy import _failures as osf_policy_failures

    return osf_policy_failures()


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        WORKFLOW_PATH,
        STATUS_MANIFEST_PATH,
        QUALITY_WORKFLOW_PATH,
        MAKEFILE_PATH,
        QUALITY_DOC_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    workflow = _read(WORKFLOW_PATH)
    for snippet in REQUIRED_MIRROR_WORKFLOW_SNIPPETS:
        if snippet not in workflow:
            failures.append(f"mirror_sync.yml is missing: {snippet}")

    checkout_refs = re.findall(r"uses:\s*actions/checkout@([A-Za-z0-9_.-]+)", workflow)
    if checkout_refs != [APPROVED_CHECKOUT_SHA]:
        failures.append("mirror_sync.yml must use the approved pinned actions/checkout SHA.")

    if re.search(r"^\s+pull_request\s*:", workflow, flags=re.MULTILINE):
        failures.append("mirror_sync.yml must not run on pull_request.")

    skip_url = workflow.find('if [ -z "$GIT_MIRROR_URL" ]; then')
    skip_key = workflow.find('if [ -z "$GIT_MIRROR_SSH_PRIVATE_KEY" ]; then')
    ssh_setup = workflow.find("mkdir -p ~/.ssh")
    push = workflow.find("git push --force --prune")
    if not (0 <= skip_url < skip_key < ssh_setup < push):
        failures.append(
            "mirror_sync.yml must skip incomplete secret pairs before SSH setup and push."
        )

    quality_workflow = _read(QUALITY_WORKFLOW_PATH)
    for snippet in (
        "pixi run python scripts\\check_osf_optional_mirror_policy.py",
        "pixi run python scripts\\check_multi_git_archive_mirroring.py",
    ):
        if snippet not in quality_workflow:
            failures.append(f"Quality workflow is missing: {snippet}")
    if quality_workflow.find("check_osf_optional_mirror_policy.py") > quality_workflow.find(
        "check_multi_git_archive_mirroring.py"
    ):
        failures.append(
            "Quality workflow must run the OSF policy check before mirror policy linkage."
        )

    makefile = _read(MAKEFILE_PATH)
    for snippet in (
        "multi-git-archive-mirroring:",
        "$(PYTHON) scripts/check_multi_git_archive_mirroring.py",
    ):
        if snippet not in makefile:
            failures.append(f"Makefile is missing: {snippet}")

    quality_doc = _read(QUALITY_DOC_PATH)
    if "scripts/check_multi_git_archive_mirroring.py" not in quality_doc:
        failures.append("docs/quality-gate.md must document the multi-git archive mirroring check.")

    failures.extend(_status_manifest_failures())
    failures.extend(f"OSF policy dependency: {failure}" for failure in _osf_policy_failures())
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"MULTI-GIT-ARCHIVE-MIRRORING: {failure}")
        return 1
    print("Multi-git archive mirroring repo-side contract is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
