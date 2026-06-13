# Spec: RDF Linked Data Public Endpoint Release

## Goal

Move RDF/JSON-LD from sample graph output to a validated linked-data endpoint release.

## MoSCoW Requirements

### Must

- Use stable URI patterns, PROV-O provenance, DCAT metadata, SKOS concept schemes, and SHACL validation.
- Preserve links to documents, source selectors, member/party/proceeding components, and generated endpoint artifacts.
- Emit Turtle/JSON-LD, SHACL shapes, SPARQL examples, manifests, and docs.

### Should

- Use W3C Time for temporal memberships, sittings, offices, and periods.
- Prepare for optional NIF linguistic annotation views.

### Could

- Publish a core graph before NLP/topic graphs.

### Won't

- Mint unstable URIs from row positions or file paths alone.

## Acceptance Criteria

- RDF parses, SHACL validation passes or deviations are documented, and SPARQL examples run against the package.
