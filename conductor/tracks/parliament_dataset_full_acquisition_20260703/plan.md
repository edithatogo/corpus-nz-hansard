# Plan: Parliament Dataset Full Acquisition

## Phase 1: Acquisition Architecture

- [ ] Task: Read completed inventory and seed-fetcher evidence.
    - [ ] Confirm approved sources and blocked/deferred sources.
    - [ ] Confirm source-specific access constraints and rate limits.
- [ ] Task: Design cache, manifest, and refresh-cadence policy.
    - [ ] Define raw snapshot paths, normalized indexes, manifest fields, and validation reports.
    - [ ] Define resume behavior and bounded target selection.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Acquisition Architecture' (Protocol in workflow.md)

## Phase 2: Tests And Validation Contracts

- [ ] Task: Write tests for acquisition contracts.
    - [ ] Cover cache writes, resume behavior, hash recording, blocked/deferred sources, excluded sources, and rights boundaries.
    - [ ] Cover cross-source reconciliation expectations for journals, papers, questions, committees, petitions, and members.
- [ ] Task: Add schemas for full acquisition manifests.
    - [ ] Validate coverage windows, counts, hashes, errors, cache paths, and publication boundaries.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Tests And Validation Contracts' (Protocol in workflow.md)

## Phase 3: Full Acquisition Builders

- [ ] Task: Implement acquisition builders for approved source groups.
    - [ ] Use bounded target selection and resumable cache writes.
    - [ ] Reuse retry/backoff and content hashing helpers.
- [ ] Task: Implement reconciliation and readiness checks.
    - [ ] Compare related source families where appropriate.
    - [ ] Record blocked, skipped, and incomplete records explicitly.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Full Acquisition Builders' (Protocol in workflow.md)

## Phase 4: Documentation, Gates, And Release Boundaries

- [ ] Task: Add operator documentation.
    - [ ] Document acquisition commands, cache layout, refresh cadence, and known blockers.
    - [ ] Document that outputs are not public-release artifacts unless promoted by a later publication track.
- [ ] Task: Integrate validation into quality gates.
    - [ ] Add checker scripts to local quality or focused release-readiness lanes without live network dependency.
- [ ] Task: Run final validation.
    - [ ] Run full acquisition checkers.
    - [ ] Run focused tests and repository lint, format, quality-gate, and test commands required by the track.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Documentation, Gates, And Release Boundaries' (Protocol in workflow.md)
