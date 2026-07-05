# Parliament Video Seed Fetchers Plan

## Implementation Protocol

- For every task: mark the task `[~]`, write mocked-network tests first where feasible, implement the seed proof, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download. No media download is allowed, including video or audio media files.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Fetcher Contracts
- [ ] Task: Define normalized video metadata, source snapshot, blocked-state, and hash fields.
- [ ] Task: Select bounded seed targets from the source inventory track.
- [ ] Task: Define fallback proof contracts for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Fetcher Contracts' (Protocol in workflow.md)

## Phase 2: Seed Implementations
- [ ] Task: Implement metadata-only seed fetchers for YouTube and Parliament website video surfaces.
- [ ] Task: Implement metadata-only seed fetchers for previous On Demand and select committee/Vimeo-era surfaces.
- [ ] Task: Implement metadata-only fallback probes for catalogue and web-archive evidence.
- [ ] Task: Add mocked network tests and fixture inputs.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Seed Implementations' (Protocol in workflow.md)

## Phase 3: Validation
- [ ] Task: Generate seed manifests with hashes, timestamps, source classifications, and blocked states.
- [ ] Task: Run targeted and repo-level validation, including `pixi run parliament-video-track-plan`.
- [ ] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff.
- [ ] Task: Conductor - User Manual Verification 'Validation' (Protocol in workflow.md)
