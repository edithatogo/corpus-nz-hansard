"""Build the NZ Parliament video media-acquisition decision manifest."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_media_acquisition_decision.json"
DOC_PATH = ROOT / "docs" / "parliament-video-media-acquisition-decision.md"


RIGHTS_EVIDENCE = [
    {
        "source_id": "parliament-copyright-and-video-terms",
        "title": "Copyright - New Zealand Parliament",
        "url": "https://www3.parliament.nz/en/footer/copyright/",
        "access_status": "official-terms-review-complete",
        "implication": "Parliament TV footage is not licensed for reuse under the CC-BY notice and needs separate terms review.",
    },
    {
        "source_id": "parliament-tv-explained",
        "title": "The Parliament TV and Radio page explained",
        "url": "https://www3.parliament.nz/en/footer/website-help/the-parliament-tv-and-radio-page-explained/",
        "access_status": "official-help-review-complete",
        "implication": "Parliament Video and Parliament on Demand are distinct hosted surfaces with separate reuse constraints.",
    },
    {
        "source_id": "standing-orders-appendix-d",
        "title": "Appendix D: Coverage of proceedings",
        "url": "https://www3.parliament.nz/en/pb/parliamentary-rules/standing-orders-2020-by-chapter/appendix-d-coverage-of-proceedings/",
        "access_status": "official-terms-review-complete",
        "implication": "Official coverage is governed by Standing Orders conditions rather than blanket media reuse permission.",
    },
    {
        "source_id": "parliament-practice-official-coverage",
        "title": "Chapter 12 - Communicating and Engaging with Parliament",
        "url": "https://www3.parliament.nz/en/visit-and-learn/how-parliament-works/parliamentary-practice-in-new-zealand-2023-by-chapter/chapter-12-communicating-and-engaging-with-parliament/",
        "access_status": "official-practice-review-complete",
        "implication": "Official coverage is published under Parliamentary authority and remains subject to stated use conditions.",
    },
    {
        "source_id": "youtube-terms-of-service",
        "title": "Terms of Service - YouTube",
        "url": "https://www.youtube.com/static?template=terms",
        "access_status": "platform-terms-review-complete",
        "implication": "YouTube-hosted Parliament videos remain governed by YouTube platform terms and channel rights metadata.",
    },
    {
        "source_id": "vimeo-terms-of-service",
        "title": "Vimeo Terms of Service",
        "url": "https://vimeo.com/legal",
        "access_status": "platform-terms-review-complete",
        "implication": "Vimeo-era Parliament video surfaces remain governed by Vimeo terms and page-specific rights signals.",
    },
    {
        "source_id": "tvnz-footage-licensing",
        "title": "TVNZ Licensing footage request",
        "url": "https://licensing.tvnz.co.nz/footage-request-public-setting/",
        "access_status": "licensing-review-complete",
        "implication": "TVNZ footage is a separate rights channel and does not authorize blanket Parliament media acquisition.",
    },
    {
        "source_id": "ngataonga-collection-home",
        "title": "Ngā Taonga Sound & Vision",
        "url": "https://www.ngataonga.org.nz/",
        "access_status": "archive-access-review-complete",
        "implication": "Ngā Taonga is an adjacent archive reference, not an automatic acquisition or redistribution right.",
    },
    {
        "source_id": "archives-nz-audiovisual-reuse",
        "title": "Audiovisual collections - Archives New Zealand",
        "url": "https://www.archives.govt.nz/research-guidance/research-guides/audiovisual",
        "access_status": "reuse-review-complete",
        "implication": "Archives New Zealand reuse requires separate permission and source-specific clearance.",
    },
    {
        "source_id": "internet-archive-terms-of-use",
        "title": "Internet Archive's Terms of Use",
        "url": "https://archive.org/about/terms.php",
        "access_status": "web-archive-terms-review-complete",
        "implication": "Web-archive copies remain subject to archive.org terms and rights review before any media claim.",
    },
]


FALLBACK_RESOURCES = [
    {
        "resource_id": "parliament-website-video",
        "title": "Parliament website video and Parliament Video help pages",
        "url": "https://www3.parliament.nz/en/footer/website-help/the-parliament-tv-and-radio-page-explained/",
        "classification": "evidence-only",
    },
    {
        "resource_id": "youtube-parliament-channel",
        "title": "Official NZ Parliament YouTube channel",
        "url": "https://www.youtube.com/channel/UCuPya3mH6P9grNmgzmVdxoQ/videos",
        "classification": "evidence-only",
    },
    {
        "resource_id": "vimeo-era-links",
        "title": "Vimeo-era Parliament video links",
        "url": "https://vimeo.com/",
        "classification": "evidence-only",
    },
    {
        "resource_id": "tvnz-licensing",
        "title": "TVNZ Licensing",
        "url": "https://licensing.tvnz.co.nz/",
        "classification": "evidence-only",
    },
    {
        "resource_id": "nga-taonga",
        "title": "Ngā Taonga Sound & Vision",
        "url": "https://www.ngataonga.org.nz/",
        "classification": "evidence-only",
    },
    {
        "resource_id": "internet-archive",
        "title": "Internet Archive",
        "url": "https://archive.org/",
        "classification": "evidence-only",
    },
]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_manifest(generated_at: str) -> dict[str, object]:
    return {
        "manifest_version": 1,
        "track_id": "parliament_video_media_acquisition_decision_20260705",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "decision_scope": "media acquisition",
        "decision_state": "excluded",
        "decision_summary": "Parliament video and audio media acquisition is not approved; metadata-only archival remains the release posture.",
        "policy": {
            "metadata_first": True,
            "no_media_download": True,
            "no_video_file_download": True,
            "no_audio_file_download": True,
            "no_public_media_release": True,
            "no_private_media_archive": True,
            "rights_review_required_before_media_acquisition": True,
        },
        "media": {
            "metadata": "allowed",
            "captions": "excluded",
            "transcripts": "excluded",
            "thumbnails": "excluded",
            "audio": "excluded",
            "video": "excluded",
            "page_snapshots": "excluded",
        },
        "guard": {
            "media_download_allowed": False,
            "approved_states": ["private preservation only", "public release"],
            "blocked_state": "excluded",
        },
        "rights_evidence": RIGHTS_EVIDENCE,
        "fallback_resources": FALLBACK_RESOURCES,
        "review_notes": [
            {
                "source_id": "rnz-reuse-terms-review",
                "status": "review_pending",
                "note": "RNZ official reuse guidance should be checked before any future approval; direct retrieval was not reliable in this run.",
            }
        ],
        "notes": [
            "Metadata-only archival is the supported posture in this track.",
            "No downloader may assume media approval without an explicit later decision state.",
            "Fallback resources stay evidence-only until a later rights decision approves a different posture.",
        ],
    }


def write_doc(manifest: dict[str, object]) -> None:
    evidence_rows = "\n".join(
        f"| `{item['source_id']}` | {item['title']} | {item['access_status']} |"
        for item in manifest["rights_evidence"]  # type: ignore[index]
    )
    media_rows = "\n".join(
        f"| `{media_type}` | {status} |"
        for media_type, status in manifest["media"].items()  # type: ignore[union-attr]
    )
    fallback_rows = "\n".join(
        f"| `{item['resource_id']}` | {item['title']} | {item['classification']} |"
        for item in manifest["fallback_resources"]  # type: ignore[index]
    )
    DOC_PATH.write_text(
        f"""# Parliament Video Media Acquisition Decision

