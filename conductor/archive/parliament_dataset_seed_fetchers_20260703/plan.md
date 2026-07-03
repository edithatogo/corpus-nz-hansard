# Plan: Parliament Dataset Seed Fetchers

## Phase 1: Seed Target Selection

- [x] Task: Read the completed Parliament dataset inventory and select seed targets.
    - [x] Prefer high-value official Parliament sources across journals, papers, questions, committees, petitions, members, and calendar/video metadata.
    - [x] Select fallback-source seeds only where the inventory marks them credible and useful.
- [x] Task: Define seed artifact layout and bounded-run policy.
    - [x] Define output paths under generated or derived seed directories.
    - [x] Define maximum fetch counts and no-bulk-acquisition safeguards.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Seed Target Selection' (Protocol in workflow.md)

## Phase 2: Tests And Fetcher Interfaces

- [x] Task: Write mocked network tests for seed-fetcher behavior.
    - [x] Cover success, retryable failures, blocked/deferred source states, and hash recording.
    - [x] Confirm no test depends on live Parliament network access.
- [x] Task: Define fetcher command interfaces.
    - [x] Provide one command or subcommand per seed family or a single orchestrator with explicit target names.
    - [x] Include dry-run/list-targets behavior if it helps operator safety.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Tests And Fetcher Interfaces' (Protocol in workflow.md)

## Phase 3: Seed Fetcher Implementation

- [x] Task: Implement seed fetchers for approved targets.
    - [x] Reuse `scripts/http_retry.py`.
    - [x] Preserve URLs, timestamps, hashes, and sample counts.
- [x] Task: Build seed manifest, schema, checker, and docs.
    - [x] Add `manifests/parliament_dataset_seed_fetchers.json`.
    - [x] Add schema, checker script, tests, and documentation.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Seed Fetcher Implementation' (Protocol in workflow.md)

## Phase 4: Validation And Full-Acquisition Handoff

- [x] Task: Run seed validation.
    - [x] Run the seed checker.
    - [x] Run focused mocked tests.
    - [x] Run repository lint, format, quality-gate, and test commands required by the track.
- [x] Task: Document full-acquisition requirements.
    - [x] List feasible sources, blocked sources, cache needs, rate limits, and expected full-acquisition artifact shape.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Validation And Full-Acquisition Handoff' (Protocol in workflow.md)
