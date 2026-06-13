# Validated Speech-Turn Component Release

## Purpose

This track is the future promotion path for speech-turn data. It does not change the existing exclusion decision for heuristic candidate turns.

## Current Release Gate

The current gate is blocked, not published.

- `blocked-pending-candidate-artifact`: the candidate speech-turn parquet is absent in this working tree.
- `blocked-pending-validated-member-identity`: even with a candidate artifact, Validated member identity is still blocked.

The generated validation manifest is `manifests/validated_speech_turn_component_validation.json`. Its release decision must remain `defer` until candidate data exists and member identity validation is available.

## Contract

The validated builder consumes candidate speech turns and emits:

- `generated/derived/hansard_speech_turns_validated.parquet`
- `derived/validated_speech_turns/speech_turn_review_queue.csv`
- `derived/validated_speech_turns/speech_turn_review_overrides.csv`
- `schemas/validated_speech_turn_component.schema.json`
- `manifests/validated_speech_turn_component_validation.json`

The row contract preserves source evidence:

- `turn_id`
- `source_stable_id`
- `source_file`
- `source_row_number`
- `parliament_document_id`
- `turn_index`
- `speaker_candidate`
- `speaker_member_id`
- `speaker_identity_status`
- `source_selector`
- `source_hash`
- `validation_hash`

## Non-Claims

- Heuristic candidate turns remain non-authoritative.
- Speaker identity remains blocked until the member identity release is validated.
- The document-level `v0.1.0` corpus remains unchanged.
- The existing explicit exclusion decision in `docs/speech-turn-release-decision.md` still applies to candidate output.
