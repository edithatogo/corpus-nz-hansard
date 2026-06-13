"""Seed data and helpers for exploratory semantic-search embeddings and topic models."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "samples/semantic-search-embeddings"
JSONL_PATH = SAMPLE_DIR / "semantic_search_embeddings_topics.jsonl"
REVIEW_PATH = SAMPLE_DIR / "semantic_search_embeddings_topics_review.csv"
README_PATH = SAMPLE_DIR / "README.md"
DOC_PATH = ROOT / "docs/semantic-search-embeddings-topics.md"
MANIFEST_PATH = ROOT / "manifests/semantic_search_embeddings_topics.json"
SCHEMA_PATH = ROOT / "schemas/semantic_search_embeddings_topics.schema.json"
RECORD_SCHEMA_PATH = ROOT / "schemas/semantic_search_embeddings_record.schema.json"

MEMBER_IDENTITY_INPUT = ROOT / "samples/member-identity/member_identity_review.csv"
PARTY_ATTRIBUTION_INPUT = ROOT / "samples/party-attribution/party_attribution_review.csv"


@dataclass(frozen=True)
class SourceRow:
    source_input_id: str
    source_file: str
    source_row_number: int
    sample_id: str
    source_document_type: str
    parliament_number: int
    source_stable_id: str
    source_excerpt: str
    selector_text: str
    label_hint: str


def _stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _sha256(payload: Any) -> str:
    return hashlib.sha256(_stable_json(payload).encode("utf-8")).hexdigest()


def _read_csv_rows(
    path: Path, source_input_id: str, selector_field: str, label_hint: str
) -> list[SourceRow]:
    rows: list[SourceRow] = []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=1):
            selector_text = (
                row.get(selector_field) or row.get("source_excerpt") or row["sample_id"]
            ).strip()
            rows.append(
                SourceRow(
                    source_input_id=source_input_id,
                    source_file=path.relative_to(ROOT).as_posix(),
                    source_row_number=index,
                    sample_id=row["sample_id"],
                    source_document_type=row["source_document_type"],
                    parliament_number=int(row["parliament_number"]),
                    source_stable_id=row["source_stable_id"],
                    source_excerpt=row["source_excerpt"],
                    selector_text=selector_text,
                    label_hint=label_hint,
                )
            )
    return rows


def source_rows() -> list[SourceRow]:
    rows: list[SourceRow] = []
    rows.extend(
        _read_csv_rows(
            MEMBER_IDENTITY_INPUT,
            "member-identity",
            "member_of_parliament_raw",
            "member-identity-review",
        )
    )
    rows.extend(
        _read_csv_rows(
            PARTY_ATTRIBUTION_INPUT,
            "party-attribution",
            "party_value",
            "party-attribution-review",
        )
    )
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _manifest_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "manifest_version",
            "track_id",
            "repository",
            "generated_at",
            "release_status",
            "sample_package",
            "dependency_groups",
            "install_commands",
            "tool_versions",
            "library_versions",
            "model_versions",
            "release_affecting_dependencies",
            "validation_command",
            "outputs",
            "source_inputs",
            "input_scope",
            "validation_counts",
            "validation_results",
        ],
        "properties": {
            "manifest_version": {"const": 1},
            "track_id": {"const": "semantic_search_embeddings_topics_20260610"},
            "repository": {"const": "corpus-nz-hansard"},
            "generated_at": {"type": "string"},
            "release_status": {"const": "sample-not-release"},
            "sample_package": {"const": "samples/semantic-search-embeddings"},
            "dependency_groups": {
                "type": "array",
                "items": {"enum": ["ml"]},
                "minItems": 1,
            },
            "install_commands": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "tool_versions": {
                "type": "object",
                "additionalProperties": {"type": "string"},
            },
            "library_versions": {
                "type": "object",
                "additionalProperties": {"type": "string"},
            },
            "model_versions": {
                "type": "array",
                "minItems": 2,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "model_id",
                        "model_name",
                        "model_version",
                        "model_family",
                        "library",
                        "library_version",
                        "parameters",
                        "input_scope",
                        "model_hash",
                        "generated_at",
                    ],
                    "properties": {
                        "model_id": {"type": "string"},
                        "model_name": {"type": "string"},
                        "model_version": {"type": "string"},
                        "model_family": {"enum": ["embedding", "topic-model"]},
                        "library": {"type": "string"},
                        "library_version": {"type": "string"},
                        "parameters": {"type": "object"},
                        "input_scope": {"type": "array", "items": {"type": "string"}},
                        "model_hash": {"type": "string"},
                        "generated_at": {"type": "string"},
                    },
                },
            },
            "release_affecting_dependencies": {"type": "string"},
            "validation_command": {"type": "string"},
            "outputs": {
                "type": "object",
                "required": ["jsonl", "review_csv", "readme", "docs"],
                "additionalProperties": False,
                "properties": {
                    "jsonl": {"type": "string"},
                    "review_csv": {"type": "string"},
                    "readme": {"type": "string"},
                    "docs": {"type": "string"},
                },
            },
            "source_inputs": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2,
            },
            "input_scope": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "source_row_count",
                    "source_document_count",
                    "embedding_dimension",
                    "topic_count",
                    "input_hash",
                ],
                "properties": {
                    "source_row_count": {"type": "integer", "minimum": 1},
                    "source_document_count": {"type": "integer", "minimum": 1},
                    "embedding_dimension": {"type": "integer", "minimum": 1},
                    "topic_count": {"type": "integer", "minimum": 1},
                    "input_hash": {"type": "string"},
                },
            },
            "validation_counts": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "record_count",
                    "review_row_count",
                    "embedding_dimension",
                    "topic_count",
                ],
                "properties": {
                    "record_count": {"type": "integer", "minimum": 1},
                    "review_row_count": {"type": "integer", "minimum": 1},
                    "embedding_dimension": {"type": "integer", "minimum": 1},
                    "topic_count": {"type": "integer", "minimum": 1},
                },
            },
            "validation_results": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "outputs_written",
                    "review_sample_written",
                    "non_authoritative",
                    "reproducibility_guidance_recorded",
                    "human_validation_required",
                ],
                "properties": {
                    "outputs_written": {"const": True},
                    "review_sample_written": {"const": True},
                    "non_authoritative": {"const": True},
                    "reproducibility_guidance_recorded": {"const": True},
                    "human_validation_required": {"const": True},
                },
            },
        },
    }


def _record_schema(embedding_dimension: int) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "record_id",
            "sample_id",
            "source_input_id",
            "source_file",
            "source_row_number",
            "source_document_type",
            "parliament_number",
            "source_stable_id",
            "source_document_link",
            "selector",
            "document_text",
            "embedding_model_id",
            "embedding_dimension",
            "embedding_vector",
            "embedding_hash",
            "topic_model_id",
            "topic_id",
            "topic_label",
            "topic_probability",
            "topic_terms",
            "validation_status",
            "review_status",
            "release_status",
            "notes",
        ],
        "properties": {
            "record_id": {"type": "string"},
            "sample_id": {"type": "string"},
            "source_input_id": {"type": "string"},
            "source_file": {"type": "string"},
            "source_row_number": {"type": "integer", "minimum": 1},
            "source_document_type": {"type": "string"},
            "parliament_number": {"type": "integer", "minimum": 1},
            "source_stable_id": {"type": "string"},
            "source_document_link": {"type": "string"},
            "selector": {
                "type": "object",
                "additionalProperties": False,
                "required": ["selector_type", "exact", "source_stable_id"],
                "properties": {
                    "selector_type": {"const": "exact"},
                    "exact": {"type": "string"},
                    "source_stable_id": {"type": "string"},
                },
            },
            "document_text": {"type": "string"},
            "embedding_model_id": {"type": "string"},
            "embedding_dimension": {"const": embedding_dimension},
            "embedding_vector": {
                "type": "array",
                "minItems": embedding_dimension,
                "maxItems": embedding_dimension,
                "items": {"type": "number"},
            },
            "embedding_hash": {"type": "string"},
            "topic_model_id": {"type": "string"},
            "topic_id": {"type": "integer", "minimum": 0},
            "topic_label": {"type": "string"},
            "topic_probability": {"type": "number", "minimum": 0, "maximum": 1},
            "topic_terms": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "validation_status": {"const": "exploratory-only"},
            "review_status": {"const": "reviewed"},
            "release_status": {"const": "sample-not-release"},
            "notes": {"type": "string"},
        },
    }


def _supporting_docs() -> tuple[str, str]:
    readme = """# Semantic Search Embeddings And Topic Models

