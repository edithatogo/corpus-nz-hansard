"""Validate the researcher client helper manifest and examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_researcher_client_helpers import DEFAULT_MANIFEST  # noqa: E402
from scripts.researcher_client_helpers import (  # noqa: E402
    DOCUMENT_SAMPLE_PATH,
    RDF_SAMPLE_PATH,
    duckdb_document_summary,
    python_document_summary,
    rdf_sample_summary,
)

MANIFEST_PATH = DEFAULT_MANIFEST
SCHEMA_PATH = ROOT / "schemas/researcher_client_helpers.schema.json"
DOC_PATH = ROOT / "docs/researcher-client-helpers.md"
TRACK_PATH = ROOT / "conductor/tracks/researcher_client_helpers_20260610/index.md"
SAMPLE_PATH = DOCUMENT_SAMPLE_PATH


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, TRACK_PATH, SAMPLE_PATH, RDF_SAMPLE_PATH):
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

    if manifest["release_status"] != "local-review-only":
        failures.append("release_status must remain local-review-only.")
    if manifest["helper_status"]["python_examples"] != "implemented":
        failures.append("python examples must be implemented.")
    if manifest["helper_status"]["duckdb_examples"] != "implemented":
        failures.append("duckdb examples must be implemented.")
    if manifest["helper_status"]["r_examples"] != "deferred":
        failures.append("r examples must remain deferred.")
    if manifest["helper_status"]["sparql_examples"] != "deferred":
        failures.append("sparql examples must remain deferred.")

    python_summary = python_document_summary(SAMPLE_PATH)
    duckdb_summary = duckdb_document_summary(SAMPLE_PATH)
    rdf_summary = rdf_sample_summary(RDF_SAMPLE_PATH)

    if python_summary["row_count"] != 3:
        failures.append("Python helper should summarize the three-row sample fixture.")
    if duckdb_summary["row_count"] != 3:
        failures.append("DuckDB helper should summarize the three-row sample fixture.")
    if duckdb_summary["rows_by_document_type"] != [
        {"document_type": "answer", "rows": 1},
        {"document_type": "debate", "rows": 1},
        {"document_type": "question", "rows": 1},
    ]:
        failures.append("DuckDB helper should return the expected grouped counts.")
    if rdf_summary["dataset_titles"] != ["RDF linked-data sample package"]:
        failures.append("RDF helper should read the expected sample dataset title.")

    doc_text = _read(DOC_PATH)
    for required in (
        "Python helper",
        "DuckDB helper",
        "samples/researcher-client-helpers/hansard-mini.csv",
        "samples/rdf-linked-data/linked-data.ttl",
        "R and standalone SPARQL examples are deferred",
    ):
        if required not in doc_text:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    track_text = _read(TRACK_PATH)
    for required in ("Supported Artifacts", "Validation", "Deferred Helpers"):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"RESEARCHER-CLIENT-HELPERS: {failure}")
        return 1
    print("Researcher client helper manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
