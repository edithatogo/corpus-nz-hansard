"""Build the sitting and proceeding component release surface."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "sitting_proceeding_component_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/sitting_proceeding_component_validation.json"
DEFAULT_COVERAGE = ROOT / "derived/sitting_proceeding_components/sitting_proceeding_coverage.json"
DEFAULT_REVIEW = ROOT / "derived/sitting_proceeding_components/sitting_proceeding_review.csv"

NEUTRAL_MODEL_PATH = ROOT / "manifests/neutral_component_model.json"
NEUTRAL_VALIDATION_PATH = ROOT / "manifests/neutral_component_validation_manifest.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
HISTORICAL_COVERAGE_PATH = ROOT / "manifests/historical_coverage_audit.json"
AUTHORITY_SOURCES_PATH = ROOT / "manifests/authority_sources.json"
DOC_PATH = ROOT / "docs/sitting-proceeding-component-release.md"
NEUTRAL_DOC_PATH = ROOT / "docs/neutral-component-model.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
RELEASE_LADDER_DOC_PATH = ROOT / "docs/release-ladder.md"
TRACK_DOC_PATH = ROOT / "conductor/tracks/sitting_proceeding_component_release_20260610/index.md"
SCHEMA_PATH = ROOT / "schemas/sitting_proceeding_component_validation.schema.json"

REVIEW_COLUMNS = [
    "component_family",
    "component_id",
    "source_stable_id",
    "status",
    "issue",
    "source_status",
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


def _validate_schema(manifest: dict[str, Any]) -> list[str]:
    schema = _read_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{location}: {error.message}")
    return failures


def _fixture_counts() -> tuple[int, int, dict[str, dict[str, Any]]]:
    fixtures = _read_json(FIXTURE_PATH)["components"]
    sittings = fixtures.get("sittings", [])
    proceeding_items = fixtures.get("proceeding_items", [])
    by_id: dict[str, dict[str, Any]] = {}
    for family_rows in fixtures.values():
        for row in family_rows:
            by_id[row["component_id"]] = row
    return len(sittings), len(proceeding_items), by_id


def _blocked_review_rows(
    sittings: list[dict[str, Any]],
    proceeding_items: list[dict[str, Any]],
    reason: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in sittings:
        rows.append(
            {
                "component_family": "sittings",
                "component_id": row["component_id"],
                "source_stable_id": row.get("sitting_date", ""),
                "status": "blocked-pending-official-reconciliation",
                "issue": reason,
                "source_status": row.get("source_status", ""),
            }
        )
    for row in proceeding_items:
        rows.append(
            {
                "component_family": "proceeding_items",
                "component_id": row["component_id"],
                "source_stable_id": row.get("source_stable_id", ""),
                "status": "blocked-pending-official-reconciliation",
                "issue": reason,
                "source_status": row.get("item_type", ""),
            }
        )
    return rows


def _coverage_payload(reason: str) -> dict[str, Any]:
    fixtures = _read_json(FIXTURE_PATH)["components"]
    sittings = fixtures.get("sittings", [])
    proceeding_items = fixtures.get("proceeding_items", [])
    historical = _read_json(HISTORICAL_COVERAGE_PATH)
    authority = _read_json(AUTHORITY_SOURCES_PATH)
    return {
        "artifact_name": "sitting_proceeding_component_coverage",
        "artifact_version": "0.1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "track_id": TRACK_ID,
        "status": "blocked",
        "reason": reason,
        "fixture_counts": {
            "sittings": len(sittings),
            "proceeding_items": len(proceeding_items),
        },
        "coverage_counts": {
            "reconciled_sittings": 0,
            "reconciled_proceedings": 0,
            "inferred_sittings": len(sittings),
            "inferred_proceedings": len(proceeding_items),
            "missing_official_sittings": len(sittings),
            "missing_official_proceedings": len(proceeding_items),
        },
        "historical_audit_status": historical["authority_cross_check"]["status"],
        "historical_coverage_status": historical["claim_boundaries"][2]["status"],
        "authority_source_count": len(authority["sources"]),
        "warnings": [
            "Fixture rows demonstrate the component shape, not official reconciliation.",
            "Endpoint consumers must not treat these components as validated release inputs.",
        ],
    }


def build_sitting_proceeding_component(
    *,
    manifest_path: Path = DEFAULT_MANIFEST,
    coverage_path: Path = DEFAULT_COVERAGE,
    review_path: Path = DEFAULT_REVIEW,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    fixtures = _read_json(FIXTURE_PATH)["components"]
    sittings = fixtures.get("sittings", [])
    proceeding_items = fixtures.get("proceeding_items", [])
    reason = (
        "Official sitting and proceeding reconciliation has not been completed; "
        "the track remains blocked pending historical coverage alignment."
    )
    coverage = _coverage_payload(reason)
    review_rows = _blocked_review_rows(sittings, proceeding_items, reason)
    _write_json(coverage_path, coverage)
    _write_csv(review_path, review_rows)

    manifest = {
        "artifact_name": "sitting_proceeding_component_validation",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "ok": False,
        "validation_status": "blocked",
        "release_gate_status": "blocked-pending-official-reconciliation",
        "track_id": TRACK_ID,
        "counts": {
            "fixture_sittings": len(sittings),
            "fixture_proceeding_items": len(proceeding_items),
            "reconciled_sittings": 0,
            "reconciled_proceeding_items": 0,
            "inferred_sittings": len(sittings),
            "inferred_proceeding_items": len(proceeding_items),
            "missing_official_sittings": len(sittings),
            "missing_official_proceeding_items": len(proceeding_items),
            "validated_rows": 0,
            "review_rows": len(review_rows),
        },
        "errors": [reason],
        "warnings": [
            "The neutral fixture set proves shape and referential integrity, not official reconciliation.",
            "Downstream endpoint publication remains blocked until official sitting and proceeding evidence is aligned.",
        ],
        "source_hashes": {
            "neutral_component_model": _sha256_path(NEUTRAL_MODEL_PATH),
            "neutral_component_validation": _sha256_path(NEUTRAL_VALIDATION_PATH),
            "neutral_component_fixtures": _sha256_path(FIXTURE_PATH),
            "historical_coverage_audit": _sha256_path(HISTORICAL_COVERAGE_PATH),
            "authority_sources": _sha256_path(AUTHORITY_SOURCES_PATH),
        },
        "source_manifests": [
            "manifests/neutral_component_model.json",
            "manifests/neutral_component_validation_manifest.json",
            "fixtures/neutral_components.json",
            "manifests/historical_coverage_audit.json",
            "manifests/authority_sources.json",
            "docs/neutral-component-model.md",
            "docs/historical-coverage-audit.md",
        ],
        "input_artifacts": {
            "neutral_component_model": NEUTRAL_MODEL_PATH.relative_to(ROOT).as_posix(),
            "neutral_component_validation": NEUTRAL_VALIDATION_PATH.relative_to(ROOT).as_posix(),
            "neutral_component_fixtures": FIXTURE_PATH.relative_to(ROOT).as_posix(),
            "historical_coverage_audit": HISTORICAL_COVERAGE_PATH.relative_to(ROOT).as_posix(),
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
            "public_claim": "No validated sitting/proceeding release is published from this blocked manifest.",
        },
    }
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the sitting and proceeding component release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_sitting_proceeding_component(
        manifest_path=args.manifest,
        coverage_path=args.coverage,
        review_path=args.review,
    )
    print(f"Wrote {args.manifest}")
    print(f"Release gate: {manifest['release_gate_status']}")
    print(f"Validated rows: {manifest['counts']['validated_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
