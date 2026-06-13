# Spec: Entity Linking Exploratory Outputs

## Goal

Add non-authoritative entity-linking outputs for people, organisations, places, legislation, ministries, portfolios, and committees.

## MoSCoW Requirements

### Must

- Mark outputs as exploratory and machine-assisted unless human validation exists.
- Preserve mentions, selectors, candidate IDs, scores, model/rule provenance, and unresolved statuses.
- Avoid altering canonical corpus or validated identity components.

### Should

- Prefer authority-backed IDs for legislation, people, organisations, committees, and portfolios.
- Provide evaluation samples and false-positive analysis.

### Could

- Feed search/RAG enrichment and RDF exploratory graphs.

### Won't

- Present entity links as authoritative legal or parliamentary metadata.

## Acceptance Criteria

- Outputs, schemas, manifests, docs, and validation checks exist with explicit exploratory status.
