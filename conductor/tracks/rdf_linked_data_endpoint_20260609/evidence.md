# Evidence: RDF Linked Data Endpoint

## Namespace Policy

- Planned namespace: `https://w3id.org/nz-hansard/`
- Component namespace: `https://w3id.org/nz-hansard/component/`
- Sample namespace: `https://w3id.org/nz-hansard/sample/`
- Sample status: `sample-not-release`
- Readiness boundary: `blocked-pending-validated-components`

## Sample Graph

- `samples/rdf-linked-data/linked-data.ttl`
- `samples/rdf-linked-data/linked-data.jsonld`
- `samples/rdf-linked-data/README.md`

## SHACL Validation

- `samples/rdf-linked-data/shapes.ttl`
- `python scripts/check_rdf_linked_data_endpoint.py`
- SHACL validation is tracked as maintainer-review evidence until validated component exports are available.

## SPARQL Examples

- `samples/rdf-linked-data/sparql-queries.rq`
- Queries cover dataset inspection and speech-turn inspection.
