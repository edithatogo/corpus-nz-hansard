# Parliament Video Ongoing Archive Plan

## Implementation Protocol

- For every task: mark the task `[~]`, add dry-run or fixture tests first where feasible, implement the operating increment, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download unless a later approved media decision explicitly changes that state. No media download is allowed by default.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Refresh Design [checkpoint: db32a33]
- [x] Task: Define refresh cadence, snapshot retention, alert thresholds, and CI workflow boundaries. `db32a33`
- [x] Task: Define stale-source, link-rot, and count-regression policies. `db32a33`
- [x] Task: Define ongoing fallback monitoring for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives. `db32a33`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `db32a33`
- [x] Task: Conductor - User Manual Verification 'Refresh Design' (Protocol in workflow.md) `db32a33`

## Phase 2: Scheduled Archive [checkpoint: db32a33]
- [x] Task: Add scheduled metadata refresh workflow and local runner. `db32a33`
- [x] Task: Add new/deleted/changed record reports and gap-ledger updates. `db32a33`
- [x] Task: Add tests and dry-run fixtures. `db32a33`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `db32a33`
- [x] Task: Conductor - User Manual Verification 'Scheduled Archive' (Protocol in workflow.md) `db32a33`

## Phase 3: Operational Gates [checkpoint: db32a33]
- [x] Task: Add quality-gate integration and no-media-download guard. `db32a33`
- [x] Task: Run full validation, including `pixi run parliament-video-track-plan`, and document operating procedure. `db32a33`
- [x] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff. `db32a33`
- [x] Task: Conductor - User Manual Verification 'Operational Gates' (Protocol in workflow.md) `db32a33`
