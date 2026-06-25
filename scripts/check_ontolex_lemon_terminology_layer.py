"""Validate the sample OntoLex-Lemon terminology layer."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RELEASE_STATUS = "release-ready-sample-ontolex-lemon-layer"
TRACK = ROOT / "conductor" / "tracks" / "ontolex_lemon_terminology_layer_20260610"
MANIFEST = ROOT / "manifests" / "ontolex_lemon_terminology_layer.json"
SCHEMA = ROOT / "schemas" / "ontolex_lemon_terminology_layer.schema.json"
SAMPLE_JSON = ROOT / "samples" / "ontolex-lemon-terminology-layer" / "terminology.json"
SAMPLE_TTL = ROOT / "samples" / "ontolex-lemon-terminology-layer" / "terminology.ttl"
README = ROOT / "samples" / "ontolex-lemon-terminology-layer" / "README.md"
DOC = ROOT / "docs" / "ontolex-lemon-terminology-layer.md"
TRACKS_MD = ROOT / "conductor" / "tracks.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    manifest = load_json(MANIFEST)
    sample = load_json(SAMPLE_JSON)
    schema = load_json(SCHEMA)
    jsonschema.validate(sample, schema)

    require(manifest["release_status"] == RELEASE_STATUS, "manifest release status is stale")
    require(sample["release_status"] == RELEASE_STATUS, "sample release status is stale")
    require(manifest["term_count"] >= 6, "manifest must record at least six sample terms")
    require(len(sample["terms"]) >= 6, "sample must contain at least six terms")

    claims = sample["public_claims"]
    require(claims["sample_terminology_layer"] is True, "sample claim must be explicit")
    for key in (
        "full_corpus_vocabulary",
        "authoritative_legal_definitions",
        "official_parliamentary_glossary",
        "external_ontology_acceptance",
        "stable_uri_review_complete",
    ):
        require(claims[key] is False, f"must not claim {key}")

    ttl = SAMPLE_TTL.read_text(encoding="utf-8")
    for token in (
        "ontolex:LexicalEntry",
        "ontolex:LexicalSense",
        "skos:Concept",
        "skos:prefLabel",
        "not an authoritative legal vocabulary",
    ):
        require(token in ttl, f"Turtle missing {token}")

    docs = "\n".join(
        [
            README.read_text(encoding="utf-8"),
            DOC.read_text(encoding="utf-8"),
            (TRACK / "plan.md").read_text(encoding="utf-8"),
            (TRACK / "index.md").read_text(encoding="utf-8"),
            (TRACK / "evidence.md").read_text(encoding="utf-8"),
        ],
    )
    for phrase in (
        RELEASE_STATUS,
        "optional terminology layer",
        "does not claim a full corpus vocabulary",
        "authoritative legal definitions",
        "stable URI review",
    ):
        require(phrase in docs, f"documentation missing: {phrase}")

    metadata = load_json(TRACK / "metadata.json")
    require(metadata.get("status") == "complete", "track metadata must be complete")
    require(
        "### [x] Track: OntoLex-Lemon Terminology Layer" in TRACKS_MD.read_text(encoding="utf-8"),
        "track registry must mark OntoLex complete",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
