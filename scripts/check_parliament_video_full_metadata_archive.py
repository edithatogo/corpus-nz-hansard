"""Validate the Parliament video full metadata archive contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_full_metadata_archive.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_full_metadata_archive.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-full-metadata-archive.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "parliament-video-full-metadata-archive.yml"
RUNNER_PATH = ROOT / "scripts" / "build_parliament_video_full_metadata_archive.py"
GAP_REPORT_PATH = (
    ROOT
    / "derived"
    / "parliament_video_full_metadata_archive"
    / "parliament_video_full_metadata_archive_gap_report.json"
)
RECORDS_PATH = (
    ROOT
    / "derived"
    / "parliament_video_full_metadata_archive"
    / "parliament_video_full_metadata_archive_records.jsonl"
)


class FullMetadataArchiveNotApprovedError(RuntimeError):
    """Raised when the archive is not configured for metadata-only operation."""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def require_full_metadata_archive_metadata_only(
    path: Path = MANIFEST_PATH,
    approval_code: str | None = None,
) -> dict[str, Any]:
    if not path.exists():
        raise FullMetadataArchiveNotApprovedError(
            "Full metadata archive manifest does not exist yet."
        )
    if approval_code != "approved":
        raise FullMetadataArchiveNotApprovedError(
            "Full metadata archive approval has not been granted."
        )
    manifest = _json(path)
    if manifest.get("policy", {}).get("no_media_download") is not True:
        raise FullMetadataArchiveNotApprovedError(
            "Full metadata archive must remain metadata-only."
        )
    return manifest


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if manifest.get("track_id") != "parliament_video_full_metadata_archive_20260705":
        failures.append("track_id must be parliament_video_full_metadata_archive_20260705.")
    if manifest.get("refresh_policy", {}).get("cadence") != "monthly":
        failures.append("refresh_policy.cadence must be monthly.")
    if manifest.get("refresh_policy", {}).get("snapshot_retention") != 12:
        failures.append("refresh_policy.snapshot_retention must be 12.")
    policy = manifest.get("policy", {})
    for key in (
        "metadata_first",
        "no_media_download",
        "no_video_file_download",
        "no_audio_file_download",
        "no_public_media_release",
        "no_completeness_claim",
        "rights_review_required_before_media_acquisition",
        "fallbacks_are_validation_only",
    ):
        if policy.get(key) is not True:
            failures.append(f"policy.{key} must be true.")
    archive = manifest.get("archive", {})
    for key in ("records_path", "snapshot_path", "gap_report_path", "snapshot_history_directory"):
        if key not in archive:
            failures.append(f"archive.{key} must be present.")
    if manifest.get("summary", {}).get("metadata_completeness_claim") is not False:
        failures.append("summary.metadata_completeness_claim must remain false.")
    if manifest.get("summary", {}).get("media_completeness_claim") is not False:
        failures.append("summary.media_completeness_claim must remain false.")
    if manifest.get("summary", {}).get("complete_video_archive") is not False:
        failures.append("summary.complete_video_archive must remain false.")
    if manifest.get("summary", {}).get("record_count", 0) < 16:
        failures.append("summary.record_count must be at least 16.")
    if manifest.get("summary", {}).get("approved_source_count", 0) < 9:
        failures.append("summary.approved_source_count must be at least 9.")
    if manifest.get("summary", {}).get("blocked_source_count", 0) < 1:
        failures.append("summary.blocked_source_count must be at least 1.")
    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        WORKFLOW_PATH,
        RUNNER_PATH,
        GAP_REPORT_PATH,
        RECORDS_PATH,
    ):
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

    failures.extend(_validate_manifest(manifest))

    doc_text = _read(DOC_PATH)
    for required in (
        "metadata-first archive",
        "monthly refresh",
        "normalized JSONL",
        "Gap Report",
        "cache policy",
        "No media download",
    ):
        if required not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    workflow_text = _read(WORKFLOW_PATH)
    for required in (
        "schedule:",
        "workflow_dispatch:",
        "build_parliament_video_full_metadata_archive.py",
        "upload-artifact",
    ):
        if required not in workflow_text:
            failures.append(f"{WORKFLOW_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    gap_report = _json(GAP_REPORT_PATH)
    if gap_report.get("track_id") != manifest.get("track_id"):
        failures.append("gap report track_id must match the manifest.")
    if gap_report.get("policy", {}).get("no_media_download") is not True:
        failures.append("gap report policy must stay metadata-only.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-FULL-METADATA-ARCHIVE: {failure}")
        return 1
    print("Parliament video full metadata archive is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
