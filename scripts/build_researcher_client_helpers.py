"""Build the researcher client helper manifest."""

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

from scripts.researcher_client_helpers import (  # noqa: E402
    DOCUMENT_SAMPLE_PATH,
    RDF_SAMPLE_PATH,
    duckdb_document_summary,
    python_document_summary,
    rdf_sample_summary,
)

DEFAULT_MANIFEST = ROOT / "manifests/researcher_client_helpers_manifest.json"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_researcher_client_helpers(
    *, manifest_path: Path | None = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    python_summary = python_document_summary(DOCUMENT_SAMPLE_PATH)
    duckdb_summary = duckdb_document_summary(DOCUMENT_SAMPLE_PATH)
    rdf_summary = rdf_sample_summary(RDF_SAMPLE_PATH)

    manifest = {
        "manifest_version": 1,
        "track_id": "researcher_client_helpers_20260610",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "release_status": "local-review-only",
        "supported_artifacts": {
            "document_sample": {
                "path": DOCUMENT_SAMPLE_PATH.relative_to(ROOT).as_posix(),
                "version": "sample-0.1.0",
                "language_surfaces": ["python", "duckdb"],
                "row_count": python_summary["row_count"],
                "document_types": [
                    item["document_type"] for item in duckdb_summary["rows_by_document_type"]
                ],
            },
            "rdf_sample": {
                "path": RDF_SAMPLE_PATH.relative_to(ROOT).as_posix(),
                "version": "sample-not-release",
                "language_surfaces": ["python"],
                "dataset_title": rdf_summary["dataset_titles"][0],
                "triple_count": rdf_summary["triple_count"],
            },
        },
        "helper_status": {
            "python_examples": "implemented",
            "duckdb_examples": "implemented",
            "r_examples": "deferred",
            "sparql_examples": "deferred",
        },
        "limitations": [
            "Helper examples are read-only and do not modify canonical generation scripts.",
            "R and standalone SPARQL examples remain deferred until RDF endpoint release artifacts are ready.",
            "The document sample is a tiny local-review fixture and not a corpus release artifact.",
        ],
        "validation_results": {
            "python_example_runs": True,
            "duckdb_example_runs": True,
            "rdf_sample_example_runs": True,
            "r_examples_deferred": True,
            "sparql_examples_deferred": True,
        },
    }
    if manifest_path is not None:
        _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the researcher client helper manifest.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_researcher_client_helpers(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Release status: {manifest['release_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
