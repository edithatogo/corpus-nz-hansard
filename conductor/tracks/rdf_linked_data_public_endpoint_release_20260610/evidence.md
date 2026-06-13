# Evidence: RDF Linked Data Public Endpoint Release

Status: blocked.

Implemented artifacts:

- `schemas/rdf_linked_data_public_endpoint_validation.schema.json`
- `manifests/rdf_linked_data_public_endpoint_validation.json`
- `docs/rdf-linked-data-public-endpoint-release.md`
- `scripts/build_rdf_linked_data_public_endpoint.py`
- `scripts/check_rdf_linked_data_public_endpoint.py`
- `tests/test_rdf_linked_data_public_endpoint.py`

Validation evidence:

- `python scripts/build_rdf_linked_data_public_endpoint.py`
- `python scripts/check_rdf_linked_data_public_endpoint.py`
- `python -m unittest tests.test_rdf_linked_data_public_endpoint`

Release boundary:

- The current RDF linked-data package remains a maintainer-review sample, not a public endpoint release.
- Validated component exports are not yet available for public linked-data output.
- SHACL evidence and stable URI review remain pending for release publication.
