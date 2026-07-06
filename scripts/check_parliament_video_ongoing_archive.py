"""Validate the NZ Parliament video ongoing archive contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_ongoing_archive.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_ongoing_archive.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-ongoing-archive.md"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "parliament-video-ongoing-archive.yml"
RUNNER_PATH = ROOT / "scripts" / "build_parliament_video_ongoing_archive.py"
MEDIA_DECISION_PATH = ROOT / "manifests" / "parliament_video_media_acquisition_decision.json"


class OngoingArchiveNotApprovedError(RuntimeError):
    """Raised when the ongoing archive is not configured for metadata-only operation."""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def require_ongoing_archive_metadata_only(
    path: Path = MANIFEST_PATH,
    approval_code: str | None = None,
) -> dict[str, Any]:
    if not path.exists():
        raise OngoingArchiveNotApprovedError("Ongoing archive manifest does not exist yet.")
    if approval_code != "approved":
        raise OngoingArchiveNotApprovedError("Ongoing archive approval has not been granted.")
    manifest = _json(path)
    if manifest.get("policy", {}).get("no_media_download") is not True:
        raise OngoingArchiveNotApprovedError("Ongoing archive must remain metadata-only.")
    return manifest


def _validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if manifest.get("track_id") != "parliament_video_ongoing_archive_20260705":
        failures.append("track_id must be parliament_video_ongoing_archive_20260705.")
    if manifest.get("refresh_policy", {}).get("cadence") != "weekly":
        failures.append("refresh_policy.cadence must be weekly.")
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
    if (
        manifest.get("workflow", {}).get("path")
        != ".github/workflows/parliament-video-ongoing-archive.yml"
    ):
        failures.append("workflow.path must target the ongoing archive workflow.")
    if manifest.get("media_acquisition_decision_state") != "excluded":
        failures.append("media acquisition decision must remain excluded.")
    if manifest.get("summary", {}).get("no_media_download") is not True:
        failures.append("summary.no_media_download must be true.")
    if manifest.get("change_summary", {}).get("new_source_count") is None:
        failures.append("change_summary.new_source_count must exist.")
    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        WORKFLOW_PATH,
        RUNNER_PATH,
        MEDIA_DECISION_PATH,
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
        "scheduled metadata refresh",
        "gap monitoring",
        "no-download guard",
        "Snapshot retention",
        "No media download",
    ):
        if required not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    workflow_text = _read(WORKFLOW_PATH)
    for required in (
        "schedule:",
        "workflow_dispatch:",
        "build_parliament_video_ongoing_archive.py",
        "upload-artifact",
    ):
        if required not in workflow_text:
            failures.append(f"{WORKFLOW_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-ONGOING-ARCHIVE: {failure}")
        return 1
    print("Parliament video ongoing archive is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
