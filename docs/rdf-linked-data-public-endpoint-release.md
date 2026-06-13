# RDF Linked Data Public Endpoint Release

## Decision

This track is implemented as a blocked public endpoint release surface and remains sample-only evidence.

## Basis

- The existing RDF / Linked Data package is a sample package and remains `sample-not-release`.
- validated component exports are not yet available for public linked-data output.
- stable URI review remains pending.
- SHACL validation evidence remains tied to the maintainer-review sample.

## Current Boundary

- Keep `samples/rdf-linked-data/linked-data.ttl`, `linked-data.jsonld`, `shapes.ttl`, `sparql-queries.rq`, and `README.md` as sample-package evidence, not public endpoint output.
- Keep `manifests/rdf_linked_data_public_endpoint_validation.json` blocked until the dependent validation evidence is available.

## Future Validation Requirements

- validated component exports must exist before the graph can be treated as release-ready.
- stable URI review must exist before minting public linked-data identifiers.
- SHACL validation and SPARQL examples must remain aligned with the declared namespace and provenance model.

## Outputs

- `manifests/rdf_linked_data_public_endpoint_validation.json`
- `samples/rdf-linked-data/linked-data.ttl`
- `samples/rdf-linked-data/linked-data.jsonld`
- `samples/rdf-linked-data/shapes.ttl`
- `samples/rdf-linked-data/sparql-queries.rq`
- `samples/rdf-linked-data/README.md`
