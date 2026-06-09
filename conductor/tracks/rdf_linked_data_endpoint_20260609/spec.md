# Spec: RDF Linked Data Endpoint

## MoSCoW Requirements

### Must

- Define stable URI patterns.
- Generate RDF Turtle or JSON-LD from neutral components.
- Include PROV-O provenance and DCAT dataset metadata.
- Validate RDF parsing and SHACL shapes.

### Should

- Use SKOS concept schemes for parties, roles, proceeding types, vote types, and topic codes.
- Reuse Popolo/Open Civic Data identifiers where appropriate.

### Could

- Add SPARQL example queries and a small sample graph.

### Won't

- Mint unstable URIs from transient file paths or row positions alone.

## Acceptance Criteria

- RDF output, SHACL shapes, URI policy, and validation manifest exist.

## Dependencies

- Depends on canonical ID/URI policy, authority-source discovery, neutral component model, release ladder, PROV-O/DCAT/SKOS mappings, W3C Time where temporal data is present, and optional NIF when linguistic annotations are exported.
