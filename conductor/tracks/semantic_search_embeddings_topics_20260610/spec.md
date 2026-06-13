# Spec: Semantic Search Embeddings And Topic Models

## Goal

Add exploratory embeddings and topic-model outputs with model cards, manifests, optional dependencies, and non-authoritative publication boundaries.

## MoSCoW Requirements

### Must

- Keep embeddings/topic models optional and separate from canonical releases.
- Record model names, versions, parameters, hashes, input scopes, and generation dates.
- Preserve selectors and source document links for each chunk/topic assignment.

### Should

- Include reproducibility guidance and quality/evaluation notes.
- Feed search/RAG and documentation examples.

### Could

- Publish vector index examples when licensing and hosting permit.

### Won't

- Treat unsupervised topics as official policy/topic labels.

## Acceptance Criteria

- Outputs and manifests are reproducible and clearly labelled exploratory.
- Optional dependencies do not affect core pipeline validation.
