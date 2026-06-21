"""Build the Bills API integration validation surface."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "bills_api_integration_20260612"
DEFAULT_MANIFEST = ROOT / "manifests/bills_api_integration_validation.json"
DEFAULT_CROSSREF = ROOT / "derived/bills_api/member_hansard_cross_reference.json"
DEFAULT_LEGACY_CROSSREF = ROOT / "derived/crossref_bills_api.json"
DEFAULT_DOC = ROOT / "docs/bills-api-integration.md"

BILLS_API_DIR = ROOT / "derived/bills_api"
AUTHORITY_SOURCES_PATH = ROOT / "manifests/authority_sources.json"
MEMBER_IDENTITY_VALIDATION_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
MEMBER_IDENTITY_CSV_PATH = ROOT / "derived/corpus_wide_member_identity/member_identity.csv"
VOTE_MOTION_BILL_QUESTION_MANIFEST_PATH = (
    ROOT / "manifests/vote_motion_bill_question_extraction_validation.json"
)
RUN_LOG_PATH = BILLS_API_DIR / "run_log.txt"
FACETS_PATH = BILLS_API_DIR / "facets.json"

HONORIFIC_RE = re.compile(
    r"^(rt\s+hon|hon|dr|sir|dame|mr|mrs|ms|miss|prof)\s+",
    flags=re.IGNORECASE,
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _latest_file(pattern: str) -> Path:
    matches = sorted(BILLS_API_DIR.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No Bills API artifact matched {pattern}")
    return matches[-1]


def _normalize_name(value: str) -> str:
    value = HONORIFIC_RE.sub("", value.strip())
    value = re.sub(r"\s+", " ", value)
    return value.casefold()


def _source_exists(source_id: str) -> bool:
    authority_sources = _read_json(AUTHORITY_SOURCES_PATH)
    return any(source.get("id") == source_id for source in authority_sources["sources"])


def _corpus_member_names() -> set[str]:
    names: set[str] = set()
    with MEMBER_IDENTITY_CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            for key in ("member_raw_token", "member_display_name"):
                value = row.get(key, "").strip()
                if value:
                    names.add(_normalize_name(value))
    return names


def _run_log_counts() -> dict[str, int]:
    text = RUN_LOG_PATH.read_text(encoding="utf-8")
    return {
        "bill_summaries_fetched": int(re.search(r"Fetched (\d+) bill summaries", text).group(1)),
        "bill_details_processed": int(re.search(r"Processed (\d+) bill details", text).group(1)),
        "unique_member_names": int(re.search(r"Unique member names found: (\d+)", text).group(1)),
    }


def _artifact_state(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    valid_json = True
    try:
        json.loads(text)
    except json.JSONDecodeError:
        valid_json = False
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": _sha256_path(path),
        "valid_json": valid_json,
        "truncated": text.rstrip().endswith("... (truncated)"),
    }


def _stage_labels(facets: dict[str, Any]) -> list[str]:
    for key in ("documentStages", "billStages", "stages"):
        values = facets.get(key)
        if isinstance(values, list):
            labels: list[str] = []
            for value in values:
                if isinstance(value, dict):
                    labels.append(
                        str(value.get("name") or value.get("label") or value.get("title"))
                    )
                else:
                    labels.append(str(value))
            return sorted(label for label in labels if label and label != "None")
    return []


def build_bills_api_integration(
    *,
    manifest_path: Path | None = DEFAULT_MANIFEST,
    crossref_path: Path | None = DEFAULT_CROSSREF,
    legacy_crossref_path: Path | None = DEFAULT_LEGACY_CROSSREF,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    members_path = _latest_file("bills_members_*.json")
    summary_path = _latest_file("bills_summary_*.json")
    details_path = _latest_file("bills_details_*.json")
    members_payload = _read_json(members_path)
    facets = _read_json(FACETS_PATH)
    run_counts = _run_log_counts()
    corpus_names = _corpus_member_names()
    bill_names = members_payload["unique_members"]
    matched_names = [name for name in bill_names if _normalize_name(name) in corpus_names]
    unmatched_names = [name for name in bill_names if _normalize_name(name) not in corpus_names]

    crossref = {
        "artifact_name": "bills_api_member_hansard_cross_reference",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "track_id": TRACK_ID,
        "status": "review-evidence",
        "source_artifact": members_path.relative_to(ROOT).as_posix(),
        "counts": {
            "bills_api_members": len(bill_names),
            "hansard_member_name_keys": len(corpus_names),
            "exact_or_honorific_normalized_matches": len(matched_names),
            "unmatched_bills_api_members": len(unmatched_names),
        },
        "matched_names": matched_names,
        "unmatched_names": unmatched_names,
        "warnings": [
            "Cross-reference is name-normalized evidence only, not validated member identity resolution.",
            "Corpus-wide member identity remains blocked pending authority coverage review.",
        ],
    }
    if crossref_path is not None:
        _write_json(crossref_path, crossref)
    if legacy_crossref_path is not None:
        _write_json(
            legacy_crossref_path,
            {
                "artifact_name": "bills_api_crossref_summary",
                "generated_at": generated_at,
                "status": "superseded-by-member-hansard-cross-reference",
                "bills_api_members_count": len(bill_names),
                "hansard_exact_or_honorific_normalized_matches": len(matched_names),
                "unmatched_bills_api_members": len(unmatched_names),
                "cross_reference_artifact": DEFAULT_CROSSREF.relative_to(ROOT).as_posix(),
            },
        )

    manifest = {
        "artifact_name": "bills_api_integration_validation",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "track_id": TRACK_ID,
        "validation_status": "review-evidence",
        "release_gate_status": "deferred-pending-full-stage-record-capture",
        "authority_source_id": "nz-parliament-bills-api",
        "authority_source_registered": _source_exists("nz-parliament-bills-api"),
        "extraction_run": {
            **run_counts,
            "members_artifact_count": members_payload["member_count"],
            "members_artifact_total_bills": members_payload["total_bills"],
            "members_artifact_total_details": members_payload["total_details"],
        },
        "captured_artifacts": {
            "facets": _artifact_state(FACETS_PATH),
            "members": _artifact_state(members_path),
            "summary": _artifact_state(summary_path),
            "details": _artifact_state(details_path),
            "run_log": {
                "path": RUN_LOG_PATH.relative_to(ROOT).as_posix(),
                "size_bytes": RUN_LOG_PATH.stat().st_size,
                "sha256": _sha256_path(RUN_LOG_PATH),
            },
        },
        "member_cross_reference": {
            "artifact": DEFAULT_CROSSREF.relative_to(ROOT).as_posix(),
            "counts": crossref["counts"],
            "status": crossref["status"],
        },
        "corpus_metadata_integration": {
            "status": "deferred",
            "metadata_source": "nz-parliament-bills-api",
            "bill_stage_labels": _stage_labels(facets),
            "bill_stage_source_available": True,
            "integration_target": "vote_motion_bill_question_extraction_validation",
            "reason": (
                "The extraction run captured full counts and member evidence, but summary/detail "
                "JSON files were stored as truncated review artifacts. Full bill-stage corpus "
                "metadata requires a non-truncated record capture before publication."
            ),
        },
        "source_manifests": [
            "manifests/authority_sources.json",
            "manifests/corpus_wide_member_identity_validation.json",
            "manifests/vote_motion_bill_question_extraction_validation.json",
        ],
        "source_hashes": {
            "authority_sources": _sha256_path(AUTHORITY_SOURCES_PATH),
            "member_identity_validation": _sha256_path(MEMBER_IDENTITY_VALIDATION_PATH),
            "vote_motion_bill_question_validation": _sha256_path(
                VOTE_MOTION_BILL_QUESTION_MANIFEST_PATH
            ),
        },
        "warnings": [
            "Do not publish truncated summary/detail artifacts as complete Bills API records.",
            "Member cross-reference is evidence only while corpus-wide member identity is blocked.",
        ],
    }
    if manifest_path is not None:
        _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Bills API integration validation.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--crossref", type=Path, default=DEFAULT_CROSSREF)
    parser.add_argument("--legacy-crossref", type=Path, default=DEFAULT_LEGACY_CROSSREF)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_bills_api_integration(
        manifest_path=args.manifest,
        crossref_path=args.crossref,
        legacy_crossref_path=args.legacy_crossref,
    )
    counts = manifest["extraction_run"]
    print(f"Wrote {args.manifest}")
    print(f"Bill details processed: {counts['bill_details_processed']}")
    print(f"Member names extracted: {counts['unique_member_names']}")
    print(f"Metadata integration: {manifest['corpus_metadata_integration']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
