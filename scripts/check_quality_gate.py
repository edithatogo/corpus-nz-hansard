"""Validate the repository quality-gate configuration."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DEV_TOOLS = {
    "basedpyright",
    "cyclonedx-py",
    "deptry",
    "detect-secrets",
    "mutmut",
    "pip-audit",
    "pyinstrument",
    "pyrefly",
    "pytest-benchmark",
    "pytest-rerunfailures",
    "pytest-socket",
    "ruff",
    "ty",
    "typos",
    "vulture",
    "zizmor",
    "taplo",
}

REQUIRED_QUALITY_SNIPPETS = (
    "iwr -UseBasicParsing https://pixi.sh/install.ps1 | iex",
    "pixi install",
    "pixi run lint",
    "pixi run format-check",
    "pixi run typecheck",
    "pixi run spell",
    "pixi run workflow-audit",
    "pixi run toml-check",
    "actionlint -color",
    "pixi run python scripts\\check_quality_gate.py",
    "pixi run python scripts\\check_conductor_learning_log.py",
    "pixi run python scripts\\check_release_provenance_policy.py",
    "pixi run python scripts\\check_release_version_consistency.py",
    "pixi run python scripts\\check_public_surface_audit.py",
    "pixi run python scripts\\check_zenodo_rights_metadata.py",
    "pixi run python scripts\\check_shared_core_schema.py",
    "pixi run python scripts\\check_metadata_packages.py",
    "pixi run python scripts\\check_osf_optional_mirror_policy.py",
    "pixi run python scripts\\check_multi_git_archive_mirroring.py",
    "pixi run python scripts\\check_hathitrust_acquisition.py",
    "pixi run python scripts\\check_parliament_website_stealth_access.py",
    "pixi run python scripts\\check_wikipedia_mp_lists_acquisition.py",
    "pixi run python scripts\\check_member_identity_triangulation.py",
    "pixi run python scripts\\check_corpus_family_alignment.py",
    "pixi run python scripts\\check_corpus_family_engineering_alignment.py",
    "pixi run python scripts\\check_authority_sources.py",
    "pixi run python scripts\\check_parliament_dataset_inventory.py",
    "pixi run python scripts\\check_parliament_dataset_seed_fetchers.py",
    "pixi run python scripts\\check_parliament_dataset_full_acquisition.py",
    "pixi run python scripts\\check_historical_sitting_inventory.py",
    "pixi run python scripts\\check_historical_sitting_official_exports.py",
    "pixi run python scripts\\build_historical_sitting_official_exports_coverage.py",
    "pixi run python scripts\\check_historical_sitting_reconciliation.py",
    "pixi run python scripts\\check_historical_coverage_audit.py",
    "pixi run python scripts\\check_release_ladder.py",
    "pixi run python scripts\\check_gold_evaluation_datasets.py",
    "pixi run python scripts\\check_canonical_id_uri_policy.py",
    "pixi run python scripts\\check_dependency_extras_policy.py",
    "pixi run python scripts\\check_nz_parliamentary_procedure_model.py",
    "pixi run python scripts\\check_neutral_component_model.py",
    "pixi run python scripts\\check_akoma_ntoso_endpoint.py",
    "pixi run python scripts\\check_parlamint_nz_endpoint.py",
    "pixi run python scripts\\check_popolo_opencivicdata_endpoint.py",
    "pixi run python scripts\\check_ud_conllu_endpoint.py",
    "pixi run python scripts\\check_rdf_linked_data_endpoint.py",
    "pixi run python scripts\\validate_derived_fields.py",
)

REQUIRED_QUALITY_DEPENDENCIES = (
    "pixi-install",
    "lint",
    "format-check",
    "typecheck",
    "spell",
    "workflow-audit",
    "toml-check",
    "workflow-syntax",
    "quality-config",
    "learning-log",
    "provenance-policy",
    "version-consistency",
    "public-surface-audit",
    "zenodo-rights",
    "shared-core",
    "metadata-packages",
    "osf-policy",
    "multi-git-archive-mirroring",
    "hathitrust-acquisition",
    "parliament-stealth-access",
    "wikipedia-mp-lists-acquisition",
    "member-identity-triangulation",
    "corpus-family-alignment",
    "corpus-family-engineering",
    "authority-sources",
    "parliament-dataset-inventory",
    "parliament-dataset-seed-fetchers",
    "parliament-dataset-full-acquisition",
    "historical-sitting-inventory",
    "historical-sitting-official-exports",
    "historical-sitting-official-exports-coverage",
    "historical-sitting-reconciliation",
    "historical-coverage",
    "release-ladder",
    "gold-evaluation",
    "canonical-ids",
    "dependency-extras",
    "procedure-model",
    "neutral-components",
    "akoma-ntoso",
    "parlamint-nz",
    "popolo-ocd",
    "ud-conllu",
    "rdf-linked-data",
    "corpus-wide-member-identity",
    "corpus-wide-party-attribution",
    "validated-speech-turn",
    "derived-fields-validation",
    "test",
)

REQUIRED_PIXI_QUALITY_DEPENDENCIES = (
    "lint",
    "format-check",
    "typecheck",
    "spell",
    "workflow-audit",
    "toml-check",
    "quality-config",
    "learning-log",
    "provenance-policy",
    "version-consistency",
    "public-surface-audit",
    "zenodo-rights",
    "shared-core",
    "metadata-packages",
    "osf-policy",
    "multi-git-archive-mirroring",
    "hathitrust-acquisition",
    "parliament-stealth-access",
    "wikipedia-mp-lists-acquisition",
    "member-identity-triangulation",
    "corpus-family-alignment",
    "corpus-family-engineering",
    "authority-sources",
    "parliament-dataset-inventory",
    "parliament-dataset-seed-fetchers",
    "parliament-dataset-full-acquisition",
    "historical-sitting-inventory",
    "historical-sitting-official-exports",
    "historical-sitting-official-exports-coverage",
    "historical-sitting-reconciliation",
    "historical-coverage",
    "release-ladder",
    "gold-evaluation",
    "canonical-ids",
    "dependency-extras",
    "procedure-model",
    "neutral-components",
    "akoma-ntoso",
    "parlamint-nz",
    "popolo-ocd",
    "ud-conllu",
    "rdf-linked-data",
    "corpus-wide-member-identity",
    "corpus-wide-party-attribution",
    "validated-speech-turn",
    "derived-fields-validation",
    "test",
)

REQUIRED_MAKE_TARGETS = (
    "quality:",
    "pixi-install:",
    "pixi-quality:",
    "quality-config:",
    "learning-log:",
    "provenance-policy:",
    "version-consistency:",
    "public-surface-audit:",
    "zenodo-rights:",
    "shared-core:",
    "metadata-packages:",
    "osf-policy:",
    "multi-git-archive-mirroring:",
    "hathitrust-acquisition:",
    "parliament-stealth-access:",
    "wikipedia-mp-lists-acquisition:",
    "member-identity-triangulation:",
    "corpus-family-alignment:",
    "corpus-family-engineering:",
    "authority-sources:",
    "parliament-dataset-inventory:",
    "parliament-dataset-seed-fetchers:",
    "parliament-dataset-full-acquisition:",
    "historical-sitting-inventory:",
    "historical-sitting-official-exports:",
    "historical-sitting-official-exports-coverage:",
    "historical-coverage:",
    "release-ladder:",
    "gold-evaluation:",
    "canonical-ids:",
    "dependency-extras:",
    "procedure-model:",
    "neutral-components:",
    "akoma-ntoso:",
    "parlamint-nz:",
    "popolo-ocd:",
    "ud-conllu:",
    "rdf-linked-data:",
    "derived-fields-validation:",
    "lint:",
    "format-check:",
    "typecheck:",
    "typecheck-basedpyright:",
    "typecheck-pyrefly:",
    "spell:",
    "workflow-audit:",
    "toml-check:",
    "workflow-syntax:",
    "test:",
    "test-offline:",
    "benchmark:",
    "profile-search-index:",
    "security-audit:",
    "sbom:",
    "dependency-check:",
    "dead-code:",
    "mutation-smoke:",
)

PUBLICATION_WORKFLOWS = (
    ".github/workflows/huggingface_publish.yml",
    ".github/workflows/zenodo_archive.yml",
    ".github/workflows/zenodo_metadata.yml",
    ".github/workflows/zenodo_publish.yml",
)

LEARNING_CANDIDATE_WORKFLOW_SNIPPETS = (
    "workflow_dispatch:",
    "event_type:",
    "ci-failure",
    "registry",
    "review",
    "skills-feedback",
    "python3 scripts/record_learning_candidate.py",
    '--snapshot "conductor/.tmp/ci-learning-candidates-${RUN_ID}.md"',
    '--message "Learning candidate (${EVENT_TYPE}) for ${WORKFLOW_NAME}"',
    "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
)


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _failures() -> list[str]:
    failures: list[str] = []

    dev_requirements = _read("requirements/dev.txt")
    for tool in sorted(REQUIRED_DEV_TOOLS):
        if not re.search(rf"^{re.escape(tool)}==", dev_requirements, flags=re.MULTILINE):
            failures.append(f"requirements/dev.txt does not pin {tool}.")

    pyproject = _read("pyproject.toml")
    for snippet in (
        "[project]",
        'name = "corpus-nz-hansard"',
        'requires-python = ">=3.14"',
        'target-version = "py314"',
    ):
        if snippet not in pyproject:
            failures.append(f"pyproject.toml is missing: {snippet}")

    if not (ROOT / "pixi.toml").exists():
        failures.append("pixi.toml must be committed.")
    pixi_manifest = _read("pixi.toml")
    for snippet in (
        'python = "3.14.*"',
        'ruff = "==0.15.18"',
        'basedpyright = "==1.39.8"',
        'pydantic-ai-slim = "==1.107.0"',
        'msgspec = "==0.21.1"',
        'tantivy = "==0.26.0"',
        "quality = { depends-on = ",
    ):
        if snippet not in pixi_manifest:
            failures.append(f"pixi.toml is missing: {snippet}")

    quality_workflow = _read(".github/workflows/quality.yml")
    for snippet in REQUIRED_QUALITY_SNIPPETS:
        if snippet not in quality_workflow:
            failures.append(f"Quality workflow is missing: {snippet}")

    makefile = _read("Makefile")
    for target in REQUIRED_MAKE_TARGETS:
        if target not in makefile:
            failures.append(f"Makefile is missing target {target}")

    quality_line = next(
        (line for line in makefile.splitlines() if line.startswith("quality: ")), ""
    )
    quality_deps = set(quality_line.split()[1:])
    for dependency in REQUIRED_QUALITY_DEPENDENCIES:
        if dependency not in quality_deps:
            failures.append(f"Makefile quality target is missing dependency {dependency}.")

    quality_doc = _read("docs/quality-gate.md")
    for snippet in REQUIRED_QUALITY_SNIPPETS:
        normalized = snippet.replace("\\", "/")
        if snippet not in quality_doc and normalized not in quality_doc:
            failures.append(f"docs/quality-gate.md is missing command: {snippet}")

    pixi_data = tomllib.loads(pixi_manifest)
    pixi_quality = pixi_data.get("tasks", {}).get("quality", {})
    pixi_quality_deps = set(pixi_quality.get("depends-on", []))
    if not pixi_quality_deps:
        failures.append("pixi.toml is missing a quality depends-on task list.")

    for dependency in REQUIRED_PIXI_QUALITY_DEPENDENCIES:
        if dependency not in pixi_quality_deps:
            failures.append(f"pixi.toml quality task is missing dependency {dependency}.")

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

    learning_workflow = workflow_texts.get(".github/workflows/ci-learning-candidates.yml", "")
    for snippet in LEARNING_CANDIDATE_WORKFLOW_SNIPPETS:
        if snippet not in learning_workflow:
            failures.append(f"CI learning candidate workflow is missing: {snippet}")

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
