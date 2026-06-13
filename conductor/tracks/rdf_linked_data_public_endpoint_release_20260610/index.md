# Track rdf_linked_data_public_endpoint_release_20260610 Context

Move RDF / Linked Data from sample graph output to a scope-declared public endpoint release.

Repo-side builder/checker are implemented, but the release is blocked until validated component exports, stable URI review, and SHACL evidence exist. This remains sample-only evidence rather than a public endpoint release.

Current implementation surface:

- `schemas/rdf_linked_data_public_endpoint_validation.schema.json`
- `manifests/rdf_linked_data_public_endpoint_validation.json`
- `docs/rdf-linked-data-public-endpoint-release.md`
- `scripts/build_rdf_linked_data_public_endpoint.py`
- `scripts/check_rdf_linked_data_public_endpoint.py`
