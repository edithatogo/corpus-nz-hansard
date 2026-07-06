"""Validate the Parliament video media-acquisition decision gate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_media_acquisition_decision.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_media_acquisition_decision.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-media-acquisition-decision.md"

APPROVED_MEDIA_STATES = {"private preservation only", "public release"}
REQUIRED_EVIDENCE_IDS = {
    "parliament-copyright-and-video-terms",
    "parliament-tv-explained",
    "standing-orders-appendix-d",
    "parliament-practice-official-coverage",
    "youtube-terms-of-service",
    "vimeo-terms-of-service",
    "tvnz-footage-licensing",
    "ngataonga-collection-home",
    "archives-nz-audiovisual-reuse",
    "internet-archive-terms-of-use",
}

REQUIRED_DOC_SNIPPETS = (
    "metadata-only, no media download",
    "Decision state: excluded",
    "Fallback resources are evidence-only",
    "scripts/check_parliament_video_media_acquisition_decision.py",
)


class MediaAcquisitionNotApprovedError(RuntimeError):
    """Raised when a media downloader runs before an approved decision exists."""


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for field in (
        "manifest_version",
        "track_id",
        "repository",
        "generated_at",
        "decision_scope",
        "decision_state",
        "decision_summary",
        "policy",
        "media",
        "guard",
        "rights_evidence",
        "fallback_resources",
        "review_notes",
        "notes",
    ):
        if field not in manifest:
            failures.append(f"missing required field: {field}")
    if failures:
        return failures

    if manifest["track_id"] != "parliament_video_media_acquisition_decision_20260705":
        failures.append("track_id must be parliament_video_media_acquisition_decision_20260705.")
    if manifest["decision_scope"] != "media acquisition":
        failures.append("decision_scope must be media acquisition.")
    if manifest["decision_state"] != "excluded":
        failures.append("decision_state must be excluded until a later approval exists.")

    policy = manifest["policy"]
    for key in (
        "metadata_first",
        "no_media_download",
        "no_video_file_download",
        "no_audio_file_download",
        "no_public_media_release",
        "no_private_media_archive",
        "rights_review_required_before_media_acquisition",
    ):
        if policy.get(key) is not True:
            failures.append(f"policy.{key} must be true.")

    media = manifest["media"]
    if media.get("metadata") != "allowed":
        failures.append("media.metadata must be allowed.")
    for media_type in ("captions", "transcripts", "thumbnails", "audio", "video", "page_snapshots"):
        if media.get(media_type) != "excluded":
            failures.append(f"media.{media_type} must be excluded.")

    guard = manifest["guard"]
    if guard.get("media_download_allowed") is not False:
        failures.append("guard.media_download_allowed must be false.")
    if set(guard.get("approved_states", [])) != APPROVED_MEDIA_STATES:
        failures.append("guard.approved_states must list the approved media states only.")
    if guard.get("blocked_state") != "excluded":
        failures.append("guard.blocked_state must be excluded.")

    evidence_ids = {item.get("source_id") for item in manifest["rights_evidence"]}
    missing_evidence = REQUIRED_EVIDENCE_IDS - evidence_ids
    if missing_evidence:
        failures.append("missing rights evidence: " + ", ".join(sorted(missing_evidence)))

    fallback_resources = manifest["fallback_resources"]
    for resource in fallback_resources:
        if resource.get("classification") != "evidence-only":
            failures.append(
                f"{resource.get('resource_id')} fallback resource must be evidence-only."
            )

    review_notes = manifest["review_notes"]
    if not any(item.get("source_id") == "rnz-reuse-terms-review" for item in review_notes):
        failures.append("review_notes must record the RNZ follow-up item.")

    return failures


def require_media_acquisition_approval(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    if not path.exists():
        raise MediaAcquisitionNotApprovedError(
            "Media acquisition is not approved; the decision manifest does not exist yet."
        )
    manifest = _json(path)
    if manifest.get("decision_state") not in APPROVED_MEDIA_STATES:
        raise MediaAcquisitionNotApprovedError(
            f"Media acquisition is not approved; current decision_state={manifest.get('decision_state')!r}."
        )
    return manifest


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH):
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

    failures.extend(validate_manifest(manifest))

    doc_text = _read(DOC_PATH)
    for snippet in REQUIRED_DOC_SNIPPETS:
        if snippet not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {snippet}")

    if "Parliament video media acquisition is not approved." not in doc_text:
        failures.append(
            f"{DOC_PATH.relative_to(ROOT).as_posix()} must state the decision is not approved."
        )

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-VIDEO-MEDIA-DECISION: {failure}")
        return 1
    print("Parliament video media-acquisition decision is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
