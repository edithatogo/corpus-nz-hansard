# Evidence: Researcher Client Helpers

Status: complete.

Implemented artifacts:

- `samples/researcher-client-helpers/hansard-mini.csv`
- `scripts/researcher_client_helpers.py`
- `manifests/researcher_client_helpers_manifest.json`
- `schemas/researcher_client_helpers.schema.json`
- `docs/researcher-client-helpers.md`
- `scripts/build_researcher_client_helpers.py`
- `scripts/check_researcher_client_helpers.py`
- `tests/test_researcher_client_helpers.py`

Validation evidence:

- `python scripts/build_researcher_client_helpers.py`
- `python scripts/check_researcher_client_helpers.py`
- `python -m unittest tests.test_researcher_client_helpers`

Boundary:

- Read-only helper examples only.
- R and standalone SPARQL examples remain deferred until RDF endpoint release artifacts are ready.
- No canonical generation scripts were modified by the helper examples.
