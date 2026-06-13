"""Validate the W3C Web Annotation selector contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/web_annotation_selector_contract.json"
SCHEMA_PATH = ROOT / "schemas/web_annotation_selector.schema.json"
DOC_PATH = ROOT / "docs/web-annotation-selector-contract.md"
MIGRATION_PATH = ROOT / "docs/web-annotation-selector-migration.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
TRACK_PATH = ROOT / "conductor/tracks/web_annotation_selector_contract_20260610/index.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        MIGRATION_PATH,
        ENDPOINT_DOC_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)

    if manifest.get("contract_id") != "web_annotation_selector_contract_20260610":
        failures.append("contract_id must match the track identifier.")
    if manifest.get("selector_schema") != "schemas/web_annotation_selector.schema.json":
        failures.append("selector_schema must reference the shared schema.")
    if manifest.get("validation_results", {}).get("blocking_errors") != 0:
        failures.append("blocking_errors must remain zero.")

    supported = set(manifest.get("supported_selector_types", []))
    expected_supported = {
        "TextQuoteSelector",
        "TextPositionSelector",
        "FragmentSelector",
        "LinePositionSelector",
        "PagePositionSelector",
    }
    if supported != expected_supported:
        failures.append("supported_selector_types must match the shared selector contract.")

    purposes = set(manifest.get("supported_annotation_purposes", []))
    expected_purposes = {"speech_turn", "topic_unit", "ud_token", "rdf_annotation", "search_chunk"}
    if purposes != expected_purposes:
        failures.append("supported_annotation_purposes must match the shared selector contract.")

    examples = manifest.get("examples", [])
    if len(examples) != 3:
        failures.append("contract examples must cover speech, UD, and RDF selectors.")
    for example in examples:
        for error in sorted(validator.iter_errors(example), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(
                f"example {example.get('selector_type', '<unknown>')} {location}: {error.message}"
            )

    docs_text = _read(DOC_PATH)
    for required in (
        "TextQuoteSelector",
        "TextPositionSelector",
        "FragmentSelector",
        "LinePositionSelector",
        "PagePositionSelector",
        "source_document_id",
        "source_hash",
    ):
        if required not in docs_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    migration_text = _read(MIGRATION_PATH)
    for required in (
        "sourceStableId",
        "StartChar",
        "TextQuoteSelector",
        "TextPositionSelector",
        "FragmentSelector",
        "LinePositionSelector",
        "PagePositionSelector",
    ):
        if required not in migration_text:
            failures.append(f"{MIGRATION_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    endpoint_text = _read(ENDPOINT_DOC_PATH)
    if "web_annotation_selector_contract.json" not in endpoint_text:
        failures.append("docs/endpoint-contracts.md must reference the shared selector contract.")

    track_text = _read(TRACK_PATH)
    for required in (
        "Shared Selector Schema",
        "Normalization Policy",
        "Migration Notes",
        "Endpoint References",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"WEB-ANNOTATION-SELECTOR: {failure}")
        return 1
    print("Web Annotation selector contract is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
