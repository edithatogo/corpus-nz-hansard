"""Build the NZ Parliament video source inventory."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"
DOC_PATH = ROOT / "docs" / "parliament-video-source-inventory.md"


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _official_source(
    source_id: str,
    title: str,
    url: str,
    *,
    platform: str,
    date_range: str,
    source_family: str,
    metadata_availability: str,
    evidence: list[str],
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "title": title,
        "url": url,
        "publisher": "New Zealand Parliament",
        "source_family": source_family,
        "platform_class": platform,
        "source_role": "official",
        "fallback_role": "not_fallback",
        "archive_status": "external_source_identified",
        "expected_date_range": date_range,
        "access_method": "metadata_probe_required",
        "rights_status": "rights_review_required",
        "media_types": ["video", "audio", "metadata"],
        "metadata_availability": metadata_availability,
        "evidence_urls": evidence,
        "known_blockers": blockers or ["no local inventory count yet"],
        "acquisition_boundary": "metadata_only_no_media_download",
    }


def _fallback_source(
    source_id: str,
    title: str,
    url: str,
    *,
    publisher: str,
    source_family: str,
    fallback_role: str,
    platform: str,
    evidence: list[str],
    metadata_availability: str = "catalogue_or_page_metadata",
    rights_status: str = "fallback_rights_review_required",
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "title": title,
        "url": url,
        "publisher": publisher,
        "source_family": source_family,
        "platform_class": platform,
        "source_role": "fallback",
        "fallback_role": fallback_role,
        "archive_status": "fallback_evidence_only",
        "expected_date_range": "Evidence range to be determined by later metadata probes.",
        "access_method": "metadata_or_catalogue_probe_required",
        "rights_status": rights_status,
        "media_types": ["metadata"],
        "metadata_availability": metadata_availability,
        "evidence_urls": evidence,
        "known_blockers": ["not an official Parliament acquisition source"],
        "acquisition_boundary": "validation_only_no_media_download",
    }


def _adjacent_repo_source(source_id: str, repo: str, role: str, evidence: str) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "title": f"Adjacent repo evidence: {repo}",
        "url": evidence,
        "publisher": repo,
        "source_family": "adjacent_repo_evidence",
        "platform_class": "repository",
        "source_role": "supporting",
        "fallback_role": "boundary_evidence",
        "archive_status": "supporting_evidence_only",
        "expected_date_range": "Repo-local evidence only; not a Parliament video source range.",
        "access_method": "repository_manifest_review",
        "rights_status": "not_media_source",
        "media_types": ["metadata"],
        "metadata_availability": role,
        "evidence_urls": [evidence],
        "known_blockers": ["does not provide a full NZ Parliament video archive"],
        "acquisition_boundary": "evidence_only_no_media_download",
    }


def build_manifest(generated_at: str) -> dict[str, Any]:
    taxonomy = {
        "source_families": [
            "house_video",
            "select_committee_video",
            "parliament_website_embeds",
            "social_video_platform",
            "broadcast_archive",
            "audio_reporting",
            "web_archive",
            "adjacent_repo_evidence",
        ],
        "platform_classes": [
            "official_parliament_video",
            "official_parliament_website",
            "youtube",
            "vimeo",
            "parliament_on_demand",
            "broadcast_catalogue",
            "audio_reporting",
            "web_archive",
            "repository",
            "search_or_sitemap",
        ],
        "fallback_roles": [
            "not_fallback",
            "historical_broadcast_validation",
            "catalogue_validation",
            "audio_or_reporting_validation",
            "link_rot_validation",
            "boundary_evidence",
        ],
        "rights_statuses": [
            "rights_review_required",
            "platform_terms_review_required",
            "fallback_rights_review_required",
            "web_archive_rights_review_required",
            "not_media_source",
        ],
        "archive_statuses": [
            "external_source_identified",
            "fallback_evidence_only",
            "supporting_evidence_only",
            "blocked_or_unknown",
        ],
    }
    sources = [
        _official_source(
            "official-parliament-video",
            "Official Parliament Video platform",
            "https://videos.parliament.nz/",
            platform="official_parliament_video",
            date_range="Current Parliament video platform; exact start date to be probed.",
            source_family="house_video",
            metadata_availability="video page metadata, search metadata, and possible API responses",
            evidence=["https://videos.parliament.nz/"],
        ),
        _official_source(
            "official-parliament-live-and-recorded",
            "Parliament website live and recorded video surface",
            "https://www.parliament.nz/",
            platform="official_parliament_website",
            date_range="Current Parliament website navigation and Parliament in action video links.",
            source_family="house_video",
            metadata_availability="site navigation, live video links, and recorded-video links",
            evidence=["https://www.parliament.nz/"],
        ),
        _official_source(
            "official-youtube-nz-parliament",
            "Official NZ Parliament YouTube channel",
            "https://www.youtube.com/channel/UCuPya3mH6P9grNmgzmVdxoQ/videos",
            platform="youtube",
            date_range="Public channel video range; exact earliest upload to be probed.",
            source_family="social_video_platform",
            metadata_availability="channel, playlist, video, livestream, and upload metadata",
            evidence=["https://www.youtube.com/channel/UCuPya3mH6P9grNmgzmVdxoQ"],
            blockers=["YouTube API quota or page access constraints"],
        ),
        _official_source(
            "parliament-on-demand-house-archive",
            "Parliament On Demand house video archive",
            "https://ondemand.parliament.nz/",
            platform="parliament_on_demand",
            date_range="House live and on-demand handoff surface; previous site redirects current viewing to Parliament Video.",
            source_family="house_video",
            metadata_availability="legacy page metadata and handoff links",
            evidence=["https://ondemand.parliament.nz/"],
        ),
        _official_source(
            "select-committee-on-demand-archive",
            "Select Committees On Demand archive",
            "https://ondemand.parliament.nz/select-committees",
            platform="parliament_on_demand",
            date_range="52nd and 53rd Parliament select committee videos according to the archive page.",
            source_family="select_committee_video",
            metadata_availability="filterable committee/date/parliament metadata",
            evidence=["https://ondemand.parliament.nz/select-committees"],
        ),
        _official_source(
            "select-committee-live-streams-current",
            "Current select committee livestream pages",
            "https://www3.parliament.nz/en/pb/sc/watch-select-committee-live-streams/",
            platform="official_parliament_website",
            date_range="Current 54th Parliament select committee livestream and archive links.",
            source_family="select_committee_video",
            metadata_availability="committee livestream pages and linked archive pages",
            evidence=["https://www3.parliament.nz/en/pb/sc/watch-select-committee-live-streams/"],
        ),
        _official_source(
            "select-committee-vimeo-pages",
            "Vimeo pages linked from select committee livestream pages",
            "https://www3.parliament.nz/en/pb/sc/watch-select-committee-live-streams/",
            platform="vimeo",
            date_range="Committee videos linked from current committee pages; pre-August 2023 handoff goes to On Demand archive.",
            source_family="select_committee_video",
            metadata_availability="Vimeo page metadata linked from Parliament pages",
            evidence=["https://www3.parliament.nz/en/pb/sc/watch-select-committee-live-streams/"],
            blockers=["some pre-29 January 2024 videos may miss hearing information"],
        ),
        _official_source(
            "parliament-website-embedded-video-pages",
            "Embedded Parliament website video pages",
            "https://www3.parliament.nz/en/get-involved/features/",
            platform="official_parliament_website",
            date_range="Feature and information pages with embedded or linked video content.",
            source_family="parliament_website_embeds",
            metadata_availability="page metadata and embedded-player references",
            evidence=[
                "https://www3.parliament.nz/mi/get-involved/features/parliament-on-demand-nz-parliament-s-new-home-of-video-content/"
            ],
        ),
        _official_source(
            "parliament-site-search-and-sitemaps",
            "Parliament website search, sitemap, and feed discovery",
            "https://www.parliament.nz/",
            platform="search_or_sitemap",
            date_range="Discovery surface for video pages; range follows indexed Parliament website content.",
            source_family="parliament_website_embeds",
            metadata_availability="search result metadata, sitemap URLs, and page discovery metadata",
            evidence=["https://www.parliament.nz/"],
            blockers=["search result coverage and sitemap format to be verified by seed fetchers"],
        ),
        _fallback_source(
            "tvnz-archive-looking-back",
            "TVNZ Archive / Looking Back historical footage references",
            "https://www3.parliament.nz/mi/get-involved/features/parliament-on-demand-nz-parliament-s-new-home-of-video-content/",
            publisher="TVNZ Archive / New Zealand Parliament",
            source_family="broadcast_archive",
            fallback_role="historical_broadcast_validation",
            platform="broadcast_catalogue",
            evidence=[
                "https://www3.parliament.nz/mi/get-involved/features/parliament-on-demand-nz-parliament-s-new-home-of-video-content/"
            ],
        ),
        _fallback_source(
            "nga-taonga-av-collection",
            "Nga Taonga Sound & Vision audiovisual collection search",
            "https://www.ngataonga.org.nz/search-use-collection/search/",
            publisher="Nga Taonga Sound & Vision",
            source_family="broadcast_archive",
            fallback_role="catalogue_validation",
            platform="broadcast_catalogue",
            evidence=["https://www.ngataonga.org.nz/search-use-collection/search/"],
        ),
        _fallback_source(
            "rnz-parliament",
            "RNZ Parliament reporting and audio evidence",
            "https://www.rnz.co.nz/parliament",
            publisher="RNZ",
            source_family="audio_reporting",
            fallback_role="audio_or_reporting_validation",
            platform="audio_reporting",
            evidence=["https://www.rnz.co.nz/parliament"],
        ),
        _fallback_source(
            "parliament-today-am-network",
            "Parliament Today and AM Network broadcast references",
            "http://parliamenttoday.co.nz/",
            publisher="Parliament Today / AM Network",
            source_family="audio_reporting",
            fallback_role="audio_or_reporting_validation",
            platform="audio_reporting",
            evidence=["http://parliamenttoday.co.nz/"],
        ),
        _fallback_source(
            "archives-new-zealand-av-catalogue",
            "Archives New Zealand audiovisual catalogue evidence",
            "https://collections.archives.govt.nz/",
            publisher="Archives New Zealand",
            source_family="broadcast_archive",
            fallback_role="catalogue_validation",
            platform="broadcast_catalogue",
            evidence=["https://collections.archives.govt.nz/"],
        ),
        _fallback_source(
            "internet-archive-webcaptures",
            "Internet Archive web captures for Parliament video URLs",
            "https://web.archive.org/",
            publisher="Internet Archive",
            source_family="web_archive",
            fallback_role="link_rot_validation",
            platform="web_archive",
            evidence=["https://web.archive.org/"],
            rights_status="web_archive_rights_review_required",
        ),
        _fallback_source(
            "memento-cdx-web-archives",
            "Memento/CDX web-archive discovery",
            "https://web.archive.org/cdx",
            publisher="Web archives",
            source_family="web_archive",
            fallback_role="link_rot_validation",
            platform="web_archive",
            evidence=["https://web.archive.org/cdx"],
            rights_status="web_archive_rights_review_required",
        ),
        _adjacent_repo_source(
            "adjacent-sm-govt-nz",
            "sm-govt-nz",
            "General NZ government YouTube metadata, not a Parliament video archive.",
            "../sm-govt-nz/",
        ),
        _adjacent_repo_source(
            "adjacent-hathi-nz",
            "hathi-nz",
            "Historical print/OCR evidence only; no Parliament video coverage.",
            "../hathi-nz/",
        ),
        _adjacent_repo_source(
            "adjacent-corpus-law-nz",
            "corpus-law-nz",
            "Legislation and Gazette boundary only; no Parliament video coverage.",
            "../corpus-law-nz/",
        ),
    ]
    family_coverage = {
        family: {
            "primary_source_ids": [
                source["source_id"]
                for source in sources
                if source["source_family"] == family and source["source_role"] == "official"
            ],
            "fallback_source_ids": [
                source["source_id"]
                for source in sources
                if source["source_family"] == family and source["source_role"] == "fallback"
            ],
            "completion_claim": "inventory-only-no-completeness-claim",
        }
        for family in taxonomy["source_families"]
    }
    return {
        "manifest_version": 1,
        "track_id": "parliament_video_source_inventory_20260705",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "inventory_status": "source-inventory",
        "policy": {
            "metadata_first": True,
            "no_media_download": True,
            "no_video_file_download": True,
            "no_audio_file_download": True,
            "no_public_media_release": True,
            "no_completeness_claim": True,
            "fallbacks_are_validation_only": True,
            "rights_review_required_before_media_acquisition": True,
        },
        "taxonomy": taxonomy,
        "sources": sources,
        "family_coverage": family_coverage,
        "next_track": "parliament_video_seed_fetchers_20260705",
    }


def write_doc(manifest: dict[str, Any]) -> None:
    rows = "\n".join(
        "| `{source_id}` | {title} | {source_role} | {fallback_role} | {archive_status} |".format(
            **source
        )
        for source in manifest["sources"]
    )
    fallback_rows = "\n".join(
        f"- `{source['source_id']}`: {source['fallback_role']} ({source['publisher']})"
        for source in manifest["sources"]
        if source["source_role"] == "fallback"
    )
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(
        f"""# Parliament Video Source Inventory

