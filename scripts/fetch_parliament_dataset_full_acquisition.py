"""Fetch bounded full-acquisition evidence for Parliament dataset families."""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import sys
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.fetch_parliament_dataset_seed_fetchers import (  # noqa: E402
    SeedTarget,
    select_seed_targets,
)
from scripts.http_retry import request_with_retries  # noqa: E402

INVENTORY_PATH = ROOT / "manifests/parliament_dataset_inventory.json"
MANIFEST_PATH = ROOT / "manifests/parliament_dataset_full_acquisition.json"
SCHEMA_PATH = ROOT / "schemas/parliament_dataset_full_acquisition.schema.json"
DOC_PATH = ROOT / "docs/parliament-dataset-full-acquisition.md"
OUTPUT_DIR = ROOT / "derived" / "parliament_dataset_full_acquisition"
TARGET_CACHE_FILENAME = "target.json"
MAX_DETAIL_FETCHES = 1

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

REFRESH_CADENCE_BY_FAMILY = {
    "hansard_debates": "daily",
    "daily_progress": "daily",
    "journals": "weekly",
    "papers_presented_ajhr": "weekly",
    "order_paper_questions_business_sitting_programme": "daily",
    "select_committees": "weekly",
    "petitions": "daily",
    "members_parties_seating_contacts": "daily",
    "parliamentary_rules_procedure": "weekly",
    "video_audio_calendar": "daily",
}


class _LinkExtractor(html.parser.HTMLParser):
    """Collect links from HTML for bounded detail discovery."""

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


