"""Validate sample-scoped NIF/RDF linguistic annotation views."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/nif_rdf_linguistic_views.json"
SCHEMA_PATH = ROOT / "schemas/nif_rdf_linguistic_views.schema.json"
TTL_PATH = ROOT / "samples/nif-rdf-linguistic-views/nif-linguistic-views.ttl"
README_PATH = ROOT / "samples/nif-rdf-linguistic-views/README.md"
DOC_PATH = ROOT / "docs/nif-rdf-linguistic-views.md"
TRACK_DIR = ROOT / "conductor/tracks/nif_rdf_linguistic_views_20260610"
INDEX_PATH = TRACK_DIR / "index.md"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
METADATA_PATH = TRACK_DIR / "metadata.json"
TRACKS_PATH = ROOT / "conductor/tracks.md"
UD_ALIGNMENT_PATH = ROOT / "samples/ud-conllu/parliament_sample.alignments.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        TTL_PATH,
        README_PATH,
        DOC_PATH,
        INDEX_PATH,
        PLAN_PATH,
        EVIDENCE_PATH,
        METADATA_PATH,
        UD_ALIGNMENT_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures
    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    for error in sorted(
        Draft202012Validator(schema).iter_errors(manifest), key=lambda item: list(item.path)
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")
    if manifest["release_status"] != "release-ready-sample-nif-rdf-view":
        failures.append("NIF/RDF release_status must be release-ready-sample-nif-rdf-view.")
    if manifest["public_claim"].get("sample_only") is not True:
        failures.append("NIF/RDF public claim must remain sample-only.")
    if manifest["public_claim"].get("full_corpus_release") is not False:
        failures.append("NIF/RDF must not claim full corpus release.")
    if manifest["public_claim"].get("stable_uri_review_complete") is not False:
        failures.append("NIF/RDF stable URI review must remain pending.")
    alignment = _json(UD_ALIGNMENT_PATH)
    ttl = _read(TTL_PATH)
    if "nif:Context" not in ttl or "nif:Word" not in ttl:
        failures.append("NIF/RDF Turtle must include nif:Context and nif:Word.")
    if "sample-only; not full corpus NIF/RDF output" not in ttl:
        failures.append("NIF/RDF Turtle must record sample-only boundary.")
    if manifest["counts"].get("token_views") != len(alignment["tokens"]):
        failures.append("NIF/RDF token count must match UD alignment tokens.")
    for token in alignment["tokens"]:
        expected = f"#char={token['start_offset']},{token['end_offset']}"
        if expected not in ttl:
            failures.append(f"NIF/RDF Turtle missing selector {expected}.")
    for path, terms in {
        DOC_PATH: (
            "release-ready-sample-nif-rdf-view",
            "sample-only",
            "stable URI review",
            "no public identifier minting claim",
        ),
        README_PATH: ("release-ready-sample-nif-rdf-view", "sample-only", "stable URI review"),
        INDEX_PATH: ("release-ready-sample-nif-rdf-view", "not full corpus NIF/RDF output"),
        EVIDENCE_PATH: (
            "release-ready-sample-nif-rdf-view",
            "not full corpus NIF/RDF output",
            "sentence-level views remain future work",
        ),
    }.items():
        text = _read(path)
        for term in terms:
            if term not in text:
                failures.append(f"{path.relative_to(ROOT).as_posix()} is missing: {term}")
    metadata = _json(METADATA_PATH)
    if metadata.get("status") != "complete":
        failures.append("NIF/RDF metadata status must be complete.")
    tracks = _read(TRACKS_PATH)
    if "### [x] Track: NIF/RDF Linguistic Annotation Views" not in tracks:
        failures.append("Track registry must mark NIF/RDF as complete.")
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"NIF-RDF-LINGUISTIC: {failure}")
        return 1
    print("NIF/RDF linguistic annotation views are sample-release consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
