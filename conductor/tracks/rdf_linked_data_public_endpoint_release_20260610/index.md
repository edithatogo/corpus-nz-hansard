# Track rdf_linked_data_public_endpoint_release_20260610 Context

Move RDF / Linked Data from sample readiness to a scope-declared public endpoint package.

Repo-side builder/checker are implemented with gate `release-ready-sample-public-endpoint` after validated component exports became available.
This remains sample-only evidence; stable URI review remains pending and there is no public identifier minting claim.

Current implementation surface:

- `schemas/rdf_linked_data_public_endpoint_validation.schema.json`
- `manifests/rdf_linked_data_public_endpoint_validation.json`
- `docs/rdf-linked-data-public-endpoint-release.md`
- `scripts/build_rdf_linked_data_public_endpoint.py`
- `scripts/check_rdf_linked_data_public_endpoint.py`
