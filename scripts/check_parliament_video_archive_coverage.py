"""Validate the NZ Parliament video archive coverage ledger."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_archive_coverage.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_archive_coverage.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-archive-coverage.md"
TRACK_PATHS = (
    ROOT / "conductor" / "tracks" / "parliament_video_archive_coverage_20260705",
    ROOT / "conductor" / "archive" / "parliament_video_archive_coverage_20260705",
)

REQUIRED_SURFACES = {
    "official-youtube-nz-parliament",
    "parliament-videos-current",
    "parliament-on-demand-previous",
    "select-committee-video-archive",
    "select-committee-live-stream-links",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if not any(path.exists() for path in TRACK_PATHS):
        failures.append(
            "conductor track or archive folder for parliament_video_archive_coverage_20260705 must exist."
        )
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    policy = manifest["policy"]
    for key in (
        "metadata_first",
        "no_video_file_download",
        "no_public_release",
        "no_completeness_claim",
        "rights_review_required_before_media_acquisition",
    ):
        if policy.get(key) is not True:
            failures.append(f"policy.{key} must be true.")

    summary = manifest["summary"]
    for key in (
        "retrospective_archive_complete",
        "ongoing_archive_complete",
        "complete_video_archive",
    ):
        if summary.get(key) is not False:
            failures.append(f"summary.{key} must remain false.")

    surface_ids = {surface["surface_id"] for surface in manifest["surfaces"]}
    missing_surfaces = REQUIRED_SURFACES - surface_ids
    if missing_surfaces:
        failures.append("missing video surfaces: " + ", ".join(sorted(missing_surfaces)))

    for surface in manifest["surfaces"]:
        if (
            surface["local_status"] == "external-only"
            and "review-required" not in surface["rights_boundary"]
        ):
            failures.append(
                f"{surface['surface_id']} external-only surface must remain rights gated."
            )

    repo_status = {
        repo["repo"]: repo["video_archive_status"] for repo in manifest["adjacent_repo_findings"]
    }
    if repo_status.get("sm-govt-nz") != "metadata-only":
        failures.append("sm-govt-nz must be recorded as metadata-only, not complete video archive.")
    for repo in ("hathi-nz", "corpus-law-nz"):
        if repo_status.get(repo) != "not-applicable":
            failures.append(f"{repo} must remain not-applicable for Parliament video coverage.")

    doc_text = _read(DOC_PATH)
    for required in (
        "does not have a complete archive",
        "Retrospective coverage is not complete",
        "ongoing coverage is not complete",
        "No video-file download",
        "sm-govt-nz",
    ):
        if required not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-COVERAGE: {failure}")
        return 1
    print("Parliament video archive coverage ledger is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
