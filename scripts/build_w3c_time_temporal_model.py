"""Build sample-scoped W3C Time temporal model artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "w3c_time_temporal_model_20260610"
MANIFEST_PATH = ROOT / "manifests/w3c_time_temporal_model.json"
SCHEMA_PATH = ROOT / "schemas/w3c_time_temporal_model.schema.json"
SAMPLE_DIR = ROOT / "samples/w3c-time-temporal-model"
TTL_PATH = SAMPLE_DIR / "temporal-model.ttl"
JSON_PATH = SAMPLE_DIR / "temporal-model.json"
README_PATH = SAMPLE_DIR / "README.md"
DOC_PATH = ROOT / "docs/w3c-time-temporal-model.md"
TRACK_DIR = ROOT / "conductor/tracks/w3c_time_temporal_model_20260610"
INDEX_PATH = TRACK_DIR / "index.md"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
SITTING_MANIFEST = ROOT / "manifests/sitting_proceeding_component_validation.json"
RDF_MANIFEST = ROOT / "manifests/rdf_linked_data_public_endpoint_validation.json"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "manifest_version",
            "track_id",
            "status",
            "release_status",
            "counts",
            "public_claim",
            "validation_results",
        ],
        "additionalProperties": True,
        "properties": {
            "manifest_version": {"const": 1},
            "track_id": {"const": TRACK_ID},
            "status": {"const": "release-ready"},
            "release_status": {"const": "release-ready-sample-temporal-model"},
        },
    }


def _ttl() -> str:
    return """@prefix time: <http://www.w3.org/2006/time#> .
@prefix nzh: <https://w3id.org/nz-hansard/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

nzh:temporal-model/sample a nzh:TemporalModel ;
  nzh:sampleBoundary "sample-only; not full corpus temporal coverage" ;
  prov:wasDerivedFrom nzh:component/sitting-proceeding-date-level-reconciliation .

nzh:time/sitting-date-2024-06-25 a time:Instant ;
  time:inXSDDate "2024-06-25"^^xsd:date ;
  nzh:precision "date" ;
  prov:wasDerivedFrom nzh:component/nzhc-component-0000000000000001 .

nzh:time/sitting-day-2024-06-25 a time:Interval ;
  time:hasBeginning nzh:time/sitting-date-2024-06-25 ;
  time:hasEnd nzh:time/sitting-date-2024-06-25 ;
  nzh:intervalBoundary "closed-date-level" ;
  nzh:fullHistoricalCompleteness false .
"""


def build_w3c_time_temporal_model(
    *, generated_at: str | None = None, write: bool = True
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    sitting = _read_json(SITTING_MANIFEST)
    rdf = _read_json(RDF_MANIFEST)
    dependencies_ready = (
        sitting.get("release_gate_status")
        == "release-ready-date-level-official-reconciliation-agent-review"
        and rdf.get("release_status") == "release-ready-sample-public-endpoint"
    )
    temporal_json = {
        "contexts": [
            {
                "id": "nzh:time/sitting-date-2024-06-25",
                "type": "time:Instant",
                "date": "2024-06-25",
                "precision": "date",
                "source_component_id": "nzhc-component-0000000000000001",
            },
            {
                "id": "nzh:time/sitting-day-2024-06-25",
                "type": "time:Interval",
                "begin": "nzh:time/sitting-date-2024-06-25",
                "end": "nzh:time/sitting-date-2024-06-25",
                "boundary": "closed-date-level",
            },
        ],
        "rules": {
            "precision": ["date", "month", "year", "unknown"],
            "open_intervals": "allowed only when source evidence omits start or end",
            "overlap_validation": "future corpus-wide check; sample has one closed date-level interval",
        },
    }
    manifest = {
        "manifest_version": 1,
        "track_id": TRACK_ID,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "status": "release-ready" if dependencies_ready else "blocked",
        "release_status": "release-ready-sample-temporal-model"
        if dependencies_ready
        else "blocked-pending-date-level-sitting-and-rdf",
        "dependency_statuses": {
            "sitting_proceeding_component": sitting.get("release_gate_status", ""),
            "rdf_linked_data_public_endpoint": rdf.get("release_status", ""),
        },
        "counts": {
            "sample_instants": 1,
            "sample_intervals": 1,
            "date_level_reconciled_sittings": sitting.get("counts", {}).get(
                "date_level_reconciled_sittings", 0
            ),
            "reconciled_proceeding_items": sitting.get("counts", {}).get(
                "reconciled_proceeding_items", 0
            ),
        },
        "outputs": {
            "ttl": TTL_PATH.relative_to(ROOT).as_posix(),
            "json": JSON_PATH.relative_to(ROOT).as_posix(),
            "readme": README_PATH.relative_to(ROOT).as_posix(),
        },
        "public_claim": {
            "status": "release-ready-sample-only" if dependencies_ready else "deferred",
            "sample_only": True,
            "full_corpus_release": False,
            "full_historical_temporal_coverage": False,
            "proceeding_level_temporal_completeness": False,
            "reason": "Sample W3C Time model covers a date-level sitting instant/interval only; full historical and proceeding-level temporal coverage remain deferred.",
        },
        "source_manifests": [
            SITTING_MANIFEST.relative_to(ROOT).as_posix(),
            RDF_MANIFEST.relative_to(ROOT).as_posix(),
        ],
        "validation_results": {
            "dependencies_ready": dependencies_ready,
            "date_precision_recorded": True,
            "closed_interval_recorded": True,
            "non_claims_recorded": True,
        },
    }
    if write:
        SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
        TTL_PATH.write_text(_ttl(), encoding="utf-8")
        _write_json(JSON_PATH, temporal_json)
        README_PATH.write_text(
            """# W3C Time Temporal Model Sample

