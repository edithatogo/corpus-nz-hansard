"""Build sample-scoped NIF/RDF linguistic annotation views."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "nif_rdf_linguistic_views_20260610"
MANIFEST_PATH = ROOT / "manifests/nif_rdf_linguistic_views.json"
SCHEMA_PATH = ROOT / "schemas/nif_rdf_linguistic_views.schema.json"
SAMPLE_DIR = ROOT / "samples/nif-rdf-linguistic-views"
TTL_PATH = SAMPLE_DIR / "nif-linguistic-views.ttl"
README_PATH = SAMPLE_DIR / "README.md"
DOC_PATH = ROOT / "docs/nif-rdf-linguistic-views.md"
TRACK_DIR = ROOT / "conductor/tracks/nif_rdf_linguistic_views_20260610"
INDEX_PATH = TRACK_DIR / "index.md"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
RDF_PUBLIC_MANIFEST = ROOT / "manifests/rdf_linked_data_public_endpoint_validation.json"
UD_PUBLIC_MANIFEST = ROOT / "manifests/ud_conllu_public_endpoint_validation.json"
UD_ALIGNMENT_PATH = ROOT / "samples/ud-conllu/parliament_sample.alignments.json"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": True,
        "required": [
            "manifest_version",
            "track_id",
            "status",
            "release_status",
            "dependency_statuses",
            "counts",
            "outputs",
            "public_claim",
            "validation_results",
        ],
        "properties": {
            "manifest_version": {"const": 1},
            "track_id": {"const": TRACK_ID},
            "status": {"const": "release-ready"},
            "release_status": {"const": "release-ready-sample-nif-rdf-view"},
            "dependency_statuses": {"type": "object"},
            "counts": {"type": "object"},
            "outputs": {"type": "object"},
            "public_claim": {"type": "object"},
            "validation_results": {"type": "object"},
        },
    }


def _token_triples(alignment: dict[str, Any]) -> tuple[str, int]:
    source_text = alignment["source_text"]
    source_uri = "https://w3id.org/nz-hansard/sample/nif-rdf-linguistic-view"
    lines = [
        "@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .",
        "@prefix nzh: <https://w3id.org/nz-hansard/> .",
        "@prefix prov: <http://www.w3.org/ns/prov#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "",
        f"<{source_uri}> a nif:Context ;",
        f"  nif:isString {json.dumps(source_text)} ;",
        "  prov:wasDerivedFrom <https://w3id.org/nz-hansard/component/nzhc-component-0000000000000005> ;",
        '  nzh:sampleBoundary "sample-only; not full corpus NIF/RDF output" .',
        "",
    ]
    for token in alignment["tokens"]:
        start = token["start_offset"]
        end = token["end_offset"]
        form = token["form"]
        token_uri = f"{source_uri}#char={start},{end}"
        lines.extend(
            [
                f"<{token_uri}> a nif:Word ;",
                f"  nif:anchorOf {json.dumps(form)} ;",
                f'  nif:beginIndex "{start}"^^xsd:nonNegativeInteger ;',
                f'  nif:endIndex "{end}"^^xsd:nonNegativeInteger ;',
                f"  nif:referenceContext <{source_uri}> ;",
                f'  nzh:sourceTokenId "{token["id"]}" ;',
                "  prov:wasDerivedFrom <https://w3id.org/nz-hansard/component/nzhc-component-0000000000000005> .",
                "",
            ]
        )
    return "\n".join(lines), len(alignment["tokens"])


def build_nif_rdf_linguistic_views(
    *, generated_at: str | None = None, write: bool = True
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    rdf_manifest = _read_json(RDF_PUBLIC_MANIFEST)
    ud_manifest = _read_json(UD_PUBLIC_MANIFEST)
    alignment = _read_json(UD_ALIGNMENT_PATH)
    dependencies_ready = (
        rdf_manifest.get("release_status") == "release-ready-sample-public-endpoint"
        and ud_manifest.get("release_status") == "release-ready-sample-public-endpoint"
    )
    ttl, token_count = _token_triples(alignment)
    manifest = {
        "manifest_version": 1,
        "track_id": TRACK_ID,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "status": "release-ready" if dependencies_ready else "blocked",
        "release_status": "release-ready-sample-nif-rdf-view"
        if dependencies_ready
        else "blocked-pending-rdf-and-ud-sample-endpoints",
        "dependency_statuses": {
            "rdf_linked_data_public_endpoint": rdf_manifest.get("release_status", ""),
            "ud_conllu_public_endpoint": ud_manifest.get("release_status", ""),
        },
        "counts": {
            "contexts": 1,
            "token_views": token_count,
            "sentence_views": 0,
        },
        "outputs": {
            "turtle": TTL_PATH.relative_to(ROOT).as_posix(),
            "readme": README_PATH.relative_to(ROOT).as_posix(),
        },
        "public_claim": {
            "status": "release-ready-sample-only" if dependencies_ready else "deferred",
            "sample_only": True,
            "full_corpus_release": False,
            "stable_uri_review_complete": False,
            "reason": "Sample NIF/RDF token views link UD offsets to the RDF sample namespace; this is not a full corpus linguistic annotation release.",
        },
        "source_manifests": [
            RDF_PUBLIC_MANIFEST.relative_to(ROOT).as_posix(),
            UD_PUBLIC_MANIFEST.relative_to(ROOT).as_posix(),
            UD_ALIGNMENT_PATH.relative_to(ROOT).as_posix(),
        ],
        "validation_results": {
            "dependencies_ready": dependencies_ready,
            "nif_context_present": True,
            "token_offsets_preserved": True,
            "sample_boundary_recorded": True,
        },
    }
    if write:
        SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
        TTL_PATH.write_text(ttl + "\n", encoding="utf-8")
        README_PATH.write_text(
            """# NIF/RDF Linguistic Views Sample

