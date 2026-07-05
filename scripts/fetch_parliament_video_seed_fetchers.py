"""Fetch bounded seed evidence for NZ Parliament video surfaces."""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.http_retry import request_with_retries  # noqa: E402

INVENTORY_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_seed_fetchers.json"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_seed_fetchers.schema.json"
DOC_PATH = ROOT / "docs" / "parliament-video-seed-fetchers.md"
OUTPUT_DIR = ROOT / "derived" / "parliament_video_seed_fetchers"

TARGET_BLUEPRINTS = (
    {
        "source_id": "official-parliament-video",
        "sample_patterns": ("videos.parliament.nz", "watch", "video"),
        "proof_role": "official-video-platform",
    },
    {
        "source_id": "official-parliament-live-and-recorded",
        "sample_patterns": ("watch", "video", "live"),
        "proof_role": "official-website-video",
    },
    {
        "source_id": "official-youtube-nz-parliament",
        "sample_patterns": ("watch", "youtube", "video", "live"),
        "proof_role": "official-youtube-channel",
    },
    {
        "source_id": "parliament-on-demand-house-archive",
        "sample_patterns": ("on-demand", "video", "house"),
        "proof_role": "legacy-house-archive",
    },
    {
        "source_id": "select-committee-on-demand-archive",
        "sample_patterns": ("select-committee", "committee", "video"),
        "proof_role": "select-committee-archive",
    },
    {
        "source_id": "select-committee-live-streams-current",
        "sample_patterns": ("vimeo", "committee", "stream"),
        "proof_role": "current-committee-streams",
    },
    {
        "source_id": "select-committee-vimeo-pages",
        "sample_patterns": ("vimeo", "committee", "video"),
        "proof_role": "vimeo-era-committee-pages",
    },
    {
        "source_id": "parliament-website-embedded-video-pages",
        "sample_patterns": ("features", "video", "embed"),
        "proof_role": "embedded-website-video",
    },
    {
        "source_id": "parliament-site-search-and-sitemaps",
        "sample_patterns": ("sitemap", "search", "video"),
        "proof_role": "site-discovery",
    },
    {
        "source_id": "tvnz-archive-looking-back",
        "sample_patterns": ("looking-back", "tvnz", "archive"),
        "proof_role": "historical-broadcast-validation",
    },
    {
        "source_id": "nga-taonga-av-collection",
        "sample_patterns": ("ngataonga", "search", "collection"),
        "proof_role": "catalogue-validation",
    },
    {
        "source_id": "rnz-parliament",
        "sample_patterns": ("rnz", "parliament"),
        "proof_role": "audio-or-reporting-validation",
    },
    {
        "source_id": "parliament-today-am-network",
        "sample_patterns": ("parliamenttoday", "am-network"),
        "proof_role": "audio-or-reporting-validation",
    },
    {
        "source_id": "archives-new-zealand-av-catalogue",
        "sample_patterns": ("archives", "catalogue", "video"),
        "proof_role": "catalogue-validation",
    },
    {
        "source_id": "internet-archive-webcaptures",
        "sample_patterns": ("web.archive.org", "archive", "parliament"),
        "proof_role": "link-rot-validation",
    },
    {
        "source_id": "memento-cdx-web-archives",
        "sample_patterns": ("cdx", "memento", "archive"),
        "proof_role": "link-rot-validation",
    },
)


@dataclass(frozen=True, slots=True)
class SeedTarget:
    """A single bounded seed-fetch target."""

    source_id: str
    title: str
    source_family: str
    source_role: str
    source_classification: str
    index_url: str
    access_constraints: str
    proof_role: str
    max_requests: int = 2
    sample_url: str | None = None
    sample_patterns: tuple[str, ...] = ()
    rights_status: str = "rights_review_required"


