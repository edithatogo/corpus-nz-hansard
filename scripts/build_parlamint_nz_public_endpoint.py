"""Build the ParlaMint-NZ public endpoint release surface."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "parlamint_nz_public_endpoint_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/parlamint_nz_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/parlamint_nz_validation_manifest.json"
SAMPLE_README_PATH = ROOT / "samples/parlamint-nz/README.md"
SAMPLE_XML_PATH = ROOT / "samples/parlamint-nz/ParlaMint-NZ.sample.xml"
SAMPLE_METADATA_PATH = ROOT / "samples/parlamint-nz/ParlaMint-NZ.metadata.xml"
MAPPING_DOC_PATH = ROOT / "docs/parlamint-nz-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/parlamint-nz-public-endpoint-release.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
NEUTRAL_MODEL_PATH = ROOT / "manifests/neutral_component_model.json"
PARTY_ATTRIBUTION_VALIDATION_PATH = ROOT / "manifests/corpus_wide_party_attribution_validation.json"
MEMBER_IDENTITY_VALIDATION_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
SPEECH_TURN_VALIDATION_PATH = ROOT / "manifests/validated_speech_turn_component_validation.json"
SITTING_PROCEEDING_VALIDATION_PATH = ROOT / "manifests/sitting_proceeding_component_validation.json"
TRACK_PATH = ROOT / "conductor/tracks/parlamint_nz_public_endpoint_release_20260610/index.md"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parlamint_nz_public_endpoint(
    *, manifest_path: Path = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    sample_manifest = _read_json(SAMPLE_MANIFEST_PATH)
    reason = (
        "Validated member identity, party attribution, speech-turn, and sitting/proceeding "
        "components are not all available for a public ParlaMint-NZ release."
    )
    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "endpoint": "ParlaMint-NZ / TEI",
        "endpoint_track": TRACK_ID,
        "release_series_id": "parlamint-nz-public-endpoint",
        "release_level": "endpoint",
        "artifact_name": "ParlaMint-NZ public endpoint release",
        "artifact_version": "0.1.0-deferred.20260610",
        "release_status": "blocked-pending-validated-components",
        "publication_target": "public endpoint release package deferred",
        "upstream_contribution_target": "ParlaMint / Parla-CLARIN maintainer review after validated component releases",
        "validation_manifest": "manifests/parlamint_nz_validation_manifest.json",
        "input_release_versions": {
            "document_level": "0.1.0",
            "neutral_components": "manifests/neutral_component_model.json",
            "authority_sources": "manifests/authority_sources.json",
            "procedure_model": "manifests/nz_parliamentary_procedure_model.json",
            "id_uri_policy": "manifests/id_uri_policy.json",
            "sample_package": sample_manifest["artifact_version"],
        },
        "known_exclusions": [
            "No public ParlaMint-NZ release is claimed.",
            "Validated member identity, party attribution, speech-turn, and sitting/proceeding inputs are missing.",
            "Full ParlaMint schema validation remains deferred until validated neutral component releases exist.",
            "Optional linguistic annotations are excluded until UD/CoNLL-U artifacts exist.",
        ],
        "dependency_groups": ["xml", "schema", "authority", "nlp"],
        "dependency_validation": {
            "tool_versions": {
                "python_xml_etree": "stdlib",
                "jsonschema": "runtime",
            },
            "library_versions": {
                "lxml": "deferred-until-release-artifact",
                "xmlschema": "deferred-until-release-artifact",
            },
            "model_versions": {
                "neutral_component_model": "manifests/neutral_component_model.json",
                "sample_package": sample_manifest["artifact_version"],
            },
            "lock_or_constraints": "requirements/xml.txt, requirements/schema.txt, requirements/authority.txt, requirements/nlp.txt",
            "install_commands": [
                "python -m pip install -r requirements/xml.txt -r requirements/schema.txt -r requirements/authority.txt -r requirements/nlp.txt"
            ],
            "release_affecting_dependencies": [
                "XML validation tooling",
                "TEI / ParlaMint schema tooling",
                "NLP libraries for optional linguistic annotations",
            ],
        },
        "validation_command": "python scripts/check_parlamint_nz_public_endpoint.py",
        "output_artifacts": [
            "samples/parlamint-nz/ParlaMint-NZ.sample.xml",
            "samples/parlamint-nz/ParlaMint-NZ.metadata.xml",
            "samples/parlamint-nz/README.md",
        ],
        "validation_results": {
            "component_metadata_validated": False,
            "readiness_status": "blocked-pending-validated-components",
            "blocking_errors": 0,
        },
        "traceability": [
            {
                "neutral_component_ids": sample_manifest["traceability"][0][
                    "neutral_component_ids"
                ],
                "sample_package": "samples/parlamint-nz",
            }
        ],
        "public_claim": {
            "status": "deferred",
            "reason": reason,
            "sample_only": True,
        },
        "source_manifests": [
            "manifests/parlamint_nz_validation_manifest.json",
            "manifests/neutral_component_model.json",
            "manifests/neutral_component_validation_manifest.json",
            "manifests/nz_parliamentary_procedure_model.json",
            "manifests/authority_sources.json",
            "manifests/release_ladder.json",
            "manifests/dependency_extras_policy.json",
            "docs/parlamint-nz-mapping.md",
            "docs/endpoint-contracts.md",
            "docs/parlamint-nz-public-endpoint-release.md",
        ],
        "source_hashes": {
            "sample_manifest": "referenced-in-sample-manifest",
            "neutral_component_model": "referenced-in-source-manifests",
            "procedure_model": "referenced-in-source-manifests",
            "authority_sources": "referenced-in-source-manifests",
            "release_ladder": "referenced-in-source-manifests",
        },
        "manifest_sha256": "deferred-public-endpoint-manifest",
    }
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the ParlaMint-NZ public endpoint release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_parlamint_nz_public_endpoint(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Release status: {manifest['release_status']}")
    print(f"Public claim: {manifest['public_claim']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