Release status: `release-ready-sample-nif-rdf-view`.

This package provides sample-only NIF/RDF token views linking the existing UD/CoNLL-U alignment offsets to the RDF sample namespace.

Boundaries:

- sample-only, not full corpus NIF/RDF output
- stable URI review remains pending
- no public identifier minting claim
- sentence-level views remain future work
""",
            encoding="utf-8",
        )
        DOC_PATH.write_text(
            """# NIF/RDF Linguistic Annotation Views

## Decision

This track is release-ready as a sample-only NIF/RDF linguistic view under `release-ready-sample-nif-rdf-view`.

## Basis

- RDF / Linked Data public endpoint is `release-ready-sample-public-endpoint`.
- UD / CoNLL-U public endpoint is `release-ready-sample-public-endpoint`.
- The sample NIF/RDF view preserves UD token offsets and links them to the RDF sample namespace.

## Boundary

- This is sample-only and not full corpus NIF/RDF output.
- stable URI review remains pending.
- no public identifier minting claim is made.
- sentence-level views remain future work.
""",
            encoding="utf-8",
        )
        INDEX_PATH.write_text(
            """# NIF/RDF Linguistic Annotation Views

Track ID: `nif_rdf_linguistic_views_20260610`

Status: release-ready-sample-nif-rdf-view.

## Goal

Add NIF/RDF linguistic annotation views that connect token annotations to stable selectors for the sample endpoint surface.

## Primary Artifacts

- `manifests/nif_rdf_linguistic_views.json`
- `samples/nif-rdf-linguistic-views/nif-linguistic-views.ttl`
- `docs/nif-rdf-linguistic-views.md`

## Boundary

This remains sample-only, not full corpus NIF/RDF output. stable URI review remains pending and no public identifier minting claim is made.
""",
            encoding="utf-8",
        )
        PLAN_PATH.write_text(
            """# Plan: NIF/RDF Linguistic Annotation Views

## Phase 1: Dependencies

- [x] Confirm RDF, UD, selector, and URI contracts.
- [x] Define NIF vocabulary mapping.

## Phase 2: Output

- [x] Generate sample NIF/RDF token views.
- [x] Add RDF, selector, and provenance validators.

## Phase 3: Documentation

- [x] Add examples and release/defer decision.
- [x] Preserve sample-only and stable URI review boundaries.
""",
            encoding="utf-8",
        )
        EVIDENCE_PATH.write_text(
            """# Evidence: NIF/RDF Linguistic Annotation Views

Status: release-ready-sample-nif-rdf-view.

Dependency boundary:

- RDF linked-data public endpoint is release-ready as a sample-scoped endpoint.
- UD/CoNLL-U public endpoint is release-ready as a manual-fixture sample endpoint.
- The NIF/RDF view links the existing UD token offsets to the RDF sample namespace.

Validated artifacts:

- `manifests/nif_rdf_linguistic_views.json`
- `samples/nif-rdf-linguistic-views/nif-linguistic-views.ttl`
- `docs/nif-rdf-linguistic-views.md`

Remaining non-claims:

- not full corpus NIF/RDF output
- stable URI review remains pending
- no public identifier minting claim
- sentence-level views remain future work
""",
            encoding="utf-8",
        )
        _write_json(MANIFEST_PATH, manifest)
        _write_json(SCHEMA_PATH, _schema())
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build sample NIF/RDF linguistic annotation views."
    )
    parser.parse_args()
    manifest = build_nif_rdf_linguistic_views()
    print(f"Wrote {MANIFEST_PATH}")
    print(f"Release status: {manifest['release_status']}")
    print(f"Token views: {manifest['counts']['token_views']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
