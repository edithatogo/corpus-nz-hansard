"""Build exploratory entity-linking outputs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _record_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "record_id",
            "entity_type",
            "example_class",
            "mention_text",
            "source_document_type",
            "parliament_number",
            "source_stable_id",
            "source_excerpt",
            "selector",
            "candidate_links",
            "linking_status",
            "provenance",
            "validation_status",
            "review_status",
            "release_status",
            "notes",
        ],
        "properties": {
            "record_id": {"type": "string"},
            "entity_type": {
                "enum": [
                    "person",
                    "organisation",
                    "place",
                    "legislation",
                    "ministry",
                    "portfolio",
                    "committee",
                ]
            },
            "example_class": {
                "enum": ["positive", "negative", "ambiguous", "unresolved", "excluded"]
            },
            "mention_text": {"type": "string"},
            "source_document_type": {"type": "string"},
            "parliament_number": {"type": "integer", "minimum": 1},
            "source_stable_id": {"type": "string"},
            "source_excerpt": {"type": "string"},
            "selector": {
                "type": "object",
                "required": ["selector_type", "exact", "source_stable_id"],
                "additionalProperties": False,
                "properties": {
                    "selector_type": {"const": "exact"},
                    "exact": {"type": "string"},
                    "source_stable_id": {"type": "string"},
                },
            },
            "candidate_links": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "candidate_id",
                        "candidate_label",
                        "candidate_uri",
                        "authority_source_id",
                        "authority_source_url",
                        "score",
                        "match_method",
                        "linking_status",
                    ],
                    "properties": {
                        "candidate_id": {"type": ["string", "null"]},
                        "candidate_label": {"type": "string"},
                        "candidate_uri": {"type": ["string", "null"]},
                        "authority_source_id": {"type": ["string", "null"]},
                        "authority_source_url": {"type": ["string", "null"]},
                        "score": {"type": "number", "minimum": 0, "maximum": 1},
                        "match_method": {"type": "string"},
                        "linking_status": {
                            "enum": ["linked", "ambiguous", "unresolved", "negative", "excluded"]
                        },
                    },
                },
            },
            "linking_status": {
                "enum": ["linked", "ambiguous", "unresolved", "negative", "excluded"]
            },
            "provenance": {
                "type": "object",
                "required": ["method", "rule_bundle", "authority_sources", "human_validation"],
                "additionalProperties": False,
                "properties": {
                    "method": {"type": "string"},
                    "rule_bundle": {"type": "string"},
                    "authority_sources": {"type": "array", "items": {"type": "string"}},
                    "human_validation": {"type": "boolean"},
                },
            },
            "validation_status": {"const": "exploratory-only"},
            "review_status": {"const": "reviewed"},
            "release_status": {"const": "sample-not-release"},
            "notes": {"type": "string"},
        },
    }


def _manifest_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "manifest_version",
            "track_id",
            "repository",
            "generated_at",
            "release_status",
            "sample_package",
            "outputs",
            "source_inputs",
            "supported_entity_types",
            "validation_counts",
            "authority_sources",
            "validation_results",
        ],
        "properties": {
            "manifest_version": {"const": 1},
            "track_id": {"const": "entity_linking_exploratory_outputs_20260610"},
            "repository": {"const": "corpus-nz-hansard"},
            "generated_at": {"type": "string"},
            "release_status": {"const": "sample-not-release"},
            "sample_package": {"type": "string"},
            "outputs": {
                "type": "object",
                "required": ["jsonl", "review_csv"],
                "additionalProperties": False,
                "properties": {
                    "jsonl": {"type": "string"},
                    "review_csv": {"type": "string"},
                },
            },
            "source_inputs": {"type": "array", "items": {"type": "string"}},
            "supported_entity_types": {
                "type": "array",
                "items": {
                    "enum": [
                        "person",
                        "organisation",
                        "place",
                        "legislation",
                        "ministry",
                        "portfolio",
                        "committee",
                    ]
                },
            },
            "validation_counts": {
                "type": "object",
                "required": [
                    "record_count",
                    "review_row_count",
                    "linked",
                    "ambiguous",
                    "unresolved",
                    "negative",
                    "excluded",
                ],
                "additionalProperties": False,
                "properties": {
                    "record_count": {"type": "integer", "minimum": 1},
                    "review_row_count": {"type": "integer", "minimum": 1},
                    "linked": {"type": "integer", "minimum": 0},
                    "ambiguous": {"type": "integer", "minimum": 0},
                    "unresolved": {"type": "integer", "minimum": 0},
                    "negative": {"type": "integer", "minimum": 0},
                    "excluded": {"type": "integer", "minimum": 0},
                },
            },
            "authority_sources": {"type": "array", "items": {"type": "string"}},
            "validation_results": {
                "type": "object",
                "required": [
                    "outputs_written",
                    "review_sample_written",
                    "non_authoritative",
                    "false_positive_analysis_recorded",
                    "human_validation_required",
                ],
                "additionalProperties": False,
                "properties": {
                    "outputs_written": {"const": True},
                    "review_sample_written": {"const": True},
                    "non_authoritative": {"const": True},
                    "false_positive_analysis_recorded": {"const": True},
                    "human_validation_required": {"const": True},
                },
            },
        },
    }


def _write_supporting_docs() -> None:
    from scripts.entity_linking_exploratory_outputs import DOC_PATH, README_PATH

    README_PATH.parent.mkdir(parents=True, exist_ok=True)
    README_PATH.write_text(
        """# Entity Linking Exploratory Outputs

