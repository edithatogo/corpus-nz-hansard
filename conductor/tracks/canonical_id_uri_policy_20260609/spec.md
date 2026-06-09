# Spec: Canonical ID and URI Policy

## MoSCoW Requirements

### Must

- Define ID patterns for neutral components and endpoint artifacts.
- Define URI patterns for RDF and linked metadata outputs.
- Prevent IDs or URIs from depending on transient file paths or row positions alone.
- Define deprecation and redirect policy for changed identifiers.

### Should

- Reuse existing `stable_id` where document-level identity is sufficient.
- Include tests for deterministic ID generation.

### Could

- Add URI examples and SPARQL-friendly namespace guidance.

### Won't

- Publish RDF or civic-data endpoints before stable identifiers are declared.

## Acceptance Criteria

- ID/URI policy exists, examples validate, and endpoint tracks reference it.