def _relativize(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


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


def _extract_candidate_links(base_url: str, text: str, content_type: str) -> list[str]:
    if "json" in content_type:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return []
        candidates: list[str] = []
        values: Iterable[Any]
        if isinstance(payload, list):
            values = payload
        elif isinstance(payload, dict):
            values = payload.values()
        else:
            values = ()
        for value in values:
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                candidates.append(value)
            elif isinstance(value, dict):
                for key in ("url", "href", "link", "uri", "web_url"):
                    candidate = value.get(key)
                    if isinstance(candidate, str) and candidate.startswith(("http://", "https://")):
                        candidates.append(candidate)
        return list(dict.fromkeys(candidates))

    parser = _LinkExtractor()
    parser.feed(text)
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


def _choose_detail_urls(
    target: SeedTarget, index_url: str, index_text: str, content_type: str
) -> list[str]:
    candidates = _extract_candidate_links(index_url, index_text, content_type)
    if not candidates:
        return []
    matched = [
        candidate for candidate in candidates if _match_patterns(candidate, target.sample_patterns)
    ]
    ordered = matched or candidates
    return ordered[:MAX_DETAIL_FETCHES]


def _request_error_reason(exc: requests.RequestException, url: str) -> str:
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


def _target_dir(output_dir: Path, target: SeedTarget) -> Path:
    return output_dir / target.dataset_family / target.source_id


def _coverage_window(target: SeedTarget) -> str:
    inventory = _source_by_id(_load_inventory())
    source = inventory.get(target.source_id, {})
    coverage_period = str(source.get("coverage_period", "")).lower()
    if "historic" in coverage_period or any(
        token in target.source_id.lower() for token in ("archive", "former", "historic")
    ):
        return "historic"
    return "current"


def _refresh_cadence(target: SeedTarget) -> str:
    return REFRESH_CADENCE_BY_FAMILY.get(target.dataset_family, "weekly")


def _rights_boundary(target: SeedTarget) -> str:
    return "not-public-release-ready"


def _cache_payload_path(output_dir: Path, target: SeedTarget) -> Path:
    return _target_dir(output_dir, target) / TARGET_CACHE_FILENAME


def _load_cached_record(
    target: SeedTarget,
    *,
    output_dir: Path,
) -> dict[str, Any] | None:
    cache_path = _cache_payload_path(output_dir, target)
    if not cache_path.exists():
        return None
    record = _json(cache_path)
    record["cache_hit"] = True
    record["resume_used"] = True
    record.setdefault("cache_dir", _relativize(_target_dir(output_dir, target)))
    return record


def _write_artifact(
    target: SeedTarget,
    *,
    output_dir: Path,
    kind: str,
    response: requests.Response,
) -> dict[str, str]:
    content_type = _content_type(response)
    target_dir = _target_dir(output_dir, target)
    path = target_dir / f"{kind}.{_extension_for_content_type(content_type)}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(response.text, encoding="utf-8", newline="\n")
    return {
        "path": _relativize(path),
        "sha256": _sha256_text(response.text),
        "content_type": content_type or "text/plain",
    }


def _blocked_record(target: SeedTarget, reason: str, *, output_dir: Path) -> dict[str, Any]:
    target_dir = _target_dir(output_dir, target)
    return {
        "access_constraints": target.access_constraints,
        "approved": target.approved,
        "blocked_reason": reason,
        "cache_dir": _relativize(target_dir),
        "cache_hit": False,
        "coverage_window": _coverage_window(target),
        "dataset_family": target.dataset_family,
        "detail_artifact_count": 0,
        "detail_paths": [],
        "detail_record_count": 0,
        "detail_sha256s": [],
        "detail_urls": [],
        "fetched_at": _utc_now(),
        "index_cache_path": _relativize(target_dir / "index.html"),
        "index_fetched_at": None,
        "index_record_count": 0,
        "index_sha256": None,
        "index_url": target.index_url,
        "proof_status": "blocked",
        "refresh_cadence": _refresh_cadence(target),
        "request_urls": [target.index_url],
        "resume_used": False,
        "rights_boundary": _rights_boundary(target),
        "source_id": target.source_id,
        "source_posture": target.source_posture,
    }


def acquire_full_target(
    target: SeedTarget,
    *,
    session: requests.Session | None = None,
    cache_dir: Path | None = None,
    output_dir: Path = OUTPUT_DIR,
    resume: bool = True,
) -> dict[str, Any]:
    """Acquire one bounded full-acquisition target and write cache artifacts."""
    output_dir = cache_dir or output_dir
    if resume:
        cached = _load_cached_record(target, output_dir=output_dir)
        if cached is not None:
            return cached

    client = session or requests.Session()
    headers = {
        "User-Agent": "corpus-nz-hansard/1.0 (full acquisition; +https://github.com/edithatogo/corpus-nz-hansard)",
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
        return _blocked_record(
            target, _request_error_reason(exc, target.index_url), output_dir=output_dir
        )

    timestamp = _utc_now()
    index_content_type = _content_type(index_response)
    index_artifact = _write_artifact(
        target,
        output_dir=output_dir,
        kind="index",
        response=index_response,
    )
    index_count = _extract_records_count(index_response.text, index_content_type)
    index_url = index_response.url or target.index_url
    detail_urls = _choose_detail_urls(
        target,
        index_url,
        index_response.text,
        index_content_type,
    )

    detail_artifacts: list[dict[str, str]] = []
    detail_counts: list[int] = []
    blocked_reason = None
    proof_status = "index-only"
    for detail_url in detail_urls:
        try:
            detail_response = request_with_retries(
                "GET",
                detail_url,
                session=client,
                headers=headers,
                timeout=30,
            )
        except requests.RequestException as exc:
            blocked_reason = f"detail fetch failed: {_request_error_reason(exc, detail_url)}"
            proof_status = "blocked"
            break
        artifact = _write_artifact(
            target,
            output_dir=output_dir,
            kind=f"detail-{len(detail_artifacts) + 1:02d}",
            response=detail_response,
        )
        detail_artifacts.append(artifact)
        detail_counts.append(
            max(_extract_records_count(detail_response.text, _content_type(detail_response)), 1)
        )
        proof_status = "fetched"

    if not detail_urls and blocked_reason is None:
        blocked_reason = "No detail link could be discovered from the index response."

    record = {
        "access_constraints": target.access_constraints,
        "approved": target.approved,
        "blocked_reason": blocked_reason,
        "cache_dir": _relativize(_target_dir(output_dir, target)),
        "cache_hit": False,
        "coverage_window": _coverage_window(target),
        "dataset_family": target.dataset_family,
        "detail_artifact_count": len(detail_artifacts),
        "detail_paths": [artifact["path"] for artifact in detail_artifacts],
        "detail_record_count": sum(detail_counts),
        "detail_sha256s": [artifact["sha256"] for artifact in detail_artifacts],
        "detail_urls": detail_urls[: len(detail_artifacts)],
        "fetched_at": timestamp,
        "index_cache_path": index_artifact["path"],
        "index_fetched_at": timestamp,
        "index_record_count": index_count,
        "index_sha256": index_artifact["sha256"],
        "index_url": target.index_url,
        "proof_status": proof_status,
        "refresh_cadence": _refresh_cadence(target),
        "request_urls": [target.index_url, *detail_urls[: len(detail_artifacts)]],
        "resume_used": False,
        "rights_boundary": _rights_boundary(target),
        "source_id": target.source_id,
        "source_posture": target.source_posture,
    }

    cache_path = _cache_payload_path(output_dir, target)
    _write_json(cache_path, record)
    return record


def select_full_acquisition_targets() -> list[SeedTarget]:
    """Select the bounded acquisition targets from the seed evidence set."""
    return select_seed_targets()


def _reconciliation_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_family: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_family.setdefault(record["dataset_family"], []).append(record)

    for family in sorted(by_family):
        family_records = by_family[family]
        hostnames = {
            urlparse(record["index_url"]).netloc
            for record in family_records
            if record.get("index_url")
        }
        fetched = sum(1 for record in family_records if record["proof_status"] == "fetched")
        blocked = sum(1 for record in family_records if record["proof_status"] == "blocked")
        rows.append(
            {
                "dataset_family": family,
                "reconciliation_status": "pass" if blocked == 0 else "partial",
                "source_ids": sorted(record["source_id"] for record in family_records),
                "shared_hostname": next(iter(hostnames)) if len(hostnames) == 1 else "mixed",
                "notes": (
                    f"{len(family_records)} bounded targets; {fetched} fetched; {blocked} blocked."
                ),
            }
        )
    return rows


def build_full_acquisition_manifest(
    *,
    targets: list[SeedTarget] | None = None,
    cache_dir: Path | None = None,
    output_dir: Path = OUTPUT_DIR,
    session: requests.Session | None = None,
    write: bool = True,
    resume: bool = True,
) -> dict[str, Any]:
    """Acquire all selected targets and optionally write the manifest."""
    output_dir = cache_dir or output_dir
    selected = targets or select_full_acquisition_targets()
    output_dir.mkdir(parents=True, exist_ok=True)

    records = [
        acquire_full_target(target, session=session, output_dir=output_dir, resume=resume)
        for target in selected
    ]
    approved = [record for record in records if record["approved"]]
    reconciliation = _reconciliation_rows(records)

    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "retrieved_at": _utc_now(),
        "inventory_manifest": "manifests/parliament_dataset_inventory.json",
        "seed_manifest": "manifests/parliament_dataset_seed_fetchers.json",
        "cache_root": _relativize(output_dir),
        "publication_boundary": "not-public-release-ready",
        "policy": {
            "official_sources_first": True,
            "rights_safe": True,
            "no_bulk_acquisition": True,
            "no_public_release": True,
            "excludes_nz_legislation": True,
            "excludes_nz_gazette": True,
            "hathitrust_not_acquisition_dependency": True,
            "internet_archive_not_acquisition_dependency": True,
            "no_historical_completeness_claim": True,
        },
        "summary": {
            "approved_target_count": len(approved),
            "blocked_target_count": sum(
                1 for record in records if record["proof_status"] == "blocked"
            ),
            "cache_hit_count": sum(1 for record in records if record["cache_hit"]),
            "detail_artifact_count": sum(record["detail_artifact_count"] for record in records),
            "family_count": len({record["dataset_family"] for record in records}),
            "fetched_target_count": sum(
                1 for record in records if record["proof_status"] == "fetched"
            ),
            "index_only_target_count": sum(
                1 for record in records if record["proof_status"] == "index-only"
            ),
            "reconciled_family_count": len(reconciliation),
            "resume_hit_count": sum(1 for record in records if record["resume_used"]),
            "total_target_count": len(records),
        },
        "targets": records,
        "reconciliation": reconciliation,
    }

    if write:
        _write_json(MANIFEST_PATH, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Parliament dataset full-acquisition evidence."
    )
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--no-resume", action="store_true", help="Ignore cached target records.")
    parser.add_argument(
        "--list-targets", action="store_true", help="Print selected targets and exit."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_targets:
        for target in select_full_acquisition_targets():
            print(f"{target.dataset_family}: {target.source_id} -> {target.index_url}")
        return 0

    manifest = build_full_acquisition_manifest(
        output_dir=args.output_dir,
        write=False,
        resume=not args.no_resume,
    )
    _write_json(args.manifest, manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
