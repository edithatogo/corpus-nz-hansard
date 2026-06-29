"""Build evidence for monthly dynamic archive publication runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "manifests" / "monthly_dynamic_archive_publication_contract.json"
DEFAULT_OUTPUT = ROOT / "manifests" / "monthly_dynamic_archive_publication_evidence.json"
DEFAULT_RECORD_VALIDATION = ROOT / "manifests" / "record_schema_validation.json"


def _repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_evidence(path: Path) -> dict[str, Any]:
    return {
        "path": _repo_path(path),
        "exists": path.exists() and path.is_file(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
        "sha256": _sha256(path),
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    return value if isinstance(value, dict) else {}


def _git_value(*args: str) -> str | None:
    try:
        completed = subprocess.run(
            ("git", *args),
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except OSError, subprocess.CalledProcessError:
        return None
    value = completed.stdout.strip()
    return value or None


def _first_present(mapping: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = mapping.get(name)
        if value not in (None, ""):
            return value
    return None


def _count_manifest_files(archive_manifest: dict[str, Any]) -> int | None:
    file_count = _first_present(archive_manifest, "file_count")
    if isinstance(file_count, int):
        return file_count
    files = archive_manifest.get("files")
    if isinstance(files, list):
        return len(files)
    return None


def _source_archive_url_configured() -> bool:
    if os.environ.get("SOURCE_ARCHIVE_URL_CONFIGURED", "").lower() == "true":
        return True
    return bool(os.environ.get("SOURCE_ARCHIVE_URL"))


def build_evidence(args: argparse.Namespace) -> dict[str, Any]:
    contract = _read_json(args.contract)
    validation = _read_json(args.record_validation)
    archive_manifest = _read_json(args.archive_manifest)
    hf_result = _read_json(args.huggingface_result)
    zenodo_result = _read_json(args.zenodo_result)

    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repository = os.environ.get("GITHUB_REPOSITORY")
    run_id = os.environ.get("GITHUB_RUN_ID")
    run_url = f"{server_url}/{repository}/actions/runs/{run_id}" if repository and run_id else None
    revision = _first_present(hf_result, "revision", "commit", "commit_sha")

    return {
        "manifest_version": 1,
        "track_id": contract.get("track_id", "monthly_dynamic_archive_publication_20260629"),
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "run": {
            "github_run_id": run_id,
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "github_run_url": run_url,
            "workflow": contract.get("workflow"),
            "publication_mode": os.environ.get("PUBLICATION_MODE", "dry-run"),
            "commit_sha": os.environ.get("GITHUB_SHA") or _git_value("rev-parse", "HEAD"),
            "ref_name": os.environ.get("GITHUB_REF_NAME") or _git_value("branch", "--show-current"),
        },
        "source": {
            "archive_url_configured": _source_archive_url_configured(),
            "source_zip_committed": False,
            "source_zip_publicly_published": False,
        },
        "archive": {
            "tarball": _file_evidence(args.archive),
            "manifest": _file_evidence(args.archive_manifest),
            "manifest_record_count": _first_present(archive_manifest, "record_count", "rows"),
            "manifest_file_count": _count_manifest_files(archive_manifest),
        },
        "huggingface": {
            "repo_id": os.environ.get("HF_REPO_ID")
            or contract.get("huggingface", {}).get("default_repo_id"),
            "public_url": contract.get("huggingface", {}).get("public_url"),
            "upload_result": _file_evidence(args.huggingface_result),
            "revision": revision,
            "revision_sha": _first_present(hf_result, "revision_sha", "sha"),
        },
        "zenodo": {
            "api_url": os.environ.get("ZENODO_API_URL")
            or contract.get("zenodo", {}).get("api_url_default"),
            "draft_result": _file_evidence(args.zenodo_result),
            "deposition_id": _first_present(zenodo_result, "deposition_id", "id"),
            "doi": _first_present(zenodo_result, "doi", "conceptdoi", "concept_doi"),
            "protected_publish_environment": contract.get("zenodo", {}).get(
                "protected_publish_environment"
            ),
            "publish_handoff_only": True,
        },
        "validation": {
            "record_validation": _file_evidence(args.record_validation),
            "record_count": _first_present(validation, "record_count", "rows"),
            "record_schema_ok": validation.get("ok"),
            "errors": validation.get("errors", []),
            "warnings": validation.get("warnings", []),
        },
        "rights_boundary": {
            "no_official_endorsement_claim": True,
            "source_zip_committed": False,
            "source_zip_publicly_published": False,
            "notes": [
                "Generated normalized artifacts are publication targets; the governed source zip is not committed or republished.",
                "Zenodo final publication is routed through the protected zenodo-production-publish environment.",
            ],
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the monthly dynamic archive publication evidence manifest."
    )
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--archive",
        type=Path,
        default=ROOT / "generated" / "zenodo" / "nz-hansard-corpus-0.1.0.tar.gz",
    )
    parser.add_argument(
        "--archive-manifest",
        type=Path,
        default=ROOT / "generated" / "zenodo" / "nz-hansard-corpus-0.1.0.manifest.json",
    )
    parser.add_argument("--record-validation", type=Path, default=DEFAULT_RECORD_VALIDATION)
    parser.add_argument(
        "--huggingface-result",
        type=Path,
        default=ROOT / "generated" / "monthly-publication" / "huggingface-upload.json",
    )
    parser.add_argument(
        "--zenodo-result",
        type=Path,
        default=ROOT / "generated" / "monthly-publication" / "zenodo-draft-upload.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evidence = build_evidence(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {_repo_path(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
