"""Validate canonical ID/URI policy and deterministic examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from scripts.canonical_ids import ID_PATTERN, canonical_id, canonical_uri
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.canonical_ids import ID_PATTERN, canonical_id, canonical_uri

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/id_uri_policy.json"
SCHEMA_PATH = ROOT / "schemas/canonical_id_uri_policy.schema.json"
DOC_PATH = ROOT / "docs/canonical-id-uri-policy.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
SHARED_CORE_DOC_PATH = ROOT / "docs/shared-nz-corpus-core-schema.md"
TRACK_PATH = ROOT / "conductor/tracks/canonical_id_uri_policy_20260609/evidence.md"

REQUIRED_CLASSES = {
    "document",
    "neutral-component",
    "endpoint-artifact",
    "authority-source",
    "gold-evaluation-sample",
}
REQUIRED_KINDS = {"document", "component", "endpoint", "authority", "sample"}
REQUIRED_ENDPOINT_TRACKS = {
    "parlamint_nz_endpoint_20260609",
    "popolo_opencivicdata_endpoint_20260609",
    "akoma_ntoso_endpoint_20260609",
    "cap_parlacap_topic_endpoint_20260609",
    "ud_conllu_endpoint_20260609",
    "rdf_linked_data_endpoint_20260609",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _kind_for_example(artifact_class: str) -> str:
    if artifact_class == "neutral-component":
        return "component"
    if artifact_class == "endpoint-artifact":
        return "endpoint"
    if artifact_class == "authority-source":
        return "authority"
    if artifact_class == "gold-evaluation-sample":
        return "sample"
    return "document"


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        COMPONENT_DOC_PATH,
        ENDPOINT_DOC_PATH,
        SHARED_CORE_DOC_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    classes = {item["artifact_class"] for item in manifest["id_patterns"]}
    if classes != REQUIRED_CLASSES:
        failures.append("ID policy must define every required artifact class.")
    uri_kinds = {item["kind"] for item in manifest["uri_policy"]["patterns"]}
    if uri_kinds != REQUIRED_KINDS:
        failures.append("URI policy must define every required URI kind.")
    if set(manifest["endpoint_tracks"]) != REQUIRED_ENDPOINT_TRACKS:
        failures.append("ID/URI policy endpoint track references are incomplete.")

    for pattern in manifest["id_patterns"]:
        forbidden = " ".join(pattern["forbidden_inputs"])
        if "alone" not in forbidden:
            failures.append(f"{pattern['artifact_class']} must forbid unstable inputs alone.")

    for example in manifest["examples"]:
        expected_id = canonical_id(example["artifact_class"], example["payload"])
        if example["expected_id"] != expected_id:
            failures.append(f"{example['name']} expected_id is not deterministic.")
        if not ID_PATTERN.fullmatch(example["expected_id"]):
            failures.append(f"{example['name']} expected_id does not match ID pattern.")
        expected_uri = canonical_uri(_kind_for_example(example["artifact_class"]), expected_id)
        if example["expected_uri"] != expected_uri:
            failures.append(f"{example['name']} expected_uri is not deterministic.")

    if manifest["document_identity"]["existing_field"] != "stable_id":
        failures.append("document identity must reuse stable_id.")
    if "row positions alone" not in manifest["document_identity"]["legacy_fallback_policy"]:
        failures.append("legacy fallback policy must forbid row-position-only future IDs.")

    required_terms = (
        "manifests/id_uri_policy.json",
        "stable_id",
        "transient file paths",
        "row positions alone",
        "https://w3id.org/nz-hansard/",
        "SPARQL",
        "manifests/id_uri_deprecations.json",
        "RDF",
        "Popolo",
    )
    for relative_path, text in {
        "docs/canonical-id-uri-policy.md": _read(DOC_PATH),
        "docs/component-contracts.md": _read(COMPONENT_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "docs/shared-nz-corpus-core-schema.md": _read(SHARED_CORE_DOC_PATH),
    }.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing ID/URI policy term: {term}")

    track = _read(TRACK_PATH)
    for required in (
        "ID Patterns",
        "URI Namespace",
        "Deprecation Policy",
        "Focused Validation",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"CANONICAL-ID-URI: {failure}")
        return 1
    print("Canonical ID/URI policy is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
