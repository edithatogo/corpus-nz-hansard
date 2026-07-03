# Plan: Parliament Dataset Full Acquisition

## Phase 1: Acquisition Architecture

- [x] Task: Read completed inventory and seed-fetcher evidence.
    - [x] Confirm approved sources and blocked/deferred sources.
    - [x] Confirm source-specific access constraints and rate limits.
- [x] Task: Design cache, manifest, and refresh-cadence policy.
    - [x] Define raw snapshot paths, normalized indexes, manifest fields, and validation reports.
    - [x] Define resume behavior and bounded target selection.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Acquisition Architecture' (Protocol in workflow.md)

## Phase 2: Tests And Validation Contracts

- [x] Task: Write tests for acquisition contracts.
    - [x] Cover cache writes, resume behavior, hash recording, blocked/deferred sources, excluded sources, and rights boundaries.
    - [x] Cover cross-source reconciliation expectations for journals, papers, questions, committees, petitions, and members.
- [x] Task: Add schemas for full acquisition manifests.
    - [x] Validate coverage windows, counts, hashes, errors, cache paths, and publication boundaries.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Tests And Validation Contracts' (Protocol in workflow.md)

## Phase 3: Full Acquisition Builders

- [x] Task: Implement acquisition builders for approved source groups.
    - [x] Use bounded target selection and resumable cache writes.
    - [x] Reuse retry/backoff and content hashing helpers.
- [x] Task: Implement reconciliation and readiness checks.
    - [x] Compare related source families where appropriate.
    - [x] Record blocked, skipped, and incomplete records explicitly.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Full Acquisition Builders' (Protocol in workflow.md)

## Phase 4: Documentation, Gates, And Release Boundaries

- [x] Task: Add operator documentation.
    - [x] Document acquisition commands, cache layout, refresh cadence, and known blockers.
    - [x] Document that outputs are not public-release artifacts unless promoted by a later publication track.
- [x] Task: Integrate validation into quality gates.
    - [x] Add checker scripts to local quality or focused release-readiness lanes without live network dependency.
- [x] Task: Run final validation.
    - [x] Run full acquisition checkers.
    - [x] Run focused tests and repository lint, format, quality-gate, and test commands required by the track.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Documentation, Gates, And Release Boundaries' (Protocol in workflow.md)
