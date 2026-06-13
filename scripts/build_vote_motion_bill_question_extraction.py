"""Build the vote, motion, bill, and question extraction release surface."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from scripts.validate_derived_fields import gold_sample_counts
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.validate_derived_fields import gold_sample_counts

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "vote_motion_bill_question_extraction_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/vote_motion_bill_question_extraction_validation.json"
DEFAULT_COVERAGE = ROOT / "derived/vote_motion_bill_question_extraction/extraction_coverage.json"
DEFAULT_REVIEW = ROOT / "derived/vote_motion_bill_question_extraction/extraction_review.csv"

NEUTRAL_MODEL_PATH = ROOT / "manifests/neutral_component_model.json"
NEUTRAL_VALIDATION_PATH = ROOT / "manifests/neutral_component_validation_manifest.json"
NEUTRAL_FIXTURES_PATH = ROOT / "fixtures/neutral_components.json"
PROCEDURE_MODEL_PATH = ROOT / "manifests/nz_parliamentary_procedure_model.json"
PROCEDURE_FIXTURES_PATH = ROOT / "fixtures/nz_parliamentary_procedure_samples.json"
GOLD_MANIFEST_PATH = ROOT / "manifests/gold_evaluation_datasets.json"
GOLD_FIXTURES_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
MEMBER_IDENTITY_VALIDATION_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
PARTY_ATTRIBUTION_VALIDATION_PATH = ROOT / "manifests/corpus_wide_party_attribution_validation.json"
SITTING_PROCEEDING_VALIDATION_PATH = ROOT / "manifests/sitting_proceeding_component_validation.json"
AUTHORITY_SOURCES_PATH = ROOT / "manifests/authority_sources.json"
DOC_PATH = ROOT / "docs/vote-motion-bill-question-extraction-release.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
NEUTRAL_DOC_PATH = ROOT / "docs/neutral-component-model.md"
PROCEDURE_DOC_PATH = ROOT / "docs/nz-parliamentary-procedure-model.md"
TRACK_PATH = (
    ROOT / "conductor/tracks/vote_motion_bill_question_extraction_release_20260610/index.md"
)
SCHEMA_PATH = ROOT / "schemas/vote_motion_bill_question_extraction_validation.schema.json"

REVIEW_COLUMNS = [
    "sample_id",
    "category",
    "document_type",
    "source_stable_id",
    "extraction_family",
    "extraction_status",
    "dependency_blockers",
    "authority_source_ids",
    "uncertainty_status",
    "review_status",
    "review_notes",
]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _render_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _sample_family(category: str) -> str:
    return {
        "party_vote": "vote",
        "personal_vote": "vote",
        "question": "question",
        "stage": "procedural_decision",
        "ruling": "procedural_decision",
        "interjection": "excluded_boundary",
    }[category]


def _dependency_blockers(category: str) -> str:
    if category in {"party_vote", "personal_vote"}:
        return "validated_member_identity,validated_party_attribution,validated_sitting_proceeding"
    if category == "question":
        return "validated_member_identity,validated_sitting_proceeding"
    if category in {"stage", "ruling"}:
        return "validated_sitting_proceeding"
    return "not-in-scope"


def _review_status(category: str) -> str:
    return "reviewed" if category != "interjection" else "reviewed-boundary"


def _review_notes(category: str, excerpt: str) -> str:
    if category == "interjection":
        return "Boundary example kept for exclusion proof; not extracted as a released component."
    return excerpt


def _procedure_samples() -> list[dict[str, Any]]:
    return _read_json(PROCEDURE_FIXTURES_PATH)["samples"]


def _neutral_fixtures() -> dict[str, list[dict[str, Any]]]:
    return _read_json(NEUTRAL_FIXTURES_PATH)["components"]


def _coverage_payload(review_rows: list[dict[str, Any]], reason: str) -> dict[str, Any]:
    procedure_samples = _procedure_samples()
    neutral_components = _neutral_fixtures()
    vote_domain_counts = gold_sample_counts("vote")
    return {
        "artifact_name": "vote_motion_bill_question_extraction_coverage",
        "artifact_version": "0.1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "track_id": TRACK_ID,
        "status": "blocked",
        "reason": reason,
        "sample_counts": {
            "procedure_samples_reviewed": len(procedure_samples),
            "extractable_samples": len(
                [
                    row
                    for row in review_rows
                    if row["extraction_status"] == "blocked-pending-validated-components"
                ]
            ),
            "excluded_boundary_samples": len(
                [row for row in review_rows if row["extraction_status"] == "excluded-by-design"]
            ),
            "vote_samples": len(
                [
                    row
                    for row in procedure_samples
                    if row["category"] in {"party_vote", "personal_vote"}
                ]
            ),
            "question_samples": len(
                [row for row in procedure_samples if row["category"] == "question"]
            ),
            "procedural_decision_samples": len(
                [row for row in procedure_samples if row["category"] in {"stage", "ruling"}]
            ),
            "boundary_samples": len(
                [row for row in procedure_samples if row["category"] == "interjection"]
            ),
        },
        "neutral_input_counts": {
            "motions": len(neutral_components.get("motions", [])),
            "votes": len(neutral_components.get("votes", [])),
            "bills": len(neutral_components.get("bills", [])),
        },
        "gold_vote_domain": vote_domain_counts,
        "blocked_dependencies": [
            "validated_member_identity",
            "validated_party_attribution",
            "validated_sitting_proceeding",
        ],
        "warnings": [
            "Procedure samples are reviewed boundary fixtures, not published extraction outputs.",
            "Vote and question extraction remains blocked until the dependent component releases are validated.",
        ],
    }


def build_vote_motion_bill_question_extraction(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    coverage_path: Path = DEFAULT_COVERAGE,
    review_path: Path = DEFAULT_REVIEW,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    samples = _procedure_samples()
    reason = (
        "Validated member identity, validated party attribution, and validated sitting/proceeding "
        "components are not yet all available for release."
    )
    review_rows = []
    for sample in samples:
        review_rows.append(
            {
                "sample_id": sample["sample_id"],
                "category": sample["category"],
                "document_type": sample["document_type"],
                "source_stable_id": sample["source_reference"].get("parliament_document_id") or "",
                "extraction_family": _sample_family(sample["category"]),
                "extraction_status": (
                    "excluded-by-design"
                    if sample["category"] == "interjection"
                    else "blocked-pending-validated-components"
                ),
                "dependency_blockers": _dependency_blockers(sample["category"]),
                "authority_source_ids": ";".join(sample["authority_source_ids"]),
                "uncertainty_status": sample["uncertainty_status"],
                "review_status": _review_status(sample["category"]),
                "review_notes": _review_notes(sample["category"], sample["text_excerpt"]),
            }
        )

    coverage = _coverage_payload(review_rows, reason)
    _write_json(coverage_path, coverage)
    _write_csv(review_path, review_rows)

    manifest = {
        "artifact_name": "vote_motion_bill_question_extraction_validation",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked",
        "release_gate_status": "blocked-pending-validated-components",
        "track_id": TRACK_ID,
        "counts": {
            "procedure_samples_reviewed": len(samples),
            "vote_samples": len([row for row in review_rows if row["extraction_family"] == "vote"]),
            "question_samples": len(
                [row for row in review_rows if row["extraction_family"] == "question"]
            ),
            "procedural_decision_samples": len(
                [row for row in review_rows if row["extraction_family"] == "procedural_decision"]
            ),
            "boundary_samples": len(
                [row for row in review_rows if row["extraction_family"] == "excluded_boundary"]
            ),
            "validated_rows": 0,
            "blocked_rows": len(
                [
                    row
                    for row in review_rows
                    if row["extraction_status"] == "blocked-pending-validated-components"
                ]
            ),
            "excluded_rows": len(
                [row for row in review_rows if row["extraction_status"] == "excluded-by-design"]
            ),
            "review_rows": len(review_rows),
            "neutral_motion_rows": len(_neutral_fixtures().get("motions", [])),
            "neutral_vote_rows": len(_neutral_fixtures().get("votes", [])),
            "neutral_bill_rows": len(_neutral_fixtures().get("bills", [])),
        },
        "errors": [reason],
        "warnings": [
            "Procedure sample rows are reviewed boundary evidence, not a published extraction release.",
            "Vote, motion, bill, and question claims remain blocked until the dependent component releases are validated.",
        ],
        "source_hashes": {
            "neutral_component_model": _sha256_path(NEUTRAL_MODEL_PATH),
            "neutral_component_validation": _sha256_path(NEUTRAL_VALIDATION_PATH),
            "neutral_component_fixtures": _sha256_path(NEUTRAL_FIXTURES_PATH),
            "procedure_model": _sha256_path(PROCEDURE_MODEL_PATH),
            "procedure_fixtures": _sha256_path(PROCEDURE_FIXTURES_PATH),
            "gold_evaluation_manifest": _sha256_path(GOLD_MANIFEST_PATH),
            "gold_evaluation_fixtures": _sha256_path(GOLD_FIXTURES_PATH),
            "member_identity_validation": _sha256_path(MEMBER_IDENTITY_VALIDATION_PATH)
            if MEMBER_IDENTITY_VALIDATION_PATH.exists()
            else "",
            "party_attribution_validation": _sha256_path(PARTY_ATTRIBUTION_VALIDATION_PATH)
            if PARTY_ATTRIBUTION_VALIDATION_PATH.exists()
            else "",
            "sitting_proceeding_validation": _sha256_path(SITTING_PROCEEDING_VALIDATION_PATH)
            if SITTING_PROCEEDING_VALIDATION_PATH.exists()
            else "",
            "authority_sources": _sha256_path(AUTHORITY_SOURCES_PATH),
        },
        "source_manifests": [
            "manifests/neutral_component_model.json",
            "manifests/neutral_component_validation_manifest.json",
            "fixtures/neutral_components.json",
            "manifests/nz_parliamentary_procedure_model.json",
            "fixtures/nz_parliamentary_procedure_samples.json",
            "manifests/gold_evaluation_datasets.json",
            "fixtures/gold_evaluation_samples.json",
            "manifests/corpus_wide_member_identity_validation.json",
            "manifests/corpus_wide_party_attribution_validation.json",
            "manifests/sitting_proceeding_component_validation.json",
            "manifests/authority_sources.json",
            "docs/component-contracts.md",
            "docs/endpoint-contracts.md",
            "docs/nz-parliamentary-procedure-model.md",
        ],
        "input_artifacts": {
            "neutral_component_model": NEUTRAL_MODEL_PATH.relative_to(ROOT).as_posix(),
            "neutral_component_validation": NEUTRAL_VALIDATION_PATH.relative_to(ROOT).as_posix(),
            "neutral_component_fixtures": NEUTRAL_FIXTURES_PATH.relative_to(ROOT).as_posix(),
            "procedure_model": PROCEDURE_MODEL_PATH.relative_to(ROOT).as_posix(),
            "procedure_fixtures": PROCEDURE_FIXTURES_PATH.relative_to(ROOT).as_posix(),
            "gold_evaluation_manifest": GOLD_MANIFEST_PATH.relative_to(ROOT).as_posix(),
            "gold_evaluation_fixtures": GOLD_FIXTURES_PATH.relative_to(ROOT).as_posix(),
            "member_identity_validation": MEMBER_IDENTITY_VALIDATION_PATH.relative_to(
                ROOT
            ).as_posix(),
            "party_attribution_validation": PARTY_ATTRIBUTION_VALIDATION_PATH.relative_to(
                ROOT
            ).as_posix(),
            "sitting_proceeding_validation": SITTING_PROCEEDING_VALIDATION_PATH.relative_to(
                ROOT
            ).as_posix(),
            "authority_sources": AUTHORITY_SOURCES_PATH.relative_to(ROOT).as_posix(),
        },
        "outputs": {
            "coverage_report": _render_path(coverage_path),
            "review_queue": _render_path(review_path),
        },
        "coverage": coverage,
        "release_decision": {
            "decision": "defer",
            "reason": reason,
            "public_claim": "No validated vote/motion/bill/question extraction release is published from this blocked manifest.",
        },
    }
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the vote, motion, bill, and question extraction release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_vote_motion_bill_question_extraction(
        manifest_path=args.manifest,
        coverage_path=args.coverage,
        review_path=args.review,
    )
    print(f"Wrote {args.manifest}")
    print(f"Release gate: {manifest['release_gate_status']}")
    print(f"Reviewed samples: {manifest['counts']['review_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
