"""Build corpus-wide member identity artifacts from normalized Hansard records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

try:
    from scripts.build_member_identity_review import _normalize_token
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_member_identity_review import _normalize_token

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARQUET = ROOT / "generated/parquet/hansard.parquet"
AUTHORITY_PATH = ROOT / "derived/corpus_wide_member_identity_authority.json"
SOURCE_INVENTORY_PATH = ROOT / "manifests/source_inventory.json"
SCHEMA_DISCOVERY_PATH = ROOT / "manifests/schema_discovery.json"
SCHEMA_PATH = ROOT / "schemas/corpus_wide_member_identity.schema.json"
OUTPUT_DIR = ROOT / "derived/corpus_wide_member_identity"
OUTPUT_CSV = OUTPUT_DIR / "member_identity.csv"
REVIEW_QUEUE_CSV = OUTPUT_DIR / "member_identity_review_queue.csv"
OVERRIDES_CSV = OUTPUT_DIR / "member_identity_review_overrides.csv"
VALIDATION_MANIFEST_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
DOC_PATH = ROOT / "docs/corpus-wide-member-identity-release.md"
TRACK_ID = "corpus_wide_member_identity_release_20260610"

OUTPUT_COLUMNS = [
    "source_stable_id",
    "source_file",
    "source_row_number",
    "parliament_number",
    "parliament_document_id",
    "document_type",
    "document_content_date",
    "member_of_parliament_raw",
    "member_raw_token",
    "member_token_index",
    "member_token_count",
    "multi_member_field",
    "member_id",
    "member_display_name",
    "member_authority_source",
    "member_authority_url",
    "member_resolution_method",
    "member_resolution_confidence",
    "member_resolution_status",
    "review_status",
    "release_status",
    "source_hash",
    "authority_snapshot_hash",
    "notes",
]

REVIEW_QUEUE_COLUMNS = OUTPUT_COLUMNS + ["review_reason"]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(rows: list[dict[str, Any]], path: Path, columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _authority_snapshot_hash(authority: dict[str, Any]) -> str:
    encoded = json.dumps(authority, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _authority_lookup(authority: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    lookup: dict[str, list[dict[str, Any]]] = {}
    for record in authority["member_records"]:
        names = [record["canonical_name"], record["display_name"], *record.get("aliases", [])]
        for name in names:
            key = _normalize_token(name).upper()
            records = lookup.setdefault(key, [])
            if all(existing["member_id"] != record["member_id"] for existing in records):
                records.append(record)
    return lookup


def _split_members(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    return [part.strip() for part in raw_value.split(";") if part.strip()]


def _resolve_token(
    *,
    token: str,
    lookup: dict[str, list[dict[str, Any]]],
    authority_snapshot_hash: str,
) -> dict[str, Any]:
    normalized = _normalize_token(token).upper()
    candidates = lookup.get(normalized, [])
    if len(candidates) > 1:
        return {
            "member_id": "",
            "member_display_name": "",
            "member_authority_source": "",
            "member_authority_url": "",
            "member_resolution_method": "conflicting-authority-match",
            "member_resolution_confidence": "none",
            "member_resolution_status": "conflict",
            "authority_snapshot_hash": authority_snapshot_hash,
            "notes": "Multiple authority records matched the same normalized token.",
        }
    if not candidates:
        return {
            "member_id": "",
            "member_display_name": "",
            "member_authority_source": "",
            "member_authority_url": "",
            "member_resolution_method": "no-authority-match",
            "member_resolution_confidence": "none",
            "member_resolution_status": "unresolved",
            "authority_snapshot_hash": authority_snapshot_hash,
            "notes": "No matching member authority record in the current local authority snapshot.",
        }
    candidate = candidates[0]
    canonical_key = _normalize_token(candidate["canonical_name"]).upper()
    method = (
        "exact-name-match" if normalized == canonical_key else "alias-or-honorific-normalized-match"
    )
    status = "exact" if normalized == canonical_key else "alias"
    return {
        "member_id": candidate["member_id"],
        "member_display_name": candidate["display_name"],
        "member_authority_source": candidate["authority_source_id"],
        "member_authority_url": candidate["authority_url"],
        "member_resolution_method": method,
        "member_resolution_confidence": "high" if status == "exact" else "medium",
        "member_resolution_status": status,
        "authority_snapshot_hash": authority_snapshot_hash,
        "notes": "Resolved against local member authority snapshot.",
    }


def _output_row(
    record: dict[str, Any],
    token: str,
    token_index: int,
    token_count: int,
    resolution: dict[str, Any],
) -> dict[str, Any]:
    status = resolution["member_resolution_status"]
    if token_count > 1 and status in {"exact", "alias"}:
        row_status = "multi-person"
    else:
        row_status = status
    return {
        "source_stable_id": record["stable_id"],
        "source_file": record["source_file"],
        "source_row_number": int(record["source_row_number"]),
        "parliament_number": int(record["parliament_number"]),
        "parliament_document_id": record["parliament_document_id"],
        "document_type": record["document_type"],
        "document_content_date": record.get("document_content_date") or "",
        "member_of_parliament_raw": record["member_of_parliament_raw"],
        "member_raw_token": token,
        "member_token_index": token_index,
        "member_token_count": token_count,
        "multi_member_field": token_count > 1,
        "member_id": resolution["member_id"],
        "member_display_name": resolution["member_display_name"],
        "member_authority_source": resolution["member_authority_source"],
        "member_authority_url": resolution["member_authority_url"],
        "member_resolution_method": resolution["member_resolution_method"],
        "member_resolution_confidence": resolution["member_resolution_confidence"],
        "member_resolution_status": row_status,
        "review_status": "needs-review"
        if status in {"unresolved", "ambiguous", "conflict"}
        else "unreviewed",
        "release_status": "blocked-pending-validation",
        "source_hash": record["source_hash"],
        "authority_snapshot_hash": resolution["authority_snapshot_hash"],
        "notes": resolution["notes"],
    }


def _records_from_parquet(parquet_path: Path) -> list[dict[str, Any]]:
    columns = [
        "stable_id",
        "source_file",
        "source_row_number",
        "parliament_number",
        "parliament_document_id",
        "document_type",
        "document_content_date",
        "member_of_parliament_raw",
        "source_hash",
    ]
    table = pq.read_table(parquet_path, columns=columns)
    return table.to_pylist()


def _source_summary() -> dict[str, Any]:
    discovery = _read_json(SCHEMA_DISCOVERY_PATH)
    inventory = _read_json(SOURCE_INVENTORY_PATH)
    return {
        "source_archive": inventory["source_archive"]["path"],
        "source_archive_sha256": inventory["source_archive"]["sha256"],
        "source_inventory_manifest": SOURCE_INVENTORY_PATH.relative_to(ROOT).as_posix(),
        "schema_discovery_manifest": SCHEMA_DISCOVERY_PATH.relative_to(ROOT).as_posix(),
        "total_rows_from_schema_discovery": discovery["summary"]["total_rows"],
        "file_count": discovery["summary"]["file_count"],
        "member_bearing_fields": ["member_of_parliament_raw"],
        "upstream_member_field": "MemberOfParliament",
    }


def _blocked_manifest(reason: str, generated_at: str) -> dict[str, Any]:
    summary = _source_summary()
    return {
        "artifact_name": "corpus_wide_member_identity",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked",
        "release_gate_status": "blocked-pending-corpus-artifact",
        "track_id": TRACK_ID,
        "counts": {
            "source_rows_from_schema_discovery": int(summary["total_rows_from_schema_discovery"]),
            "source_files_from_schema_discovery": int(summary["file_count"]),
            "derived_rows": 0,
            "review_queue_rows": 0,
            "exact": 0,
            "alias": 0,
            "multi-person": 0,
            "unresolved": 0,
            "ambiguous": 0,
            "conflict": 0,
        },
        "errors": [reason],
        "warnings": [
            "No corpus-wide member identity artifact is published until normalized records are available and validation is rerun."
        ],
        "source_hashes": {
            "authority_snapshot": _sha256_path(AUTHORITY_PATH),
            "source_inventory": _sha256_path(SOURCE_INVENTORY_PATH),
            "schema_discovery": _sha256_path(SCHEMA_DISCOVERY_PATH),
        },
        "source_manifests": [
            "manifests/source_inventory.json",
            "manifests/schema_discovery.json",
            "derived/corpus_wide_member_identity_authority.json",
        ],
        "input_artifacts": {
            "normalized_parquet": DEFAULT_PARQUET.relative_to(ROOT).as_posix(),
        },
        "source_summary": summary,
        "outputs": {},
        "release_decision": {
            "decision": "defer",
            "reason": reason,
            "public_claim": "No corpus-wide member identity release is published from this blocked manifest.",
        },
    }


def build_corpus_wide_release(
    *,
    parquet_path: Path = DEFAULT_PARQUET,
    output_csv: Path = OUTPUT_CSV,
    review_queue_csv: Path = REVIEW_QUEUE_CSV,
    overrides_csv: Path = OVERRIDES_CSV,
    manifest_path: Path = VALIDATION_MANIFEST_PATH,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    if not parquet_path.exists():
        manifest = _blocked_manifest(
            f"Normalized corpus artifact not found: {parquet_path.relative_to(ROOT).as_posix()}",
            generated_at,
        )
        _write_json(manifest, manifest_path)
        _write_csv([], review_queue_csv, REVIEW_QUEUE_COLUMNS)
        if not overrides_csv.exists():
            _write_csv(
                [],
                overrides_csv,
                [
                    "source_stable_id",
                    "member_raw_token",
                    "reviewed_member_id",
                    "reviewer",
                    "review_date",
                    "notes",
                ],
            )
        return manifest

    authority = _read_json(AUTHORITY_PATH)
    lookup = _authority_lookup(authority)
    authority_snapshot = _authority_snapshot_hash(authority)
    rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    source_records = _records_from_parquet(parquet_path)

    for record in source_records:
        tokens = _split_members(record.get("member_of_parliament_raw"))
        for index, token in enumerate(tokens, start=1):
            resolution = _resolve_token(
                token=token,
                lookup=lookup,
                authority_snapshot_hash=authority_snapshot,
            )
            row = _output_row(record, token, index, len(tokens), resolution)
            rows.append(row)
            if row["member_resolution_status"] in {"unresolved", "ambiguous", "conflict"}:
                review_row = dict(row)
                review_row["review_reason"] = row["member_resolution_status"]
                review_rows.append(review_row)

    _write_csv(rows, output_csv, OUTPUT_COLUMNS)
    _write_csv(review_rows, review_queue_csv, REVIEW_QUEUE_COLUMNS)
    if not overrides_csv.exists():
        _write_csv(
            [],
            overrides_csv,
            [
                "source_stable_id",
                "member_raw_token",
                "reviewed_member_id",
                "reviewer",
                "review_date",
                "notes",
            ],
        )

    status_counts = Counter(row["member_resolution_status"] for row in rows)
    summary = _source_summary()
    manifest = {
        "artifact_name": "corpus_wide_member_identity",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked",
        "release_gate_status": "blocked-pending-authority-coverage-review",
        "track_id": TRACK_ID,
        "counts": {
            "source_rows_from_schema_discovery": int(summary["total_rows_from_schema_discovery"]),
            "source_files_from_schema_discovery": int(summary["file_count"]),
            "source_rows_read": len(source_records),
            "source_rows_with_member_field": sum(
                1
                for record in source_records
                if _split_members(record.get("member_of_parliament_raw"))
            ),
            "derived_rows": len(rows),
            "review_queue_rows": len(review_rows),
            "exact": status_counts.get("exact", 0),
            "alias": status_counts.get("alias", 0),
            "multi-person": status_counts.get("multi-person", 0),
            "unresolved": status_counts.get("unresolved", 0),
            "ambiguous": status_counts.get("ambiguous", 0),
            "conflict": status_counts.get("conflict", 0),
        },
        "errors": [
            "Authority snapshot is corpus-derived and not yet human-validated against official sources; corpus-wide publication is deferred until authority coverage is reviewed."
        ],
        "warnings": [
            "Artifact is generated as blocked-pending-validation and must not be published as a validated component."
        ],
        "source_hashes": {
            "authority_snapshot": authority_snapshot,
            "normalized_parquet": _sha256_path(parquet_path),
            "source_inventory": _sha256_path(SOURCE_INVENTORY_PATH),
            "schema_discovery": _sha256_path(SCHEMA_DISCOVERY_PATH),
        },
        "source_manifests": [
            "manifests/source_inventory.json",
            "manifests/schema_discovery.json",
            "derived/corpus_wide_member_identity_authority.json",
        ],
        "input_artifacts": {
            "normalized_parquet": parquet_path.relative_to(ROOT).as_posix()
            if parquet_path.is_relative_to(ROOT)
            else str(parquet_path),
        },
        "outputs": {
            "member_identity_csv": output_csv.relative_to(ROOT).as_posix()
            if output_csv.is_relative_to(ROOT)
            else str(output_csv),
            "review_queue_csv": review_queue_csv.relative_to(ROOT).as_posix()
            if review_queue_csv.is_relative_to(ROOT)
            else str(review_queue_csv),
            "review_overrides_csv": overrides_csv.relative_to(ROOT).as_posix()
            if overrides_csv.is_relative_to(ROOT)
            else str(overrides_csv),
            "schema": SCHEMA_PATH.relative_to(ROOT).as_posix(),
        },
        "source_summary": summary,
        "release_decision": {
            "decision": "defer",
            "reason": "Generated output remains blocked until authority coverage, unresolved cases, and human review gates are complete.",
            "public_claim": "This is a corpus-wide blocked derived component, not a validated public member identity release.",
        },
    }
    _write_json(manifest, manifest_path)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build corpus-wide member identity release artifacts."
    )
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    parser.add_argument("--output-csv", type=Path, default=OUTPUT_CSV)
    parser.add_argument("--review-queue-csv", type=Path, default=REVIEW_QUEUE_CSV)
    parser.add_argument("--overrides-csv", type=Path, default=OVERRIDES_CSV)
    parser.add_argument("--manifest", type=Path, default=VALIDATION_MANIFEST_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_corpus_wide_release(
        parquet_path=args.parquet,
        output_csv=args.output_csv,
        review_queue_csv=args.review_queue_csv,
        overrides_csv=args.overrides_csv,
        manifest_path=args.manifest,
    )
    print(f"Wrote {args.manifest}")
    print(f"Release gate: {manifest['release_gate_status']}")
    print(f"Derived rows: {manifest['counts']['derived_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
