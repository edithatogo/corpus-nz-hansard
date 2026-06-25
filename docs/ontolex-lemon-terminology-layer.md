# OntoLex-Lemon Terminology Layer

Release status: release-ready-sample-ontolex-lemon-layer.

This track provides an optional terminology layer for sample parliamentary corpus vocabulary. It maps sample terms to SKOS concepts and OntoLex-Lemon lexical entries so RDF/NLP consumers can inspect labels, variants, concepts, sources, provenance, and review status separately from canonical corpus facts.

The layer does not claim a full corpus vocabulary, authoritative legal definitions, an official parliamentary glossary, external ontology acceptance, or completed stable URI review.

Artifacts:

- `samples/ontolex-lemon-terminology-layer/terminology.json`
- `samples/ontolex-lemon-terminology-layer/terminology.ttl`
- `manifests/ontolex_lemon_terminology_layer.json`
- `schemas/ontolex_lemon_terminology_layer.schema.json`

Validation:

- `python scripts/build_ontolex_lemon_terminology_layer.py`
- `python scripts/check_ontolex_lemon_terminology_layer.py`
- `python -m pytest tests/test_ontolex_lemon_terminology_layer.py`