Maintainer-review sample package for exploratory entity linking.
This package is sample-not-release and explicitly non-authoritative.

Files:

- `entity_linking_exploratory.jsonl`
- `entity_linking_exploratory_review.csv`
- `README.md`

Validation and traceability:

- Manifest: `manifests/entity_linking_exploratory_outputs.json`
- Schema: `schemas/entity_linking_exploratory_outputs.schema.json`
- Record schema: `schemas/entity_linking_exploratory_record.schema.json`
- Docs: `docs/entity-linking-exploratory-outputs.md`

Exploratory boundary:

- Entity mentions, selectors, candidate IDs, and scores are preserved.
- Model/rule provenance is preserved.
- human validation is still required before any downstream release claim.
""",
        encoding="utf-8",
    )
    DOC_PATH.write_text(
        """# Entity Linking Exploratory Outputs

## Scope

This track publishes non-authoritative, machine-assisted entity-linking outputs for
people, organisations, places, legislation, ministries, portfolios, and committees.
The outputs are exploratory only and must not be treated as validated parliamentary or
legal metadata.

## Outputs

- `samples/entity-linking-exploratory/entity_linking_exploratory.jsonl`
- `samples/entity-linking-exploratory/entity_linking_exploratory_review.csv`

## Review Sample

The review sample records positive, ambiguous, unresolved, negative, and excluded
examples. It preserves mention text, selectors, candidate IDs, candidate scores,
authority-source references, and provenance.

## False-Positive Analysis

Known false-positive patterns include:

- office titles mistaken for people or portfolios
- electorate labels mistaken for places
- generic procedural phrases mistaken for committees
- ministry names that need dated authority snapshots
- bill titles that should only be linked when the title match is exact

These patterns are explicitly retained so downstream evaluation can measure where a
rule or model would over-link text.

## Downstream Use

Exploratory outputs may feed search or RAG enrichment and RDF exploratory graphs, but
they remain non-authoritative until independently validated.

## Validation

- `python scripts/build_entity_linking_exploratory_outputs.py`
- `python scripts/check_entity_linking_exploratory_outputs.py`
- `python -m unittest tests.test_entity_linking_exploratory_outputs`
""",
        encoding="utf-8",
    )


def build_entity_linking_exploratory_outputs(
    *, manifest_path: Path | None = None, generated_at: str | None = None
) -> dict[str, Any]:
    from scripts.entity_linking_exploratory_outputs import (  # noqa: I001
        build_entity_linking_exploratory_outputs as build_entity_linking_seed_outputs,
        MANIFEST_PATH,
        RECORD_SCHEMA_PATH,
        SCHEMA_PATH,
    )

    manifest_path = manifest_path or MANIFEST_PATH
    generated_at = generated_at or datetime.now(UTC).isoformat()
    manifest = build_entity_linking_seed_outputs(generated_at=generated_at, write=True)
    _write_json(manifest_path, manifest)
    _write_json(SCHEMA_PATH, _manifest_schema())
    _write_json(RECORD_SCHEMA_PATH, _record_schema())
    _write_supporting_docs()
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build exploratory entity-linking outputs.")
    from scripts.entity_linking_exploratory_outputs import MANIFEST_PATH

    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    return parser.parse_args()


def main() -> int:
    from scripts.entity_linking_exploratory_outputs import JSONL_PATH, REVIEW_PATH

    args = parse_args()
    manifest = build_entity_linking_exploratory_outputs(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Wrote {JSONL_PATH}")
    print(f"Wrote {REVIEW_PATH}")
    print(f"Records rendered: {manifest['validation_counts']['record_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
