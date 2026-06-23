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
DEFAULT_STAGE_METADATA = ROOT / "derived/bills_api/bill_stage_metadata.json"

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


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path | None, payload: Any) -> None:
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


def _artifact_state(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    valid_json = True
    record_count: int | None = None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        valid_json = False
    else:
        if isinstance(payload, (list, dict)):
            record_count = len(payload)
    state: dict[str, Any] = {
        "path": path.relative_to(ROOT).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": _sha256_path(path),
        "valid_json": valid_json,
        "truncated": text.rstrip().endswith("... (truncated)"),
    }
    if record_count is not None:
        state["record_count"] = record_count
    return state


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


def _member_names_from_bill(bill: dict[str, Any]) -> list[str]:
    names = []
    for member in bill.get("Members", []) or []:
        name = member.get("PreferredFormOfAddress") or member.get("DisplayName")
        if name:
            names.append(str(name))
    return names


def _build_stage_metadata(details: list[dict[str, Any]], *, generated_at: str) -> dict[str, Any]:
    bill_records: list[dict[str, Any]] = []
    stage_records: list[dict[str, Any]] = []
    for bill in details:
        bill_id = str(bill.get("Id") or "")
        bill_records.append(
            {
                "bill_id": bill_id,
                "title": bill.get("Title"),
                "parliament_number": bill.get("ParliamentNumber"),
                "bill_number": bill.get("BillNumber"),
                "bill_type": bill.get("BillTypeName"),
                "bill_status": bill.get("BillStatusName"),
                "current_stage": bill.get("BillCurrentStageName"),
                "legislation_url": bill.get("BillLegislationUrl"),
                "members": _member_names_from_bill(bill),
            }
        )
        for stage in bill.get("Stages", []) or []:
            stage_records.append(
                {
                    "bill_id": bill_id,
                    "stage_id": stage.get("Id"),
                    "stage_code": stage.get("StageCode"),
                    "stage_name": stage.get("StageName"),
                    "stage_date": stage.get("StageDate"),
                    "outcome": stage.get("OutcomeName"),
                    "type": stage.get("TypeName"),
                    "start_date": stage.get("StartDate"),
                    "end_date": stage.get("EndDate"),
                }
            )
    return {
        "artifact_name": "bills_api_bill_stage_metadata",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "track_id": TRACK_ID,
        "source": "nz-parliament-bills-api",
        "status": "metadata-ready",
        "counts": {
            "bills": len(bill_records),
            "stage_records": len(stage_records),
        },
        "bills": bill_records,
        "stages": stage_records,
    }


def build_bills_api_integration(
    *,
    manifest_path: Path | None = DEFAULT_MANIFEST,
    crossref_path: Path | None = DEFAULT_CROSSREF,
    legacy_crossref_path: Path | None = DEFAULT_LEGACY_CROSSREF,
    stage_metadata_path: Path | None = DEFAULT_STAGE_METADATA,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    members_path = _latest_file("bills_members_*.json")
    summary_path = _latest_file("bills_summary_*.json")
    details_path = _latest_file("bills_details_*.json")
    members_payload = _read_json(members_path)
    summary_payload = _read_json(summary_path)
    details_payload = _read_json(details_path)
    facets = _read_json(FACETS_PATH)

    if not isinstance(summary_payload, list):
        raise ValueError("Bills summary artifact must be a JSON array.")
    if not isinstance(details_payload, list):
        raise ValueError("Bills details artifact must be a JSON array.")

    corpus_names = _corpus_member_names()
    bill_names = members_payload["unique_members"]
    matched_names = [name for name in bill_names if _normalize_name(name) in corpus_names]
    unmatched_names = [name for name in bill_names if _normalize_name(name) not in corpus_names]

    stage_metadata = _build_stage_metadata(details_payload, generated_at=generated_at)
    _write_json(stage_metadata_path, stage_metadata)

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
    _write_json(crossref_path, crossref)
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

    summary_state = _artifact_state(summary_path)
    details_state = _artifact_state(details_path)
    complete_capture = (
        summary_state["valid_json"]
        and details_state["valid_json"]
        and not summary_state["truncated"]
        and not details_state["truncated"]
        and summary_state.get("record_count") == members_payload["total_bills"]
        and details_state.get("record_count") == members_payload["total_details"]
    )
    metadata_status = "ready" if complete_capture else "deferred"
    release_gate_status = (
        "ready-for-corpus-metadata-integration"
        if complete_capture
        else "deferred-pending-full-stage-record-capture"
    )

    manifest = {
        "artifact_name": "bills_api_integration_validation",
        "artifact_version": "0.2.0",
        "generated_at": generated_at,
        "track_id": TRACK_ID,
        "validation_status": "metadata-ready" if complete_capture else "review-evidence",
        "release_gate_status": release_gate_status,
        "authority_source_id": "nz-parliament-bills-api",
        "authority_source_registered": _source_exists("nz-parliament-bills-api"),
        "extraction_run": {
            "bill_summaries_fetched": len(summary_payload),
            "bill_details_processed": len(details_payload),
            "unique_member_names": members_payload["member_count"],
            "members_artifact_count": members_payload["member_count"],
            "members_artifact_total_bills": members_payload["total_bills"],
            "members_artifact_total_details": members_payload["total_details"],
        },
        "captured_artifacts": {
            "facets": _artifact_state(FACETS_PATH),
            "members": _artifact_state(members_path),
            "summary": summary_state,
            "details": details_state,
            "bill_stage_metadata": _artifact_state(DEFAULT_STAGE_METADATA),
            "run_log": {
                "path": RUN_LOG_PATH.relative_to(ROOT).as_posix(),
                "size_bytes": RUN_LOG_PATH.stat().st_size,
                "sha256": _sha256_path(RUN_LOG_PATH),
                "status": "historical-run-log",
            },
        },
        "member_cross_reference": {
            "artifact": DEFAULT_CROSSREF.relative_to(ROOT).as_posix(),
            "counts": crossref["counts"],
            "status": crossref["status"],
        },
        "corpus_metadata_integration": {
            "status": metadata_status,
            "metadata_source": "nz-parliament-bills-api",
            "bill_stage_labels": _stage_labels(facets),
            "bill_stage_source_available": True,
            "integration_target": "vote_motion_bill_question_extraction_validation",
            "metadata_artifact": DEFAULT_STAGE_METADATA.relative_to(ROOT).as_posix(),
            "reason": (
                "Non-truncated Bills API summary and detail records are captured; derived bill-stage "
                "metadata is available for governed downstream corpus integration."
                if complete_capture
                else "Full bill-stage corpus metadata requires non-truncated summary/detail captures."
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
            "Member cross-reference is evidence only while corpus-wide member identity is blocked.",
            "Downstream publication must use governed release gates and not infer Hansard bill debate linkage from title matching alone.",
        ],
    }
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Bills API integration validation.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--crossref", type=Path, default=DEFAULT_CROSSREF)
    parser.add_argument("--legacy-crossref", type=Path, default=DEFAULT_LEGACY_CROSSREF)
    parser.add_argument("--stage-metadata", type=Path, default=DEFAULT_STAGE_METADATA)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_bills_api_integration(
        manifest_path=args.manifest,
        crossref_path=args.crossref,
        legacy_crossref_path=args.legacy_crossref,
        stage_metadata_path=args.stage_metadata,
    )
    counts = manifest["extraction_run"]
    print(f"Wrote {args.manifest}")
    print(f"Bill details processed: {counts['bill_details_processed']}")
    print(f"Member names extracted: {counts['unique_member_names']}")
    print(f"Metadata integration: {manifest['corpus_metadata_integration']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
