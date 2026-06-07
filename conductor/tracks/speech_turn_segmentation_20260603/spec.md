# Spec: Speech Turn Segmentation MVP

## Goal

Build a conservative speech-turn candidate extraction pipeline from the normalized Hansard document-level Parquet dataset.

## Required Outputs

- Segmentation contract and limitations.
- Script to generate speech-turn candidate Parquet and validation JSON.
- Fixture-based tests.
- Generated validation report with document/turn counts and confidence categories.
- Conductor evidence and no authoritative speaker-attribution claim.

## Acceptance Criteria

- Source and normalized document-level artifacts are not modified.
- Generated speech-turn output lives under `generated/`.
- Manifest/validation artifacts are tracked under `manifests/`.
- Script handles tab-separated Hansard content fragments and colon speech markers.
- Output records candidate speaker, text, confidence, and source document linkage.
- Documentation states this is heuristic and not authoritative.

## Non-Goals

- No member identity resolution.
- No party inference.
- No claim of perfect speech-turn segmentation.
- No public release of turn-level data.