class _LinkExtractor(html.parser.HTMLParser):
    """Collect links from HTML for bounded sample discovery."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        attributes = dict(attrs)
        href = attributes.get("href")
        if href:
            self.links.append(href)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")
    return path


def _content_type(response: requests.Response) -> str:
    return (response.headers.get("Content-Type") or "").lower()


def _extension_for_content_type(content_type: str) -> str:
    if "json" in content_type:
        return "json"
    if "html" in content_type:
        return "html"
    return "txt"


def _extract_records_count(text: str, content_type: str) -> int:
    if "json" in content_type:
        payload = json.loads(text)
        if isinstance(payload, list):
            return len(payload)
        if isinstance(payload, dict):
            for key in ("results", "items", "rows", "data", "videos"):
                value = payload.get(key)
                if isinstance(value, list):
                    return len(value)
            return 1
        return 0

    parser = _LinkExtractor()
    parser.feed(text)
    return len({href for href in parser.links if href and not href.startswith("#")})


def _extract_candidate_links(base_url: str, html_text: str) -> list[str]:
    parser = _LinkExtractor()
    parser.feed(html_text)
    base_parts = urlparse(base_url)
    candidates: list[str] = []
    for href in parser.links:
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        absolute = urljoin(base_url, href)
        parts = urlparse(absolute)
        if parts.scheme not in {"http", "https"}:
            continue
        if parts.netloc and parts.netloc != base_parts.netloc:
            continue
        if absolute == base_url:
            continue
        candidates.append(absolute)
    return list(dict.fromkeys(candidates))


def _match_patterns(url: str, patterns: Iterable[str]) -> bool:
    candidate = url.lower()
    return any(pattern.lower() in candidate for pattern in patterns)


def _choose_sample_url(
    target: SeedTarget, index_url: str, index_text: str, content_type: str
) -> str | None:
    if "html" not in content_type:
        return None
    candidates = _extract_candidate_links(index_url, index_text)
    if not candidates:
        return None
    for candidate in candidates:
        if target.sample_patterns and _match_patterns(candidate, target.sample_patterns):
            return candidate
    for candidate in candidates:
        if urlparse(candidate).path not in {"", "/"}:
            return candidate
    return candidates[0]


def _request_error_reason(exc: requests.RequestException, url: str) -> str:
    """Render a short blocked-state reason from a requests exception."""
    response = getattr(exc, "response", None)
    status_code = getattr(response, "status_code", None)
    if status_code:
        return f"HTTP {status_code} fetching {url}"
    message = str(exc).strip()
    return message or f"Request failed for {url}"


def _source_by_id() -> dict[str, dict[str, Any]]:
    inventory = _json(INVENTORY_PATH)
    return {source["source_id"]: source for source in inventory["sources"]}


def _classification_for(source: dict[str, Any]) -> str:
    if source["source_role"] == "official":
        if source["platform_class"] in {"youtube", "vimeo"}:
            return "rights-gated"
        return "official"
    if source["source_family"] == "broadcast_archive":
        return "catalogue-only"
    if source["source_family"] == "web_archive":
        return "fallback-validation"
    if source["source_family"] == "audio_reporting":
        return "evidence-only"
    return "evidence-only"


def select_seed_targets() -> list[SeedTarget]:
    """Select approved bounded seed targets from the inventory manifest."""
    sources = _source_by_id()
    targets: list[SeedTarget] = []
    for blueprint in TARGET_BLUEPRINTS:
        source = sources.get(blueprint["source_id"])
        if source is None:
            msg = f"Inventory manifest is missing source {blueprint['source_id']}"
            raise KeyError(msg)
        targets.append(
            SeedTarget(
                source_id=source["source_id"],
                title=source["title"],
                source_family=source["source_family"],
                source_role=source["source_role"],
                source_classification=_classification_for(source),
                index_url=source["url"],
                access_constraints=source["rights_status"],
                proof_role=blueprint["proof_role"],
                max_requests=2,
                sample_patterns=tuple(blueprint["sample_patterns"]),
                rights_status=source["rights_status"],
            ),
        )
    return targets


def _artifact_path(target: SeedTarget, kind: str, content_type: str) -> Path:
    target_dir = OUTPUT_DIR / target.source_family / target.source_id
    return target_dir / f"{kind}.{_extension_for_content_type(content_type)}"


def _write_artifact(
    target: SeedTarget,
    kind: str,
    response: requests.Response,
) -> dict[str, str]:
    content_type = _content_type(response)
    path = _artifact_path(target, kind, content_type)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(response.text, encoding="utf-8", newline="\n")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": _sha256_text(response.text),
        "content_type": content_type or "text/plain",
    }


def _blocked_record(target: SeedTarget, reason: str) -> dict[str, Any]:
    return {
        "access_constraints": target.access_constraints,
        "approved": True,
        "blocked_reason": reason,
        "fetched_at": _utc_now(),
        "index_fetched_at": None,
        "index_record_count": 0,
        "index_sha256": None,
        "index_url": target.index_url,
        "output_paths": {},
        "proof_role": target.proof_role,
        "proof_status": "blocked",
        "request_urls": [target.index_url],
        "sample_fetched_at": None,
        "sample_record_count": 0,
        "sample_sha256": None,
        "sample_url": target.sample_url,
        "source_classification": target.source_classification,
        "source_family": target.source_family,
        "source_id": target.source_id,
        "source_role": target.source_role,
        "title": target.title,
        "rights_status": target.rights_status,
    }


def fetch_seed_target(
    target: SeedTarget,
    *,
    session: requests.Session | None = None,
    output_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    """Fetch one bounded seed target and write artifacts to ``output_dir``."""
    client = session or requests.Session()
    headers = {
        "User-Agent": "corpus-nz-hansard/1.0 (parliament video seed fetcher; +https://github.com/edithatogo/corpus-nz-hansard)",
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    }

    try:
        index_response = request_with_retries(
            "GET",
            target.index_url,
            session=client,
            headers=headers,
            timeout=30,
        )
    except requests.RequestException as exc:
        return _blocked_record(target, _request_error_reason(exc, target.index_url))

    index_content_type = _content_type(index_response)
    index_artifact = _write_artifact(target, "index", index_response)
    index_count = _extract_records_count(index_response.text, index_content_type)
    sample_url = target.sample_url or _choose_sample_url(
        target,
        index_response.url or target.index_url,
        index_response.text,
        index_content_type,
    )

    sample_artifact: dict[str, str] = {}
    sample_count = 0
    sample_fetched_at: str | None = None
    sample_sha256: str | None = None
    proof_status = "index-only"
    blocked_reason = None

    if sample_url and sample_url != target.index_url:
        try:
            sample_response = request_with_retries(
                "GET",
                sample_url,
                session=client,
                headers=headers,
                timeout=30,
            )
        except requests.RequestException as exc:
            blocked_reason = f"sample fetch failed: {_request_error_reason(exc, sample_url)}"
            proof_status = "blocked"
        else:
            sample_artifact = _write_artifact(target, "sample", sample_response)
            sample_count = max(
                _extract_records_count(sample_response.text, _content_type(sample_response)),
                1,
            )
            sample_fetched_at = _utc_now()
            sample_sha256 = sample_artifact["sha256"]
            proof_status = "fetched"

    record = {
        "access_constraints": target.access_constraints,
        "approved": True,
        "blocked_reason": blocked_reason,
        "fetched_at": _utc_now(),
        "index_fetched_at": _utc_now(),
        "index_record_count": index_count,
        "index_sha256": index_artifact["sha256"],
        "index_url": target.index_url,
        "output_paths": {
            "index": index_artifact["path"],
            **({"sample": sample_artifact["path"]} if sample_artifact else {}),
        },
        "proof_role": target.proof_role,
        "proof_status": proof_status,
        "request_urls": [target.index_url]
        + ([sample_url] if sample_url and sample_url != target.index_url else []),
        "sample_fetched_at": sample_fetched_at,
        "sample_record_count": sample_count,
        "sample_sha256": sample_sha256,
        "sample_url": sample_url,
        "source_classification": target.source_classification,
        "source_family": target.source_family,
        "source_id": target.source_id,
        "source_role": target.source_role,
        "title": target.title,
        "rights_status": target.rights_status,
    }
    if proof_status == "index-only" and blocked_reason is None and sample_url is None:
        record["blocked_reason"] = "No sample link could be discovered from the index response."
    return record


def build_seed_manifest(
    *,
    targets: list[SeedTarget] | None = None,
    output_dir: Path = OUTPUT_DIR,
    session: requests.Session | None = None,
    write: bool = True,
) -> dict[str, Any]:
    """Fetch all selected seed targets and optionally write the manifest."""
    selected = targets or select_seed_targets()
    output_dir.mkdir(parents=True, exist_ok=True)

    records = [
        fetch_seed_target(target, session=session, output_dir=output_dir) for target in selected
    ]

    manifest = {
        "manifest_version": 1,
        "track_id": "parliament_video_seed_fetchers_20260705",
        "repository": "corpus-nz-hansard",
        "generated_at": _utc_now(),
        "inventory_manifest": "manifests/parliament_video_source_inventory.json",
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
        "summary": {
            "target_count": len(records),
            "official_target_count": sum(
                1 for record in records if record["source_role"] == "official"
            ),
            "fallback_target_count": sum(
                1 for record in records if record["source_role"] == "fallback"
            ),
            "rights_gated_target_count": sum(
                1 for record in records if record["source_classification"] == "rights-gated"
            ),
            "blocked_target_count": sum(
                1 for record in records if record["proof_status"] == "blocked"
            ),
            "fetched_target_count": sum(
                1 for record in records if record["proof_status"] == "fetched"
            ),
            "index_only_target_count": sum(
                1 for record in records if record["proof_status"] == "index-only"
            ),
        },
        "targets": records,
        "source_summary": {
            "official_source_ids": [
                record["source_id"] for record in records if record["source_role"] == "official"
            ],
            "fallback_source_ids": [
                record["source_id"] for record in records if record["source_role"] == "fallback"
            ],
            "rights_gated_source_ids": [
                record["source_id"]
                for record in records
                if record["source_classification"] == "rights-gated"
            ],
            "proof_statuses": sorted({record["proof_status"] for record in records}),
        },
        "handoff": [
            {
                "source_family": "house_video",
                "next_track": "parliament_video_full_metadata_archive_20260705",
                "proof_requirement": "Preserve metadata-only retrieval boundaries before any bulk archive step.",
            },
            {
                "source_family": "select_committee_video",
                "next_track": "parliament_video_full_metadata_archive_20260705",
                "proof_requirement": "Reuse select-committee archive and Vimeo-era proof shapes for the archive track.",
            },
            {
                "source_family": "broadcast_archive",
                "next_track": "parliament_video_full_metadata_archive_20260705",
                "proof_requirement": "Keep fallback validation evidence separate from acquisition sources.",
            },
            {
                "source_family": "audio_reporting",
                "next_track": "parliament_video_full_metadata_archive_20260705",
                "proof_requirement": "Record evidence-only references without media acquisition.",
            },
            {
                "source_family": "web_archive",
                "next_track": "parliament_video_full_metadata_archive_20260705",
                "proof_requirement": "Retain link-rot evidence only; do not elevate archived pages to acquisition sources.",
            },
        ],
    }

    if write:
        _write_json(MANIFEST_PATH, manifest)
        write_doc(manifest)
    return manifest


def _supporting_doc_lines() -> str:
    return "\n".join(
        [
            "- `tvnz-archive-looking-back`: historical broadcast validation only.",
            "- `nga-taonga-av-collection`: catalogue validation only.",
            "- `rnz-parliament`: evidence-only reporting surface.",
            "- `parliament-today-am-network`: evidence-only reporting surface.",
            "- `archives-new-zealand-av-catalogue`: catalogue validation only.",
            "- `internet-archive-webcaptures`: link-rot validation only.",
            "- `memento-cdx-web-archives`: link-rot validation only.",
        ]
    )


def write_doc(manifest: dict[str, Any]) -> None:
    rows = "\n".join(
        "| `{source_id}` | {title} | {source_role} | {source_classification} | {proof_status} |".format(
            **source
        )
        for source in manifest["targets"]
    )
    official_rows = "\n".join(
        f"- `{source['source_id']}`: {source['title']} ({source['proof_role']})"
        for source in manifest["targets"]
        if source["source_role"] == "official"
    )
    fallback_rows = "\n".join(
        f"- `{source['source_id']}`: {source['source_classification']} ({source['title']})"
        for source in manifest["targets"]
        if source["source_role"] == "fallback"
    )
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(
        f"""# Parliament Video Seed Fetchers

