# Spec: Neutral Parliamentary Component Model

## MoSCoW Requirements

### Must

- Add machine-readable schemas for neutral component families.
- Define stable ID patterns for sittings, proceeding items, speech turns, members, parties, motions, votes, bills, topics, and linguistic annotations.
- Require provenance, validation status, derivation method, and derivation version on every derived component.
- Add validation manifests for component artifacts.

### Should

- Add small fixtures for each component family.
- Add cross-component referential-integrity checks.
- Use `jsonschema`, `pydantic`, or `pandera` where appropriate.

### Could

- Add LinkML schemas to generate JSON Schema and RDF shapes later.

### Won't

- Bind the neutral component model to a single external ontology.
- Publish new derived data before endpoint-specific validation exists.

## Acceptance Criteria

- Component schemas and validation manifests exist.
- Tests cover schema validity and referential-integrity examples.
- Docs explain how each endpoint consumes the neutral components.
