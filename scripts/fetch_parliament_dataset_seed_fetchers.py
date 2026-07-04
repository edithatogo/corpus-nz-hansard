"""Fetch bounded seed evidence for Parliament dataset families."""

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

INVENTORY_PATH = ROOT / "manifests/parliament_dataset_inventory.json"
MANIFEST_PATH = ROOT / "manifests/parliament_dataset_seed_fetchers.json"
SCHEMA_PATH = ROOT / "schemas/parliament_dataset_seed_fetchers.schema.json"
DOC_PATH = ROOT / "docs/parliament-dataset-seed-fetchers.md"
OUTPUT_DIR = ROOT / "derived" / "parliament_dataset_seed_fetchers"

REQUIRED_DATASET_FAMILIES = {
    "hansard_debates",
    "daily_progress",
    "journals",
    "papers_presented_ajhr",
    "order_paper_questions_business_sitting_programme",
    "select_committees",
    "petitions",
    "members_parties_seating_contacts",
    "parliamentary_rules_procedure",
    "video_audio_calendar",
}

TARGET_BLUEPRINTS = (
    {
        "dataset_family": "hansard_debates",
        "source_id": "nz-parliament-hansard-current",
        "sample_patterns": ("hansard", "debates", "read-hansard"),
    },
    {
        "dataset_family": "daily_progress",
        "source_id": "nz-parliament-daily-progress",
        "sample_patterns": ("daily-progress", "progress"),
    },
    {
        "dataset_family": "journals",
        "source_id": "nz-parliament-weekly-journals-archive",
        "sample_patterns": ("weekly-journals", "journals"),
    },
    {
        "dataset_family": "journals",
        "source_id": "nz-parliament-journals-session-indexes",
        "sample_patterns": ("journals", "index"),
    },
    {
        "dataset_family": "papers_presented_ajhr",
        "source_id": "nz-parliament-papers-presented",
        "sample_patterns": ("papers-presented",),
    },
    {
        "dataset_family": "papers_presented_ajhr",
        "source_id": "nz-parliament-current-papers",
        "sample_patterns": ("current-papers",),
    },
    {
        "dataset_family": "papers_presented_ajhr",
        "source_id": "nz-parliament-ajhr",
        "sample_patterns": ("papers-presented", "ajhr"),
    },
    {
        "dataset_family": "papers_presented_ajhr",
        "source_id": "papers-past-ajhr",
        "sample_patterns": ("parliamentary", "ajhr"),
    },
    {
        "dataset_family": "order_paper_questions_business_sitting_programme",
        "source_id": "nz-parliament-order-paper",
        "sample_patterns": ("order-paper",),
    },
    {
        "dataset_family": "order_paper_questions_business_sitting_programme",
        "source_id": "nz-parliament-oral-questions",
        "sample_patterns": ("oral-questions",),
    },
    {
        "dataset_family": "order_paper_questions_business_sitting_programme",
        "source_id": "nz-parliament-written-questions",
        "sample_patterns": ("written-questions",),
    },
    {
        "dataset_family": "select_committees",
        "source_id": "nz-parliament-select-committee-reports",
        "sample_patterns": ("reports",),
    },
    {
        "dataset_family": "select_committees",
        "source_id": "nz-parliament-select-committee-submissions-advice",
        "sample_patterns": ("submissions", "advice"),
    },
    {
        "dataset_family": "select_committees",
        "source_id": "nz-parliament-select-committee-meetings",
        "sample_patterns": ("meetings",),
    },
    {
        "dataset_family": "petitions",
        "source_id": "nz-parliament-petitions",
        "sample_patterns": ("petition",),
    },
    {
        "dataset_family": "members_parties_seating_contacts",
        "source_id": "nz-parliament-members-current",
        "sample_patterns": ("members-of-parliament",),
    },
    {
        "dataset_family": "members_parties_seating_contacts",
        "source_id": "nz-parliament-former-members",
        "sample_patterns": ("former-members",),
    },
    {
        "dataset_family": "members_parties_seating_contacts",
        "source_id": "nz-parliament-parties-current",
        "sample_patterns": ("political-parties",),
    },
    {
        "dataset_family": "members_parties_seating_contacts",
        "source_id": "nz-parliament-member-contact-downloads",
        "sample_patterns": ("contact-an-mp",),
    },
    {
        "dataset_family": "parliamentary_rules_procedure",
        "source_id": "nz-parliament-parliamentary-rules",
        "sample_patterns": ("parliamentary-rules",),
    },
    {
        "dataset_family": "parliamentary_rules_procedure",
        "source_id": "nz-parliament-standing-orders",
        "sample_patterns": ("standing-orders",),
    },
    {
        "dataset_family": "parliamentary_rules_procedure",
        "source_id": "nz-parliament-speakers-rulings",
        "sample_patterns": ("speakers-rulings",),
    },
    {
        "dataset_family": "video_audio_calendar",
        "source_id": "nz-parliament-video",
        "sample_patterns": ("watch-parliament", "video"),
    },
    {
        "dataset_family": "video_audio_calendar",
        "source_id": "nz-parliament-calendar",
        "sample_patterns": ("meetings-of-parliament", "calendar"),
    },
)


@dataclass(frozen=True, slots=True)
class SeedTarget:
    """A single bounded seed-fetch target."""

    dataset_family: str
    source_id: str
    source_posture: str
    index_url: str
    sample_patterns: tuple[str, ...]
    access_constraints: str
    fallback_for: tuple[str, ...]
    approved: bool


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


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
            for key in ("results", "items", "rows", "data"):
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
    for candidate in _extract_candidate_links(index_url, index_text):
        if candidate == index_url:
            continue
        if target.sample_patterns and _match_patterns(candidate, target.sample_patterns):
            return candidate
    candidates = _extract_candidate_links(index_url, index_text)
    return candidates[0] if candidates else None


