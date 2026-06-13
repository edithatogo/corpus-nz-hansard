# Evidence: OntoLex-Lemon Terminology Layer

Status: blocked.

Tracked artifacts:

- `spec.md`
- `plan.md`
- `metadata.json`
- `index.md`

Dependency boundary:

- OntoLex-Lemon is a lexicon model for enriching ontologies with lexical data,
  not a replacement for the corpus core or a generic text annotation format.
- The repository’s interoperability design keeps OntoLex-Lemon as a later
  optional terminology layer.
- Current RDF work is still sample-not-release and centers on PROV-O, DCAT,
  SKOS, and stable URIs, not on a released lexical resource.
- No curated terminology release surface exists yet for parliamentary and legal
  vocabulary.

Planned scope:

- terminology and lexicon records
- source authority and review status
- variant and multilingual labels where evidence exists
- RDF mappings to SKOS and linked-data outputs
- optional glossary and search-expansion examples

Reference surfaces:

- `docs/interoperability-requirements-moscow.md`
- `docs/interoperability-design.md`
- `docs/endpoint-contracts.md`
- `docs/rdf-linked-data-mapping.md`
- `conductor/tracks/rdf_linked_data_public_endpoint_release_20260610/`
- `conductor/tracks/semantic_search_embeddings_topics_20260610/`
