# Evidence: Entity Linking Exploratory Outputs

Status: complete.

Implemented artifacts:

- `samples/entity-linking-exploratory/entity_linking_exploratory.jsonl`
- `samples/entity-linking-exploratory/entity_linking_exploratory_review.csv`
- `samples/entity-linking-exploratory/README.md`
- `docs/entity-linking-exploratory-outputs.md`
- `manifests/entity_linking_exploratory_outputs.json`
- `schemas/entity_linking_exploratory_outputs.schema.json`
- `schemas/entity_linking_exploratory_record.schema.json`
- `scripts/entity_linking_exploratory_outputs.py`
- `scripts/build_entity_linking_exploratory_outputs.py`
- `scripts/check_entity_linking_exploratory_outputs.py`
- `tests/test_entity_linking_exploratory_outputs.py`

Validation evidence:

- `python scripts/build_entity_linking_exploratory_outputs.py`
- `python scripts/check_entity_linking_exploratory_outputs.py`
- `python -m unittest tests.test_entity_linking_exploratory_outputs`

Boundary:

- Outputs are sample-not-release and non-authoritative.
- Human validation remains required before any downstream release claim.
- The bundle is suitable for evaluation, search/RAG enrichment, and RDF exploratory use only.
