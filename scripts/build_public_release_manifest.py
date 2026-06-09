"""Build a public dataset release-readiness manifest from pipeline evidence."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_SOURCE_INVENTORY = Path("manifests/source_inventory.json")
DEFAULT_SCHEMA_DISCOVERY = Path("manifests/schema_discovery.json")
DEFAULT_NORMALIZATION_VALIDATION = Path("manifests/normalization_validation.json")
DEFAULT_RECORD_SCHEMA_VALIDATION = Path("manifests/record_schema_validation.json")
DEFAULT_DUCKDB_VALIDATION = Path("manifests/duckdb_validation.json")
DEFAULT_OUTPUT = Path("manifests/public_dataset_release_manifest.json")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_release_manifest(
    source_inventory_path: Path | str = DEFAULT_SOURCE_INVENTORY,
    schema_discovery_path: Path | str = DEFAULT_SCHEMA_DISCOVERY,
    normalization_validation_path: Path | str = DEFAULT_NORMALIZATION_VALIDATION,
    record_schema_validation_path: Path | str = DEFAULT_RECORD_SCHEMA_VALIDATION,
    duckdb_validation_path: Path | str = DEFAULT_DUCKDB_VALIDATION,
) -> dict[str, Any]:
    """Combine existing pipeline evidence into a public release manifest."""
    source_inventory_path = Path(source_inventory_path)
    schema_discovery_path = Path(schema_discovery_path)
    normalization_validation_path = Path(normalization_validation_path)
    record_schema_validation_path = Path(record_schema_validation_path)
    duckdb_validation_path = Path(duckdb_validation_path)

    source = _read_json(source_inventory_path)
    schema = _read_json(schema_discovery_path)
    normalization = _read_json(normalization_validation_path)
    record_schema = _read_json(record_schema_validation_path)
    duckdb = _read_json(duckdb_validation_path)

    return {
        "manifest_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "publication_status": "published",
        "published": True,
        "publication": {
            "github_repository": "https://github.com/edithatogo/corpus-nz-hansard",
            "github_release": "https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0",
            "huggingface_dataset": "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus",
            "zenodo_record": "https://zenodo.org/records/20595194",
            "doi": "10.5281/zenodo.20595194",
            "doi_url": "https://doi.org/10.5281/zenodo.20595194",
            "conceptdoi": "10.5281/zenodo.20591996",
            "conceptdoi_url": "https://doi.org/10.5281/zenodo.20591996",
            "publication_date": "2026-06-08",
        },
        "license": {
            "repository_materials": "MIT",
            "license_file": "LICENSE",
            "notice_file": "NOTICE.md",
            "source_material": "New Zealand Parliamentary Debates/Hansard; no copyright exists in Hansard / New Zealand Parliamentary Debates per documented Parliament guidance.",
            "source_zip_redistributed": False,
        },
        "source": {
            "archive_name": source["source_archive"]["name"],
            "sha256": source["source_archive"]["sha256"],
            "member_count": source["summary"]["member_count"],
        },
        "counts": {
            "source_files": schema["summary"]["file_count"],
            "schema_rows": schema["summary"]["total_rows"],
            "normalized_rows": normalization["summary"]["output_rows"],
            "schema_validated_rows": record_schema["record_count"],
            "duckdb_rows": duckdb["summary"]["row_count"],
        },
        "quality": {
            "normalization_warnings": normalization["summary"]["warning_count"],
            "record_schema_valid": record_schema["ok"],
            "record_schema_errors": len(record_schema["errors"]),
            "record_schema_warnings": len(record_schema["warnings"]),
            "duckdb_row_count_matches_expected": duckdb["summary"]["row_count_matches_expected"],
        },
        "artifacts": {
            "dataset_card": "DATASET_CARD.md",
            "license": "LICENSE",
            "notice": "NOTICE.md",
            "record_schema": "schemas/hansard_record.schema.json",
            "record_schema_validation": "manifests/record_schema_validation.json",
            "licensing_and_provenance": "docs/licensing-and-provenance.md",
            "public_release_checklist": "docs/public-release-checklist.md",
            "pipeline_handoff": "docs/pipeline-handoff.md",
            "readiness_review": "docs/readiness-review.md",
            "parquet": "generated/parquet/hansard.parquet",
            "duckdb": "generated/duckdb/hansard.duckdb",
        },
        "limitations": [
            "No explicit source Party column.",
            "MemberOfParliament is unresolved raw source text.",
            "Content remains document-level text, not speech-turn segmentation.",
            "Source ZIP is not redistributed in public dataset artifacts.",
            "Publication does not imply official Parliament endorsement.",
        ],
        "recommended_next_tracks": [
            "release_hosting_and_versioning",
            "dataset_card_review_and_publication",
            "speech_turn_segmentation",
            "reporting_powerbi_model",
            "search_rag_indexing",
        ],
    }


def write_manifest(manifest: dict[str, Any], output_path: Path | str) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a public dataset release-readiness manifest."
    )
    parser.add_argument("--source-inventory", type=Path, default=DEFAULT_SOURCE_INVENTORY)
    parser.add_argument("--schema-discovery", type=Path, default=DEFAULT_SCHEMA_DISCOVERY)
    parser.add_argument(
        "--normalization-validation",
        type=Path,
        default=DEFAULT_NORMALIZATION_VALIDATION,
    )
    parser.add_argument(
        "--record-schema-validation",
        type=Path,
        default=DEFAULT_RECORD_SCHEMA_VALIDATION,
    )
    parser.add_argument("--duckdb-validation", type=Path, default=DEFAULT_DUCKDB_VALIDATION)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_release_manifest(
        source_inventory_path=args.source_inventory,
        schema_discovery_path=args.schema_discovery,
        normalization_validation_path=args.normalization_validation,
        record_schema_validation_path=args.record_schema_validation,
        duckdb_validation_path=args.duckdb_validation,
    )
    write_manifest(manifest, args.output)
    print(f"Wrote {args.output}")
    print(f"Publication status: {manifest['publication_status']}")
    print(f"Published: {manifest['published']}")
    print(f"Rows: {manifest['counts']['normalized_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
