"""Build the NZ Parliament video full metadata archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INVENTORY_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"
SEED_FETCHERS_PATH = ROOT / "manifests" / "parliament_video_seed_fetchers.json"
RECONCILIATION_PATH = ROOT / "manifests" / "parliament_video_reconciliation.json"
ARCHIVE_COVERAGE_PATH = ROOT / "manifests" / "parliament_video_archive_coverage.json"
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_full_metadata_archive.json"
DOC_PATH = ROOT / "docs" / "parliament-video-full-metadata-archive.md"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_full_metadata_archive.schema.json"
ARCHIVE_DIR = ROOT / "derived" / "parliament_video_full_metadata_archive"
SNAPSHOT_DIR = ARCHIVE_DIR / "snapshots"
SNAPSHOT_PATH = ARCHIVE_DIR / "parliament_video_full_metadata_archive_snapshot.json"
RECORDS_PATH = ARCHIVE_DIR / "parliament_video_full_metadata_archive_records.jsonl"
GAP_REPORT_PATH = ARCHIVE_DIR / "parliament_video_full_metadata_archive_gap_report.json"

DEFAULT_RETENTION = 12
DEFAULT_CADENCE = "monthly"
DEFAULT_CACHE_ROOT = "derived/parliament_video_full_metadata_archive/cache"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _stable_digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _latest_snapshot() -> Path | None:
    if not SNAPSHOT_DIR.exists():
        return None
    snapshots = sorted(SNAPSHOT_DIR.glob("*.json"))
    return snapshots[-1] if snapshots else None


def compare_snapshots(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> dict[str, list[str]]:
    def _record_id(record: dict[str, Any]) -> str:
        return str(record.get("record_id") or record.get("source_id"))

    previous_records = (
        {_record_id(record): record for record in previous.get("records", [])} if previous else {}
    )
    current_records = {_record_id(record): record for record in current.get("records", [])}
    previous_ids = set(previous_records)
    current_ids = set(current_records)
    new_ids = sorted(current_ids - previous_ids)
    deleted_ids = sorted(previous_ids - current_ids)
    changed_ids = sorted(
        record_id
        for record_id in current_ids & previous_ids
        if current_records[record_id].get("digest") != previous_records[record_id].get("digest")
    )
    return {
        "new_source_ids": new_ids,
        "deleted_source_ids": deleted_ids,
        "changed_source_ids": changed_ids,
    }


def _source_records(
    inventory: dict[str, Any],
    seed_fetchers: dict[str, Any],
    reconciliation: dict[str, Any],
) -> list[dict[str, Any]]:
    ledger_by_id = {row["source_id"]: row for row in reconciliation["ledger"]}
    seed_by_id = {row["source_id"]: row for row in seed_fetchers["targets"]}
    records: list[dict[str, Any]] = []

    for source in inventory["sources"]:
        source_id = source["source_id"]
        if source_id not in seed_by_id:
            continue
        seed_row = seed_by_id[source_id]
        ledger_row = ledger_by_id.get(source_id, {})
        record = {
            "record_id": source_id,
            "source_id": source_id,
            "source_family": source["source_family"],
            "source_role": source["source_role"],
            "source_classification": seed_row["source_classification"],
            "source_priority": ledger_row.get("source_priority"),
            "gap_status": ledger_row.get("gap_status", "metadata-only"),
            "proof_status": seed_row["proof_status"],
            "rights_status": seed_row["rights_status"],
            "access_constraints": seed_row["access_constraints"],
            "inventory_archive_status": source["archive_status"],
            "inventory_rights_status": source["rights_status"],
            "index_url": seed_row["index_url"],
            "sample_url": seed_row["sample_url"],
            "request_urls": seed_row["request_urls"],
            "blocked_reason": seed_row["blocked_reason"],
            "index_sha256": seed_row["index_sha256"],
            "sample_sha256": seed_row["sample_sha256"],
            "index_record_count": seed_row["index_record_count"],
            "sample_record_count": seed_row["sample_record_count"],
            "output_paths": seed_row["output_paths"],
            "evidence": [
                "manifests/parliament_video_source_inventory.json",
                "manifests/parliament_video_seed_fetchers.json",
                "manifests/parliament_video_reconciliation.json",
            ],
            "archive_state": "captured" if seed_row["proof_status"] != "blocked" else "blocked",
        }
        record["digest"] = _stable_digest(
            {key: value for key, value in record.items() if key != "digest"}
        )
        records.append(record)

    return records


def _load_previous_snapshot() -> dict[str, Any] | None:
    latest = _latest_snapshot()
    if latest is None:
        return None
    return _read_json(latest)


def _build_manifest(
    generated_at: str,
    inventory: dict[str, Any],
    seed_fetchers: dict[str, Any],
    reconciliation: dict[str, Any],
    archive_coverage: dict[str, Any],
    records: list[dict[str, Any]],
    diff: dict[str, list[str]],
) -> dict[str, Any]:
    record_status_counts = Counter(record["proof_status"] for record in records)
    gap_status_counts = Counter(record["gap_status"] for record in records)
    source_classification_counts = Counter(record["source_classification"] for record in records)
    source_role_counts = Counter(record["source_role"] for record in records)
    approved_source_count = len(records)
    captured_source_count = sum(1 for record in records if record["proof_status"] != "blocked")
    blocked_source_count = record_status_counts["blocked"]
    fetched_source_count = record_status_counts["fetched"]
    index_only_source_count = record_status_counts["index-only"]
    rights_gated_source_count = sum(
        1 for record in records if record["source_classification"] == "rights-gated"
    )
    return {
        "manifest_version": 1,
        "track_id": "parliament_video_full_metadata_archive_20260705",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "refresh_policy": {
            "cadence": DEFAULT_CADENCE,
            "snapshot_retention": DEFAULT_RETENTION,
            "comparison_basis": "latest_snapshot",
            "preserve_history": True,
        },
        "cache_policy": {
            "root": DEFAULT_CACHE_ROOT,
            "normalized_id_prefix": "parliament-video-full-metadata-archive",
            "retry_policy": {
                "max_attempts": 3,
                "backoff_strategy": "exponential",
                "max_backoff_seconds": 60,
            },
            "pagination_policy": {
                "stable_sort": True,
                "page_size": 50,
            },
        },
        "policy": {
            "metadata_first": True,
            "no_media_download": True,
            "no_video_file_download": True,
            "no_audio_file_download": True,
            "no_public_media_release": True,
            "no_completeness_claim": True,
            "rights_review_required_before_media_acquisition": True,
            "fallbacks_are_validation_only": True,
        },
        "source_manifests": {
            "inventory_manifest": "manifests/parliament_video_source_inventory.json",
            "seed_fetchers_manifest": "manifests/parliament_video_seed_fetchers.json",
            "reconciliation_manifest": "manifests/parliament_video_reconciliation.json",
            "archive_coverage_manifest": "manifests/parliament_video_archive_coverage.json",
        },
        "archive": {
            "records_path": "derived/parliament_video_full_metadata_archive/parliament_video_full_metadata_archive_records.jsonl",
            "snapshot_path": "derived/parliament_video_full_metadata_archive/parliament_video_full_metadata_archive_snapshot.json",
            "gap_report_path": "derived/parliament_video_full_metadata_archive/parliament_video_full_metadata_archive_gap_report.json",
            "snapshot_history_directory": "derived/parliament_video_full_metadata_archive/snapshots",
        },
        "summary": {
            "record_count": len(records),
            "approved_source_count": approved_source_count,
            "captured_source_count": captured_source_count,
            "blocked_source_count": blocked_source_count,
            "fetched_source_count": fetched_source_count,
            "index_only_source_count": index_only_source_count,
            "official_source_count": len(inventory["source_summary"]["official_source_ids"]),
            "fallback_source_count": len(inventory["source_summary"]["fallback_source_ids"]),
            "rights_gated_source_count": rights_gated_source_count,
            "adjacent_repo_finding_count": len(archive_coverage["adjacent_repo_findings"]),
            "metadata_completeness_claim": False,
            "media_completeness_claim": False,
            "retrospective_archive_complete": False,
            "ongoing_archive_complete": False,
            "complete_video_archive": False,
            "record_status_counts": dict(sorted(record_status_counts.items())),
            "gap_status_counts": dict(sorted(gap_status_counts.items())),
            "source_classification_counts": dict(sorted(source_classification_counts.items())),
            "source_role_counts": dict(sorted(source_role_counts.items())),
        },
        "comparison": diff,
        "adjacent_repo_findings": archive_coverage["adjacent_repo_findings"],
        "notes": [
            "Metadata archive completeness remains separate from media archive completeness.",
            "Normalized JSONL, hashes, and request logs are archived without downloading video or audio media files.",
            "Fallback sources remain validation-only unless a later rights decision changes their status.",
        ],
    }


def _build_gap_report(
    generated_at: str,
    manifest: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    by_status = {
        status: sorted(record["source_id"] for record in records if record["gap_status"] == status)
        for status in sorted({record["gap_status"] for record in records})
    }
    by_proof = {
        status: sorted(
            record["source_id"] for record in records if record["proof_status"] == status
        )
        for status in sorted({record["proof_status"] for record in records})
    }
    return {
        "manifest_version": 1,
        "track_id": manifest["track_id"],
        "generated_at": generated_at,
        "policy": manifest["policy"],
        "gap_taxonomy": sorted({record["gap_status"] for record in records}),
        "gap_status_counts": manifest["summary"]["gap_status_counts"],
        "proof_status_counts": manifest["summary"]["record_status_counts"],
        "records_by_gap_status": by_status,
        "records_by_proof_status": by_proof,
        "adjacent_repo_findings": manifest["adjacent_repo_findings"],
        "notes": [
            "Gap report reflects metadata-only capture and does not imply media completeness.",
            "Blocked records remain blocked until an approved retrieval path is created.",
        ],
    }


def _write_doc(manifest: dict[str, Any]) -> None:
    summary = manifest["summary"]
    doc = f"""# Parliament Video Full Metadata Archive

