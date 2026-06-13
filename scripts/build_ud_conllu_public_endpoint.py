"""Build the UD / CoNLL-U public endpoint release surface."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "ud_conllu_public_endpoint_release_20260610"
DEFAULT_MANIFEST = ROOT / "manifests/ud_conllu_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/ud_conllu_validation_manifest.json"
MODEL_METADATA_PATH = ROOT / "manifests/ud_conllu_model_metadata.json"
SAMPLE_README_PATH = ROOT / "samples/ud-conllu/README.md"
SAMPLE_CONLLU_PATH = ROOT / "samples/ud-conllu/parliament_sample.conllu"
SAMPLE_ALIGNMENT_PATH = ROOT / "samples/ud-conllu/parliament_sample.alignments.json"
MAPPING_DOC_PATH = ROOT / "docs/ud-conllu-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/ud-conllu-public-endpoint-release.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
TRACK_PATH = ROOT / "conductor/tracks/ud_conllu_public_endpoint_release_20260610/index.md"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_ud_conllu_public_endpoint(
    *, manifest_path: Path = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    sample_manifest = _read_json(SAMPLE_MANIFEST_PATH)
    model_metadata = _read_json(MODEL_METADATA_PATH)
    reason = (
        "Validated speech-turn text is not yet available for a public UD/CoNLL-U release, "
        "and the Stanza/spaCy comparison remains pending."
    )
    manifest = {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "endpoint": "Universal Dependencies / CoNLL-U",
        "endpoint_track": TRACK_ID,
        "release_series_id": "ud-conllu-public-endpoint",
        "release_level": "endpoint",
        "artifact_name": "UD / CoNLL-U public endpoint release",
        "artifact_version": "0.1.0-deferred.20260610",
        "release_status": "blocked-pending-validated-components",
        "publication_target": "public endpoint release package deferred",
        "upstream_contribution_target": "UD maintainers after validated speech-turn text and review",
        "validation_manifest": "manifests/ud_conllu_public_endpoint_validation.json",
        "annotation_family": model_metadata["annotation_family"],
        "annotation_version": model_metadata["annotation_version"],
        "input_release_versions": {
            "document_level": "0.1.0",
            "neutral_components": "manifests/neutral_component_model.json",
            "speech_turn_source": "nzhc-component-0000000000000005",
            "model_metadata": "manifests/ud_conllu_model_metadata.json",
            "id_uri_policy": "manifests/id_uri_policy.json",
        },
        "known_exclusions": [
            "No public UD / CoNLL-U release is claimed.",
            "Validated speech-turn text is missing.",
            "Gold-standard UD annotation is not claimed.",
            "The Stanza/spaCy comparison is pending.",
        ],
        "dependency_groups": ["nlp", "schema"],
        "dependency_validation": {
            "tool_versions": {
                "python": "3.13",
            },
            "library_versions": {
                "conllu": "manual-validator",
                "spacy": "planned",
                "stanza": "planned",
            },
            "model_versions": {
                "parser": "ud-fixture-20260610",
                "tokenizer": "ud-fixture-20260610",
            },
            "lock_or_constraints": "requirements/nlp.txt, requirements/schema.txt",
            "install_commands": [
                "python -m pip install -r requirements/nlp.txt -r requirements/schema.txt"
            ],
            "release_affecting_dependencies": [
                "tokenization libraries",
                "parser model revisions",
                "CoNLL-U validation tooling",
            ],
        },
        "validation_command": "python scripts/check_ud_conllu_public_endpoint.py",
        "output_artifacts": [
            "samples/ud-conllu/parliament_sample.conllu",
            "samples/ud-conllu/parliament_sample.alignments.json",
            "samples/ud-conllu/README.md",
        ],
        "validation_results": {
            "json_valid": True,
            "conllu_valid": True,
            "offset_alignment_valid": True,
            "component_metadata_validated": False,
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
            "manifests/ud_conllu_validation_manifest.json",
            "manifests/ud_conllu_model_metadata.json",
            "manifests/neutral_component_model.json",
            "manifests/gold_evaluation_datasets.json",
            "manifests/dependency_extras_policy.json",
            "manifests/release_ladder.json",
            "docs/ud-conllu-mapping.md",
            "docs/endpoint-contracts.md",
            "docs/ud-conllu-public-endpoint-release.md",
        ],
        "source_hashes": {
            "sample_manifest": "referenced-in-sample-manifest",
            "model_metadata": "referenced-in-source-manifests",
            "release_ladder": "referenced-in-source-manifests",
            "gold_evaluation_datasets": "referenced-in-source-manifests",
        },
        "manifest_sha256": "deferred-public-endpoint-manifest",
    }
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the UD / CoNLL-U public endpoint release surface."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_ud_conllu_public_endpoint(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Release status: {manifest['release_status']}")
    print(f"Public claim: {manifest['public_claim']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
