# Evidence: OntoLex-Lemon Terminology Layer

Status: complete.

Release status: release-ready-sample-ontolex-lemon-layer.

Evidence added:

- `scripts/build_ontolex_lemon_terminology_layer.py` generates the sample terminology JSON and Turtle artifacts.
- `scripts/check_ontolex_lemon_terminology_layer.py` validates schema, release status, OntoLex/SKOS Turtle tokens, track metadata, registry state, and non-claims.
- `tests/test_ontolex_lemon_terminology_layer.py` exercises build and validation.
- `samples/ontolex-lemon-terminology-layer/terminology.json` records terms, variants, concepts, sources, provenance, and review status.
- `samples/ontolex-lemon-terminology-layer/terminology.ttl` provides sample SKOS and OntoLex-Lemon RDF mappings.

The optional terminology layer does not claim a full corpus vocabulary, authoritative legal definitions, an official parliamentary glossary, external ontology acceptance, or completed stable URI review.
