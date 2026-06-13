# Evidence: Validated Speech-Turn Component Release

## Status

Blocked.

Repo-side implementation is present and the candidate artifact (`generated/parquet/hansard_speech_turns.parquet`, 439 turns) has been generated. Builder and checker pass. Publication is deferred because validated member identity is not yet available (authority coverage review pending).

## Implemented

- `scripts/build_validated_speech_turn_component.py`
- `scripts/check_validated_speech_turn_component.py`
- `schemas/validated_speech_turn_component.schema.json`
- `docs/validated-speech-turn-component-release.md`
- `tests/test_validated_speech_turn_component.py`
- `manifests/validated_speech_turn_component_validation.json`

## Artifacts

- Candidate: `generated/parquet/hansard_speech_turns.parquet` (439 turns)
- Validated: `generated/derived/hansard_speech_turns_validated.parquet` (blocked, not published)
- Review queue: `derived/validated_speech_turns/speech_turn_review_queue.csv`

## Validation Evidence

- Builder: `python scripts\build_validated_speech_turn_component.py` — passes, writes manifest with 439 validated rows.
- Checker: `python scripts\check_validated_speech_turn_component.py` — passes, release gate is consistent.
- Manifest status: `ok: false`, `validation_status: blocked`, `release_gate_status: blocked-pending-validated-member-identity`.

## Release Decision

Decision: defer.

Reasons:

- Validated member identity is not available (authority coverage review pending).
- All 439 candidate turns are classified as `blocked_speaker_identity`.
- The existing speech-turn exclusion decision remains in force for heuristic candidates.

## Validation Commands

- `python scripts\build_validated_speech_turn_component.py`
- `python scripts\check_validated_speech_turn_component.py`
- `python -m unittest tests.test_validated_speech_turn_component tests.test_speech_turn_release_decision`
