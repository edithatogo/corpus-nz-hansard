# Semantic Search Embeddings And Topic Models

Track ID: `semantic_search_embeddings_topics_20260610`

Status: complete.

## Goal

Add exploratory embeddings and topic-model outputs with model cards, manifests, optional dependencies, and non-authoritative publication boundaries.

## Primary Artifacts

- `spec.md`
- `plan.md`
- `evidence.md`

## Outputs

- `samples/semantic-search-embeddings/semantic_search_embeddings_topics.jsonl`
- `samples/semantic-search-embeddings/semantic_search_embeddings_topics_review.csv`

## Model Card

The embeddings use a TF-IDF + TruncatedSVD projection and the topic model uses
LatentDirichletAllocation, both from the optional ML group.

## Reproducibility

The manifest records model versions, parameters, hashes, and input scope.

## Quality Notes

The outputs are exploratory only and are not official policy labels.