Release posture: metadata-first archive with normalized JSONL, hashes, monthly refresh, and cache policy.

This track captures approved NZ Parliament video metadata surfaces without downloading video or audio media files. It archives normalized JSONL, source snapshots, request logs, hashes, and blocked records. It is not a complete media archive.

The cache policy keeps normalized IDs, retry behavior, and pagination stable across refreshes.

## Refresh Policy

- Cadence: {manifest["refresh_policy"]["cadence"]}
- Snapshot retention: {manifest["refresh_policy"]["snapshot_retention"]}
- Comparison basis: {manifest["refresh_policy"]["comparison_basis"]}

## Cache Policy

- Cache root: `{manifest["cache_policy"]["root"]}`
- Normalized ID prefix: `{manifest["cache_policy"]["normalized_id_prefix"]}`
- Retry attempts: {manifest["cache_policy"]["retry_policy"]["max_attempts"]}
- Backoff strategy: {manifest["cache_policy"]["retry_policy"]["backoff_strategy"]}
- Pagination page size: {manifest["cache_policy"]["pagination_policy"]["page_size"]}

## Policy

- Metadata-first only.
- No media download.
- No public media release.
- No completeness claim.
- Rights review required before media acquisition.
- Fallbacks are validation only.

## Summary

| Field | Value |
| --- | --- |
| Records | {summary["record_count"]} |
| Approved sources | {summary["approved_source_count"]} |
| Captured sources | {summary["captured_source_count"]} |
| Blocked sources | {summary["blocked_source_count"]} |
| Fetched sources | {summary["fetched_source_count"]} |
| Index-only sources | {summary["index_only_source_count"]} |
| Official sources | {summary["official_source_count"]} |
| Fallback sources | {summary["fallback_source_count"]} |
| Rights-gated sources | {summary["rights_gated_source_count"]} |
| Adjacent repo findings | {summary["adjacent_repo_finding_count"]} |

