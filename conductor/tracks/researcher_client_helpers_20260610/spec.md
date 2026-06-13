# Spec: Researcher Client Helpers

## Goal

Provide practical examples for consuming document-level and endpoint artifacts in common researcher workflows.

## MoSCoW Requirements

### Must

- Add examples for Python and DuckDB local analysis.
- Keep helpers read-only and separate from canonical generation scripts.
- Document expected input files, release versions, and limitations.

### Should

- Add R examples and SPARQL examples once RDF endpoint is release-ready.
- Include citation and provenance examples.

### Could

- Publish a small helper package after APIs stabilize.

### Won't

- Introduce a new dependency burden into the core pipeline.

## Acceptance Criteria

- Examples run against declared sample or release artifacts.
- Docs make helper status and supported artifact versions explicit.
