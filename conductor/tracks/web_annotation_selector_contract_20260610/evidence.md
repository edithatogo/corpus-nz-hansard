# Evidence: W3C Web Annotation Selector Contract

Status: complete.

Implemented artifacts:

- `schemas/web_annotation_selector.schema.json`
- `manifests/web_annotation_selector_contract.json`
- `docs/web-annotation-selector-contract.md`
- `docs/web-annotation-selector-migration.md`
- `scripts/build_web_annotation_selector_contract.py`
- `scripts/check_web_annotation_selector_contract.py`
- `tests/test_web_annotation_selector_contract.py`

Validation evidence:

- `python scripts/build_web_annotation_selector_contract.py`
- `python scripts/check_web_annotation_selector_contract.py`
- `python -m unittest tests.test_web_annotation_selector_contract`

Release boundary:

- The contract standardizes source-linked selectors without forcing full annotation graphs.
- Selectors preserve source document IDs, source hashes, offsets, and quote text where appropriate.
- Existing endpoint specs reference the shared contract via `docs/endpoint-contracts.md`.
