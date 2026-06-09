"""Validate shared NZ corpus core schema documentation and contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/shared_nz_corpus_core.schema.json"
DOC_PATH = ROOT / "docs/shared-nz-corpus-core-schema.md"
EVIDENCE_PATH = ROOT / "conductor/tracks/shared_nz_corpus_core_schema_20260609/evidence.md"

REQUIRED_FIELDS = (
    "corpus_id",
    "record_id",
    "source_id",
    "jurisdiction",
    "country",
    "document_type",
    "record_schema_version",
    "canonical_uri",
    "source_url",
    "source_version",
    "effective_date",
    "published_date",
    "last_modified_date",
    "content_sha256",
    "manifest_sha256",
    "provenance",
)

REQUIRED_PROVENANCE_FIELDS = (
    "pipeline_name",
    "pipeline_version",
    "source_name",
    "source_record_id",
    "source_retrieved_at",
    "release_version",
    "release_commit",
    "license_note",
)

REQUIRED_DOC_SNIPPETS = (
    "corpus-nz-hansard",
    "corpus-nz-legislation",
    "GitHub",
    "Hugging Face",
    "Zenodo",
    "OSF",
    "future metadata",
    "existing published URLs and DOI records",
    "generated endpoint",
)

REQUIRED_EVIDENCE_SNIPPETS = (
    "docs/shared-nz-corpus-core-schema.md",
    "schemas/shared_nz_corpus_core.schema.json",
    "scripts/check_shared_core_schema.py",
    "tests/test_shared_core_schema.py",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_schema() -> dict[str, Any]:
    return json.loads(_read_text(SCHEMA_PATH))


def _failures() -> list[str]:
    failures: list[str] = []

    try:
        schema = _load_schema()
    except (json.JSONDecodeError, OSError) as exc:
        return [f"Shared core schema cannot be loaded: {exc}"]

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema raises several schema validation subclasses.
        failures.append(f"Shared core schema is not a valid Draft 2020-12 schema: {exc}")

    required = set(schema.get("required", []))
    for field in REQUIRED_FIELDS:
        if field not in required:
            failures.append(f"Shared core schema does not require {field}.")

    properties = schema.get("properties", {})
    corpus_enum = properties.get("corpus_id", {}).get("enum", [])
    for corpus_id in ("corpus-nz-hansard", "corpus-nz-legislation"):
        if corpus_id not in corpus_enum:
            failures.append(f"Shared core schema corpus_id does not allow {corpus_id}.")

    provenance_required = set(properties.get("provenance", {}).get("required", []))
    for field in REQUIRED_PROVENANCE_FIELDS:
        if field not in provenance_required:
            failures.append(f"Shared core schema provenance does not require {field}.")

    docs = _read_text(DOC_PATH) if DOC_PATH.exists() else ""
    if not docs:
        failures.append("Shared core schema documentation is missing.")
    for snippet in REQUIRED_DOC_SNIPPETS:
        if snippet not in docs:
            failures.append(f"Shared core schema documentation is missing: {snippet}")

    evidence = _read_text(EVIDENCE_PATH) if EVIDENCE_PATH.exists() else ""
    if not evidence:
        failures.append("Shared core schema evidence is missing.")
    for snippet in REQUIRED_EVIDENCE_SNIPPETS:
        if snippet not in evidence:
            failures.append(f"Shared core schema evidence is missing: {snippet}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"SHARED-CORE-SCHEMA: {failure}")
        return 1
    print("Shared NZ corpus core schema contract is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
