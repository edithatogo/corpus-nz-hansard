"""Validate exploratory semantic-search embeddings and topic-model outputs."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.semantic_search_embeddings_topics import (  # noqa: E402
    DOC_PATH,
    JSONL_PATH,
    MANIFEST_PATH,
    README_PATH,
    RECORD_SCHEMA_PATH,
    REVIEW_PATH,
    SCHEMA_PATH,
)

TRACK_PATH = ROOT / "conductor/tracks/semantic_search_embeddings_topics_20260610/index.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _jsonl_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        RECORD_SCHEMA_PATH,
        JSONL_PATH,
        REVIEW_PATH,
        DOC_PATH,
        README_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    record_schema = _json(RECORD_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    rows = _jsonl_rows(JSONL_PATH)
    row_validator = Draft202012Validator(record_schema)
    for index, row in enumerate(rows):
        for error in sorted(row_validator.iter_errors(row), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(
                f"{JSONL_PATH.relative_to(ROOT).as_posix()}[{index}] {location}: {error.message}"
            )

    review_rows = _csv_rows(REVIEW_PATH)
    if len(rows) != manifest["validation_counts"]["record_count"]:
        failures.append("JSONL row count must match manifest record_count.")
    if len(review_rows) != manifest["validation_counts"]["review_row_count"]:
        failures.append("Review CSV row count must match manifest review_row_count.")

    if manifest["release_status"] != "sample-not-release":
        failures.append("Manifest release_status must remain sample-not-release.")
    if manifest["validation_results"]["non_authoritative"] is not True:
        failures.append("Manifest must stay non-authoritative.")
    if manifest["validation_results"]["human_validation_required"] is not True:
        failures.append("Manifest must require human validation.")

    if manifest["validation_counts"]["embedding_dimension"] <= 0:
        failures.append("Embedding dimension must be positive.")
    if manifest["validation_counts"]["topic_count"] < 2:
        failures.append("Expected at least two exploratory topics.")

    required_source_inputs = {
        "samples/member-identity/member_identity_review.csv",
        "samples/party-attribution/party_attribution_review.csv",
    }
    if set(manifest["source_inputs"]) != required_source_inputs:
        failures.append(
            "Manifest source inputs must cover the reviewed member and party sample packages."
        )

    required_text = (
        "sample-not-release",
        "non-authoritative",
        "TF-IDF + TruncatedSVD",
        "LatentDirichletAllocation",
        "requirements/ml.txt",
        "search or RAG enrichment",
    )
    doc = _read(DOC_PATH)
    for required in required_text:
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    readme = _read(README_PATH)
    for required in (
        "sample-not-release",
        "semantic_search_embeddings_topics.jsonl",
        "semantic_search_embeddings_topics_review.csv",
        "human validation",
    ):
        if required not in readme:
            failures.append(f"{README_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    track = _read(TRACK_PATH)
    for required in ("Outputs", "Model Card", "Reproducibility", "Quality Notes"):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    embedding_dimensions = {len(row["embedding_vector"]) for row in rows}
    if embedding_dimensions != {manifest["validation_counts"]["embedding_dimension"]}:
        failures.append("Embedding vectors must all match the manifest embedding dimension.")

    if len({row["topic_id"] for row in rows}) < 2:
        failures.append("Expected at least two exploratory topics to be populated.")

    if not all(0.0 <= row["topic_probability"] <= 1.0 for row in rows):
        failures.append("Topic probabilities must be between 0 and 1.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"SEMANTIC-SEARCH-EMBEDDINGS-TOPICS: {failure}")
        return 1
    print("Semantic search embeddings and topic-model outputs are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
