"""Build the NZ Parliament video archive coverage ledger."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_archive_coverage.json"
DOC_PATH = ROOT / "docs" / "parliament-video-archive-coverage.md"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_manifest(generated_at: str) -> dict[str, object]:
    surfaces = [
        {
            "surface_id": "official-youtube-nz-parliament",
            "title": "Official NZ Parliament YouTube channel",
            "url": "https://www.youtube.com/channel/UCuPya3mH6P9grNmgzmVdxoQ/videos",
            "coverage_period": "Public channel videos; local completeness not established.",
            "local_status": "not-archived",
            "rights_boundary": "third-party-platform-terms-review-required",
        },
        {
            "surface_id": "parliament-videos-current",
            "title": "Parliament website video platform",
            "url": "https://videos.parliament.nz/",
            "coverage_period": "54th Parliament onward according to Parliament website help.",
            "local_status": "metadata-inventory-only",
            "rights_boundary": "media-rights-review-required",
        },
        {
            "surface_id": "parliament-on-demand-previous",
            "title": "Previous Parliament On Demand site",
            "url": "https://ondemand.parliament.nz/",
            "coverage_period": "53rd Parliament and earlier according to Parliament website help.",
            "local_status": "external-only",
            "rights_boundary": "media-rights-review-required",
        },
        {
            "surface_id": "select-committee-video-archive",
            "title": "Select committee video archive",
            "url": "https://ondemand.parliament.nz/select-committees",
            "coverage_period": "Select committee archive, including 2018-2023 references.",
            "local_status": "external-only",
            "rights_boundary": "media-rights-review-required",
        },
        {
            "surface_id": "select-committee-live-stream-links",
            "title": "Select committee live stream links",
            "url": "https://www.parliament.nz/en/pb/sc/watch-select-committee-live-streams/",
            "coverage_period": "Current and historical live-stream link surface, including Vimeo-era links.",
            "local_status": "external-only",
            "rights_boundary": "third-party-platform-terms-review-required",
        },
    ]
    return {
        "manifest_version": 1,
        "track_id": "parliament_video_archive_coverage_20260705",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "coverage_status": "not-complete",
        "policy": {
            "metadata_first": True,
            "no_video_file_download": True,
            "no_public_release": True,
            "no_completeness_claim": True,
            "rights_review_required_before_media_acquisition": True,
        },
        "summary": {
            "surface_count": len(surfaces),
            "retrospective_archive_complete": False,
            "ongoing_archive_complete": False,
            "complete_video_archive": False,
        },
        "surfaces": surfaces,
        "adjacent_repo_findings": [
            {
                "repo": "sm-govt-nz",
                "video_archive_status": "metadata-only",
                "finding": "General NZ government YouTube metadata archival exists, but local evidence did not show a complete official NZ Parliament YouTube or Parliament website video archive.",
                "evidence": "../sm-govt-nz/conductor/youtube_archive_summary.md and ../sm-govt-nz/conductor/govt_archive_readiness_matrix.json",
            },
            {
                "repo": "hathi-nz",
                "video_archive_status": "not-applicable",
                "finding": "HathiTrust-side work covers historical print/OCR evidence, not Parliament video.",
                "evidence": "../hathi-nz/manifests/hathitrust-nz/nz_parliamentary_debates_hansard.json",
            },
            {
                "repo": "corpus-law-nz",
                "video_archive_status": "not-applicable",
                "finding": "Legislation and Gazette boundaries are adjacent but do not provide Parliament video coverage.",
                "evidence": "../corpus-law-nz/docs/shared_nz_corpus_core_schema.md",
            },
        ],
        "next_actions": [
            "Create a metadata-only seed fetcher for the official NZ Parliament YouTube channel.",
            "Create metadata probes for videos.parliament.nz and the previous On Demand site.",
            "Inventory select committee archive and Vimeo-era links before any media-file acquisition decision.",
            "Run a rights review before video download, transcript extraction, or public media publication.",
        ],
    }


def write_doc(manifest: dict[str, object]) -> None:
    surface_rows = "\n".join(
        f"| `{surface['surface_id']}` | {surface['title']} | {surface['local_status']} | {surface['coverage_period']} |"
        for surface in manifest["surfaces"]  # type: ignore[index]
    )
    DOC_PATH.write_text(
        f"""# Parliament Video Archive Coverage

Release posture: metadata-first coverage ledger.

This repo does not have a complete archive of NZ Parliament videos. Retrospective coverage is not complete, ongoing coverage is not complete, and adjacent repos do not provide a complete substitute.

## Policy

- Metadata-first only.
- No video-file download in this track.
- No public release claim for video or media-derived text.
- No completeness claim.
- Rights review required before media acquisition.

## Surfaces

| Surface | Title | Local status | Coverage period |
| --- | --- | --- | --- |
{surface_rows}

## Adjacent Repos

- `sm-govt-nz` has general NZ government YouTube metadata archival, but it is metadata-only and not evidence of complete NZ Parliament video coverage.
- `hathi-nz` is print/OCR evidence, not video.
- `corpus-law-nz` is the legislation/Gazette boundary, not video.

## Next Actions

{chr(10).join(f"- {action}" for action in manifest["next_actions"])}  # type: ignore[index]
""",
        encoding="utf-8",
    )


def main() -> None:
    generated_at = datetime.now(UTC).replace(microsecond=0).date().isoformat()
    manifest = build_manifest(generated_at)
    write_json(MANIFEST_PATH, manifest)
    write_doc(manifest)


if __name__ == "__main__":
    main()