Metadata completeness claim: {summary["metadata_completeness_claim"]}
Media completeness claim: {summary["media_completeness_claim"]}
Retrospective archive complete: {summary["retrospective_archive_complete"]}
Ongoing archive complete: {summary["ongoing_archive_complete"]}
Complete video archive: {summary["complete_video_archive"]}

## Normalized JSONL

The archive writes normalized JSONL records and a snapshot history so refreshes remain resumable and hash-backed.

## Gap Report

The gap report separates fetched, index-only, blocked, and rights-gated metadata records.

## Next Actions

- Keep monthly refreshes resumable and hash-backed.
- Preserve the separation between metadata completeness and media completeness.
- Keep fallback resources validation-only unless the rights decision changes.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def build_manifest(*, write_outputs: bool = True) -> dict[str, Any]:
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    inventory = _read_json(SOURCE_INVENTORY_PATH)
    seed_fetchers = _read_json(SEED_FETCHERS_PATH)
    reconciliation = _read_json(RECONCILIATION_PATH)
    archive_coverage = _read_json(ARCHIVE_COVERAGE_PATH)
    records = _source_records(inventory, seed_fetchers, reconciliation)
    current_snapshot = {
        "manifest_version": 1,
        "track_id": "parliament_video_full_metadata_archive_20260705",
        "generated_at": generated_at,
        "records": records,
    }
    previous_snapshot = _load_previous_snapshot()
    diff = compare_snapshots(previous_snapshot, current_snapshot)
    manifest = _build_manifest(
        generated_at, inventory, seed_fetchers, reconciliation, archive_coverage, records, diff
    )
    gap_report = _build_gap_report(generated_at, manifest, records)

    if write_outputs:
        _write_json(MANIFEST_PATH, manifest)
        _write_json(
            SNAPSHOT_PATH,
            {
                "manifest_version": 1,
                "track_id": manifest["track_id"],
                "generated_at": generated_at,
                "records": records,
                "previous_snapshot_path": _latest_snapshot().as_posix()
                if _latest_snapshot()
                else None,
            },
        )
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        _write_json(SNAPSHOT_DIR / f"{generated_at.replace(':', '-')}.json", current_snapshot)
        _write_json(GAP_REPORT_PATH, gap_report)
        _write_jsonl(RECORDS_PATH, records)
        _write_doc(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-write", action="store_true", help="Compute outputs without writing files."
    )
    args = parser.parse_args()
    manifest = build_manifest(write_outputs=not args.no_write)
    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT).as_posix()}")
    print(f"Records: {manifest['summary']['record_count']}")


if __name__ == "__main__":
    main()
