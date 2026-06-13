# Semantic Search Embeddings And Topic Models

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
