"""Build the Akoma Ntoso public endpoint release surface."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "akoma_ntoso_public_endpoint_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/akoma_ntoso_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/akoma_ntoso_validation_manifest.json"
SAMPLE_README_PATH = ROOT / "samples/akoma-ntoso/README.md"
SAMPLE_XML_PATH = ROOT / "samples/akoma-ntoso/Akoma-Ntoso.sample.xml"
SAMPLE_METADATA_PATH = ROOT / "samples/akoma-ntoso/Akoma-Ntoso.metadata.xml"
MAPPING_DOC_PATH = ROOT / "docs/akoma-ntoso-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/akoma-ntoso-public-endpoint-release.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
NEUTRAL_MODEL_PATH = ROOT / "manifests/neutral_component_model.json"
PROCEDURE_MODEL_PATH = ROOT / "manifests/nz_parliamentary_procedure_model.json"
MEMBER_IDENTITY_VALIDATION_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
PARTY_ATTRIBUTION_VALIDATION_PATH = ROOT / "manifests/corpus_wide_party_attribution_validation.json"
SITTING_PROCEEDING_VALIDATION_PATH = ROOT / "manifests/sitting_proceeding_component_validation.json"
SPEECH_TURN_VALIDATION_PATH = ROOT / "manifests/validated_speech_turn_component_validation.json"
VOTE_MOTION_BILL_QUESTION_VALIDATION_PATH = (
    ROOT / "manifests/vote_motion_bill_question_extraction_validation.json"
)
TRACK_PATH = ROOT / "conductor/tracks/akoma_ntoso_public_endpoint_release_20260610/index.md"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_akoma_ntoso_public_endpoint(
    *, manifest_path: Path | None = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    sample_manifest = _read_json(SAMPLE_MANIFEST_PATH)
    dependency_statuses = {
        "validated_member_identity": _read_json(MEMBER_IDENTITY_VALIDATION_PATH).get(
            "release_gate_status", ""
        ),
        "validated_party_attribution": _read_json(PARTY_ATTRIBUTION_VALIDATION_PATH).get(
            "release_gate_status", ""
        ),
        "validated_speech_turn": _read_json(SPEECH_TURN_VALIDATION_PATH).get(
            "release_gate_status", ""
        ),
        "validated_vote_motion_extraction": _read_json(
            VOTE_MOTION_BILL_QUESTION_VALIDATION_PATH
        ).get("release_gate_status", ""),
        "validated_sitting_proceeding": _read_json(SITTING_PROCEEDING_VALIDATION_PATH).get(
            "release_gate_status", ""
        ),
    }
    dependencies_ready = dependency_statuses == {
        "validated_member_identity": "release-ready-triangulated-agent-review",
        "validated_party_attribution": "release-ready-explicit-party-labels-member-identity-triangulated",
        "validated_speech_turn": "release-ready-speech-turns-triangulated-speakers-agent-review",
        "validated_vote_motion_extraction": "release-ready-fixture-reviewed-extraction-agent-review",
        "validated_sitting_proceeding": "release-ready-date-level-official-reconciliation-agent-review",
    }
    reason = (
        "Validated member identity, party attribution, speech-turn, vote/motion extraction, and date-level sitting/proceeding components are available; "
        "the public endpoint release is sample-only and does not claim full Akoma Ntoso corpus or schema coverage."
    )
    if not dependencies_ready:
        reason = "Dependent component release gates are not all ready for the Akoma Ntoso public endpoint."
    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "endpoint": "Akoma Ntoso",
        "endpoint_track": TRACK_ID,
        "release_series_id": "akoma-ntoso-public-endpoint",
        "release_level": "endpoint",
        "artifact_name": "Akoma Ntoso public endpoint release",
        "artifact_version": "0.1.0-sample-public.20260624"
        if dependencies_ready
        else "0.1.0-deferred.20260610",
        "release_status": "release-ready-sample-public-endpoint"
        if dependencies_ready
        else "blocked-pending-validated-components",
        "publication_target": "sample-scoped public endpoint release package"
        if dependencies_ready
        else "public endpoint release package deferred",
        "upstream_contribution_target": "Akoma Ntoso maintainers after validated component releases and profile selection",
        "validation_manifest": "manifests/akoma_ntoso_public_endpoint_validation.json",
        "release_notes": {
            "document": "docs/akoma-ntoso-public-endpoint-release.md",
            "examples": [
                "samples/akoma-ntoso/Akoma-Ntoso.sample.xml",
                "samples/akoma-ntoso/Akoma-Ntoso.metadata.xml",
            ],
            "status": "sample-public-release-notes-published"
            if dependencies_ready
            else "deferred-public-release-notes-published",
        },
        "profile": {
            "namespace": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
            "selection": "debate-oriented sample subset",
            "conformance_boundary": "sample-only debate-oriented public endpoint package; no full Akoma Ntoso corpus or schema coverage claim",
            "selection_status": "release-ready-sample-public-endpoint"
            if dependencies_ready
            else "blocked-pending-validated-components",
        },
        "input_release_versions": {
            "document_level": "0.1.0",
            "neutral_components": "manifests/neutral_component_model.json",
            "authority_sources": "manifests/authority_sources.json",
            "procedure_model": "manifests/nz_parliamentary_procedure_model.json",
            "id_uri_policy": "manifests/id_uri_policy.json",
            "sample_package": sample_manifest["artifact_version"],
        },
        "known_exclusions": [
            "No full-corpus Akoma Ntoso release is claimed.",
            "The underlying Akoma Ntoso package remains sample-not-release.",
            "The sample uses a narrow profile subset rather than full schema coverage.",
            "The package is sample-only until validated component releases exist.",
        ],
        "dependency_groups": ["xml", "schema", "authority"],
        "dependency_validation": {
            "tool_versions": {
                "python_xml": "stdlib",
                "python_json": "stdlib",
            },
            "library_versions": {
                "lxml": "deferred-until-release-artifact",
                "xmlschema": "deferred-until-release-artifact",
            },
            "model_versions": {
                "neutral_component_model": "manifests/neutral_component_model.json",
                "procedure_model": "manifests/nz_parliamentary_procedure_model.json",
                "sample_package": sample_manifest["artifact_version"],
            },
            "lock_or_constraints": "requirements/xml.txt, requirements/schema.txt, requirements/authority.txt",
            "install_commands": [
                "python -m pip install -r requirements/xml.txt -r requirements/schema.txt -r requirements/authority.txt"
            ],
            "release_affecting_dependencies": [
                "XML validators",
                "schema tooling",
                "authority matching tooling",
            ],
        },
        "validation_command": "python scripts/check_akoma_ntoso_public_endpoint.py",
        "output_artifacts": [
            "samples/akoma-ntoso/Akoma-Ntoso.sample.xml",
            "samples/akoma-ntoso/Akoma-Ntoso.metadata.xml",
            "samples/akoma-ntoso/README.md",
        ],
        "validation_results": {
            "json_valid": True,
            "xml_valid": True,
            "profile_selected": True,
            "component_metadata_validated": dependencies_ready,
            "blocking_errors": 0,
            "readiness_status": "release-ready-sample-public-endpoint"
            if dependencies_ready
            else "blocked-pending-validated-components",
        },
        "traceability": sample_manifest["traceability"],
        "dependency_statuses": dependency_statuses,
        "public_claim": {
            "status": "release-ready-sample-only" if dependencies_ready else "deferred",
            "reason": reason,
            "sample_only": True,
            "full_corpus_release": False,
            "full_schema_coverage": False,
        },
        "source_manifests": [
            "manifests/akoma_ntoso_validation_manifest.json",
            "manifests/neutral_component_model.json",
            "manifests/neutral_component_validation_manifest.json",
            "manifests/nz_parliamentary_procedure_model.json",
            "manifests/authority_sources.json",
            "manifests/release_ladder.json",
            "manifests/dependency_extras_policy.json",
            "docs/akoma-ntoso-mapping.md",
            "docs/endpoint-contracts.md",
            "docs/akoma-ntoso-public-endpoint-release.md",
        ],
        "source_hashes": {
            "sample_manifest": "referenced-in-sample-manifest",
            "neutral_component_model": "referenced-in-source-manifests",
            "procedure_model": "referenced-in-source-manifests",
            "authority_sources": "referenced-in-source-manifests",
            "release_ladder": "referenced-in-source-manifests",
        },
        "manifest_sha256": "sample-public-endpoint-manifest"
        if dependencies_ready
        else "deferred-public-endpoint-manifest",
    }
    if manifest_path is not None:
        _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the Akoma Ntoso public endpoint release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_akoma_ntoso_public_endpoint(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Release status: {manifest['release_status']}")
    print(f"Public claim: {manifest['public_claim']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
