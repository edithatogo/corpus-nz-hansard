# RDF Linked Data Public Endpoint Release

## Decision

This track is release-ready as a sample-only public endpoint package under `release-ready-sample-public-endpoint`.

## Basis

- The existing RDF / Linked Data package is a sample package and remains `sample-not-release`.
- validated component exports are available for sample linked-data output.
- stable URI review remains pending.
- SHACL validation evidence remains tied to the maintainer-review sample.

## Current Boundary

- Publish `samples/rdf-linked-data/linked-data.ttl`, `linked-data.jsonld`, `shapes.ttl`, `sparql-queries.rq`, and `README.md` as sample-scoped public endpoint outputs.
- Keep the public claim sample-only and do not claim full RDF / linked-data corpus readiness.
- Make no public identifier minting claim until stable URI review is complete.

## Future Validation Requirements

- Corpus-wide RDF export must run against normalized Hansard inputs before broad endpoint release claims are made.
- stable URI review must exist before minting public linked-data identifiers.
- SHACL validation and SPARQL examples must remain aligned with the declared namespace and provenance model.

## Outputs

- `manifests/rdf_linked_data_public_endpoint_validation.json`
- `samples/rdf-linked-data/linked-data.ttl`
- `samples/rdf-linked-data/linked-data.jsonld`
- `samples/rdf-linked-data/shapes.ttl`
- `samples/rdf-linked-data/sparql-queries.rq`
- `samples/rdf-linked-data/README.md`
