# Validated Speech-Turn Component Release

## Purpose

This track promotes the candidate speech-turn parquet into a validated downstream component without changing the document-level v0.1.0 corpus.

## Current Release Gate

The current gate is `release-ready-speech-turns-triangulated-speakers-agent-review`.

Inputs are present:

- candidate speech-turn parquet: `generated/parquet/hansard_speech_turns.parquet`
- member identity gate: `release-ready-triangulated-agent-review`

Speaker candidates are resolved against the triangulated member authority. Unresolved or ambiguous speakers are routed to the agent-review fallback queue and are not authoritative speaker identity claims.

## Contract

The validated builder consumes candidate speech turns and emits:

- `generated/derived/hansard_speech_turns_validated.parquet`
- `derived/validated_speech_turns/speech_turn_review_queue.csv`
- `derived/validated_speech_turns/speech_turn_review_overrides.csv`
- `schemas/validated_speech_turn_component.schema.json`
- `manifests/validated_speech_turn_component_validation.json`

## Non-Claims

- Agent-review fallback rows are not authoritative speaker identity claims.
- The document-level corpus remains unchanged.
- Candidate segmentation remains method-scoped to `tab_colon_marker_v1` unless a later track broadens it.
