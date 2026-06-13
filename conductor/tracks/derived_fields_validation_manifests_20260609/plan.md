# Plan: Derived Fields Validation Manifests

## Phase 1: Framework Contract

- [x] Task: Define shared manifest contract.
    - [x] Required top-level fields.
    - [x] Error/warning structure.
    - [x] Source linkage and hash fields.
    - [x] Release gate status.
- [x] Task: Document derived-field validation policy.
    - [x] Add `docs/derived-fields-validation.md`.
    - [x] Define publication-blocking conditions.

## Phase 2: Test Harness

- [x] Task: Add test fixtures.
    - [x] Valid derived row.
    - [x] Missing provenance.
    - [x] Invalid confidence/status.
    - [x] Broken source linkage.
    - [x] Cross-artifact inconsistency.
- [x] Task: Implement validation helper.
    - [x] Validate member identity outputs.
    - [x] Validate party attribution outputs.
    - [x] Validate speech-turn outputs.

## Phase 3: Integration

- [x] Task: Wire validation into derived tracks.
    - [x] Member identity track consumes shared validation.
    - [x] Party attribution track consumes shared validation.
    - [x] Speech-turn decision track consumes shared validation if promoted.
- [x] Task: Record evidence.
    - [x] Run tests.
    - [x] Record manifest outputs and release gate status.
