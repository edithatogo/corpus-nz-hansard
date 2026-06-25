"""Build the Popolo/Open Civic Data public endpoint release surface."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "popolo_opencivicdata_public_endpoint_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/popolo_opencivicdata_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/popolo_opencivicdata_validation_manifest.json"
SAMPLE_README_PATH = ROOT / "samples/popolo-opencivicdata/README.md"
SAMPLE_PEOPLE_PATH = ROOT / "samples/popolo-opencivicdata/people.json"
SAMPLE_ORGANIZATIONS_PATH = ROOT / "samples/popolo-opencivicdata/organizations.json"
SAMPLE_MEMBERSHIPS_PATH = ROOT / "samples/popolo-opencivicdata/memberships.json"
SAMPLE_MOTIONS_PATH = ROOT / "samples/popolo-opencivicdata/motions.json"
SAMPLE_VOTE_EVENTS_PATH = ROOT / "samples/popolo-opencivicdata/vote-events.json"
SAMPLE_VOTES_PATH = ROOT / "samples/popolo-opencivicdata/votes.jsonl"
SAMPLE_SPEECHES_PATH = ROOT / "samples/popolo-opencivicdata/speeches.jsonl"
MAPPING_DOC_PATH = ROOT / "docs/popolo-opencivicdata-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/popolo-opencivicdata-public-endpoint-release.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
NEUTRAL_MODEL_PATH = ROOT / "manifests/neutral_component_model.json"
PROCEDURE_MODEL_PATH = ROOT / "manifests/nz_parliamentary_procedure_model.json"
MEMBER_IDENTITY_VALIDATION_PATH = ROOT / "manifests/corpus_wide_member_identity_validation.json"
PARTY_ATTRIBUTION_VALIDATION_PATH = ROOT / "manifests/corpus_wide_party_attribution_validation.json"
SITTING_PROCEEDING_VALIDATION_PATH = ROOT / "manifests/sitting_proceeding_component_validation.json"
VOTE_MOTION_BILL_QUESTION_VALIDATION_PATH = (
    ROOT / "manifests/vote_motion_bill_question_extraction_validation.json"
)
SPEECH_TURN_VALIDATION_PATH = ROOT / "manifests/validated_speech_turn_component_validation.json"
TRACK_PATH = (
    ROOT / "conductor/tracks/popolo_opencivicdata_public_endpoint_release_20260610/index.md"
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_popolo_opencivicdata_public_endpoint(
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
        "validated_vote_motion_extraction": _read_json(
            VOTE_MOTION_BILL_QUESTION_VALIDATION_PATH
        ).get("release_gate_status", ""),
        "validated_speech_turn": _read_json(SPEECH_TURN_VALIDATION_PATH).get(
            "release_gate_status", ""
        ),
        "validated_sitting_proceeding": _read_json(SITTING_PROCEEDING_VALIDATION_PATH).get(
            "release_gate_status", ""
        ),
    }
    dependencies_ready = dependency_statuses == {
        "validated_member_identity": "release-ready-triangulated-agent-review",
        "validated_party_attribution": "release-ready-explicit-party-labels-member-identity-triangulated",
        "validated_vote_motion_extraction": "release-ready-fixture-reviewed-extraction-agent-review",
        "validated_speech_turn": "release-ready-speech-turns-triangulated-speakers-agent-review",
        "validated_sitting_proceeding": "release-ready-date-level-official-reconciliation-agent-review",
    }
    reason = (
        "Validated member identity, party attribution, vote/motion extraction, speech-turn, and date-level sitting/proceeding components are available; "
        "the public endpoint release is sample-only and does not claim full Popolo/Open Civic Data corpus readiness."
    )
    if not dependencies_ready:
        reason = "Dependent component release gates are not all ready for the Popolo/Open Civic Data public endpoint."
    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "endpoint": "Popolo / Open Civic Data",
        "endpoint_track": TRACK_ID,
        "release_series_id": "popolo-opencivicdata-public-endpoint",
        "release_level": "endpoint",
        "artifact_name": "Popolo / Open Civic Data public endpoint release",
        "artifact_version": "0.1.0-sample-public.20260624"
        if dependencies_ready
        else "0.1.0-deferred.20260610",
        "release_status": "release-ready-sample-public-endpoint"
        if dependencies_ready
        else "blocked-pending-validated-components",
        "publication_target": "sample-scoped public endpoint release package"
        if dependencies_ready
        else "public endpoint release package deferred",
        "upstream_contribution_target": "mySociety/PublicWhip-style parser comparison after validated component releases and maintainer agreement",
        "validation_manifest": "manifests/popolo_opencivicdata_public_endpoint_validation.json",
        "input_release_versions": {
            "document_level": "0.1.0",
            "neutral_components": "manifests/neutral_component_model.json",
            "authority_sources": "manifests/authority_sources.json",
            "procedure_model": "manifests/nz_parliamentary_procedure_model.json",
            "id_uri_policy": "manifests/id_uri_policy.json",
            "sample_package": sample_manifest["artifact_version"],
        },
        "known_exclusions": [
            "No full-corpus Popolo/Open Civic Data release is claimed.",
            "The underlying Popolo/Open Civic Data package remains sample-not-release.",
            "Full voting records are not inferred from text patterns alone.",
            "RDF output is excluded until the RDF endpoint exists.",
        ],
        "dependency_groups": ["data", "schema", "authority"],
        "dependency_validation": {
            "tool_versions": {
                "python_json": "stdlib",
                "csv": "stdlib",
            },
            "library_versions": {
                "pandas": "deferred-until-release-artifact",
                "pydantic": "deferred-until-release-artifact",
                "rapidfuzz": "deferred-until-release-artifact",
            },
            "model_versions": {
                "neutral_component_model": "manifests/neutral_component_model.json",
                "procedure_model": "manifests/nz_parliamentary_procedure_model.json",
                "sample_package": sample_manifest["artifact_version"],
            },
            "lock_or_constraints": "requirements/data.txt, requirements/schema.txt, requirements/authority.txt",
            "install_commands": [
                "python -m pip install -r requirements/data.txt -r requirements/schema.txt -r requirements/authority.txt"
            ],
            "release_affecting_dependencies": [
                "dataframe tooling",
                "schema validation tooling",
                "authority matching tooling",
            ],
        },
        "validation_command": "python scripts/check_popolo_opencivicdata_public_endpoint.py",
        "output_artifacts": [
            "samples/popolo-opencivicdata/people.json",
            "samples/popolo-opencivicdata/organizations.json",
            "samples/popolo-opencivicdata/memberships.json",
            "samples/popolo-opencivicdata/motions.json",
            "samples/popolo-opencivicdata/vote-events.json",
            "samples/popolo-opencivicdata/votes.jsonl",
            "samples/popolo-opencivicdata/speeches.jsonl",
            "samples/popolo-opencivicdata/README.md",
        ],
        "validation_results": {
            "json_valid": True,
            "jsonl_valid": True,
            "date_ranges_valid": True,
            "referential_integrity": True,
            "party_vote_distinguished": True,
            "individual_votes_present": False,
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
        },
        "source_manifests": [
            "manifests/popolo_opencivicdata_validation_manifest.json",
            "manifests/neutral_component_model.json",
            "manifests/neutral_component_validation_manifest.json",
            "manifests/nz_parliamentary_procedure_model.json",
            "manifests/authority_sources.json",
            "manifests/release_ladder.json",
            "manifests/dependency_extras_policy.json",
            "docs/popolo-opencivicdata-mapping.md",
            "docs/endpoint-contracts.md",
            "docs/popolo-opencivicdata-public-endpoint-release.md",
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
        description="Build the Popolo/Open Civic Data public endpoint release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_popolo_opencivicdata_public_endpoint(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Release status: {manifest['release_status']}")
    print(f"Public claim: {manifest['public_claim']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
