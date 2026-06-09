"""Build a release evidence ledger for public corpus artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = Path("manifests/release_evidence_ledger.json")
DEFAULT_REPOSITORY = "edithatogo/corpus-nz-hansard"
DEFAULT_COVERAGE = "Document-level New Zealand Hansard corpus release."
LEDGER_VERSION = 1

PROVENANCE_POLICY = (
    {
        "artifact_class": "zenodo_archive",
        "strategy": "github_artifact_attestation",
        "status": "enforced",
        "evidence": (
            ".github/workflows/zenodo_archive.yml attests generated Zenodo tarballs "
            "and manifests with actions/attest-build-provenance."
        ),
    },
    {
        "artifact_class": "zenodo_manifest",
        "strategy": "github_artifact_attestation",
        "status": "enforced",
        "evidence": (
            "Zenodo archive manifests are included in the attestation subject-path "
            "and also carry per-file SHA-256 checksums."
        ),
    },
    {
        "artifact_class": "huggingface_dataset_revision",
        "strategy": "revision_and_manifest_hash",
        "status": "documented",
        "evidence": (
            "Hugging Face publication evidence is the immutable revision plus the "
            "release manifest hash recorded in this ledger."
        ),
    },
    {
        "artifact_class": "github_review_package",
        "strategy": "signed_checksum",
        "status": "documented",
        "evidence": (
            "Review ZIP packages are accompanied by JSON manifests with SHA-256 "
            "checksums; stronger signing is deferred to release automation."
        ),
    },
    {
        "artifact_class": "derived_candidate_outputs",
        "strategy": "documented_deferral",
        "status": "deferred",
        "evidence": (
            "Speech-turn, search-index, DuckDB, and other derived candidate outputs "
            "are not final public release artifacts until their validation tracks land."
        ),
    },
)


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_evidence(path: Path) -> dict[str, Any]:
    return {
        "path": path.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": _sha256_path(path),
    }


def _git_commit_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip() or "unknown"


def _workflow_run_url(repository: str, run_id: str | None) -> str | None:
    if not run_id:
        return None
    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    return f"{server_url}/{repository}/actions/runs/{run_id}"


def build_release_evidence_ledger(
    output: Path | str = DEFAULT_OUTPUT,
    repository: str = DEFAULT_REPOSITORY,
    commit_sha: str | None = None,
    workflow_name: str | None = None,
    workflow_run_id: str | None = None,
    huggingface_repo_id: str | None = None,
    huggingface_revision: str | None = None,
    zenodo_doi: str | None = None,
    zenodo_concept_doi: str | None = None,
    schema_version: str = "1",
    record_count: int | None = None,
    coverage_statement: str = DEFAULT_COVERAGE,
    manifests: tuple[Path, ...] = (),
    artifacts: tuple[Path, ...] = (),
) -> dict[str, Any]:
    """Build and write a release evidence ledger."""
    output = Path(output)
    resolved_commit = commit_sha or os.environ.get("GITHUB_SHA") or _git_commit_sha()
    resolved_repository = repository or os.environ.get("GITHUB_REPOSITORY") or DEFAULT_REPOSITORY
    resolved_run_id = workflow_run_id or os.environ.get("GITHUB_RUN_ID")
    resolved_workflow_name = workflow_name or os.environ.get("GITHUB_WORKFLOW")

    ledger = {
        "ledger_version": LEDGER_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "repository": resolved_repository,
        "commit_sha": resolved_commit,
        "workflow": {
            "name": resolved_workflow_name,
            "run_id": resolved_run_id,
            "run_url": _workflow_run_url(resolved_repository, resolved_run_id),
        },
        "dataset": {
            "schema_version": schema_version,
            "record_count": record_count,
            "coverage_statement": coverage_statement,
        },
        "huggingface": {
            "repo_id": huggingface_repo_id or os.environ.get("HF_REPO_ID"),
            "revision": huggingface_revision or os.environ.get("HF_REVISION"),
        },
        "zenodo": {
            "doi": zenodo_doi or os.environ.get("ZENODO_DOI"),
            "concept_doi": zenodo_concept_doi or os.environ.get("ZENODO_CONCEPT_DOI"),
        },
        "manifests": [_file_evidence(path) for path in manifests],
        "artifacts": [_file_evidence(path) for path in artifacts],
        "provenance_policy": list(PROVENANCE_POLICY),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ledger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a corpus release evidence ledger.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--repository", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPOSITORY)
    )
    parser.add_argument("--commit-sha", default=None)
    parser.add_argument("--workflow-name", default=None)
    parser.add_argument("--workflow-run-id", default=None)
    parser.add_argument("--huggingface-repo-id", default=None)
    parser.add_argument("--huggingface-revision", default=None)
    parser.add_argument("--zenodo-doi", default=None)
    parser.add_argument("--zenodo-concept-doi", default=None)
    parser.add_argument("--schema-version", default="1")
    parser.add_argument("--record-count", type=int, default=None)
    parser.add_argument("--coverage-statement", default=DEFAULT_COVERAGE)
    parser.add_argument("--manifest", type=Path, action="append", default=[])
    parser.add_argument("--artifact", type=Path, action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_release_evidence_ledger(
        output=args.output,
        repository=args.repository,
        commit_sha=args.commit_sha,
        workflow_name=args.workflow_name,
        workflow_run_id=args.workflow_run_id,
        huggingface_repo_id=args.huggingface_repo_id,
        huggingface_revision=args.huggingface_revision,
        zenodo_doi=args.zenodo_doi,
        zenodo_concept_doi=args.zenodo_concept_doi,
        schema_version=args.schema_version,
        record_count=args.record_count,
        coverage_statement=args.coverage_statement,
        manifests=tuple(args.manifest),
        artifacts=tuple(args.artifact),
    )
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