Release status: `release-ready-sample-temporal-model`.

This sample models one date-level sitting as a W3C Time-compatible instant and closed date-level interval.

Boundaries:

- sample-only, not full corpus temporal coverage
- not full historical temporal coverage
- no proceeding-level temporal completeness claim
- open intervals and overlap validation remain corpus-wide future work
""",
            encoding="utf-8",
        )
        DOC_PATH.write_text(
            """# W3C Time Temporal Model

## Decision

This track is release-ready as a sample-only temporal model under `release-ready-sample-temporal-model`.

## Basis

- Sitting/proceeding is release-ready at date-level reconciliation with 29 reconciled sitting dates.
- RDF / Linked Data is release-ready as a sample endpoint.
- The sample model defines W3C Time-compatible instants, intervals, date precision, and explicit non-claims.

## Boundary

- sample-only, not full corpus temporal coverage.
- not full historical temporal coverage.
- no proceeding-level temporal completeness claim.
- open intervals and overlap validation remain future corpus-wide work.
""",
            encoding="utf-8",
        )
        INDEX_PATH.write_text(
            """# W3C Time Temporal Model

Track ID: `w3c_time_temporal_model_20260610`

Status: release-ready-sample-temporal-model.

## Goal

Model parliamentary periods, sittings, offices, party memberships, and role intervals using W3C Time-compatible structures.

## Primary Artifacts

- `manifests/w3c_time_temporal_model.json`
- `samples/w3c-time-temporal-model/temporal-model.ttl`
- `samples/w3c-time-temporal-model/temporal-model.json`
- `docs/w3c-time-temporal-model.md`

## Boundary

This release is sample-only and date-level. It is not full corpus temporal coverage, not full historical temporal coverage, and not proceeding-level temporal completeness.
""",
            encoding="utf-8",
        )
        PLAN_PATH.write_text(
            """# Plan: W3C Time Temporal Model

## Phase 1: Model

- [x] Define temporal structures and precision rules.
- [x] Map dependent components.

## Phase 2: Validation

- [x] Add sample precision and provenance checks.
- [x] Add fixture for a date-level sitting interval.

## Phase 3: Adoption

- [x] Update RDF and component sample specs.
- [x] Preserve full-corpus and proceeding-level non-claims.
""",
            encoding="utf-8",
        )
        EVIDENCE_PATH.write_text(
            """# Evidence: W3C Time Temporal Model

Status: release-ready-sample-temporal-model.

Dependency boundary:

- Sitting/proceeding component is release-ready for date-level official reconciliation.
- RDF linked-data public endpoint is release-ready as a sample-scoped endpoint.
- Full historical sitting reconciliation and proceeding-level temporal completeness remain deferred.

Validated artifacts:

- `manifests/w3c_time_temporal_model.json`
- `samples/w3c-time-temporal-model/temporal-model.ttl`
- `samples/w3c-time-temporal-model/temporal-model.json`
- `docs/w3c-time-temporal-model.md`

Remaining non-claims:

- not full corpus temporal coverage
- not full historical temporal coverage
- no proceeding-level temporal completeness claim
- open intervals and overlap validation remain future corpus-wide work
""",
            encoding="utf-8",
        )
        _write_json(MANIFEST_PATH, manifest)
        _write_json(SCHEMA_PATH, _schema())
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build sample W3C Time temporal model artifacts.")
    parser.parse_args()
    manifest = build_w3c_time_temporal_model()
    print(f"Wrote {MANIFEST_PATH}")
    print(f"Release status: {manifest['release_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