Release posture: metadata-only, no media download.

This track records the decision gate that keeps Parliament video/audio acquisition blocked. The current decision state is `excluded`, so no downloader may run unless a later approved state is recorded and validated.
Parliament video media acquisition is not approved.

## Decision

- Decision scope: media acquisition
- Decision state: excluded
- Media download: disabled
- Public media release: disabled
- Private preservation: not approved

## Media Rights Split

| Media type | Status |
| --- | --- |
{media_rows}

## Rights Evidence

| Source | Title | Access status |
| --- | --- | --- |
{evidence_rows}

## Fallback Resources

Fallback resources are evidence-only in this track. They cannot be used for acquisition unless a later rights decision explicitly approves them.

| Resource | Title | Classification |
| --- | --- | --- |
{fallback_rows}

## Review Notes

- RNZ reuse guidance remains a follow-up item because official retrieval was not reliable in this run.
- The guard remains metadata-first and blocks media acquisition until a later approved state exists.

## Guard

The repo gate is implemented by `scripts/check_parliament_video_media_acquisition_decision.py`. It blocks any media acquisition path until the manifest records `private preservation only` or `public release`.
""",
        encoding="utf-8",
    )


def main() -> None:
    generated_at = datetime.now(UTC).date().isoformat()
    manifest = build_manifest(generated_at)
    write_json(MANIFEST_PATH, manifest)
    write_doc(manifest)


if __name__ == "__main__":
    main()