Release posture: metadata-first/no-download seed evidence.

This track records bounded seed proofs for the video surfaces identified by `parliament_video_source_inventory_20260705`. It is not a video archive and does not claim retrospective or ongoing completeness.

## Policy

- Metadata-first only.
- No media download, including video or audio files.
- No public media release.
- No completeness claim.
- Fallback resources are validation-only until a later rights decision says otherwise.
- Rights review is required before any media acquisition.

## Target Inventory

Official source surfaces:

{official_rows}

Fallback resources:

{fallback_rows}

| Source ID | Title | Role | Classification | Proof status |
| --- | --- | --- | --- | --- |
{rows}

## Fallback Resources

{_supporting_doc_lines()}

## Output Layout

Seed artifacts are written beneath:

`derived/parliament_video_seed_fetchers/<source_family>/<source_id>/`

Each target writes bounded raw response artifacts plus the manifest entry describing request URLs, hashes, sample counts, and proof status.

## Handoff

The full metadata archive track should reuse these source IDs, request URLs, and rights boundaries.

The handoff requirements are:

1. keep request counts bounded in seed mode;
2. preserve hashes and timestamps;
3. promote only the approved sources with stable retrieval behavior;
4. keep blocked or deferred sources explicitly marked until the archive strategy changes.

No seed artifact in this track should be interpreted as a final corpus snapshot.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch bounded Parliament video seed proofs.")
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Print the selected seed targets and exit.",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default=str(MANIFEST_PATH),
        help="Path to write the seed manifest JSON.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(OUTPUT_DIR),
        help="Directory for per-target seed artifacts.",
    )
    args = parser.parse_args()

    if args.list_targets:
        for target in select_seed_targets():
            print(f"{target.source_id}: {target.index_url}")
        return 0

    manifest = build_seed_manifest(output_dir=Path(args.output_dir), write=False)
    _write_json(Path(args.manifest), manifest)
    write_doc(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
