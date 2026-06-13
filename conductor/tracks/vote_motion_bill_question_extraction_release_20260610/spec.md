# Spec: Vote Motion Bill Question Extraction Release

## Goal

Create validated neutral components for votes, motions, bills, oral/written questions, answers, and procedural decisions.

## MoSCoW Requirements

### Must

- Define schemas for each component type with source links, selectors, dates, chamber/session metadata, and provenance.
- Distinguish authoritative extraction, inferred extraction, unresolved cases, and sample-only outputs.
- Validate against fixtures and corpus-wide consistency checks.

### Should

- Link bills, motions, and questions to stable external authority identifiers where available.
- Support vote tallies, member/party votes, result labels, and abstentions when evidence permits.
- Feed Popolo/Open Civic Data, Akoma Ntoso, RDF, and CAP/ParlaCAP endpoints.

### Could

- Publish one component family at a time if validation maturity differs.

### Won't

- Infer formal votes or procedural outcomes from prose without evidence and status labels.

## Acceptance Criteria

- Schemas, outputs, validators, docs, and manifests exist for each released component family.
- Coverage and unresolved counts are visible and reproducible.
