# Plan: Parliament Dataset Seed Fetchers

## Phase 1: Seed Target Selection

- [ ] Task: Read the completed Parliament dataset inventory and select seed targets.
    - [ ] Prefer high-value official Parliament sources across journals, papers, questions, committees, petitions, members, and calendar/video metadata.
    - [ ] Select fallback-source seeds only where the inventory marks them credible and useful.
- [ ] Task: Define seed artifact layout and bounded-run policy.
    - [ ] Define output paths under generated or derived seed directories.
    - [ ] Define maximum fetch counts and no-bulk-acquisition safeguards.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Seed Target Selection' (Protocol in workflow.md)

## Phase 2: Tests And Fetcher Interfaces

- [ ] Task: Write mocked network tests for seed-fetcher behavior.
    - [ ] Cover success, retryable failures, blocked/deferred source states, and hash recording.
    - [ ] Confirm no test depends on live Parliament network access.
- [ ] Task: Define fetcher command interfaces.
    - [ ] Provide one command or subcommand per seed family or a single orchestrator with explicit target names.
    - [ ] Include dry-run/list-targets behavior if it helps operator safety.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Tests And Fetcher Interfaces' (Protocol in workflow.md)

## Phase 3: Seed Fetcher Implementation

- [ ] Task: Implement seed fetchers for approved targets.
    - [ ] Reuse `scripts/http_retry.py`.
    - [ ] Preserve URLs, timestamps, hashes, and sample counts.
- [ ] Task: Build seed manifest, schema, checker, and docs.
    - [ ] Add `manifests/parliament_dataset_seed_fetchers.json`.
    - [ ] Add schema, checker script, tests, and documentation.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Seed Fetcher Implementation' (Protocol in workflow.md)

## Phase 4: Validation And Full-Acquisition Handoff

- [ ] Task: Run seed validation.
    - [ ] Run the seed checker.
    - [ ] Run focused mocked tests.
    - [ ] Run repository lint, format, quality-gate, and test commands required by the track.
- [ ] Task: Document full-acquisition requirements.
    - [ ] List feasible sources, blocked sources, cache needs, rate limits, and expected full-acquisition artifact shape.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Validation And Full-Acquisition Handoff' (Protocol in workflow.md)
