# Evidence: Sitting And Proceeding Component Release

Status: blocked.

Implemented artifacts:

- `schemas/sitting_proceeding_component_validation.schema.json`
- `manifests/sitting_proceeding_component_validation.json`
- `derived/sitting_proceeding_components/sitting_proceeding_coverage.json`
- `derived/sitting_proceeding_components/sitting_proceeding_review.csv`
- `docs/sitting-proceeding-component-release.md`
- `scripts/build_sitting_proceeding_component.py`
- `scripts/check_sitting_proceeding_component.py`

Validation evidence:

- `python scripts/build_sitting_proceeding_component.py`
- `python scripts/check_sitting_proceeding_component.py`
- `python scripts/validate_derived_fields.py`
- `python -m unittest tests.test_sitting_proceeding_component tests.test_derived_fields_validation`
- `ruff check scripts/build_sitting_proceeding_component.py scripts/check_sitting_proceeding_component.py tests/test_sitting_proceeding_component.py`

Release boundary:

- The fixture set proves the component shape and referential integrity boundaries.
- Official sitting and proceeding reconciliation has not yet been completed, so the release remains blocked.
- Downstream endpoint work must continue to consume the neutral component boundary, not the blocked review scaffolding.
