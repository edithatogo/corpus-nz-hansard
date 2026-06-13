"""Build corpus-wide party attribution artifacts from normalized Hansard records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

try:
    from scripts.canonical_ids import canonical_id
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.canonical_ids import canonical_id

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARQUET = ROOT / "generated/parquet/hansard.parquet"
AUTHORITY_PATH = ROOT / "derived/party_attribution_authority.json"
MEMBER_IDENTITY_VALIDATION_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
SCHEMA_DISCOVERY_PATH = ROOT / "manifests/schema_discovery.json"
SOURCE_INVENTORY_PATH = ROOT / "manifests/source_inventory.json"
SCHEMA_PATH = ROOT / "schemas/corpus_wide_party_attribution.schema.json"
OUTPUT_DIR = ROOT / "derived/corpus_wide_party_attribution"
OUTPUT_CSV = OUTPUT_DIR / "party_attribution.csv"
REVIEW_QUEUE_CSV = OUTPUT_DIR / "party_attribution_review_queue.csv"
OVERRIDES_CSV = OUTPUT_DIR / "party_attribution_review_overrides.csv"
VALIDATION_MANIFEST_PATH = ROOT / "manifests/corpus_wide_party_attribution_validation.json"
DOC_PATH = ROOT / "docs/corpus-wide-party-attribution-release.md"
TRACK_ID = "corpus_wide_party_attribution_release_20260610"

OUTPUT_COLUMNS = [
    "source_stable_id",
    "source_file",
    "source_row_number",
    "parliament_number",
    "parliament_document_id",
    "document_type",
    "document_content_date",
    "party_vote_side",
    "party_label_raw",
    "party_label_normalized",
    "party_vote_count",
    "party_id",
    "party_attribution_source",
    "party_attribution_url",
    "party_attribution_method",
    "party_attribution_confidence",
    "party_attribution_status",
    "member_id",
    "member_display_name",
    "member_identity_status",
    "dependency_state",
    "review_status",
    "release_status",
    "source_hash",
    "authority_snapshot_hash",
    "notes",
]

REVIEW_QUEUE_COLUMNS = OUTPUT_COLUMNS + ["review_reason"]

PARTY_SEGMENT_RE = re.compile(
    r"\b(Ayes|Noes)\s+\d+(.*?)(?=\bAyes\b|\bNoes\b|Motion agreed to|Motion not agreed to|Bill read|The question was put|$)",
    re.IGNORECASE | re.DOTALL,
)


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


def _normalize_label(value: str) -> str:
    return " ".join(value.split())


def _extract_vote_labels(text: str) -> list[dict[str, Any]]:
    labels: list[dict[str, Any]] = []
    for match in PARTY_SEGMENT_RE.finditer(text or ""):
        side = match.group(1).title()
        segment = match.group(2)
        for chunk in segment.split(";"):
            cleaned = _normalize_label(chunk.strip(" ."))
            if not cleaned:
                continue
            count_match = re.match(r"^(.*?)(?:\s+(\d+))?$", cleaned)
            if not count_match:
                continue
            label = _normalize_label(count_match.group(1).strip())
            count = int(count_match.group(2)) if count_match.group(2) else None
            if label:
                labels.append(
                    {"party_vote_side": side, "party_label_raw": label, "party_vote_count": count}
                )
    return labels


def _records_from_parquet(parquet_path: Path) -> list[dict[str, Any]]:
    columns = [
        "stable_id",
        "source_file",
        "source_row_number",
        "parliament_number",
        "parliament_document_id",
        "document_type",
        "document_content_date",
        "content",
        "member_of_parliament_raw",
        "source_hash",
    ]
    pf = pq.ParquetFile(parquet_path)
    rows: list[dict[str, Any]] = []
    for batch in pf.iter_batches(batch_size=1000, columns=columns):
        rows.extend(batch.to_pylist())
    return rows


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
        "explicit_party_vote_labels": True,
    }


def _blocked_manifest(reason: str, generated_at: str) -> dict[str, Any]:
    summary = _source_summary()
    return {
        "artifact_name": "corpus_wide_party_attribution",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked",
        "release_gate_status": "blocked-pending-validated-member-identity",
        "track_id": TRACK_ID,
        "counts": {
            "source_rows_from_schema_discovery": int(summary["total_rows_from_schema_discovery"]),
            "source_files_from_schema_discovery": int(summary["file_count"]),
            "derived_rows": 0,
            "review_queue_rows": 0,
            "explicit_party_labels": 0,
            "unresolved_member_dependency": 0,
            "authoritative": 0,
            "alias": 0,
            "ambiguous": 0,
            "unresolved": 0,
            "excluded": 0,
            "blocked": 0,
        },
        "errors": [reason],
        "warnings": [
            "No corpus-wide party attribution release is published while validated member identity remains blocked."
        ],
        "source_hashes": {
            "authority_snapshot": _sha256_path(AUTHORITY_PATH),
            "member_identity_validation": _sha256_path(MEMBER_IDENTITY_VALIDATION_PATH)
            if MEMBER_IDENTITY_VALIDATION_PATH.exists()
            else "",
            "source_inventory": _sha256_path(SOURCE_INVENTORY_PATH),
            "schema_discovery": _sha256_path(SCHEMA_DISCOVERY_PATH),
        },
        "source_manifests": [
            "manifests/source_inventory.json",
            "manifests/schema_discovery.json",
            "derived/party_attribution_authority.json",
            "manifests/corpus_wide_member_identity_validation.json",
        ],
        "input_artifacts": {
            "normalized_parquet": DEFAULT_PARQUET.relative_to(ROOT).as_posix(),
            "member_identity_validation": MEMBER_IDENTITY_VALIDATION_PATH.relative_to(
                ROOT
            ).as_posix(),
        },
        "source_summary": summary,
        "outputs": {},
        "release_decision": {
            "decision": "defer",
            "reason": reason,
            "public_claim": "No corpus-wide party attribution release is published from this blocked manifest.",
        },
    }


def _output_row(
    record: dict[str, Any], vote_label: dict[str, Any], authority_hash: str
) -> dict[str, Any]:
    label = vote_label["party_label_raw"]
    normalized = _normalize_label(label)
    return {
        "source_stable_id": record["stable_id"],
        "source_file": record["source_file"],
        "source_row_number": int(record["source_row_number"]),
        "parliament_number": int(record["parliament_number"]),
        "parliament_document_id": record["parliament_document_id"] or "",
        "document_type": record["document_type"] or "",
        "document_content_date": record.get("document_content_date") or "",
        "party_vote_side": vote_label["party_vote_side"],
        "party_label_raw": label,
        "party_label_normalized": normalized,
        "party_vote_count": vote_label["party_vote_count"],
        "party_id": canonical_id("party", {"party_label": normalized}),
        "party_attribution_source": "explicit-party-vote-text",
        "party_attribution_url": "",
        "party_attribution_method": "explicit-party-label",
        "party_attribution_confidence": "high",
        "party_attribution_status": "authoritative",
        "member_id": "",
        "member_display_name": "",
        "member_identity_status": "blocked-pending-validated-member-identity",
        "dependency_state": "validated-member-identity-required",
        "review_status": "unreviewed",
        "release_status": "blocked-pending-validation",
        "source_hash": record["source_hash"],
        "authority_snapshot_hash": authority_hash,
        "notes": "Explicit party label extracted from vote text; member identity remains blocked for corpus-wide release.",
    }


def _review_row(record: dict[str, Any], authority_hash: str) -> dict[str, Any]:
    return {
        "source_stable_id": record["stable_id"],
        "source_file": record["source_file"],
        "source_row_number": int(record["source_row_number"]),
        "parliament_number": int(record["parliament_number"]),
        "parliament_document_id": record["parliament_document_id"] or "",
        "document_type": record["document_type"] or "",
        "document_content_date": record.get("document_content_date") or "",
        "party_vote_side": "",
        "party_label_raw": "",
        "party_label_normalized": "",
        "party_vote_count": None,
        "party_id": "",
        "party_attribution_source": "",
        "party_attribution_url": "",
        "party_attribution_method": "member-identity-blocked",
        "party_attribution_confidence": "none",
        "party_attribution_status": "blocked",
        "member_id": "",
        "member_display_name": "",
        "member_identity_status": "blocked-pending-validated-member-identity",
        "dependency_state": "member-identity-required",
        "review_status": "needs-review",
        "release_status": "blocked-pending-validation",
        "source_hash": record["source_hash"],
        "authority_snapshot_hash": authority_hash,
        "notes": "Party attribution remains blocked because validated member identity is not available.",
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
        _write_csv([], output_csv, OUTPUT_COLUMNS)
        _write_csv([], review_queue_csv, REVIEW_QUEUE_COLUMNS)
        if not overrides_csv.exists():
            _write_csv(
                [],
                overrides_csv,
                [
                    "source_stable_id",
                    "party_label_raw",
                    "reviewed_party_id",
                    "reviewer",
                    "review_date",
                    "notes",
                ],
            )
        return manifest

    authority = _read_json(AUTHORITY_PATH)
    authority_hash = _authority_snapshot_hash(authority)
    rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    source_records = _records_from_parquet(parquet_path)

    for record in source_records:
        if "vote" in (record.get("document_type") or "").lower():
            for vote_label in _extract_vote_labels(record.get("content") or ""):
                rows.append(_output_row(record, vote_label, authority_hash))
        elif record.get("member_of_parliament_raw"):
            review_rows.append(_review_row(record, authority_hash))

    _write_csv(rows, output_csv, OUTPUT_COLUMNS)
    _write_csv(review_rows, review_queue_csv, REVIEW_QUEUE_COLUMNS)
    if not overrides_csv.exists():
        _write_csv(
            [],
            overrides_csv,
            [
                "source_stable_id",
                "party_label_raw",
                "reviewed_party_id",
                "reviewer",
                "review_date",
                "notes",
            ],
        )

    label_counts = Counter(row["party_attribution_status"] for row in rows)
    summary = _source_summary()
    manifest = {
        "artifact_name": "corpus_wide_party_attribution",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked",
        "release_gate_status": "blocked-pending-validated-member-identity",
        "track_id": TRACK_ID,
        "counts": {
            "source_rows_from_schema_discovery": int(summary["total_rows_from_schema_discovery"]),
            "source_files_from_schema_discovery": int(summary["file_count"]),
            "source_rows_read": len(source_records),
            "derived_rows": len(rows),
            "review_queue_rows": len(review_rows),
            "explicit_party_labels": len(rows),
            "unresolved_member_dependency": len(review_rows),
            "authoritative": label_counts.get("authoritative", 0),
            "alias": label_counts.get("alias", 0),
            "ambiguous": label_counts.get("ambiguous", 0),
            "unresolved": label_counts.get("unresolved", 0),
            "blocked": label_counts.get("blocked", 0),
            "excluded": 0,
        },
        "errors": [
            "Validated member identity output must be available before corpus-wide party attribution can be promoted."
        ],
        "warnings": [
            "Explicit party-vote labels can be extracted, but the release remains blocked until member identity is validated."
        ],
        "source_hashes": {
            "authority_snapshot": authority_hash,
            "normalized_parquet": _sha256_path(parquet_path),
            "member_identity_validation": _sha256_path(MEMBER_IDENTITY_VALIDATION_PATH)
            if MEMBER_IDENTITY_VALIDATION_PATH.exists()
            else "",
            "source_inventory": _sha256_path(SOURCE_INVENTORY_PATH),
            "schema_discovery": _sha256_path(SCHEMA_DISCOVERY_PATH),
        },
        "source_manifests": [
            "manifests/source_inventory.json",
            "manifests/schema_discovery.json",
            "derived/party_attribution_authority.json",
            "manifests/corpus_wide_member_identity_validation.json",
        ],
        "input_artifacts": {
            "normalized_parquet": parquet_path.relative_to(ROOT).as_posix()
            if parquet_path.is_relative_to(ROOT)
            else str(parquet_path),
            "member_identity_validation": MEMBER_IDENTITY_VALIDATION_PATH.relative_to(
                ROOT
            ).as_posix(),
        },
        "outputs": {
            "party_attribution_csv": output_csv.relative_to(ROOT).as_posix()
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
            "reason": "Validated member identity is not available in this working tree.",
            "public_claim": "This is a corpus-wide blocked derived component, not a validated public party attribution release.",
        },
    }
    _write_json(manifest, manifest_path)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build corpus-wide party attribution release artifacts."
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
