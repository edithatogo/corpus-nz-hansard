# Evidence: NZ Parliamentary Procedure Model

## Procedural Taxonomy

- Added `manifests/nz_parliamentary_procedure_model.json`.
- Added `schemas/nz_parliamentary_procedure_model.schema.json`.
- The model covers `party_vote`, `personal_vote`, `question`, `supplementary_question`, `stage`, `ruling`, `interjection`, and `procedural_unit`.
- The model links procedure components to `document`, `sitting`, `member`, `party`, `motion`, `bill`, and `vote` components where applicable.
- The model cites authority sources from `manifests/authority_sources.json`: Parliamentary Rules, Order Paper, Hansard, Daily Progress, Bills, written questions, and oral questions.

## Procedure Fixtures

- Added `fixtures/nz_parliamentary_procedure_samples.json`.
- Added `schemas/nz_parliamentary_procedure_samples.schema.json`.
- Fixtures cover `Hansard - vote`, `Hansard - question`, stage transitions, rulings, and interjections.
- Fixture reviews are manual and explicitly not model-generated labels.

## Endpoint Mappings

- Added `docs/nz-parliamentary-procedure-model.md`.
- Updated `docs/component-contracts.md` with procedure component fields.
- Updated `docs/endpoint-contracts.md` with procedure mapping requirements for ParlaMint-NZ / TEI, Popolo / Open Civic Data, Akoma Ntoso, and CAP / ParlaCAP.

## Focused Validation

- Added `scripts/check_nz_parliamentary_procedure_model.py`.
- Added `tests/test_nz_parliamentary_procedure_model.py`.
- Wired the checker into `make quality`, `.github/workflows/quality.yml`, `docs/quality-gate.md`, and `scripts/check_quality_gate.py`.
