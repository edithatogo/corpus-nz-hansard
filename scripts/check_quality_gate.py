"""Validate the repository quality-gate configuration."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DEV_TOOLS = {
    "ruff",
    "ty",
    "typos",
    "zizmor",
    "taplo",
}

REQUIRED_QUALITY_SNIPPETS = (
    "python -m ruff check --no-cache .",
    "python -m ruff format --check --no-cache .",
    "ty check --error all .",
    "typos --config typos.toml",
    "zizmor --min-severity medium .github/workflows",
    "taplo format --check pyproject.toml typos.toml",
    "actionlint -color",
    "python scripts\\check_quality_gate.py",
    "python scripts\\check_release_provenance_policy.py",
)

REQUIRED_MAKE_TARGETS = (
    "quality:",
    "quality-config:",
    "provenance-policy:",
    "lint:",
    "format-check:",
    "typecheck:",
    "spell:",
    "workflow-audit:",
    "toml-check:",
    "workflow-syntax:",
    "test:",
)

PUBLICATION_WORKFLOWS = (
    ".github/workflows/huggingface_publish.yml",
    ".github/workflows/zenodo_archive.yml",
    ".github/workflows/zenodo_metadata.yml",
    ".github/workflows/zenodo_publish.yml",
)


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _failures() -> list[str]:
    failures: list[str] = []

    dev_requirements = _read("requirements/dev.txt")
    for tool in sorted(REQUIRED_DEV_TOOLS):
        if not re.search(rf"^{re.escape(tool)}==", dev_requirements, flags=re.MULTILINE):
            failures.append(f"requirements/dev.txt does not pin {tool}.")

    quality_workflow = _read(".github/workflows/quality.yml")
    for snippet in REQUIRED_QUALITY_SNIPPETS:
        if snippet not in quality_workflow:
            failures.append(f"Quality workflow is missing: {snippet}")

    makefile = _read("Makefile")
    for target in REQUIRED_MAKE_TARGETS:
        if target not in makefile:
            failures.append(f"Makefile is missing target {target}")

    quality_doc = _read("docs/quality-gate.md")
    for snippet in REQUIRED_QUALITY_SNIPPETS:
        normalized = snippet.replace("\\", "/")
        if snippet not in quality_doc and normalized not in quality_doc:
            failures.append(f"docs/quality-gate.md is missing command: {snippet}")

    workflow_paths = sorted(
        path.relative_to(ROOT).as_posix() for path in (ROOT / ".github/workflows").glob("*.yml")
    )
    workflow_texts = {path: _read(path) for path in workflow_paths}
    for workflow_path, workflow_text in workflow_texts.items():
        for ref in re.findall(r"uses:\s*[^#\n]*?@([A-Za-z0-9_.-]+)", workflow_text):
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                failures.append(f"{workflow_path} uses an unpinned action ref: @{ref}")

    for workflow_path in PUBLICATION_WORKFLOWS:
        workflow_text = workflow_texts[workflow_path]
        if "workflow_dispatch:" not in workflow_text:
            failures.append(f"{workflow_path} must be manually dispatched.")
        if re.search(r"^\s+pull_request\s*:", workflow_text, flags=re.MULTILINE):
            failures.append(f"{workflow_path} must not run on pull_request.")
        if re.search(r"^\s+push\s*:", workflow_text, flags=re.MULTILINE):
            failures.append(f"{workflow_path} must not run on push.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"QUALITY-GATE: {failure}")
        return 1
    print("Quality gate configuration is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
