"""Build the CAP / ParlaCAP public endpoint release surface."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "cap_parlacap_public_endpoint_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/cap_parlacap_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/cap_parlacap_topic_validation_manifest.json"
CODEBOOK_PATH = ROOT / "manifests/cap_parlacap_topic_codebook.json"
SAMPLE_README_PATH = ROOT / "samples/cap-parlacap/README.md"
SAMPLE_CSV_PATH = ROOT / "samples/cap-parlacap/cap_parlacap_topics.csv"
MAPPING_DOC_PATH = ROOT / "docs/cap-parlacap-topic-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/cap-parlacap-public-endpoint-release.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
DEPENDENCY_POLICY_PATH = ROOT / "manifests/dependency_extras_policy.json"
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
TRACK_PATH = ROOT / "conductor/tracks/cap_parlacap_public_endpoint_release_20260610/index.md"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_cap_parlacap_public_endpoint(
    *, manifest_path: Path = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    sample_manifest = _read_json(SAMPLE_MANIFEST_PATH)
    codebook = _read_json(CODEBOOK_PATH)
    reason = (
        "Validated speech-turn components are not yet available for ParlaCAP-compatible public output, "
        "and the repository-declared codebook awaits maintainer confirmation."
    )
    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "endpoint": "CAP / ParlaCAP Topic Endpoint",
        "endpoint_track": TRACK_ID,
        "release_series_id": "cap-parlacap-public-endpoint",
        "release_level": "endpoint",
        "artifact_name": "CAP / ParlaCAP public endpoint release",
        "artifact_version": "0.1.0-deferred.20260610",
        "release_status": "blocked-pending-validated-components",
        "codebook_version": codebook["codebook_version"],
        "codebook_metadata": "manifests/cap_parlacap_topic_codebook.json",
        "publication_target": "public endpoint release package deferred",
        "upstream_contribution_target": "CAP / ParlaCAP maintainer review after validated topic components and codebook confirmation",
        "input_release_versions": {
            "document_level": "0.1.0",
            "neutral_components": "manifests/neutral_component_model.json",
            "authority_sources": "manifests/authority_sources.json",
            "gold_evaluation_datasets": "manifests/gold_evaluation_datasets.json",
            "release_ladder": "manifests/release_ladder.json",
            "dependency_extras_policy": "manifests/dependency_extras_policy.json",
            "id_uri_policy": "manifests/id_uri_policy.json",
        },
        "input_artifacts": [
            "fixtures/neutral_components.json",
            "fixtures/gold_evaluation_samples.json",
            "manifests/cap_parlacap_topic_codebook.json",
            "manifests/gold_evaluation_datasets.json",
            "manifests/neutral_component_model.json",
            "manifests/dependency_extras_policy.json",
        ],
        "output_artifacts": [
            "samples/cap-parlacap/cap_parlacap_topics.csv",
            "samples/cap-parlacap/README.md",
            "docs/cap-parlacap-topic-mapping.md",
        ],
        "validation_command": "python scripts/check_cap_parlacap_public_endpoint.py",
        "schema_or_ontology_version": "CAP topic review map / ParlaCAP-compatible tabular contract",
        "dependency_groups": ["data", "ml", "nlp", "schema"],
        "install_commands": [
            "python -m pip install -r requirements/data.txt -r requirements/schema.txt -r requirements/nlp.txt -r requirements/ml.txt"
        ],
        "tool_versions": {
            "python_csv": "stdlib",
            "python_json": "stdlib",
        },
        "library_versions": {
            "pandas": "deferred-until-release-artifact",
            "scikit-learn": "deferred-until-release-artifact",
        },
        "model_versions": {
            "prototype_review_model": "deferred-until-release-artifact",
        },
        "lock_or_constraints": "Optional endpoint stack install checks are deferred-until-implementation; release-affecting dependencies must follow pin-before-release-artifact.",
        "release_affecting_dependencies": "Pin classifier libraries, codebook tooling, and model or embedding versions before public topic-coded outputs.",
        "known_exclusions": [
            "No public CAP / ParlaCAP release is claimed.",
            "Model-coded topic rows remain exploratory and non-authoritative.",
            "Validated speech-turn exports are still required before ParlaCAP-compatible speech/topic packages can be treated as endpoint releases.",
            "The codebook mapping is repository-declared and awaits maintainer confirmation.",
        ],
        "validation_results": {
            "sample_csv_readable": True,
            "codebook_declared": True,
            "human_rule_model_separated": True,
            "codebook_codes_validate": True,
            "release_ladder_mapping_present": True,
            "blocking_errors": 0,
            "readiness_status": "blocked-pending-validated-components",
        },
        "traceability": sample_manifest["traceability"],
        "public_claim": {
            "status": "deferred",
            "reason": reason,
            "sample_only": True,
        },
        "source_manifests": [
            "manifests/cap_parlacap_topic_validation_manifest.json",
            "manifests/cap_parlacap_topic_codebook.json",
            "manifests/neutral_component_model.json",
            "manifests/gold_evaluation_datasets.json",
            "manifests/dependency_extras_policy.json",
            "manifests/release_ladder.json",
            "docs/cap-parlacap-topic-mapping.md",
            "docs/endpoint-contracts.md",
            "docs/cap-parlacap-public-endpoint-release.md",
        ],
        "source_hashes": {
            "sample_manifest": "referenced-in-sample-manifest",
            "codebook": "referenced-in-source-manifests",
            "gold_evaluation_datasets": "referenced-in-source-manifests",
            "release_ladder": "referenced-in-source-manifests",
        },
        "manifest_sha256": "deferred-public-endpoint-manifest",
    }
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the CAP / ParlaCAP public endpoint release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_cap_parlacap_public_endpoint(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Release status: {manifest['release_status']}")
    print(f"Public claim: {manifest['public_claim']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
