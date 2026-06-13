"""Build the validated speech-turn component release surface."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

try:
    from scripts.canonical_ids import canonical_id
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.canonical_ids import canonical_id

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATE = ROOT / "generated/parquet/hansard_speech_turns.parquet"
DEFAULT_OUTPUT = ROOT / "generated/derived/hansard_speech_turns_validated.parquet"
DEFAULT_REVIEW_QUEUE = ROOT / "derived/validated_speech_turns/speech_turn_review_queue.csv"
DEFAULT_OVERRIDES = ROOT / "derived/validated_speech_turns/speech_turn_review_overrides.csv"
DEFAULT_MANIFEST = ROOT / "manifests/validated_speech_turn_component_validation.json"
SCHEMA_PATH = ROOT / "schemas/validated_speech_turn_component.schema.json"
DOC_PATH = ROOT / "docs/validated-speech-turn-component-release.md"
MEMBER_IDENTITY_VALIDATION_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
SEGMENTATION_VALIDATION_PATH = ROOT / "manifests/speech_turn_segmentation_validation.json"
RELEASE_DECISION_PATH = ROOT / "manifests/speech_turn_release_decision.json"
TRACK_ID = "validated_speech_turn_component_release_20260610"

OUTPUT_COLUMNS = [
    "turn_id",
    "source_stable_id",
    "source_file",
    "source_row_number",
    "parliament_document_id",
    "parliament_number",
    "document_type",
    "title",
    "turn_index",
    "speaker_candidate",
    "speaker_member_id",
    "speaker_identity_status",
    "speaker_resolution_confidence",
    "speech_text",
    "source_selector",
    "confidence",
    "method",
    "review_status",
    "release_status",
    "source_hash",
    "validation_hash",
    "notes",
]

REVIEW_QUEUE_COLUMNS = OUTPUT_COLUMNS + ["review_reason"]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


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


def _turn_id(record: dict[str, Any]) -> str:
    payload = {
        "candidate_method": record.get("method", ""),
        "document_id": record.get("parliament_document_id", ""),
        "row_number": record.get("source_row_number", 0),
        "speaker_candidate": record.get("speaker_candidate", ""),
        "turn_index": record.get("turn_index", 0),
        "validation_manifest": DEFAULT_MANIFEST.relative_to(ROOT).as_posix(),
    }
    return canonical_id("speech-turn", payload)


def _source_selector(record: dict[str, Any]) -> str:
    return f"{record.get('parliament_document_id', '')}#turn-{int(record.get('turn_index', 0))}"


def _output_row(
    record: dict[str, Any],
    *,
    member_identity_ready: bool,
    member_identity_hash: str,
) -> dict[str, Any]:
    source_hash_payload = json.dumps(
        {
            "parliament_document_id": record.get("parliament_document_id"),
            "turn_index": record.get("turn_index"),
            "speaker_candidate": record.get("speaker_candidate"),
            "speech_text": record.get("speech_text"),
            "method": record.get("method"),
            "confidence": record.get("confidence"),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    turn_id = _turn_id(record)
    identity_status = (
        "validated" if member_identity_ready else "blocked-pending-validated-member-identity"
    )
    release_status = (
        "validated-component" if member_identity_ready else "blocked-pending-validation"
    )
    review_status = "reviewed" if member_identity_ready else "needs-review"
    speaker_member_id = record.get("speaker_member_id") or ""
    return {
        "turn_id": turn_id,
        "source_stable_id": record.get("parliament_document_id") or "",
        "source_file": record.get("source_file") or "",
        "source_row_number": int(record.get("source_row_number") or 0),
        "parliament_document_id": record.get("parliament_document_id") or "",
        "parliament_number": int(record.get("parliament_number") or 0),
        "document_type": record.get("document_type") or "",
        "title": record.get("title") or "",
        "turn_index": int(record.get("turn_index") or 0),
        "speaker_candidate": record.get("speaker_candidate") or "",
        "speaker_member_id": speaker_member_id,
        "speaker_identity_status": identity_status,
        "speaker_resolution_confidence": "medium" if not member_identity_ready else "high",
        "speech_text": record.get("speech_text") or "",
        "source_selector": _source_selector(record),
        "confidence": record.get("confidence") or "medium",
        "method": record.get("method") or "tab_colon_marker_v1",
        "review_status": review_status,
        "release_status": release_status,
        "source_hash": _sha256_text(source_hash_payload),
        "validation_hash": _sha256_text(f"{turn_id}|{member_identity_hash}|{source_hash_payload}"),
        "notes": (
            "Validated speech-turn promotion is blocked until member identity is validated."
            if not member_identity_ready
            else "Validated speech-turn row."
        ),
    }


def _candidate_records_from_parquet(candidate_path: Path) -> list[dict[str, Any]]:
    columns = [
        "parliament_document_id",
        "parliament_number",
        "document_type",
        "title",
        "source_file",
        "source_row_number",
        "turn_index",
        "speaker_candidate",
        "speech_text",
        "confidence",
        "method",
    ]
    table = pq.read_table(candidate_path, columns=columns)
    return table.to_pylist()


def _source_summary() -> dict[str, Any]:
    segmentation = _read_json(SEGMENTATION_VALIDATION_PATH)
    member_identity = (
        _read_json(MEMBER_IDENTITY_VALIDATION_PATH)
        if MEMBER_IDENTITY_VALIDATION_PATH.exists()
        else {}
    )
    return {
        "segmentation_validation_manifest": SEGMENTATION_VALIDATION_PATH.relative_to(
            ROOT
        ).as_posix(),
        "release_decision_manifest": RELEASE_DECISION_PATH.relative_to(ROOT).as_posix(),
        "member_identity_validation_manifest": MEMBER_IDENTITY_VALIDATION_PATH.relative_to(
            ROOT
        ).as_posix(),
        "documents_read": segmentation["summary"]["documents_read"],
        "documents_with_turns": segmentation["summary"]["documents_with_turns"],
        "documents_without_turns": segmentation["summary"]["documents_without_turns"],
        "candidate_turns_written": segmentation["summary"]["turns_written"],
        "candidate_medium_confidence": segmentation["summary"]["confidence_counts"].get(
            "medium", 0
        ),
        "member_identity_ok": member_identity.get("ok") if member_identity else False,
    }


def _blocked_manifest(reason: str, generated_at: str, candidate_exists: bool) -> dict[str, Any]:
    summary = _source_summary()
    return {
        "artifact_name": "validated_speech_turn_component",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked",
        "release_gate_status": (
            "blocked-pending-validated-member-identity"
            if candidate_exists
            else "blocked-pending-candidate-artifact"
        ),
        "track_id": TRACK_ID,
        "counts": {
            "documents_read": int(summary["documents_read"]),
            "documents_with_turns": int(summary["documents_with_turns"]),
            "documents_without_turns": int(summary["documents_without_turns"]),
            "candidate_turns_written": int(summary["candidate_turns_written"]),
            "candidate_medium_confidence": int(summary["candidate_medium_confidence"]),
            "validated_rows": 0,
            "review_queue_rows": 0,
            "validated_speaker_identity": 0,
            "blocked_speaker_identity": 0,
        },
        "errors": [reason],
        "warnings": [
            "Speech-turn promotion remains blocked until validated member identity is available.",
            "The public final scope still excludes heuristic candidates.",
        ],
        "source_hashes": {
            "segmentation_validation": _sha256_path(SEGMENTATION_VALIDATION_PATH),
            "speech_turn_release_decision": _sha256_path(RELEASE_DECISION_PATH),
            "member_identity_validation": _sha256_path(MEMBER_IDENTITY_VALIDATION_PATH)
            if MEMBER_IDENTITY_VALIDATION_PATH.exists()
            else "",
        },
        "source_manifests": [
            "manifests/speech_turn_segmentation_validation.json",
            "manifests/speech_turn_release_decision.json",
            "docs/speech-turn-release-decision.md",
            "manifests/corpus_wide_member_identity_validation.json",
        ],
        "input_artifacts": {
            "candidate_parquet": DEFAULT_CANDIDATE.relative_to(ROOT).as_posix(),
            "member_identity_validation": MEMBER_IDENTITY_VALIDATION_PATH.relative_to(
                ROOT
            ).as_posix(),
            "segmentation_validation": SEGMENTATION_VALIDATION_PATH.relative_to(ROOT).as_posix(),
        },
        "source_summary": summary,
        "outputs": {},
        "release_decision": {
            "decision": "defer",
            "reason": reason,
            "public_claim": "No validated speech-turn release is published from this blocked manifest.",
        },
    }


def build_validated_speech_turn_component(
    *,
    candidate_parquet: Path = DEFAULT_CANDIDATE,
    output_parquet: Path = DEFAULT_OUTPUT,
    review_queue_csv: Path = DEFAULT_REVIEW_QUEUE,
    overrides_csv: Path = DEFAULT_OVERRIDES,
    manifest_path: Path = DEFAULT_MANIFEST,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    candidate_exists = candidate_parquet.exists()
    if not candidate_exists:
        manifest = _blocked_manifest(
            f"Candidate speech-turn parquet not found: {candidate_parquet.relative_to(ROOT).as_posix()}",
            generated_at,
            candidate_exists=False,
        )
        _write_json(manifest, manifest_path)
        _write_csv([], review_queue_csv, REVIEW_QUEUE_COLUMNS)
        if not overrides_csv.exists():
            _write_csv(
                [],
                overrides_csv,
                [
                    "turn_id",
                    "speaker_candidate",
                    "reviewed_member_id",
                    "reviewer",
                    "review_date",
                    "notes",
                ],
            )
        return manifest

    member_identity_ready = False
    member_identity_hash = ""
    if MEMBER_IDENTITY_VALIDATION_PATH.exists():
        member_identity = _read_json(MEMBER_IDENTITY_VALIDATION_PATH)
        member_identity_ready = (
            bool(member_identity.get("ok")) and member_identity.get("validation_status") == "ok"
        )
        member_identity_hash = _sha256_path(MEMBER_IDENTITY_VALIDATION_PATH)
    rows = [
        _output_row(
            record,
            member_identity_ready=member_identity_ready,
            member_identity_hash=member_identity_hash,
        )
        for record in _candidate_records_from_parquet(candidate_parquet)
    ]
    review_rows = [
        dict(
            row,
            review_reason="member-identity-required" if not member_identity_ready else "validated",
        )
        for row in rows
        if not member_identity_ready
    ]

    pq.write_table(pa.Table.from_pylist(rows), output_parquet) if rows else None
    _write_csv(review_rows, review_queue_csv, REVIEW_QUEUE_COLUMNS)
    if not overrides_csv.exists():
        _write_csv(
            [],
            overrides_csv,
            [
                "turn_id",
                "speaker_candidate",
                "reviewed_member_id",
                "reviewer",
                "review_date",
                "notes",
            ],
        )

    summary = _source_summary()
    manifest = {
        "artifact_name": "validated_speech_turn_component",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked" if not member_identity_ready else "ok",
        "release_gate_status": (
            "blocked-pending-validated-member-identity" if not member_identity_ready else "ready"
        ),
        "track_id": TRACK_ID,
        "counts": {
            "documents_read": int(summary["documents_read"]),
            "documents_with_turns": int(summary["documents_with_turns"]),
            "documents_without_turns": int(summary["documents_without_turns"]),
            "candidate_turns_written": len(rows),
            "candidate_medium_confidence": int(summary["candidate_medium_confidence"]),
            "validated_rows": len(rows),
            "review_queue_rows": len(review_rows),
            "validated_speaker_identity": len(rows) if member_identity_ready else 0,
            "blocked_speaker_identity": len(rows) if not member_identity_ready else 0,
        },
        "errors": []
        if member_identity_ready
        else [
            "Validated member identity is not available, so speech-turn promotion remains blocked."
        ],
        "warnings": [
            "Heuristic speech-turn candidates remain non-authoritative until member identity is validated.",
        ],
        "source_hashes": {
            "candidate_parquet": _sha256_path(candidate_parquet),
            "segmentation_validation": _sha256_path(SEGMENTATION_VALIDATION_PATH),
            "speech_turn_release_decision": _sha256_path(RELEASE_DECISION_PATH),
            "member_identity_validation": member_identity_hash,
        },
        "source_manifests": [
            "generated/parquet/hansard_speech_turns.parquet",
            "manifests/speech_turn_segmentation_validation.json",
            "manifests/speech_turn_release_decision.json",
            "docs/speech-turn-release-decision.md",
            "manifests/corpus_wide_member_identity_validation.json",
        ],
        "input_artifacts": {
            "candidate_parquet": candidate_parquet.relative_to(ROOT).as_posix()
            if candidate_parquet.is_relative_to(ROOT)
            else str(candidate_parquet),
            "member_identity_validation": MEMBER_IDENTITY_VALIDATION_PATH.relative_to(
                ROOT
            ).as_posix(),
        },
        "outputs": {
            "validated_parquet": output_parquet.relative_to(ROOT).as_posix()
            if output_parquet.is_relative_to(ROOT)
            else str(output_parquet),
            "review_queue_csv": review_queue_csv.relative_to(ROOT).as_posix()
            if review_queue_csv.is_relative_to(ROOT)
            else str(review_queue_csv),
        },
        "source_summary": summary,
        "release_decision": {
            "decision": "defer" if not member_identity_ready else "promote",
            "reason": "Validated member identity is not available"
            if not member_identity_ready
            else "Validated component criteria satisfied.",
            "public_claim": (
                "No validated speech-turn release is published from this blocked manifest."
                if not member_identity_ready
                else "Validated speech-turn component ready for downstream endpoint consumption."
            ),
        },
    }
    _write_json(manifest, manifest_path)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the validated speech-turn component release surface."
    )
    parser.add_argument("--candidate-parquet", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--output-parquet", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--review-queue-csv", type=Path, default=DEFAULT_REVIEW_QUEUE)
    parser.add_argument("--overrides-csv", type=Path, default=DEFAULT_OVERRIDES)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_validated_speech_turn_component(
        candidate_parquet=args.candidate_parquet,
        output_parquet=args.output_parquet,
        review_queue_csv=args.review_queue_csv,
        overrides_csv=args.overrides_csv,
        manifest_path=args.manifest,
    )
    print(f"Wrote {args.manifest}")
    print(f"Release gate: {manifest['release_gate_status']}")
    print(f"Validated rows: {manifest['counts']['validated_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
