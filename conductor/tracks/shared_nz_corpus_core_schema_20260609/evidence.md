# Evidence: Shared NZ Corpus Core Schema

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Worker 2 Implementation Evidence

Date: 2026-06-10.

Owned files added:

- `docs/shared-nz-corpus-core-schema.md`
- `schemas/shared_nz_corpus_core.schema.json`
- `scripts/check_shared_core_schema.py`
- `tests/test_shared_core_schema.py`

Current local implementation before this worker pass: no shared core schema doc, schema, checker, or tests existed. Existing corpus-specific `schemas/hansard_record.schema.json` remains unchanged.

Target state implemented: a Draft 2020-12 shared compatibility schema for `corpus-nz-hansard` and `corpus-nz-legislation`, plus documentation for required source identity, jurisdiction, document type, date/version fields, canonical URI, source URL, record schema version, manifest hash, and provenance fields.

Public-surface implications recorded in `docs/shared-nz-corpus-core-schema.md`:

- GitHub remains the source-code and manifest home for schemas, scripts, tests, and migration notes.
- Hugging Face dataset cards should preserve corpus-family labels and clarify viewer row grain.
- Zenodo DOI records should not be changed for this compatibility contract unless a new version is minted.
- OSF remains optional mirror infrastructure and should reuse the same labels and manifest hashes if adopted.
- Future metadata packages should reference this schema instead of duplicating incompatible field names.

Focused validation commands:

- `python scripts/check_shared_core_schema.py`
- `python -m unittest tests.test_shared_core_schema`

Blocked or deferred:

- `conductor/tracks.md`, `Makefile`, CI, and shared quality-gate files were intentionally not edited by Worker 2 ownership constraints.
- Zenodraft sandbox proof is not part of this schema-owned worker pass and remains governed by the Zenodo rights track blocker.

## Coordination Completion - 2026-06-10

Central integration completed:

- Added shared quality-gate wiring for `python scripts\check_shared_core_schema.py`.
- Marked the track registry and metadata complete.
- Full integrated validation is recorded in the coordinating commit.
