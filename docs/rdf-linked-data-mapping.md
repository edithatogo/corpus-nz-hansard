# RDF Linked Data Mapping Notes

This package is a maintainer-review sample, not a release artifact.

References used by this sample package:

- `manifests/rdf_linked_data_validation_manifest.json`
- `manifests/rdf_linked_data_model_metadata.json`
- `samples/rdf-linked-data/linked-data.ttl`
- `samples/rdf-linked-data/linked-data.jsonld`
- `samples/rdf-linked-data/shapes.ttl`
- `samples/rdf-linked-data/sparql-queries.rq`
- `fixtures/neutral_components.json`

## Namespace Policy

- Planned namespace: `https://w3id.org/nz-hansard/`
- Component namespace: `https://w3id.org/nz-hansard/component/`
- Sample namespace: `https://w3id.org/nz-hansard/sample/`

## Vocabulary Mappings

- PROV-O records derivation and source provenance.
- DCAT describes the linked-data dataset and distributions.
- SKOS records party, role, proceeding-type, vote-type, and topic-code concept schemes.
- W3C Time records the sitting date used by the sample graph.

## Notes

- The sample stays inside the planned namespace and preserves stable IDs from neutral components.
- Turtle and JSON-LD outputs describe the same graph.
- SHACL shapes validate dataset metadata and speech-turn-linked fields.
- SPARQL examples are included for dataset and speech-turn inspection.
- `stanza` and `spacy` remain prototype comparison candidates for any future linguistic annotation export path.
- The sample is `sample-not-release` and remains `blocked-pending-validated-components`.
- `stanza` and `spacy` remain prototype comparison candidates for any future linguistic annotation export path.
