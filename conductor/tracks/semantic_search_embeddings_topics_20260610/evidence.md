# Evidence: Semantic Search Embeddings And Topic Models

Status: complete.

## Phase 1

Status: complete.

Created:

- `tests/test_semantic_search_embeddings_topics.py`
- `docs/semantic-search-embeddings-topics.md`

## Phase 2

Status: complete.

Created:

- `scripts/semantic_search_embeddings_topics.py`
- `scripts/build_semantic_search_embeddings_topics.py`
- `scripts/check_semantic_search_embeddings_topics.py`
- `manifests/semantic_search_embeddings_topics.json`
- `schemas/semantic_search_embeddings_topics.schema.json`
- `schemas/semantic_search_embeddings_record.schema.json`
- `samples/semantic-search-embeddings/semantic_search_embeddings_topics.jsonl`
- `samples/semantic-search-embeddings/semantic_search_embeddings_topics_review.csv`
- `samples/semantic-search-embeddings/README.md`

### Validation

Validation commands:

- `python scripts/build_semantic_search_embeddings_topics.py`
- `python scripts/check_semantic_search_embeddings_topics.py`
- `python -m unittest tests.test_semantic_search_embeddings_topics`

## Boundary

- Outputs are sample-not-release and non-authoritative.
- Embedding and topic outputs are exploratory only and are not official policy labels.
- Core pipeline validation does not depend on the optional ML stack.
