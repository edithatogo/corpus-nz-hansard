# Evidence: Neutral Parliamentary Component Model

## Machine-Readable Schemas

- Added `manifests/neutral_component_model.json`.
- Added `schemas/neutral_component_model.schema.json`.
- Added `schemas/neutral_component_fixtures.schema.json`.
- The model defines stable `nzhc-component-<hash>` ID patterns for `sittings`, `proceeding_items`, `speech_turns`, `members`, `parties`, `motions`, `votes`, `bills`, `topics`, and `linguistic_annotations`.
- Every component family requires `derivation_method`, `derivation_version`, `validation_status`, `provenance`, and authority-source fields through common required fields.

## Fixtures And Referential Integrity

- Added `fixtures/neutral_components.json` with one row per required component family.
- Added referential-integrity examples linking proceeding items to sittings, speech turns to proceeding items and members, motions to proceeding items, votes to motions, bills to motions, topics to proceeding items, and linguistic annotations to speech turns.

## Validation Manifest

- Added `manifests/neutral_component_validation_manifest.json`.
- The validation manifest records schema paths, fixture paths, input release versions, validation command, fixture referential-integrity status, and `not-published-derived-fixtures-only` publication status.

## Focused Validation

- Added `scripts/check_neutral_component_model.py`.
- Added `tests/test_neutral_component_model.py`.
- Wired the checker into `make quality`, `.github/workflows/quality.yml`, `docs/quality-gate.md`, and `scripts/check_quality_gate.py`.
