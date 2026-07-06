# Parliament Video Reconciliation Plan

## Implementation Protocol

- For every task: mark the task `[~]`, add representative reconciliation tests first where feasible, implement the reconciliation increment, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download. No media download is allowed, including video or audio media files.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Reconciliation Model
- [x] Task: Define reconciliation grains, source priorities, gap statuses, and duplicate/migration rules. `6204542`
- [x] Task: Map video sources to sitting, committee, and calendar evidence. `6204542`
- [x] Task: Map fallback resources including TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives to evidence-only reconciliation roles. `6204542`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `6204542`
- [x] Task: Conductor - User Manual Verification 'Reconciliation Model' (Protocol in workflow.md) `6204542`

## Phase 2: Reconciliation Builders
- [x] Task: Build cross-source reconciliation manifests and exception ledgers. `6204542`
- [x] Task: Add checks for fallback-only, blocked, duplicate, and missing-everywhere cases. `6204542`
- [x] Task: Add tests for representative reconciliation scenarios. `6204542`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `6204542`
- [x] Task: Conductor - User Manual Verification 'Reconciliation Builders' (Protocol in workflow.md) `6204542`

## Phase 3: Completeness Gates
- [x] Task: Add gates for metadata completeness and media completeness separation. `6204542`
- [x] Task: Run full validation, including `pixi run parliament-video-track-plan`, and document residual gaps. `6204542`
- [ ] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff.
- [ ] Task: Conductor - User Manual Verification 'Completeness Gates' (Protocol in workflow.md)
