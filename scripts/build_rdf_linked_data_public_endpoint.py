"""Build the RDF / Linked Data public endpoint release surface."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "rdf_linked_data_public_endpoint_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/rdf_linked_data_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/rdf_linked_data_validation_manifest.json"
MODEL_METADATA_PATH = ROOT / "manifests/rdf_linked_data_model_metadata.json"
SAMPLE_README_PATH = ROOT / "samples/rdf-linked-data/README.md"
TURTLE_PATH = ROOT / "samples/rdf-linked-data/linked-data.ttl"
JSONLD_PATH = ROOT / "samples/rdf-linked-data/linked-data.jsonld"
SHAPES_PATH = ROOT / "samples/rdf-linked-data/shapes.ttl"
SPARQL_PATH = ROOT / "samples/rdf-linked-data/sparql-queries.rq"
MAPPING_DOC_PATH = ROOT / "docs/rdf-linked-data-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/rdf-linked-data-public-endpoint-release.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
TRACK_PATH = ROOT / "conductor/tracks/rdf_linked_data_public_endpoint_release_20260610/index.md"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_rdf_linked_data_public_endpoint(
    *, manifest_path: Path = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    sample_manifest = _read_json(SAMPLE_MANIFEST_PATH)
    reason = (
        "Validated component exports are not yet available for a public RDF/linked-data release, "
        "and stable URI review remains pending."
    )
    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "endpoint": "RDF / Linked Data",
        "endpoint_track": TRACK_ID,
        "release_series_id": "rdf-linked-data-public-endpoint",
        "release_level": "endpoint",
        "artifact_name": "RDF / Linked Data public endpoint release",
        "artifact_version": "0.1.0-deferred.20260610",
        "release_status": "blocked-pending-validated-components",
        "publication_target": "public endpoint release package deferred",
        "upstream_contribution_target": "RDF / linked-data maintainers after validated component exports and SHACL review",
        "validation_manifest": "manifests/rdf_linked_data_public_endpoint_validation.json",
        "input_release_versions": {
            "document_level": "0.1.0",
            "neutral_components": "manifests/neutral_component_model.json",
            "authority_sources": "manifests/authority_sources.json",
            "id_uri_policy": "manifests/id_uri_policy.json",
            "model_metadata": "manifests/rdf_linked_data_model_metadata.json",
        },
        "known_exclusions": [
            "No public RDF / linked-data release is claimed.",
            "NIF export is excluded.",
            "External ontology acceptance is excluded.",
            "Stable URI review is pending.",
        ],
        "dependency_groups": ["authority", "metadata", "rdf", "schema"],
        "dependency_validation": {
            "tool_versions": {
                "python": "3.13",
            },
            "library_versions": {
                "pyshacl": "manual-validator",
                "rdflib": "manual-validator",
            },
            "model_versions": {
                "vocabulary": "rdf-linked-data-fixture-20260610",
            },
            "lock_or_constraints": "requirements/rdf.txt, requirements/schema.txt, requirements/metadata.txt, requirements/authority.txt",
            "install_commands": [
                "python -m pip install -r requirements/rdf.txt -r requirements/schema.txt -r requirements/metadata.txt -r requirements/authority.txt"
            ],
            "release_affecting_dependencies": [
                "RDF serializer versions",
                "SHACL validator versions",
                "ontology/mapping libraries",
                "metadata export tooling",
            ],
        },
        "validation_command": "python scripts/check_rdf_linked_data_public_endpoint.py",
        "output_artifacts": [
            "samples/rdf-linked-data/linked-data.ttl",
            "samples/rdf-linked-data/linked-data.jsonld",
            "samples/rdf-linked-data/shapes.ttl",
            "samples/rdf-linked-data/sparql-queries.rq",
            "samples/rdf-linked-data/README.md",
        ],
        "validation_results": {
            "component_metadata_validated": False,
            "readiness_status": "blocked-pending-validated-components",
            "blocking_errors": 0,
        },
        "traceability": sample_manifest["traceability"],
        "public_claim": {
            "status": "deferred",
            "reason": reason,
            "sample_only": True,
        },
        "source_manifests": [
            "manifests/rdf_linked_data_validation_manifest.json",
            "manifests/rdf_linked_data_model_metadata.json",
            "manifests/neutral_component_model.json",
            "manifests/dependency_extras_policy.json",
            "manifests/release_ladder.json",
            "docs/rdf-linked-data-mapping.md",
            "docs/endpoint-contracts.md",
            "docs/rdf-linked-data-public-endpoint-release.md",
        ],
        "source_hashes": {
            "sample_manifest": "referenced-in-sample-manifest",
            "model_metadata": "referenced-in-source-manifests",
            "release_ladder": "referenced-in-source-manifests",
        },
        "manifest_sha256": "deferred-public-endpoint-manifest",
    }
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the RDF / Linked Data public endpoint release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_rdf_linked_data_public_endpoint(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Release status: {manifest['release_status']}")
    print(f"Public claim: {manifest['public_claim']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