def _request_error_reason(exc: requests.RequestException, url: str) -> str:
    """Render a short blocked-state reason from a requests exception."""
    response = getattr(exc, "response", None)
    status_code = getattr(response, "status_code", None)
    if status_code:
        return f"HTTP {status_code} fetching {url}"
    message = str(exc).strip()
    return message or f"Request failed for {url}"


def _load_inventory() -> dict[str, Any]:
    return _json(INVENTORY_PATH)


def _source_by_id(inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {source["id"]: source for source in inventory["sources"]}


def select_seed_targets() -> list[SeedTarget]:
    """Select approved bounded seed targets from the inventory manifest."""
    inventory = _load_inventory()
    sources = _source_by_id(inventory)
    targets: list[SeedTarget] = []
    for blueprint in TARGET_BLUEPRINTS:
        source = sources.get(blueprint["source_id"])
        if source is None:
            msg = f"Inventory manifest is missing source {blueprint['source_id']}"
            raise KeyError(msg)
        targets.append(
            SeedTarget(
                dataset_family=blueprint["dataset_family"],
                source_id=source["id"],
                source_posture=source["source_posture"],
                index_url=source["url"],
                sample_patterns=tuple(blueprint["sample_patterns"]),
                access_constraints=source["access_constraints"],
                fallback_for=tuple(source.get("fallback_for", [])),
                approved=source["source_posture"] in {"official", "fallback", "supporting"},
            ),
        )
    return targets


def _artifact_path(target: SeedTarget, kind: str, content_type: str) -> Path:
    target_dir = OUTPUT_DIR / target.dataset_family / target.source_id
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
        "approved": target.approved,
        "blocked_reason": reason,
        "dataset_family": target.dataset_family,
        "fetched_at": _utc_now(),
        "index_fetched_at": None,
        "index_record_count": 0,
        "index_sha256": None,
        "index_url": target.index_url,
        "output_paths": {},
        "proof_status": "blocked",
        "request_urls": [target.index_url],
        "sample_fetched_at": None,
        "sample_record_count": 0,
        "sample_sha256": None,
        "sample_url": None,
        "source_id": target.source_id,
        "source_posture": target.source_posture,
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
        "User-Agent": "corpus-nz-hansard/1.0 (seed fetcher; +https://github.com/edithatogo/corpus-nz-hansard)",
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
    sample_url = _choose_sample_url(
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

    if sample_url:
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
        "approved": target.approved,
        "blocked_reason": blocked_reason,
        "dataset_family": target.dataset_family,
        "fetched_at": _utc_now(),
        "index_fetched_at": _utc_now(),
        "index_record_count": index_count,
        "index_sha256": index_artifact["sha256"],
        "index_url": target.index_url,
        "output_paths": {
            "index": index_artifact["path"],
            **({"sample": sample_artifact["path"]} if sample_artifact else {}),
        },
        "proof_status": proof_status,
        "request_urls": [target.index_url, sample_url] if sample_url else [target.index_url],
        "sample_fetched_at": sample_fetched_at,
        "sample_record_count": sample_count,
        "sample_sha256": sample_sha256,
        "sample_url": sample_url,
        "source_id": target.source_id,
        "source_posture": target.source_posture,
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
    approved = [record for record in records if record["approved"]]

    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "retrieved_at": _utc_now(),
        "inventory_manifest": "manifests/parliament_dataset_inventory.json",
        "policy": {
            "official_sources_first": True,
            "no_bulk_acquisition": True,
            "no_completion_claim": True,
        },
        "summary": {
            "approved_target_count": len(approved),
            "blocked_target_count": sum(
                1 for record in records if record["proof_status"] == "blocked"
            ),
            "deferred_target_count": sum(
                1 for record in records if record["proof_status"] == "deferred"
            ),
            "fetched_target_count": sum(
                1 for record in records if record["proof_status"] == "fetched"
            ),
            "index_only_target_count": sum(
                1 for record in records if record["proof_status"] == "index-only"
            ),
            "total_target_count": len(records),
        },
        "targets": records,
        "handoff": [
            {
                "dataset_family": "journals",
                "next_track": "parliament_dataset_full_acquisition_20260703",
                "proof_requirement": "Use one bounded seed proof per family before any bulk-acquisition implementation.",
            },
            {
                "dataset_family": "papers_presented_ajhr",
                "next_track": "parliament_dataset_full_acquisition_20260703",
                "proof_requirement": "Preserve source URLs, hashes, and rights notes for the full-acquisition track.",
            },
            {
                "dataset_family": "order_paper_questions_business_sitting_programme",
                "next_track": "parliament_dataset_full_acquisition_20260703",
                "proof_requirement": "Keep question/business pages bounded and resumable.",
            },
            {
                "dataset_family": "select_committees",
                "next_track": "parliament_dataset_full_acquisition_20260703",
                "proof_requirement": "Use the same sample URLs and hashes as the acquisition contract entry points.",
            },
            {
                "dataset_family": "petitions",
                "next_track": "parliament_dataset_full_acquisition_20260703",
                "proof_requirement": "Record access constraints before any petition content harvesting.",
            },
            {
                "dataset_family": "members_parties_seating_contacts",
                "next_track": "parliament_dataset_full_acquisition_20260703",
                "proof_requirement": "Preserve contact-download and seating-page provenance before any expansion.",
            },
        ],
    }

    if write:
        _write_json(MANIFEST_PATH, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch bounded Parliament dataset seed proofs.")
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
            print(f"{target.dataset_family}: {target.source_id} -> {target.index_url}")
        return 0

    manifest = build_seed_manifest(output_dir=Path(args.output_dir), write=False)
    _write_json(Path(args.manifest), manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