Exploratory sample package for semantic-search embeddings and topic models.
This package is sample-not-release and explicitly non-authoritative.

Files:

- `semantic_search_embeddings_topics.jsonl`
- `semantic_search_embeddings_topics_review.csv`
- `README.md`

Validation and traceability:

- Manifest: `manifests/semantic_search_embeddings_topics.json`
- Schema: `schemas/semantic_search_embeddings_topics.schema.json`
- Record schema: `schemas/semantic_search_embeddings_record.schema.json`
- Docs: `docs/semantic-search-embeddings-topics.md`

Exploratory boundary:

- Embedding vectors are generated from reviewed sample rows only.
- Topic assignments are provisional and do not define policy or official labels.
- human validation is required before any downstream release claim.
"""
    docs = """# Semantic Search Embeddings And Topic Models

## Scope

This track publishes non-authoritative, machine-assisted embeddings and topic-model
outputs built from reviewed member-identity and party-attribution sample rows.
The outputs are exploratory only and must not be treated as official policy labels
or canonical publication metadata.

This package is sample-not-release and human validation remains required.

## Optional Dependencies

- `requirements/ml.txt`

The builder uses scikit-learn from the optional ML group. Core repository validation
does not depend on this stack.

## Outputs

- `samples/semantic-search-embeddings/semantic_search_embeddings_topics.jsonl`
- `samples/semantic-search-embeddings/semantic_search_embeddings_topics_review.csv`

