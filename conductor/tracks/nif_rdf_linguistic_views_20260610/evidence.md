# Evidence: NIF/RDF Linguistic Annotation Views

Status: blocked.

Tracked artifacts:

- `spec.md`
- `plan.md`
- `metadata.json`
- `index.md`

Dependency boundary:

- RDF linked-data is still sample-not-release and remains blocked pending
  validated component exports.
- UD/CoNLL-U remains a sample endpoint, so the linguistic views do not yet have
  a validated token layer to anchor against.
- W3C Web Annotation selector contracts exist, but the NIF-specific export path
  is not implemented yet.

Planned scope:

- token-level and sentence-level NIF views
- stable document selectors and source hashes
- RDF parsing and vocabulary checks
- selector consistency checks
- SPARQL examples for linguistic annotations

Reference surfaces:

- `docs/interoperability-requirements-moscow.md`
- `docs/interoperability-design.md`
- `docs/endpoint-contracts.md`
- `docs/rdf-linked-data-mapping.md`
- `conductor/tracks/ud_conllu_public_endpoint_release_20260610/`
- `conductor/tracks/rdf_linked_data_public_endpoint_release_20260610/`