Release posture: metadata-first/no-download source inventory.

This inventory records public NZ Parliament video source surfaces and validation fallbacks. It is an input to `parliament_video_seed_fetchers_20260705`; it is not a media archive and does not claim retrospective or ongoing completeness.

## Policy

- Metadata-first only.
- No media download, including video or audio files.
- No public media release.
- No completeness claim.
- Fallback resources are validation-only until a later rights decision says otherwise.
- Rights review is required before any media acquisition.

## Taxonomy

- Source families: {", ".join(manifest["taxonomy"]["source_families"])}
- Platform classes: {", ".join(manifest["taxonomy"]["platform_classes"])}
- Fallback roles: {", ".join(manifest["taxonomy"]["fallback_roles"])}
- Rights statuses: {", ".join(manifest["taxonomy"]["rights_statuses"])}
- Archive statuses: {", ".join(manifest["taxonomy"]["archive_statuses"])}

## Source Inventory

| Source ID | Title | Role | Fallback role | Archive status |
| --- | --- | --- | --- | --- |
{rows}

## Fallback Resources

{fallback_rows}

## Adjacent Repo Boundaries

- `sm-govt-nz` can provide general NZ government YouTube metadata evidence, but not a complete Parliament video archive.
- `hathi-nz` is relevant to historical print/OCR evidence, not Parliament video.
- `corpus-law-nz` is the legislation/Gazette boundary and does not provide Parliament video coverage.

## Handoff

The next track must use this manifest to select bounded seed targets, preserve the no-download policy, record source-specific blocked states, and keep fallback resources separate from official acquisition sources.
""",
        encoding="utf-8",
    )


def main() -> None:
    generated_at = datetime.now(UTC).replace(microsecond=0).date().isoformat()
    manifest = build_manifest(generated_at)
    _write_json(MANIFEST_PATH, manifest)
    write_doc(manifest)


if __name__ == "__main__":
    main()