## Model Card

Embedding model:

- `TF-IDF + TruncatedSVD`
- Purpose: dense exploratory vector projection for search/RAG similarity experiments
- Library: scikit-learn
- Inputs: reviewed sample excerpts only
- Limitations: lexical features, small sample scope, no external embedding service

Topic model:

- `LatentDirichletAllocation`
- Purpose: exploratory topic assignment for the same reviewed sample scope
- Library: scikit-learn
- Inputs: reviewed sample excerpts only
- Limitations: unsupervised, unstable at small sample sizes, not an official label set

## Reproducibility

- The manifest records model versions, parameters, hashes, and input scope.
- The sample corpus is fixed to reviewed rows from the member-identity and
  party-attribution review packages.
- All outputs are deterministic for the current model parameters and input scope.

## Quality Notes

- Topic labels are shorthand, not policy statements.
- The sample is intentionally small and is intended for exploratory evaluation,
  documentation examples, and search or RAG enrichment prototypes.
- No public vector index is published here.

## Validation

- `python scripts/build_semantic_search_embeddings_topics.py`
- `python scripts/check_semantic_search_embeddings_topics.py`
- `python -m unittest tests.test_semantic_search_embeddings_topics`
"""
    return readme, docs


def _build_vectors(
    texts: list[str],
) -> tuple[
    list[list[float]],
    int,
    dict[str, Any],
    dict[str, Any],
    list[list[float]],
    list[int],
    list[list[str]],
]:
    import sklearn  # noqa: I001

    from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD  # noqa: I001
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer  # noqa: I001

    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", min_df=1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    embedding_dimension = min(4, max(2, min(tfidf_matrix.shape[0] - 1, tfidf_matrix.shape[1] - 1)))
    svd = TruncatedSVD(n_components=embedding_dimension, random_state=42)
    embeddings = svd.fit_transform(tfidf_matrix)

    count_vectorizer = CountVectorizer(stop_words="english", min_df=1)
    counts = count_vectorizer.fit_transform(texts)
    topic_count = 3 if len(texts) >= 6 else 2
    topic_count = min(topic_count, max(2, min(counts.shape[0] - 1, counts.shape[1] - 1)))
    lda = LatentDirichletAllocation(
        n_components=topic_count,
        random_state=42,
        learning_method="batch",
        max_iter=25,
    )
    topic_distributions = lda.fit_transform(counts)

    feature_names = count_vectorizer.get_feature_names_out()
    topic_terms: list[list[str]] = []
    for topic_index in range(topic_count):
        top_indices = lda.components_[topic_index].argsort()[::-1][:5]
        topic_terms.append([feature_names[index] for index in top_indices])

    embedding_params = {
        "model_id": "tfidf-truncated-svd",
        "model_name": "TF-IDF + TruncatedSVD",
        "model_version": "1.0.0",
        "model_family": "embedding",
        "library": "scikit-learn",
        "library_version": sklearn.__version__,
        "parameters": {
            "tfidf": {
                "ngram_range": [1, 2],
                "stop_words": "english",
                "min_df": 1,
            },
            "svd": {
                "n_components": embedding_dimension,
                "random_state": 42,
            },
        },
    }
    topic_params = {
        "model_id": "lda-topic-model",
        "model_name": "LatentDirichletAllocation",
        "model_version": "1.0.0",
        "model_family": "topic-model",
        "library": "scikit-learn",
        "library_version": sklearn.__version__,
        "parameters": {
            "count_vectorizer": {
                "stop_words": "english",
                "min_df": 1,
            },
            "lda": {
                "n_components": topic_count,
                "learning_method": "batch",
                "max_iter": 25,
                "random_state": 42,
            },
        },
    }
    return (
        [[round(float(value), 6) for value in vector] for vector in embeddings],
        embedding_dimension,
        embedding_params,
        topic_params,
        [[round(float(value), 6) for value in row] for row in topic_distributions],
        [int(index) for index in topic_distributions.argmax(axis=1)],
        topic_terms,
    )


def build_semantic_search_embeddings_topics(
    *, generated_at: str, write: bool = True
) -> dict[str, Any]:
    rows = source_rows()
    texts = [row.source_excerpt for row in rows]
    (
        embeddings,
        embedding_dimension,
        embedding_params,
        topic_params,
        topic_distribution_matrix,
        topic_ids,
        topic_terms,
    ) = _build_vectors(texts)
    record_hash_input = [
        {
            "sample_id": row.sample_id,
            "source_input_id": row.source_input_id,
            "source_row_number": row.source_row_number,
            "source_excerpt": row.source_excerpt,
            "selector_text": row.selector_text,
        }
        for row in rows
    ]
    input_hash = f"sha256:{_sha256(record_hash_input)}"
    embedding_model_hash = f"sha256:{_sha256({**embedding_params, 'input_hash': input_hash})}"
    topic_model_hash = f"sha256:{_sha256({**topic_params, 'input_hash': input_hash})}"

    record_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []

    for row_index, row in enumerate(rows):
        embedding_vector = embeddings[row_index]
        topic_id = topic_ids[row_index]
        topic_probability = round(float(topic_distribution_matrix[row_index][topic_id]), 6)
        record = {
            "record_id": f"semantic-search-embedding-{row_index + 1:02d}",
            "sample_id": row.sample_id,
            "source_input_id": row.source_input_id,
            "source_file": row.source_file,
            "source_row_number": row.source_row_number,
            "source_document_type": row.source_document_type,
            "parliament_number": row.parliament_number,
            "source_stable_id": row.source_stable_id,
            "source_document_link": f"{row.source_file}#row-{row.source_row_number}",
            "selector": {
                "selector_type": "exact",
                "exact": row.selector_text,
                "source_stable_id": row.source_stable_id,
            },
            "document_text": row.source_excerpt,
            "embedding_model_id": embedding_params["model_id"],
            "embedding_dimension": embedding_dimension,
            "embedding_vector": embedding_vector,
            "embedding_hash": f"sha256:{_sha256({'record_id': row.sample_id, 'vector': embedding_vector})}",
            "topic_model_id": topic_params["model_id"],
            "topic_id": topic_id,
            "topic_label": f"exploratory topic {topic_id}",
            "topic_probability": topic_probability,
            "topic_terms": topic_terms[topic_id],
            "validation_status": "exploratory-only",
            "review_status": "reviewed",
            "release_status": "sample-not-release",
            "notes": (
                f"{row.label_hint} row retained for exploratory semantic search and topic analysis only."
            ),
        }
        record_rows.append(record)
        review_rows.append(
            {
                "record_id": record["record_id"],
                "sample_id": row.sample_id,
                "source_input_id": row.source_input_id,
                "source_row_number": row.source_row_number,
                "source_stable_id": row.source_stable_id,
                "selector_text": row.selector_text,
                "topic_id": topic_id,
                "topic_label": record["topic_label"],
                "topic_probability": topic_probability,
                "topic_terms": " | ".join(topic_terms[topic_id]),
                "embedding_dimension": embedding_dimension,
                "embedding_model_id": embedding_params["model_id"],
                "topic_model_id": topic_params["model_id"],
                "release_status": record["release_status"],
                "notes": record["notes"],
            }
        )

    model_versions = [
        {
            **embedding_params,
            "input_scope": [
                MEMBER_IDENTITY_INPUT.relative_to(ROOT).as_posix(),
                PARTY_ATTRIBUTION_INPUT.relative_to(ROOT).as_posix(),
            ],
            "model_hash": embedding_model_hash,
            "generated_at": generated_at,
        },
        {
            **topic_params,
            "input_scope": [
                MEMBER_IDENTITY_INPUT.relative_to(ROOT).as_posix(),
                PARTY_ATTRIBUTION_INPUT.relative_to(ROOT).as_posix(),
            ],
            "model_hash": topic_model_hash,
            "generated_at": generated_at,
        },
    ]

    manifest = {
        "manifest_version": 1,
        "track_id": "semantic_search_embeddings_topics_20260610",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "release_status": "sample-not-release",
        "sample_package": "samples/semantic-search-embeddings",
        "dependency_groups": ["ml"],
        "install_commands": ["python -m pip install -r requirements/ml.txt"],
        "tool_versions": {"python": sys.version.split()[0]},
        "library_versions": {
            "scikit-learn": embedding_params["library_version"],
            "jsonschema": package_version("jsonschema"),
        },
        "model_versions": model_versions,
        "release_affecting_dependencies": (
            "Pin ML libraries and model revisions before any future public vector or topic artifact."
        ),
        "validation_command": "python scripts/check_semantic_search_embeddings_topics.py",
        "outputs": {
            "jsonl": JSONL_PATH.relative_to(ROOT).as_posix(),
            "review_csv": REVIEW_PATH.relative_to(ROOT).as_posix(),
            "readme": README_PATH.relative_to(ROOT).as_posix(),
            "docs": DOC_PATH.relative_to(ROOT).as_posix(),
        },
        "source_inputs": [
            MEMBER_IDENTITY_INPUT.relative_to(ROOT).as_posix(),
            PARTY_ATTRIBUTION_INPUT.relative_to(ROOT).as_posix(),
        ],
        "input_scope": {
            "source_row_count": len(rows),
            "source_document_count": len({row.source_stable_id for row in rows}),
            "embedding_dimension": embedding_dimension,
            "topic_count": len(topic_terms),
            "input_hash": input_hash,
        },
        "validation_counts": {
            "record_count": len(record_rows),
            "review_row_count": len(review_rows),
            "embedding_dimension": embedding_dimension,
            "topic_count": len(topic_terms),
        },
        "validation_results": {
            "outputs_written": True,
            "review_sample_written": True,
            "non_authoritative": True,
            "reproducibility_guidance_recorded": True,
            "human_validation_required": True,
        },
    }

    if write:
        _write_jsonl(JSONL_PATH, record_rows)
        _write_csv(
            REVIEW_PATH,
            review_rows,
            [
                "record_id",
                "sample_id",
                "source_input_id",
                "source_row_number",
                "source_stable_id",
                "selector_text",
                "topic_id",
                "topic_label",
                "topic_probability",
                "topic_terms",
                "embedding_dimension",
                "embedding_model_id",
                "topic_model_id",
                "release_status",
                "notes",
            ],
        )
        README_PATH.parent.mkdir(parents=True, exist_ok=True)
        readme_text, docs_text = _supporting_docs()
        README_PATH.write_text(readme_text, encoding="utf-8")
        DOC_PATH.write_text(docs_text, encoding="utf-8")

    return manifest
