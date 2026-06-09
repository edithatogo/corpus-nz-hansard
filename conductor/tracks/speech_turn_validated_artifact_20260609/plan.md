# Plan: Speech-Turn Validated Artifact Decision

## Phase 1: Candidate Audit

- [ ] Task: Review existing candidate segmentation.
    - [ ] Read `docs/speech-turn-segmentation-report.md`.
    - [ ] Read `manifests/speech_turn_segmentation_validation.json`.
    - [ ] Identify failure modes and confidence distribution.
- [ ] Task: Define validation thresholds.
    - [ ] Define sample design.
    - [ ] Define acceptable segmentation and attribution error rates.

## Phase 2: Decision and Tests

- [ ] Task: Add decision fixtures/tests.
    - [ ] Hard colon-marker case.
    - [ ] Embedded heading case.
    - [ ] No-speaker fallback case.
    - [ ] Multi-speaker document case.
- [ ] Task: Choose release path.
    - [ ] Promote to validated derived artifact, or
    - [ ] Keep explicitly excluded from public final scope.

## Phase 3: Implementation

- [ ] Task: Implement chosen path.
    - [ ] If promoted, add schema/output/manifest/docs.
    - [ ] If excluded, add exclusion decision and future validation checklist.
- [ ] Task: Record evidence.
    - [ ] Document validation results and release boundary.

