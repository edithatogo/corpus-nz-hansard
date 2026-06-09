# Plan: Derived Fields Validation Manifests

## Phase 1: Framework Contract

- [ ] Task: Define shared manifest contract.
    - [ ] Required top-level fields.
    - [ ] Error/warning structure.
    - [ ] Source linkage and hash fields.
    - [ ] Release gate status.
- [ ] Task: Document derived-field validation policy.
    - [ ] Add `docs/derived-fields-validation.md`.
    - [ ] Define publication-blocking conditions.

## Phase 2: Test Harness

- [ ] Task: Add test fixtures.
    - [ ] Valid derived row.
    - [ ] Missing provenance.
    - [ ] Invalid confidence/status.
    - [ ] Broken source linkage.
    - [ ] Cross-artifact inconsistency.
- [ ] Task: Implement validation helper.
    - [ ] Validate member identity outputs.
    - [ ] Validate party attribution outputs.
    - [ ] Validate speech-turn outputs.

## Phase 3: Integration

- [ ] Task: Wire validation into derived tracks.
    - [ ] Member identity track consumes shared validation.
    - [ ] Party attribution track consumes shared validation.
    - [ ] Speech-turn decision track consumes shared validation if promoted.
- [ ] Task: Record evidence.
    - [ ] Run tests.
    - [ ] Record manifest outputs and release gate status.

