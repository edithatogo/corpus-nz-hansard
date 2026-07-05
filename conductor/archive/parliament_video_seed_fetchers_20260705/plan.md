# Parliament Video Seed Fetchers Plan

## Implementation Protocol

- For every task: mark the task `[~]`, write mocked-network tests first where feasible, implement the seed proof, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download. No media download is allowed, including video or audio media files.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Fetcher Contracts
- [x] Task: Define normalized video metadata, source snapshot, blocked-state, and hash fields. `5aea39e`
- [x] Task: Select bounded seed targets from the source inventory track. `5aea39e`
- [x] Task: Define fallback proof contracts for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives. `5aea39e`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `5aea39e`
- [x] Task: Conductor - User Manual Verification 'Fetcher Contracts' (Protocol in workflow.md) `5aea39e`

## Phase 2: Seed Implementations
- [x] Task: Implement metadata-only seed fetchers for YouTube and Parliament website video surfaces. `5aea39e`
- [x] Task: Implement metadata-only seed fetchers for previous On Demand and select committee/Vimeo-era surfaces. `5aea39e`
- [x] Task: Implement metadata-only fallback probes for catalogue and web-archive evidence. `5aea39e`
- [x] Task: Add mocked network tests and fixture inputs. `5aea39e`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `5aea39e`
- [x] Task: Conductor - User Manual Verification 'Seed Implementations' (Protocol in workflow.md) `5aea39e`

## Phase 3: Validation
## Phase 3: Validation [checkpoint: 81132c9]
- [x] Task: Generate seed manifests with hashes, timestamps, source classifications, and blocked states. `5aea39e`
- [x] Task: Run targeted and repo-level validation, including `pixi run parliament-video-track-plan`. `5aea39e`
- [x] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff. `81132c9`
- [x] Task: Conductor - User Manual Verification 'Validation' (Protocol in workflow.md) `81132c9`
