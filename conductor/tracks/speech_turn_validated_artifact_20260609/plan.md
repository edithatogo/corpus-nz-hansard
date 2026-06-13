# Plan: Speech-Turn Validated Artifact Decision

## Phase 1: Candidate Audit

- [x] Task: Review existing candidate segmentation.
    - [x] Read `docs/speech-turn-segmentation-report.md`.
    - [x] Read `manifests/speech_turn_segmentation_validation.json`.
    - [x] Identify failure modes and confidence distribution.
- [x] Task: Define validation thresholds.
    - [x] Define sample design.
    - [x] Define acceptable segmentation and attribution error rates.

## Phase 2: Decision and Tests

- [x] Task: Add decision fixtures/tests.
    - [x] Hard colon-marker case.
    - [x] Embedded heading case.
    - [x] No-speaker fallback case.
    - [x] Multi-speaker document case.
- [x] Task: Choose release path.
    - [x] Keep explicitly excluded from public final scope.
    - [x] Do not promote to a validated derived artifact.

## Phase 3: Implementation

- [x] Task: Implement chosen path.
    - [x] If excluded, add exclusion decision and future validation checklist.
    - [x] Do not add schema/output/manifest/docs for a promoted artifact.
- [x] Task: Record evidence.
    - [x] Document validation results and release boundary.
